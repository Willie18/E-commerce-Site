from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    
    def create_user(self,email,username,password,**other_fields):
        if not email:
            raise ValueError(_("Email address is a required field"))
        email=self.normalize_email(email=email)
        user=self.model(email=email,username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,username,password,**other_fields):
        other_fields.setdefault("is_staff",True)
        other_fields.setdefault("is_superuser",True)
        other_fields.setdefault("is_active",True)
        
        if other_fields.get("is_staff") is not True:
            raise ValueError("SuperUser must be assigned is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser must be assigned is_superuser=True")
        
        return self.create_user(email,username,password,**other_fields)
        

# Create your models here.

class CustomerUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(_("email address"),max_length=255, unique=True)
    password=models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True )

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=["username"]
    
    objects=CustomAccountManager()

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.username

            

# @receiver(post_save, sender=CustomerUser)
# def create_auth_token(instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)