Feature: Modify Existing Reviews
  As a reviewer
  I want to update the text or score of a review I created
  To adapt my feedback after subsequent matches

  Background: Setup existing review
    Given a country "ES" exists
    And a registered user "player1" exists
    And a registered user "player2" exists
    And a registered user "player3" exists
    And "player1" has reviewed "player2" with title "Decent game", rating "3", description "Normal match."

  Scenario: Successfully update an own review
    Given I log in as "player1"
    When I visit the review page for "player2"
    And I click to view my review details
    And I click on "Modify" button
    And I update the review form with title "Outstanding match", rating "5", and description "He improved remarkably."
    And I save the modifications
    Then I should see the updated review title "Outstanding match" on the review detail page

  Scenario: Security restriction prevents modifying another user's review
    Given "player3" has reviewed "player2" with title "Cheater", rating "1", description "Aimbot active."
    And I log in as "player1"
    When I visit the review detail page of "player3" on "player2"
    Then I should not see the "Modify" button