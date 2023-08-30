# Lenovo-"Xie Yan"

# Lenovo-"Xie Yan"
from datetime import timedelta, datetime
from accounts.models import User as CustomUser
from django.core.mail import send_mail
from django.conf import settings
import random
from loguru import logger

from accounts.repositories import verify_token_repo, user_repo

register_template = '''
The verification code for your {Website} account is {code}.

The activation code will expired in 30 minutes. So please use it in time.

If you've received this mail in error, it's likely that another user entered your email address by mistake while trying
to reset a password. If you didn't initiate the request, you don't need to take any further action and can safely
disregard this email.

Thanks
'''

FROM_EMAIL = "cqusv@qq.com"
from utils.exceptions import Status


class BaseAuthProvider:

    def this_code_time(self) -> float:
        '''
        :return: code 当前的时间（s）
        '''
        return datetime.now().timestamp()

    def auth_email_img_code(self, email: str, email_code: str = '', img_code: str = '') -> bool:
        '''
        :return: True False
        '''
        if email_code is not '':
            img_ = False
            auth_code = email_code
        elif img_code is not '':
            img_ = True
            auth_code = img_code
        else:
            logger.error('No code for auth_email/img.')
            return False
        code, time = verify_token_repo.search_img_email_code(email=email, img_=img_)  # 从数据库中取出code和time
        if code == auth_code:
            logger.info('The verify {} code is successful.'.format('img' if img_ else 'email'))
            # check the time
            exp_time = int(time) + timedelta(minutes=settings.JWT_EMAIL_EXPIRE_MINUTE).total_seconds()  # 计算此次code的有效时间
            if self.this_code_time() < exp_time:
                logger.info('The {} code is useful....'.format('img' if img_ else 'email'))
                return True
        else:
            return False
        return True

    def search_user_info(self, email):
        # 查询用户
        user = user_repo.get_by_email(email=email)
        if user is False:
            return Status.NotFoundUserError, None
        return user, user['id']
