from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, identifier, password=None,**extra_fields):
        if '@' in identifier:
            email = self.normalize_email(identifier)
            phone_number = extra_fields.pop('phone_number', None)
        else:
            email = extra_fields.pop('email', None)
            phone_number = identifier
        if not phone_number and not email:
            raise ValueError(_('Users must have either a phone number or email address'))
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, identifier, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(identifier, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True,null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True,null=True,blank=True)
    phone_number = models.CharField(_('phone number'), max_length=30, blank=True, unique=True,null=True)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    is_banned = models.BooleanField(_('banned'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name or self.email or self.phone_number