from loguru import logger

from accounts.models import Token, User as CustomUser, UserBaseModel, VerifyToken
from accounts.serializers import UserSerializers, TokenSerializers, BaseUserSerializers, VerifyTokenSerializers
from datetime import datetime
from django.db import models
from rest_framework import serializers

from utils.exceptions import Status


class BaseUserRepo:
    def __init__(self, model: UserBaseModel, serializer: BaseUserSerializers):
        self.model = model
        self.serializer = serializer

    def _get_query_by_soft_deleted(self, data_id: int, is_deleted: bool):
        return (
            self.get_model_element(id=data_id, deleted_at__isnull=False)
            if is_deleted
            else self.get_model_element(id=data_id, deleted_at__isnull=True)
        )

    def _validate_serializer_and_save(self, serializer: BaseUserSerializers):
        if serializer.is_valid(raise_exception=False):  # 有效
            serializer.save()
            return serializer.data
        else:
            return Status.InValidEmailError

        # if serializer.is_valid(raise_exception=False):
        #     serializer.save()
        #     return serializer.data
        # else:

    def get(self, data_id: int, is_deleted: bool = False) -> dict:
        query = self._get_query_by_soft_deleted(data_id, is_deleted)
        if query is not False:
            return self.serializer(query).data
        return False

    def create(self, data: dict):
        serializer = self.serializer(data=data)
        return self._validate_serializer_and_save(serializer)

    def update(self, data_id: int, data: dict, is_deleted: bool = False) -> dict:
        target = self._get_query_by_soft_deleted(data_id, is_deleted)
        if target is not False:
            serializer = self.serializer(target, data=data, partial=True)
            return self._validate_serializer_and_save(serializer)
        else:
            return False

    def delete(self, data_id: int, soft_delete: bool = True) -> None:
        if soft_delete:
            self.update(data_id, {"id": data_id, "deleted_at": datetime.now()})
        else:
            res = self.get_model_element(id=data_id)
            res.delete()
        return

    def get_model_element(self, **kw):
        try:
            res = self.model.objects.get(**kw)
            return res
        except:
            return False


class UserRepo(BaseUserRepo):
    def get_by_email(self, email: str) -> dict:
        user_element = self.get_model_element(email=email, deleted_at=None)
        if user_element is not False:
            return self.serializer(user_element).data
        return False


class TokenRepo(BaseUserRepo):
    def upsert(self, user_id: int, user: CustomUser, token: str):
        obj, created = self.model.objects.update_or_create(
            user=user_id,
            defaults={"user": user, "token": token, "deleted_at": None},
        )
        return self.serializer(obj).data

    def get_by_user_id(self, user: int) -> dict:
        token_element = self.model.objects.get(user_id=user, deleted_at=None)
        if token_element is not False:
            return self.serializer(token_element).data
        return False

    def delete_by_user_id(self, user: int) -> None:
        # token = self.model.objects.get(user_id=user, deleted_at=None)
        # serilizer = self.serializer(
        #     token, data={"deleted_at": datetime.now()}, partial=True
        # )
        #
        # self._validate_serializer_and_save(serilizer)
        # self.delete(data_id=user,soft_delete=False)
        res = self.get_model_element(user_id=user)
        if res is not False:
            res.delete()
            logger.info('delete cookie for user : %s ' % user)


class VerifyTokenRepo(BaseUserRepo):
    def update_img_code(self, email: str, img_code: str):  # 更新图片验证码
        obj, created = self.model.objects.update_or_create(
            email=email,
            defaults={"email": email, "img_code": img_code, "img_code_updated": datetime.now().timestamp()},
        )
        return self.serializer(obj).data

    def update_email_code(self, email: str, email_code: str):  # 更新图片验证码
        obj, created = self.model.objects.update_or_create(
            email=email,
            defaults={"email": email, "email_code": email_code, "email_code_updated": datetime.now().timestamp()},
        )
        return self.serializer(obj).data

    def search_img_email_code(self, email: str, img_=True):
        '''
        :param email: str
        :param img_: bool if img_== True, 查询 img——code；否则查询 email_code
        :return: code and time
        '''
        code, time = ("img_code", "img_code_updated") if img_ else ("email_code", "email_code_updated")
        res = self.get_model_element(email=email)
        if res is not False:
            data = self.serializer(res).data
            return data[code], data[time]
        return False


user_repo = UserRepo(model=CustomUser, serializer=UserSerializers)
token_repo = TokenRepo(model=Token, serializer=TokenSerializers)
verify_token_repo = VerifyTokenRepo(model=VerifyToken, serializer=VerifyTokenSerializers)
