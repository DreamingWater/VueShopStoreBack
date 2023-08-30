# Lenovo-"Xie Yan"
import os
from enum import Enum

import django

from accounts.forms import LoginForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()
from accounts.auth_dealer.email_auth import email_provider
from accounts.auth_dealer.img_auth import img_provider
from accounts.repositories import user_repo, token_repo
from accounts.services import user_service


# data = user_service.sign_up(email='d12fd12341fsdfq.com',password="dsfdd23s233e@fd2ere3D")
# print(data)
#
# user = user_repo.get_by_email(email='d12fd123sdf32341fsdf@qq.com')
# print(user)
# # token_repo.delete_by_user_id(4)
# # print('successs')
# user = user_repo.get_by_email(email='d12fd12341fsdf@qq.com')
# print(user)


def test_vericaiton_img():
    import kaptcha

    code, img = kaptcha.Captcha(width=120, height=40,chips=1).digit()  # 验证码的宽度 px,  # 验证码的高度 px
    print(code)
    print(img)


def test_emai():
    email_provider.send_register_email('324231')
    print('success to send email')


if __name__ == '__main__':
    test_vericaiton_img()
    from accounts.views import ask_email_code
    # email_provider.email_code('*@qq.com')
    # res = user_service.sign_up(email='*@qq.com', password='dfsf3242f',
    #                      email_code='711250'
    #                      )
    # login
    # img_dict = img_provider.img_code(email='*@qq.com')
    # res = user_service.login(email='*@qq.com', password='dfsf3242f',
    #                                img_code='CTsA')
    # print(res)

    # test_emai()

    # data = {'email':'**@qq.com','password':'dfsf3242f',   'img_code':'CTsA','f':1,'fd':'dsdse2324fd'}
    # schema = LoginForm(data=data)
    # print(schema)
    # schema.is_valid(raise_exception=True)
    # print(schema['email'])
