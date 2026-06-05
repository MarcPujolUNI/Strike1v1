Feature: Remove Existing Reviews
  As a reviewer
  I want to delete a review I submitted
  To withdraw my feedback from the player profile

  Background: Setup existing review for deletion
    Given a country "ES" exists
    And a registered user "player1" exists
    And a registered user "player2" exists
    And a registered user "player3" exists
    And "player1" has reviewed "player2" with title "Toxic behavior", rating "1", description "Flame in chat."

  Scenario: Successfully remove an own review via confirmation modal
    Given I log in as "player1"
    When I visit the review page for "player2"
    And I click to view my review details
    And I click on "Delete" button
    And I confirm the deletion by clicking "Yes, Delete Review" button
    Then I should be redirected to the review page of "player2"
    And I should not see "Toxic behavior" in the reviews list

  Scenario: Security restriction prevents deleting another user's review
    Given "player3" has reviewed "player2" with title "Fair player", rating "4", description "Good connections."
    And I log in as "player1"
    When I visit the review detail page of "player3" on "player2"
    Then I should not see the "Delete" button