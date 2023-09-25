from pprint import pprint

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.models import Exists, OuterRef, When, Case, Value

from apps.post.models import Post
from apps.post.services.like.action import LikeAction
from utils.query_debugger import query_debugger

User = get_user_model()


class Command(BaseCommand):
    help = f'This test command.'

    def handle(self, *_, **__) -> None:
        @query_debugger
        def test(my_user):
            posts = Post.objects.all()
            liked = Exists(
                my_user.liked_posts.filter(id=OuterRef('id'))
            )
            posts = posts.annotate(
                action=Case(
                    When(liked, then=Value(LikeAction.UNLIKE)),
                    defult=Value(LikeAction.LIKE)
                )
            )
            pprint(my_user.liked_posts.all().count())
            pprint(posts.filter(action=Value(LikeAction.UNLIKE)).count())

        test(my_user=User.objects.all()[1:2].get())

