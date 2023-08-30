import logging
import random

from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.db.models import TextField
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()
lg = logging.getLogger(__name__)


class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = ('PB', 'Published')
        DRAFT = ('DF', 'Draft')

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='posts')
    slug = models.SlugField(max_length=128, unique=True)
    description = TextField()
    photo = models.ImageField(upload_to='posts/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.PUBLISHED)

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
        )

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except IntegrityError:
            lg.warning('Post slug integrity error!')
            self.slug = None
            self.save(*args, **kwargs)

    def __str__(self) -> str:
        return self.description[:30]


@receiver(pre_save, sender=Post)
def set_slug_by_title(sender, instance: Post, *_, **__) -> None:
    lg.debug(f'Slug signal worked')
    slug = instance.slug
    if slug is None or slug == '':
        instance.slug = random.randint(100_000_000_000, 999_999_999_999_999)
