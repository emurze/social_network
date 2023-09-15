import logging
from collections.abc import Iterable

lg = logging.getLogger(__name__)


def list_mixins_to_context(mixins: Iterable, attrs: dict) -> dict:
    # Make solution for LIST

    class Returns:
        def get_context_data(self, **kwargs):
            return kwargs

    class Receiver(*mixins, Returns):
        def __init__(self):
            for key, value in attrs.items():
                setattr(self, key, value)

    return Receiver().get_context_data()
