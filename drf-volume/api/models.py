from django.db import models
from django.contrib.auth.signals import user_logged_in

# from django.contrib.auth.signals import user_logged_in, user_logged_out # ログアウトも呼びたかったらこれ使って．
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
import uuid as uuid_lib
def upload_avator_path(instance,filename):
    # 拡張子の導出
    ext = filename.split('.')[-1]
    # User毎にDirectoryを作成
    return '/'.join(['avatars', str(instance.userProfile.id) + str(instance.usertag) + str(".") + str(ext)])

# pathを返す。instanceはオブジェクト情報 Postしたやつのフォルダに格納
def upload_post_path(instance,filename):
    # 拡張子の導出
    ext = filename.split('.')[-1]
    # User毎にDirectoryを作成
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])

# Userを管理する
class UserManager(BaseUserManager):
    # active
    def create_user(self, email, password=None):
        # emailがないときに例外処理を発生。
        if not email:
            raise ValueError('email is must')
        # メールアドレスは小文字なので小文字に強制変換
        user = self.model(email=self.normalize_email(email))
        # パスワードをハッシュ化してからセーブする。
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Supeuser
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid_lib.uuid4,
                            primary_key=True, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15,null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    def __str__(self):
        # Printするときにこいつを返す。
        return self.email

class Profile(models.Model):
    post_id = models.UUIDField(default=uuid_lib.uuid4,
                               primary_key=True, editable=False)
    nickname = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    middlename = models.CharField(max_length=20,null=True)
    lastname = models.CharField(max_length=20)
    dob = models.DateTimeField(null=True)
    sex = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    login_time = models.DateTimeField(blank=True, null=True)
    # 一旦後回し
    # fun

class Address(models.Model):
    postnumber = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    ward = models.CharField(max_length=10)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    lastName = models.CharField(max_length=20)
    userAddress = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userAddress',
        on_delete=models.CASCADE
    )



@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """ログインした際に呼ばれる"""
    Profile.objects.create(user=userProfile, login_time=timezone.now())

