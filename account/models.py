from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password')
        # if not full_name:
        #     raise ValueError('Users must have an full name')
        # if not address:
        #     raise ValueError('Users must have an address')

        user_obj = self.model(email=self.normalize_email(email))
        user_obj.password = password
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name=None, address=None, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name=None, address=None, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address', max_length=250, unique=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=True)  # non super user
    admin = models.BooleanField(default=True)  # super user
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    update_password = True

    # def save(self, *args, **kwargs):
    #     if self.admin != "True" and self.update_password:
    #         self.set_password(self.password)
    #     super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_address(self):
        if self.address:
            return self.address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have  specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permission to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
