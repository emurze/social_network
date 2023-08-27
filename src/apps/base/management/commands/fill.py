import logging
from datetime import datetime
import random

import lorem
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.post.models import Post

lg = logging.getLogger(__name__)
User = get_user_model()
DEFAULT_USER_AMOUNT = 30
DEFAULT_POST_AMOUNT = 100


class Command(BaseCommand):
    help = f'This command fill database.'

    def handle(self, *_, **__) -> None:
        User.objects.exclude(is_staff=True).delete()
        Post.objects.all().delete()

        current_year = datetime.now().year
        for index in range(1, DEFAULT_USER_AMOUNT+1):
            User.objects.create_user(
                username=f'user_{index}',
                email='user_{index}@gmail.com',
                password='qwerty123',
                birthday=datetime(
                    year=(current_year - random.randint(16, 36)),
                    month=1,
                    day=1,
                ).strftime('%Y-%m-%d'),
                gender=random.choice(('ML', 'FL')),
                description=lorem.sentence(),
            )
            lg.debug(f'user_{index} was created.')

        staff_user = User.objects.filter(is_staff=True).first()

        for index in range(1, DEFAULT_POST_AMOUNT):
            Post.objects.create(
                user=staff_user,
                title=f'Post_{index}',
                description=lorem.sentence(),
            )
            lg.debug(f'Post_{index} was created.')
