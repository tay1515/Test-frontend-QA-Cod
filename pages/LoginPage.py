from pages.ProductListPage import ProductListPage

class LoginPage:

    def __init__(self, page):
        self.page = page
        self._username = page.get_by_placeholder("Username")
        self._password = page.get_by_placeholder("Password")
        self._login_btn = page.get_by_text("Login")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    def enter_username(self, u_name):
        self._username.clear()
        self._username.fill(u_name)

    def enter_password(self, p_word):
        self._password.clear()
        self._password.fill(p_word)

    def click_login(self):
        self._login_btn.click()

    def do_login(self, credentials):
        self.enter_username(credentials['username'])
        self.enter_password(credentials['password'])
        self.click_login()
        return ProductListPage(self.page)
