@loginfeature @mobile
Feature: Login

  @login1
  Scenario: Successful login mobile web
    Given [mweb] the user navigates to the login page
    When [mweb] the user enters valid credentials
    Then [mweb] the user should be logged in
