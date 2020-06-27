from django.db import models
from django.contrib.auth.models import AbstractUser
from . managers import CustomUserManager


class Department(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Name', blank=False)
    code = models.CharField(
        max_length=60, verbose_name='Code department', blank=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(
        max_length=100, verbose_name='First name', blank=True)
    last_name = models.CharField(
        max_length=100, verbose_name='Last name', blank=True)
    phone_number = models.CharField(
        max_length=100, verbose_name='Phone number', unique=True, blank=False)
    status = models.BooleanField(default=False, verbose_name='Status')
    is_collaborator = models.BooleanField(
        default=False, verbose_name='Collaborator')
    password = models.CharField(
        max_length=128, verbose_name='Password', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='department', verbose_name='Code department', null=True)

    USERNAME_FIELD = 'phone_number'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @ property
    def full_fio(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return f'Phone: {self.phone_number}, First name: {self.first_name}'
