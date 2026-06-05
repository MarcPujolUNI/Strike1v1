Feature: Log In / Log Out User
  In order to access my competitive profile and matchmaking
  As a registered player
  I want to log into my account and log out when I finish

  Background:
    Given I am an anonymous user on the landing page
    And A WebUser exists with username "test" and password "patata123"

  Scenario: Successful login with valid credentials
    When I navigate to the login page
    And I fill out the login form with username "test" and password "patata123"
    And I submit the login form
    Then I should be redirected to the landing page
    And I should see a welcome message or my dashboard

  Scenario: Successful logout
    When I navigate to the login page
    And I fill out the login form with username "test" and password "patata123"
    And I submit the login form
    And I click on the logout button
    Then I should be redirected to the landing page
    And I should see the "Login" and "Sign Up" button again on the header