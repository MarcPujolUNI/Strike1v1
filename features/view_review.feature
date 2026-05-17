Feature: Review Page Navigation and Security Restrictions
  As a registered user
  I want to visit another player's review list
  To check their community reputation

  Background: Setup base infrastructure
    Given a country "ES" exists
    And a registered user "player1" exists
    And a registered user "player2" exists

  Scenario: Successfully view another player's review page
    Given I log in as "player1"
    When I visit the review page for "player2"
    Then I see the header "Reviews from the player - player2 -"
    And I should see the text "NO REVIEWS FOUND FOR THIS PLAYER"

  Scenario: Cannot review oneself due to security constraints
    Given I log in as "player1"
    When I visit the review page for "player1"
    Then I should not see the option to write a review