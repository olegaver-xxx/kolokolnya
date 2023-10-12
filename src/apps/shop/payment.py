import uuid
from django.views.generic import View
from yookassa import Configuration, Payment


class PaymentView(View):
    def get(self, request):
        with open(...) as f:
            ...



# Configuration.account_id = 266415
# Configuration.secret_key = 'test_O2RjdQ4_RePoGfTKkCPlbD5rMmzg2nRNNkxTPQ9LCKI'
#
# payment = Payment.create({
#     "amount": {
#         "value": "100.00",
#         "currency": "RUB"
#     },
#     "confirmation": {
#         "type": "redirect",
#         "return_url": "home"
#     },
#     "capture": True,
#     "description": "Заказ №1"
# }, uuid.uuid4())