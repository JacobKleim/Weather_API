import logging
from functools import update_wrapper, wraps

from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def external_api_error_handler(func):
    """
    Оборачивает функцию для перехвата ошибок внешнего API
    и возвращает 503 в случае ValueError.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Внешняя ошибка API в {func.__name__}: {str(e)}", exc_info=True)
            return Response({"error": "Ошибка внешнего API"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return update_wrapper(wrapper, func)
