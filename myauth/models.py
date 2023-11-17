from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.core.validators import MaxValueValidator , MinValueValidator
# Create your models here


class User(AbstractBaseUser , PermissionsMixin):
    username = models.CharField(
                    max_length=32
                )
    year  = models.IntegerField(
                validators=[
                    MinValueValidator(1),
                    MaxValueValidator(5)
                ]
            )
    display_picture = models.URLField(max_length=200 , null=True , blank=True)
    email = models.EmailField(
                verbose_name="email address",
                max_length=255,
                unique=True
            )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['year']




def get_anonymous_user_instance(User):
    return User(username='anonymus' , display_picture='null' , year=1 , email='anonymus@anonymus.com')