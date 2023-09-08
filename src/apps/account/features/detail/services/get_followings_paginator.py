from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

User = get_user_model()


def get_followings_paginator(*, user: User) -> Paginator:
    all_following_users = (user.followings
                           .order_by('-username'))

    paginator = Paginator(all_following_users, 8)
    return paginator
