# Lenovo-"Xie Yan"


import kaptcha
from datetime import timedelta, datetime

from accounts.auth_dealer.base_auth import BaseAuthProvider
from accounts.models import User as CustomUser
from django.core.mail import send_mail
from django.conf import settings
import random
from loguru import logger
from accounts.repositories import verify_token_repo, user_repo


class ImgProvider(BaseAuthProvider):
    def auth_img_code(self, email:str, img_code: str) -> bool:
        '''
        :return: True False
        '''
        return self.auth_email_img_code(email=email, img_code=img_code)

    # kaptcha 生成验证码
    def generate_kaptcha(self):
        '''
        :return: 验证码结果，以及base64图像
        '''
        code, img = kaptcha.Captcha(width=200, height=80).letter_digit()  # 验证码的宽度 px,  # 验证码的高度 px
        return code, img

    def img_code(self, email: str) -> dict:
        # img code
        img_code, img_base64 = self.generate_kaptcha()  # 验证码结果，以及base64图像
        # save code to db
        logger.info('img_code:{}'.format(img_code))
        verify_token_repo.update_img_code(email=email, img_code=img_code)
        # 返回base64图像数据
        return {'img_code': img_base64}


img_provider = ImgProvider()
