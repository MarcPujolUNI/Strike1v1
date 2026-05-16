Feature: Sign Up User
  In order to join the competitive platform and track my match statistics
  As an anonymous player
  I want to register an account with my credentials and country

  Scenario: Successful registration with valid data
    Given I am an anonymous user on the landing page
    Given a country exists with id 68 and name "Spain" and iso "ES"
    When I navigate to the registration page
    And I fill out the sign up form with data:
      | username | email          | password  | user_country_name |
      | test     | test@gmail.com | patata123 | Spain             |
    And I submit the registration form
    Then I should be redirected to the login page
    And A WebUser with username "test" should exist in the database
    And A CounterUser profile for "test" should be automatically initialized