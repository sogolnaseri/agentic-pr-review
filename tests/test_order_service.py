import pytest
from sample_app.order_service import calculate_order_total, check_inventory, calculate_shipping

def test_calculate_order_total_positive_inputs():
    assert calculate_order_total(100, 2, 10) == 180  # Normal case: 100 * 2 - 10% discount

def test_calculate_order_total_zero_quantity():
    assert calculate_order_total(100, 0, 10) == 0  # Total should be zero when quantity is 0

def test_calculate_order_total_negative_price():
    with pytest.raises(ValueError):
        calculate_order_total(-100, 2, 10)  # Negative price should raise ValueError

def test_calculate_order_total_negative_quantity():
    with pytest.raises(ValueError):
        calculate_order_total(100, -2, 10)  # Negative quantity should raise ValueError

def test_calculate_order_total_negative_discount():
    with pytest.raises(ValueError):
        calculate_order_total(100, 2, -10)  # Negative discount should raise ValueError

def test_calculate_order_total_large_values():
    assert calculate_order_total(1e10, 100, 5) == 9.95e11  # Test with large values

def test_check_inventory_sufficient_stock():
    assert check_inventory(10, 5) is True  # Enough stock available

def test_check_inventory_exact_stock():
    assert check_inventory(10, 10) is True  # Edge case: exactly enough stock

def test_check_inventory_insufficient_stock():
    assert check_inventory(10, 15) is False  # Not enough stock available

def test_check_inventory_negative_available_stock():
    with pytest.raises(ValueError):
        check_inventory(-5, 2)  # Negative stock should raise ValueError

def test_calculate_shipping_below_threshold():
    assert calculate_shipping(99.99) == 10  # Shipping cost should be 10 below the threshold

def test_calculate_shipping_exact_threshold():
    assert calculate_shipping(100) == 0  # Shipping cost should be 0 at threshold

def test_calculate_shipping_above_threshold():
    assert calculate_shipping(101) == 0  # Shipping cost should be 0 above the threshold