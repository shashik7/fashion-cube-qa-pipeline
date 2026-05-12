# FC-001 | Fashion Cube – Shopping Cart Feature
# Requirement: AC-06 (Shopping Cart), AC-07 (Checkout)

Feature: Shopping Cart Management and Checkout
  As an authenticated Fashion Cube user
  I want to manage my shopping cart
  So that I can purchase products via PayPal checkout

  # ---------- Functional Test Cases ----------

  @FC-001 @smoke @ui
  Scenario: FC-001_TC025 – Add product to cart
    Given the user is logged in
    When the user navigates to a product detail page
    And the user clicks "Add to Cart"
    Then the product should be added to the cart
    And the cart badge count should increase by 1

  @FC-001 @ui
  Scenario: FC-001_TC026 – View shopping cart page
    Given the user is logged in
    And the user has items in the cart
    When the user navigates to the cart page
    Then the cart should display all added items
    And the subtotal, taxes, shipping, and total should be displayed

  @FC-001 @ui
  Scenario: FC-001_TC027 – Increase item quantity in cart
    Given the user is logged in
    And the user has items in the cart
    When the user increases the quantity of an item
    Then the quantity should update
    And the total price should recalculate

  @FC-001 @ui
  Scenario: FC-001_TC028 – Decrease item quantity in cart
    Given the user is logged in
    And the user has items in the cart
    When the user decreases the quantity of an item
    Then the quantity should update
    And the total price should recalculate

  @FC-001 @ui
  Scenario: FC-001_TC029 – Cart shows empty state
    Given the user is logged in
    And the user has no items in the cart
    When the user navigates to the cart page
    Then the empty cart image should be displayed

  @FC-001 @smoke @ui
  Scenario: FC-001_TC030 – Initiate checkout
    Given the user is logged in
    And the user has items in the cart
    When the user clicks "Confirm Checkout"
    Then the user should be redirected to PayPal payment page

  # ---------- Negative Test Cases ----------

  @FC-001 @negative @ui
  Scenario: FC-001_TC031 – Access cart without authentication
    Given the user is not logged in
    When the user navigates to the cart page directly
    Then the user should be redirected to PageNotFound

  @FC-001 @negative @ui
  Scenario: FC-001_TC032 – Add invalid product to cart via API
    Given the user is logged in
    When a cart request is made with an invalid product ID
    Then the API should return "invalid request body" error

  # ---------- Edge Cases ----------

  @FC-001 @edge @ui
  Scenario: FC-001_TC033 – Add same product to cart multiple times
    Given the user is logged in
    When the user adds the same product to cart 3 times
    Then the cart should show 1 line item with quantity 3

  @FC-001 @edge @ui
  Scenario: FC-001_TC034 – Add product variant (size/color) to cart
    Given the user is logged in
    When the user selects a product variant with color "Red" and size "L"
    And the user adds it to the cart
    Then the cart should display the variant details

  # ---------- Boundary Cases ----------

  @FC-001 @boundary @ui
  Scenario: FC-001_TC035 – Decrease item quantity to zero
    Given the user is logged in
    And the user has 1 item with quantity 1 in the cart
    When the user decreases the quantity
    Then the item should be removed from the cart

  # ---------- State Transition ----------

  @FC-001 @ui
  Scenario: FC-001_TC036 – Cart state: Empty → Item Added → Quantity Changed → Checkout
    Given the user is logged in
    And the cart is empty
    When the user adds a product
    Then the cart should transition from empty to populated state
    When the user increases the quantity
    Then the total should update
    When the user clicks "Confirm Checkout"
    Then the checkout process should initiate
