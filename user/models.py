from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # Set related_name for user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_user_permissions',
        verbose_name='client_user',
        blank=True,
    )

    # Set related_name for groups
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        verbose_name='client_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    def __str__(self):
        return self.email
