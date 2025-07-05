from playwright.sync_api import Page

# fyi:
# CSS: "selector" atau "css=selector"
# XPath: "xpath=//path"
# ID: "#idname"
# Text: "text=TextHere"

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_button_home = 'xpath=//span[text()="Masuk"]'
        self.username_input = '#username'
        self.password_input = '#password'
        self.login_button_popup = 'xpath=//button[text()="Masuk"]'
        self.dontallow_notification = '#moe-dontallow_button'
        self.account_header = 'xpath=//*[@data-testid="profile-menu-header"]'     

    def navigate(self):
        self.page.goto("https://jamtangan.com")

    def login(self, username: str, password: str):
        self.page.locator(self.dontallow_notification).wait_for(state="visible")
        self.page.click(self.dontallow_notification)
        self.page.click(self.login_button_home)
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button_popup)

    def is_logged_in(self):
        try:
            self.page.locator(self.account_header).wait_for(state="visible", timeout=3000)
            print('login success')
        except TimeoutError:
            print('login failed')
