import os
from apps.utils.services import get_value


def get_credentials():
    yookassa_shop_id = get_value('yookassa_apikey') or os.getenv('YOOKASSA_SHOP_ID')
    yookassa_api_key = get_value('yookassa_secretkey') or os.getenv('YOOKASSA_API_KEY')
    return yookassa_shop_id, yookassa_api_key

