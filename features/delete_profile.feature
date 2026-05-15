Feature: Delete User Profile Account
  In order to maintain my privacy and data control
  As a logged-in player
  I want to be able to permanently delete my own account

  Background:
    Given A WebUser exists with username "tester" and password "patata123"
    And I am logged in as "tester" with password "patata123"

  Scenario: Successfully delete own user account
    When I navigate to the profile page
    And I click on the delete account trigger button
    And I confirm the account deletion inside the modal
    Then I should be redirected to the landing page