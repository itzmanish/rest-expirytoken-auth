import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator

from rest_framework.authtoken.models import Token
from . import identicon

USERNAME_REGEX = '^[a-zA-Z0-9]+(?:[_]?[a-zA-Z0-9])*$'


def image_handler(instance, filename):
    ext = filename.split('.')[-1]
    return f"user_{instance.id}.{ext}"


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.set_identicon()
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(username, self.normalize_email(email), password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, self.normalize_email(email), password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Username must be alphanumeric and cannot contain any special character.',
                           code='invalid_username'
                           )],
        unique=True
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email_address',
    )
    name = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to=image_handler, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        # I don't know what is it. so let it be true for now
        return True

    def has_perm(self, perm, obj=None):
        # I don't know what is it. so let it be true for now
        return True

    def set_identicon(self):
        avatar = identicon.render(self.username)
        upload_path = os.path.join(settings.MEDIA_ROOT, 'avatar')
        file = f'{upload_path}/avatar_user_{self.username}.png'
        with open(file, 'wb') as f:
            f.write(avatar)
        self.avatar = f'avatar/user_{self.username}.png'


class ExpiringToken(Token):

    """Extend Token to add an expired method."""

    class Meta(object):
        proxy = True

    def expired(self):
        """Return boolean indicating token expiration."""
        now = timezone.now()
        if self.created < now - settings.TOKEN_EXPIRE_TIME:
            return True
        return False
