from pytest_bdd import scenarios, given, when, then

scenarios('../scenario/login_mweb.feature')

@given('[mweb] the user navigates to the login page')
def go_to_login_page(login_page):
    login_page.navigate()

@when('[mweb] the user enters valid credentials')
def enter_credentials(login_page):
    login_page.login("testingprodfahmi@yopmail.com", "P@ssw0rd")

@then('[mweb] the user should be logged in')
def check_dashboard(login_page):
    login_page.is_logged_in()
