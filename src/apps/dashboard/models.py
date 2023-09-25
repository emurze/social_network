import reprlib

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Action(models.Model):
    """User do the action to any object."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='actions')
    verb = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
            models.Index(fields=['content_type', 'object_id']),
        )

    def __str__(self):
        return f'{self.user} {self.verb} {reprlib.repr(self.content_object)}'
