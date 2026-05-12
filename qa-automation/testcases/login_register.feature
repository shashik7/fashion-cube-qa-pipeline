# FC-001 | Fashion Cube – Login & Registration Feature
# Requirement: AC-01 (Registration), AC-02 (Login)

Feature: User Authentication – Login and Registration
  As a Fashion Cube user
  I want to register and login to the platform
  So that I can access my shopping cart and checkout

  # ---------- Functional Test Cases ----------

  @FC-001 @smoke @ui
  Scenario: FC-001_TC001 – Successful login with valid credentials
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user enters valid email "testuser@fashioncube.com"
    And the user enters valid password "Test@12345"
    And the user clicks the "Log in" button
    Then the user should be logged in successfully
    And the page should reload with authenticated state

  @FC-001 @smoke @ui
  Scenario: FC-001_TC002 – Successful registration with valid details
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user clicks "New user ? Please Register"
    And the user enters name "John Doe"
    And the user enters email "john.doe@example.com"
    And the user enters password "Secure@123"
    And the user clicks the "Register" button
    Then the registration should be successful
    And the login form should be displayed

  # ---------- Negative Test Cases ----------

  @FC-001 @negative @ui
  Scenario: FC-001_TC003 – Login with invalid email format
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user enters invalid email "not-an-email"
    And the user enters valid password "Test@12345"
    And the user clicks the "Log in" button
    Then the login should fail with validation error

  @FC-001 @negative @ui
  Scenario: FC-001_TC004 – Login with incorrect password
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user enters valid email "testuser@fashioncube.com"
    And the user enters wrong password "WrongPassword"
    And the user clicks the "Log in" button
    Then the login should fail with "Incorrect email or password"

  @FC-001 @negative @ui
  Scenario: FC-001_TC005 – Login with empty email field
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user leaves the email field empty
    And the user enters valid password "Test@12345"
    And the user clicks the "Log in" button
    Then the login should fail with validation error

  @FC-001 @negative @ui
  Scenario: FC-001_TC006 – Login with empty password field
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user enters valid email "testuser@fashioncube.com"
    And the user leaves the password field empty
    And the user clicks the "Log in" button
    Then the login should fail with validation error

  @FC-001 @negative @ui
  Scenario: FC-001_TC007 – Register with duplicate email
    Given the user is on the Fashion Cube home page
    When the user opens the registration form
    And the user registers with an already existing email "testuser@fashioncube.com"
    Then the registration should fail with "user is existed"

  @FC-001 @negative @ui
  Scenario: FC-001_TC008 – Register with empty fields
    Given the user is on the Fashion Cube home page
    When the user opens the registration form
    And the user clicks the "Register" button without filling any fields
    Then the registration should fail with validation error

  # ---------- Edge Cases ----------

  @FC-001 @edge @ui
  Scenario: FC-001_TC009 – Login with SQL injection in email field
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user enters email "' OR '1'='1"
    And the user enters password "anything"
    And the user clicks the "Log in" button
    Then the login should fail safely without exposing system errors

  @FC-001 @edge @ui
  Scenario: FC-001_TC010 – Login with XSS payload in email field
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user enters email "<script>alert('xss')</script>"
    And the user enters password "anything"
    And the user clicks the "Log in" button
    Then the login should fail and no script should execute

  # ---------- Boundary Cases ----------

  @FC-001 @boundary @ui
  Scenario: FC-001_TC011 – Login with minimum length password (1 char)
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    And the user enters valid email "testuser@fashioncube.com"
    And the user enters password "a"
    And the user clicks the "Log in" button
    Then the login should fail

  @FC-001 @boundary @ui
  Scenario: FC-001_TC012 – Register with extremely long name (255 chars)
    Given the user is on the Fashion Cube home page
    When the user opens the registration form
    And the user enters a 255-character name
    And the user enters email "longname@example.com"
    And the user enters password "Valid@123"
    And the user clicks the "Register" button
    Then the system should handle the long name gracefully

  # ---------- State Transition ----------

  @FC-001 @ui
  Scenario: FC-001_TC013 – Toggle between Login and Register forms
    Given the user is on the Fashion Cube home page
    When the user opens the login modal
    Then the login form should be displayed
    When the user clicks "New user ? Please Register"
    Then the registration form should be displayed
    When the user clicks "Already have an account ? Please login."
    Then the login form should be displayed
