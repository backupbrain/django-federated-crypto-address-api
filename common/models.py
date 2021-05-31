from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
import uuid
from rest_framework_api_key.models import AbstractAPIKey


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers.

    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    email = models.EmailField(_('Email Address'), unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    success_message = "%(calculated_field)s was created successfully"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Represent as String."""
        return self.email


class Coin(models.Model):
    """Coin."""

    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Represent as string."""
        return self.code


class WalletAddress(models.Model):
    """WalletAddress."""

    username = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
