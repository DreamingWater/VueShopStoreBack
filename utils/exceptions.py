from rest_framework import status
from enum import Enum


class Status(Enum):
    NotFoundError = {'code': 100, 'msg': 'not found error'}
    NotFoundUserError = {'code': 101, 'msg': 'not found user error'}
    NotAuthorizedError = {'code': 102, 'msg': 'not authorized error'}
    TokenExpiredError = {'code': 103, 'msg': 'token expired error'}
    PasswordError = {'code': 104, 'msg': 'password error'}
    ImgCodeError = {'code': 105, 'msg': 'img code error'}
    EmailCodeError = {'code': 106, 'msg': 'email code error'}
    InValidFormError = {'code': 107, 'msg': 'invalid form error'}
    InValidEmailError = {'code': 107, 'msg': 'invalid email error'}
