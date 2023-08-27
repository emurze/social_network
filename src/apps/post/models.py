import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()
lg = logging.getLogger(__name__)


class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = ('PB', 'Published')
        DRAFT = ('DF', 'Draft')

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='posts')
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
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

    def get_absolute_url(self):
        return reverse('post:detail', args=(self.slug,))

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=Post)
def set_slug_by_title(sender, instance: Post, *_, **__) -> None:
    slug = instance.slug
    if slug is None or slug == '':
        instance.slug = slugify(instance.title)
    lg.debug(f'WORKED {instance.title}')
