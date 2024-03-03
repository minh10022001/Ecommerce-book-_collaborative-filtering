# Create your models here.
from cgi import test
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, id, fullname, username, email, password=None):
        if not email:
            raise ValueError('Email address is required')

        # Tạo đối tượng user mới
        user = self.model(
            id = id,
            email=self.normalize_email(email=email),    # Chuyển email về dạng bình thường
            username=username,
            fullname =  fullname,
            is_staff=False,
           
         
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,id,fullname, email, username, password):
        user = self.create_user(
            id =id,
            email=self.normalize_email(email=email),
            username=username,
            password=password,
            fullname  = fullname,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
class Account(AbstractBaseUser):
    id = models.IntegerField(db_column='ID_account', primary_key=True) 
    fullname = models.CharField(max_length=50, null= True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
   

    # required

    last_login = models.DateTimeField(auto_now_add=True, null= True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    # Trường quyêt định khi login
    REQUIRED_FIELDS = ['username', 'fullname', 'id']    # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password

    objects = UserAccountManager()




 
   