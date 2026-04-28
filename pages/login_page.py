from pages.base_page import BasePage


class LoginPage(BasePage):

    username = "#username"
    password = "#password"
    login_button = "button[type='submit']"

    def login(self, user, pwd):
        self.fill(self.username, user)
        self.fill(self.password, pwd)
        self.click(self.login_button)