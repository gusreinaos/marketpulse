from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, User, BaseUserManager, PermissionsMixin
from .models import CustomUser

#admin.site.unregister(User)
admin.site.register(CustomUser)