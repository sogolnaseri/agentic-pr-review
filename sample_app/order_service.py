def calculate_order_total(price, quantity, discount_percent):
    subtotal = price * quantity
    discount = subtotal * discount_percent / 100
    total = subtotal - discount

    return total


def check_inventory(available_stock, requested_quantity):
    return available_stock >= requested_quantity


def calculate_shipping(order_total):
    if order_total >= 100:
        return 0

    return 10