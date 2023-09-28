import abc
import logging

from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest

User = get_user_model()
lg = logging.getLogger(__name__)


class BaseAuthBackend(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, request: WSGIRequest,
                     **credentials) -> User | None: ...

    @abc.abstractmethod
    def get_user(self, user_id: int) -> User | None: ...


class EmailAuthBackend(BaseAuthBackend):
    def authenticate(self, request: WSGIRequest, **credentials) -> User | None:
        lg.debug('works')

        if (email := credentials.get('username')) is None:
            lg.debug('bad')
            return None
        if (password := credentials.get('password')) is None:
            return None

        try:
            user = User.objects.get(email=email)

            lg.debug(f'password {password}')

            if user.check_password(password):
                return user
            else:
                return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int) -> User | None:
        try:
            user = User.objects.get(id=user_id)
            return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
