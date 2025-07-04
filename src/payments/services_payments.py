from cart import models


def get_line_items(order):
    line_items = []

    order_items = models.OrderItemModel.objects.filter(order=order)

    for item in order_items:
        line_items.append(
            {
                "price_data": {
                    "currency": "uah",
                    "product_data": {"name": item.product.title},
                    "unit_amount": int(item.price_at_order_time * 100),
                },
                "quantity": item.quantity,
            }
        )

    return line_items
