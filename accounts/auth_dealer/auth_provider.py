import loguru

from accounts.auth_dealer.email_auth import email_provider
from accounts.auth_dealer.img_auth import img_provider
from accounts.repositories import user_repo, token_repo, verify_token_repo
from accounts.models import User as CustomUser
import jwt
from datetime import timedelta
from django.conf import settings
from loguru import logger
from utils.common import check_email_format
from utils.exceptions import Status
from datetime import datetime
import bcrypt
import re


class AuthProvider:
    def __init__(self):
        self.key = settings.JWT_KEY
        self.expire_sec = timedelta(days=settings.JWT_EXPIRE_DAYS).total_seconds()

    def _get_curr_sec(self):
        return datetime.now().timestamp()

    def hashpw(self, password: str):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def checkpw(self, password: str, hashed: str):
        return bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8"))

    def _decode(self, token: str):
        decoded = jwt.decode(token, self.key, algorithms=["HS256"])
        if decoded["exp"] <= self._get_curr_sec():
            return Status.TokenExpiredError
        else:
            return decoded

    def get_token_from_request(self, request):
        return request.META.get("HTTP_AUTHORIZATION", None)

    def create_token(self, user_id: str, is_expired: bool = False):
        exp = 0 if is_expired else self._get_curr_sec() + self.expire_sec
        encoded_jwt = jwt.encode(
            {"id": user_id, "exp": exp},
            self.key,
            algorithm="HS256",
        )
        return {"token": encoded_jwt}

    def login(self, email: str, password: str, img_code: str):
        user = user_repo.get_by_email(email=email)
        if user is False:
            return Status.NotFoundUserError
        code_verify = img_provider.auth_img_code(email=email, img_code=img_code)  # 验证验证码
        if not code_verify:  # 识别不成功
            return Status.ImgCodeError
        if self.checkpw(password, user["password"]):
            token = self.create_token(user["id"])["token"]
            token_repo.upsert(
                user_id=user["id"],
                user=CustomUser(**user),
                token=token,
            )
            return {'token': token}
        else:
            return Status.PasswordError

    def check_auth(self, token: str):
        decoded = self._decode(token)  # decode func will raise error on expired
        user = user_repo.get(decoded["id"])
        if user is False:
            return Status.NotFoundUserError
        saved_token = token_repo.get_by_user_id(user["id"])
        if saved_token is not None and (token == saved_token["token"]):
            return user["id"]
        else:
            return Status.NotAuthorizedError

    def register(self, email: str, password: str, email_code: str):
        '''
        :param email:
        :param password:
        :param email_code:
        :return: 错误码 或者 {’token':}
        '''
        if check_email_format(email) is None:
            return Status.InValidEmailError
        code_verify = email_provider.auth_email_code(email=email, email_code=email_code)  # 验证验证码
        if not code_verify:  # 邮箱验证码识别不成功
            return Status.EmailCodeError
        password = auth_provider.hashpw(password)
        user = user_repo.create({"email": email, "password": password})
        if isinstance(user, Status):
            return user  # InValidEmailError
        logger.info('register ---> email:{} -- password:{}'.format(email,password))
        # 自动登录，创建 token
        token = self.create_token(user["id"])["token"]
        token_repo.upsert(
            user_id=user["id"],
            user=CustomUser(**user),
            token=token,
        )
        return {'token': token}


auth_provider = AuthProvider()
