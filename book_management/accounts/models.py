import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager




def generate_unique_username(base):
    while True:
        suffix = ''.join(random.choices(string.digits + string.ascii_lowercase, k=4))
        uname = f"{base}{suffix}"
        if not Accounts.objects.filter(username=uname).exists():
            return uname    
                
                
# Custom User Manager
class MyAccountManager(BaseUserManager):
    
    def create_user(self, email, username=None, password=None, first_name='', last_name='', **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        if not username:
            base_username = email.split('@')[0]
            username = generate_unique_username(base_username)  

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, **extra_fields)


# Custom User Model
class Accounts(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100,blank=True,null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image=models.ImageField(blank=True,null=True,upload_to='profiles/')
    google_id = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
