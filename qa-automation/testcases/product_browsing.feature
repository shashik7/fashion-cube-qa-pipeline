# FC-001 | Fashion Cube – Product Browsing Feature
# Requirement: AC-03 (Product Browsing), AC-04 (Search & Filter), AC-05 (Categories)

Feature: Product Browsing, Search, and Category Navigation
  As a Fashion Cube user
  I want to browse, search, and filter products
  So that I can find the items I want to purchase

  # ---------- Functional Test Cases ----------

  @FC-001 @smoke @ui
  Scenario: FC-001_TC014 – Home page displays product listings
    Given the user is on the Fashion Cube home page
    Then the page should display a list of products
    And each product should show image, title, and price

  @FC-001 @smoke @ui
  Scenario: FC-001_TC015 – Navigate to single product detail page
    Given the user is on the Fashion Cube home page
    When the user clicks on a product
    Then the user should be redirected to the product detail page
    And the product detail page should display title, description, price, and image

  @FC-001 @ui
  Scenario: FC-001_TC016 – Search products by keyword
    Given the user is on the Fashion Cube home page
    When the user searches for "shirt"
    Then the search results should display products matching "shirt"

  @FC-001 @ui
  Scenario: FC-001_TC017 – Navigate to category page via shop menu
    Given the user is on the Fashion Cube home page
    When the user hovers over the "shop" menu
    And selects a department category
    Then the user should be redirected to the category page
    And products from that category should be displayed

  @FC-001 @ui
  Scenario: FC-001_TC018 – Filter products by price range
    Given the user is on a category page
    When the user applies a price range filter
    Then only products within the selected price range should be displayed

  # ---------- Negative Test Cases ----------

  @FC-001 @negative @ui
  Scenario: FC-001_TC019 – Search with no matching results
    Given the user is on the Fashion Cube home page
    When the user searches for "xyznonexistent123"
    Then the page should display no products found message

  @FC-001 @negative @ui
  Scenario: FC-001_TC020 – Navigate to non-existent product ID
    Given the user navigates to "/fashion-cube/single-product/invalidid123"
    Then the page should display an error or not found state

  # ---------- Edge Cases ----------

  @FC-001 @edge @ui
  Scenario: FC-001_TC021 – Search with special characters
    Given the user is on the Fashion Cube home page
    When the user searches for "<script>alert(1)</script>"
    Then the system should handle the input safely without executing scripts

  @FC-001 @edge @ui
  Scenario: FC-001_TC022 – Search with empty query
    Given the user is on the Fashion Cube home page
    When the user searches with an empty query
    Then the system should display all products or a helpful message

  # ---------- Boundary Cases ----------

  @FC-001 @boundary @ui
  Scenario: FC-001_TC023 – Search with maximum length query (500 chars)
    Given the user is on the Fashion Cube home page
    When the user searches with a 500-character query string
    Then the system should handle the long query without crashing

  # ---------- State Transition ----------

  @FC-001 @ui
  Scenario: FC-001_TC024 – Navigate Home → Product → Back to Home
    Given the user is on the Fashion Cube home page
    When the user clicks on a product
    And then navigates back to the home page
    Then the home page should display correctly with all products
