Feature: Create New Player Reviews
  As a registered user
  I want to publish a new review for an opponent
  To rate my competitive matchmaking experience

  Background: Setup base infrastructure
    Given a country "ES" exists
    And a registered user "player1" exists
    And a registered user "player2" exists

  Scenario: Successfully publish a 5-star review
    Given I log in as "player1"
    When I visit the review page for "player2"
    And I click the write a review button
    And I fill in the review form with title "Excellent aim", rating "5", and description "Very good crosshair placement."
    And I submit the review form
    Then I should see my review with title "Excellent aim" in the "Your review" section