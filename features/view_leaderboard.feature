Feature: View Global Leaderboard
  In order to see how I compare against other players
  As a player
  I want to view a structured ranking sorted by competitive score

  Background:
    Given the following countries exist:
      | country_iso | country_name   |
      | ES          | Spain          |
      | US          | United States  |
    And the following players exist with scores:
      | username  | score | country_iso |
      | player_ES | 1500  | ES          |
      | player_US | 2800  | US          |
      | player_B2 | 2100  | US          |

  Scenario: Display players sorted by ranking points
    When I navigate to the leaderboard page
    Then I should see "LEADERBOARD" in the header
    And the players should be listed in this order:
      | username  |
      | player_US |
      | player_B2 |
      | player_ES |

  Scenario: Filter leaderboard by country
    When I navigate to the leaderboard page
    And I filter the leaderboard by country "Spain"
    Then the players should be listed in this order:
      | username  |
      | player_ES |
    And I should not see "player_US"