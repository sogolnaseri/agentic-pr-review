### 1. Potential Bugs

- **Division by Zero**: If `discount_percent` is not validated, a user might accidentally pass an unexpected type (like a string or None), leading to an unexpected calculation in `discount = subtotal * discount_percent / 100`.
- **Negative Values**: The `price`, `quantity`, and `discount_percent` could be negative, which does not make sense for an order total calculation. It would lead to incorrect total amounts or unexpected results.
- **Floating Point Precision**: When dealing with financial calculations, the potential inaccuracy of floating-point arithmetic can lead to incorrect totals.

### 2. Missing Validations

- **Input Types**: The function does not validate if `price`, `quantity`, and `discount_percent` are of numeric types (e.g., int or float).
- **Valid Range**: There should be checks to ensure `price` and `quantity` are non-negative values. Typically, a discount percent should also be between 0 and 100 (inclusive).
- **Inventory Check**: In `check_inventory`, there’s no validation whether `available_stock` or `requested_quantity` are non-negative. They should also be checked for numeric types.

### 3. Edge Cases

- **Zero Values**: What happens if `quantity` is 0? The total should be 0; however, consider if it affects the overall logic.
- **Large Values**: Extremely large input values for `price`, `quantity`, or `discount_percent` might cause overflow errors or unexpected behavior.
- **Negative Discount**: If a negative discount percent is passed, it might not throw an error but could provide an illogical `total`.
- **Boundary Testing**: Check scenarios where the `order_total` is exactly 100, ensuring it behaves correctly at the threshold in `calculate_shipping`.

### 4. Recommended Unit Tests

- For `calculate_order_total`:
  - Test with positive integers/floats for `price`, `quantity`, and `discount_percent`.
  - Test with zero values for `price` and `quantity`.
  - Test with negative values for `price`, `quantity`, and `discount_percent`.
  - Test with large values (e.g., maximum float).
- For `check_inventory`:
  - Test with `available_stock` greater than, less than, and equal to `requested_quantity`.
  - Test with zero/negative values for both `available_stock` and `requested_quantity`.

- For `calculate_shipping`:
  - Test with `order_total` being less than, equal to, and greater than 100.
  - Test extreme values, checking how the function responds to very high order totals.

By addressing the above points, you ensure that the code is more robust, reliable, and secure against invalid inputs and unexpected usage.
