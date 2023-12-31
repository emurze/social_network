import logging

from django.contrib.auth import get_user_model
from django.db import models, IntegrityError

from apps.post.dal import PostDAL

User = get_user_model()
lg = logging.getLogger(__name__)


class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = ('PB', 'Published')
        DRAFT = ('DF', 'Draft')

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='posts')
    description = models.TextField()
    photo = models.ImageField(upload_to='posts/%Y/%m/%d', null=True,
                              blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.PUBLISHED)
    liked_users = models.ManyToManyField(User, through='LikeContract',
                                         related_name='liked_posts')

    objects = models.Manager()
    ext_objects = PostDAL()

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
        )

    def __str__(self) -> str:
        return self.description[:30]


class LikeContract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='like_contracts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='like_contracts')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'user {self.user} liked post {self.post}'


class Reply(models.Model):
    content = models.CharField(max_length=128)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='replies')
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
        )
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self) -> str:
        return ('user <%s> add comment <%s> for post <%s>' %
                (self.user, self.content, self.post))
