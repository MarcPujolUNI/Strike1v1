Feature: Configuration & Legal Pages
  In order to know about legal, privacy and cookie policy
  As a user
  I want to view the Terms of Service, Privacy Policy, and Cookie Policy pages

  Scenario: View Terms of Service
    When I navigate to the "Terms of Service" page
    Then I should see "Terms of Service" in the title
    And I should see the educational disclaimer

  Scenario: View Privacy Policy
    When I navigate to the "Privacy Policy" page
    Then I should see "Privacy Policy" in the title
    And I should see how academic data is handled

  Scenario: View Cookie Policy
    When I navigate to the "Cookie Policy" page
    Then I should see "Cookie Policy" in the title
    And I should see information about session tokens