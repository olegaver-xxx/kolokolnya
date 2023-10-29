from yookassa import Configuration
import os
from apps.utils.services import get_value

YOOKASSA_SHOP_ID = get_value('yookassa_apikey') or os.getenv('YOOKASSA_SHOP_ID')
YOOKASSA_API_KEY = get_value('yookassa_secretkey') or os.getenv('YOOKASSA_API_KEY')

Configuration.configure(YOOKASSA_SHOP_ID, YOOKASSA_API_KEY)
print('YOOKASSA INITIALIZED')
