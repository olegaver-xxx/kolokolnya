# import django
# django.setup()
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from django.conf import settings

redis_broker = RedisBroker(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
#     # middleware=[m() for m in default_middleware]+[CurrentMessage(), MonitorMiddleware()]
)
dramatiq.set_broker(redis_broker)

from . import payment_tasks