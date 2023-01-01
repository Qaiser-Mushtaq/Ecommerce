from django import template


register = template.Library()

@register.filter(name='order_price_total')
def order_price_total(product  , quantity):
    return product.price*product.quantity


@register.filter(name='orders_total')
def order_total(product, quantity):
    sum = 0
    for p in product:
        sum += order_price_total(p, quantity)
    return sum