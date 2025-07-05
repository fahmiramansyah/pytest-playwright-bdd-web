@loginfeature @desktop
Feature: Login

  @login1
  Scenario: Successful login desktop
    Given [desktop] the user navigates to the login page
    When [desktop] the user enters valid credentials
    Then [desktop] the user should be logged in
