from django.db import models
from django.contrib.auth.models import AbstractUser
from loguru import logger
import imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _


class UserBaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True
        managed = False


class User(UserBaseModel):
    email = models.EmailField(_('email address'), unique=True, blank=True, null=False, default="")
    # email = models.CharField(max_length=50, unique=True, null=False, default="")
    password = models.CharField(max_length=255, null=False, default="")



    class Meta:
        abstract = False
        managed = True
        db_table = "user"


class Token(UserBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="user_id"
    )
    token = models.CharField(max_length=255, default=None)

    class Meta:
        abstract = False
        managed = True
        db_table = "user_token"

# register_email_token
class VerifyToken(UserBaseModel):
    email = models.EmailField(_('email address'), unique=True, blank=True, null=False, default="")
    email_code = models.CharField(max_length=10, default='', null=True)       # 邮箱验证码
    email_code_updated =  models.FloatField(default=0, null=True)   # 邮箱验证码的更新时间
    img_code = models.CharField(max_length=10, default='', null=True)         # 图片验证码
    img_code_updated = models.FloatField(default=0, null=True)  # 图片验证码的更新时间

    class Meta:
        abstract = False
        managed = True
        db_table = "verify_token"


#重构user model
class UserProfile(AbstractUser):
    id = models.AutoField(primary_key=True, verbose_name='编号')
    user = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING,
                                 verbose_name='user')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female',
                              verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    avatar = ProcessedImageField(upload_to='avatar', default='avatar/default.png', verbose_name='头像',
                                 processors=[ResizeToFill(100, 100)],  # 处理后的图像大小
                                 format='JPEG',  # 处理后的图片格式
                                 options={'quality': 95}  # 处理后的图片质量
                                 )
    login_time = models.DateTimeField(auto_now=True, verbose_name='登录时间')  # .sava() 能够改变其时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')

    def save(self, *args, **kwargs):
        logger.info('the avator save fun is None')
        # 当用户更改头像的时候，avatar.name = '文件名'，其他情况下avatar.name = 'upload_to/文件名'
        if len(self.avatar.name.split('/')) == 1:
            self.avatar.name = self.username + '/' + self.avatar.name
        # 调用父类的save()方法后，avatar.name就变成了'upload_to/用户名/文件名'
        # super(UserProfile, self).save()

    class Meta:
        verbose_name = 'UserInfo'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
