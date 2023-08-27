import logging

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.urls import reverse

lg = logging.getLogger(__name__)


class Account(AbstractUser):
    class Gender(models.TextChoices):
        FEMALE = ('FL', 'Female')
        MALE = ('ML', 'Male')
        CUSTOM = ('CM', 'Custom')

    description = models.TextField(
        null=True,
        verbose_name='Description',
        max_length=120,
    )
    photo = models.ImageField(upload_to='accounts/%Y/%m/%d/',
                              blank=True, null=True, verbose_name='Avatar')
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=2, choices=Gender.choices)

    def get_absolute_url(self):
        return reverse('account:detail', args=(self.username,))
