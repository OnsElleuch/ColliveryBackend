from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Trip(models.Model):
    starting_address = models.CharField(max_length=200)
    arrival_address = models.CharField(max_length=200)
    date = models.DateTimeField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return "Trip {} user {} ".format(self.id, self.user_id)

    def to_dict(self):
        return {
            "id": self.id,
            "start address": self.starting_address,
            "arrival address": self.arrival_address,
            "date": self.date,
            "user": self.user_id
        }


class Delivery(models.Model):
    starting_address = models.CharField(max_length=200)
    arrival_address = models.CharField(max_length=200)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    info = models.CharField(max_length=500)

    def __str__(self):
        return "Delivery ID {} to the user {} by the trip {} .".format(self.id, self.user_id, self.trip_id)

    def to_dict(self):
        return {
            "id": self.id,
            "start address": self.starting_address,
            "arrival address": self.arrival_address,
            "user": self.user_id,
            "weight": self.weight,
            "trip": self.trip_id,
            "more info": self.info
        }
