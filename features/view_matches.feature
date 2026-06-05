Feature: View Match History
  In order to track my performance and past games
  As a logged-in player
  I want to be able to view my match history

  Background:
    Given A WebUser exists with username "tester" and password "patata123"
    And I am logged in as "tester" with password "patata123"

  Scenario: Successfully view empty match history
    When I navigate to the match history page
    Then I should see a message "No matches found in the logs"

  Scenario: Successfully view recent matches list and pagination
    Given The user has "12" recorded matches on map "1v1_crete"
    When I navigate to the match history page
    Then I should see a list of "10" matches
    And I should see the pagination controls