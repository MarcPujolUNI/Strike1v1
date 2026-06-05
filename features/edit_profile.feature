Feature: Edit User Profile
  In order to keep my information updated
  As a logged-in player
  I want to be able to edit my profile details, password, and avatar

  Background:
    Given A WebUser exists with username "tester" and password "patata123"
    And I am logged in as "tester" with password "patata123"

  Scenario: Successfully update profile information
    When I navigate to the profile page
    And I click on the "Edit Profile Info" button
    And I fill in the profile username with "tester_updated"
    And I fill in the profile email with "updated@gmail.com"
    And I select "1v1_crete" as my favourite map
    And I click the "Save Changes" button
    Then I should see a success message "Profile updated successfully."
    And the username input should have "tester_updated"

  Scenario: Change user password
    When I navigate to the profile page
    And I click on the "Edit Password" button
    And I fill in the password change form with old "patata123" and new "new_patata123"
    And I click the "Update Password" button
    Then I should see a success message "Password updated successfully."

  Scenario: Successfully update profile avatar picture
    When I navigate to the profile page
    And I upload a new profile picture asset "default.png"
    Then I should see a success message "Profile updated successfully."