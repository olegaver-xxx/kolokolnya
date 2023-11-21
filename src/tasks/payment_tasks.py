from dramatiq import actor
from apps.shop.services import order_changed_event


@actor
def on_order_changed(order_id: int):
    order_changed_event(order_id)
    # print("Order changed: {}".format(order_id))
