from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# from django.db.models.query import QuerySet



# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,username,email,is_doctor,password=None,**extra_fields):
        if not email:
            raise ValueError('User Must Have an Email Address!!!')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_doctor=is_doctor,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self,username,email,password=None,is_doctor=False):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_doctor=is_doctor
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




class UserCustomModel(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    is_doctor = models.BooleanField(default=False ,null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    objects = UserManager()
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']  
    
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    
    def has_module_perms(self,app_labels):
        return True
    
    
    
    @property
    def is_staff(self):
        return self.is_admin


class Doctor(models.Model):
    user = models.OneToOneField(UserCustomModel,on_delete=models.CASCADE)
    hospital = models.CharField(max_length=255,null=True,blank=True)
    department = models.CharField(max_length=255,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    
    
    

    