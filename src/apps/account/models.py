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
    followings = models.ManyToManyField('self', through='Contract',
                                        symmetrical=False,
                                        related_name='followers')

    def get_absolute_url(self):
        return reverse('account:detail', args=(self.username,))

    def __str__(self) -> str:
        return self.username


class Contract(models.Model):
    user_from = models.ForeignKey(Account, on_delete=models.CASCADE,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey(Account, on_delete=models.CASCADE,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
        )

    def __str__(self) -> str:
        return f'{self.user_from} follows {self.user_to}'

