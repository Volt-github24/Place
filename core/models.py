from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, username=None, **extra_fields):
        
        if not email:
            raise ValueError('le champ email est requis')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password=None, username=None):
        
        user = self.create_user(email=email, password=password, username=username)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=False, null=True)
    last_name = models.CharField(max_length=150, blank=False, null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile')
    date_joined = models.DateTimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    class Meta:
        ordering = ('username',)

    def __str__(self):
        
        if self.username:
            return self.username
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True