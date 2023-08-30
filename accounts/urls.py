from django.conf.urls import re_path
from . import views as  accounts_views
from django.conf.urls import url
app_name = "accounts"
# from accounts import views as  accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^users/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,200})/$',
        accounts_views.activationview, name='user-activation-link'),
    url(r'^login/$', accounts_views.login, name='login'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),          # PC Using...
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]

