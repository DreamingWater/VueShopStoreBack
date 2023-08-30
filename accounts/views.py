from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpRequest, JsonResponse

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView

from utils.common import get_data_from_request
from .auth_dealer.email_auth import email_provider
from .auth_dealer.img_auth import img_provider
# from Commerce.utils import recaptcha_is_valid
#
# from .forms import SignUpForm, UserInformationUpdateForm
from .models import UserProfile as User

# 注册账户
# def signup(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = SignUpForm(request.POST)
#         if form.is_valid() and recaptcha_is_valid(request):
#             user = form.save()
#             #user.is_active = False          #不激活该账户
#             user.save()
#             from django.contrib.auth.tokens import default_token_generator
#             from django.utils.http import urlsafe_base64_encode
#             from django.utils.encoding import force_bytes
#             id = user.pk
#             this_user = User.objects.get(pk=id)
#             print(this_user.username)
#             token = default_token_generator.make_token(this_user)        #生成tocken
#             print(token)
#             uid = urlsafe_base64_encode(force_bytes(this_user.pk))
#
#             if default_token_generator.check_token(this_user, token):
#                 print('sccusgfsg')
#             print('users/validate/'+ uid +'/'+ token)
#             auth_login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'accounts/signup.html', {'form': form})


# 注册账户
# 登录业务
# @require_POST  # 只允许post请求的方式登录
# def login1(request: HttpRequest):
#     try:
#
#         email = payload['email']
#         password = payload['password'].encode()
#         user = User.objects.get(email=email)  # 只有一条
#
#         print(user.password, '~~~~~~~~~', type(password))
#         if bcrypt.checkpw(password, user.password.encode()):
#             # # 验证成功
#             # token = gen_token(user.id)
#             # res = JsonResponse({
#             #     # 'use_id': user.id,
#             #     # 'email': email,
#             #     # 'name': user.name,
#             #     'user': json_ify(user, exclude=('password', )),
#             #     'token': token
#             # })
#             # # res.set_cookie('jwt', token)
#             # return res
#             session: SessionStore = request.session
#             print(type(session), session)
#             print(session.keys())
#             session.set_expiry(300)  # 会话过期，单位秒
#             session['user_id'] = user.id
#             # 对于频繁需要使用的数据，使用字符串拼出来，省得还要从数据库中查询
#             session['user_info'] = "{} {} {}".format(user.id, user.name, user.email)
#             res = JsonResponse({
#                 'user': json_ify(user, exclude=['password']),
#                 'user_info': session['user_info']
#             })
#
#             return res
#         else:
#             return JsonResponse({'error': "用户名或密码错误"}, status=400)
#     except Exception as e:
#         logging.error(e)
#         # 失败返回错误信息和400，所有其他错误一律用户名密码错误；有时候错误信息不宜太详细
#         return JsonResponse({'error': "用户名或密码错误"}, status=400)
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def login(request:ASGIRequest):
#     if request.method == 'POST':
#         import json
#         body = request.body.decode('utf-8')
#         data = json.loads(body)
#         username = data.get('username')
#         password = data.get('password')
#         print('username:{},passwd:{}'.format(username,password))
#         res = JsonResponse({
#             'data':"hello world",
#             "code": 400,
#             "message": 'success',
#             "ok": True,
#         })
#         return res
#     return JsonResponse("输入有误")
#
# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(UpdateView):
#     form_class = UserInformationUpdateForm
#     template_name = 'accounts/my_account.html'
#     success_url = reverse_lazy('my_account')
#
#     def get_object(self):
#         return self.request.user
#
# #账号的邮箱验证，但是由于解密的时候存在错误，不能使用。
# def activationview(request,uidb64,token):
#     # print(request.GET)
#     # uidb64 = request.GET.get('uidb64')
#     # token = request.GET.get('token')
#     print(uidb64)
#     if uidb64 is not None and token is not None:
#         from django.utils.http import urlsafe_base64_decode
#         uid = urlsafe_base64_decode(uidb64)
#         try:
#             from django.contrib.auth import get_user_model
#             from django.contrib.auth.tokens import default_token_generator
#             user_model = get_user_model()
#             user = user_model.objects.get(pk=uid)
#             if default_token_generator.check_token(user, token) and user.is_active == False:
#                 user.is_active = True
#                 return redirect('home')
#         except Exception as e:
#             print(e)
#             print('failed to active the account')
#     print('failed to active the account')


from accounts.services import user_service
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from accounts.forms import SignUpForm, LoginForm
from accounts.auth_dealer.auth_decorators import must_be_user
from .repositories import user_repo
from .returns import accounts_return
from utils.exceptions import Status


@api_view(["POST"])
def signup(request):
    request_data = get_data_from_request(request)
    schema = SignUpForm(data=request_data)
    if schema.is_valid(raise_exception=False):
        request_data = schema.data
        signup_res = user_service.sign_up(email=request_data["email"], password=request_data["password"],
                                          email_code=request_data["email_code"]
                                          )
        return JsonResponse(accounts_return.deal_event(signup_res))
    else:
        return JsonResponse(accounts_return.return_error_status(Status.InValidFormError))


@api_view(["POST"])
def login(request):
    request_data = get_data_from_request(request)
    schema = LoginForm(data=request_data)
    if schema.is_valid(raise_exception=False):
        request_data = schema.data
        login_res = user_service.login(email=request_data["email"], password=request_data["password"],
                                       img_code=request_data["img_code"])
        # login
        return JsonResponse(accounts_return.deal_event(login_res))
    else:
        return JsonResponse(accounts_return.return_error_status(Status.InValidFormError))


@api_view(["POST"])
def logout(request):
    return JsonResponse(
        {"success": user_service.logout(request.user)},
        status=status.HTTP_201_CREATED,
    )


# 请求图片验证码
def ask_img_code(request, email):
    img_dict = img_provider.img_code(email=email)  # 获取base64编码，同时保存到数据库 {'img_code':'*'}
    return JsonResponse(accounts_return.deal_event(img_dict))


# 请求发送邮箱验证码
def ask_email_code(request, email):
    email_dict = email_provider.email_code(email=email)
    return JsonResponse(accounts_return.deal_event(email_dict))
