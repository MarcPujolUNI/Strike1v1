Feature: Play Page and Matchmaking UI
  In order to start a game
  As a logged-in player
  I want to access the play page and see the matchmaking button

  Scenario: Display matchmaking options correctly
    When I navigate to the play page
    Then I should see the header "START PLAYING"
    And I should see a button with text "FIND MATCH"
    Then I click on the matchmaking button