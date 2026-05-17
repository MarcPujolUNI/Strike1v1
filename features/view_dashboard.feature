Feature: View Dashboard
  In order to review my competitive standing
  As an authenticated player
  I want to view a dashboard with my match summary

  Background:
    Given I am an anonymous user on the landing page
    And A WebUser exists with username "test" and password "patata123"

  Scenario: Successful display of personalized dashboard data
    When I navigate to the login page
    And I fill out the login form with username "test" and password "patata123"
    And I submit the login form
    Then I should be redirected to the landing page
    And The navigation link should display "DASHBOARD"
    And I should see my competitive status summary