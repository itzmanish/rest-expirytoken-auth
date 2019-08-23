import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.conf import settings
from django.core.validators import RegexValidator
from . import identicon

USERNAME_REGEX = '^[a-zA-Z0-9]+(?:[_]?[a-zA-Z0-9])*$'


def image_handler(instance, filename):
    ext = filename.split('.')[-1]
    return f"user_{instance.id}.{ext}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.set_identicon()
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):

        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


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
