from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser

# Create your models here.

# Custom User Manager


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('User must have a valid name')
        if not first_name:
            raise ValueError('User must have a valid first name')
        if not last_name:
            raise ValueError('User must have a valid last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_admin = True
        user.role = 'admin'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    Custom user manager for our own user model
    All we have to do is override
    '''
    first_name = models.CharField(
        max_length=64, blank=False, null=False, verbose_name='First Name')
    last_name = models.CharField(
        max_length=64, blank=False, null=False, verbose_name='Last Name')
    email = models.EmailField(blank=False, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    role = models.CharField(max_length=16, default='worker')
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return '{fname} {lname}'.format(fname=self.first_name, lname=self.last_name)

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def username(self):
        return self.get_full_name()
