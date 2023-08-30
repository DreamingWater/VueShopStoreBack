# Lenovo-"Xie Yan"
from datetime import timedelta, datetime

from accounts.auth_dealer.base_auth import BaseAuthProvider
from accounts.models import User as CustomUser
from django.core.mail import send_mail
from django.conf import settings
import random
from loguru import logger

from accounts.repositories import verify_token_repo

register_template = '''
The verification code for your {Website} account is {code}.

The activation code will expired in 30 minutes. So please use it in time.

If you've received this mail in error, it's likely that another user entered your email address by mistake while trying
to reset a password. If you didn't initiate the request, you don't need to take any further action and can safely
disregard this email.

Thanks
'''

FROM_EMAIL = "1954769331@qq.com"


class EmailProvider(BaseAuthProvider):
    def send_register_email(self, code: str, to_email="2010582488@qq.com"):
        data = {"code": code, "Website": settings.WEBSITE_NAME}
        send_message = register_template.format(**data)
        send_mail(
            "Email Activation",
            send_message,
            FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )

    def generate_email_code(self) -> str:
        '''
        :return: 6位数邮箱验证码
        '''
        return str(random.randint(100000, 999999))

    def auth_email_code(self, email:str, email_code: str) -> bool:
        '''
        :return: True False
        '''
        return self.auth_email_img_code(email=email, email_code=email_code)

    def email_code(self, email: str):
        # email code
        email_code = self.generate_email_code()
        # save code to db
        verify_token_repo.update_email_code(email=email, email_code=email_code)
        # send email
        logger.info('email_code:{}'.format(email_code))
        self.send_register_email(code=email_code, to_email=email)
        return {'email':'Ture'}


email_provider = EmailProvider()
