from playwright.sync_api._generated import Locator
from pages.base import Base


class AuthPage(Base):
    @property
    def keep_login_checkbox(self):
        return self.page.locator("label[data-name='remember']")

    @property
    def login_submit(self) -> Locator:
        return self.login_panel.locator("button[type='submit']")

    @property
    def login_panel(self) -> Locator:
        return self.page.locator(".panel.login")

    @property
    def logout_submit(self) -> Locator:
        return self.logout_panel.locator("button[type='submit']")

    @property
    def logout_panel(self) -> Locator:
        return self.page.locator(".panel.logout")

    @property
    def password_field(self) -> Locator:
        return self.login_panel.locator("input[name='password']")

    @property
    def password_new_field(self) -> Locator:
        return self.password_panel.locator("input[type='password'][name='new']")

    @property
    def password_old_field(self) -> Locator:
        return self.password_panel.locator("input[type='password'][name='old']")

    @property
    def password_panel(self) -> Locator:
        return self.page.locator(".panel.password")

    @property
    def show_password_button(self):
        return self.password_panel.locator(".toggle-view.tooltip")

    @property
    def save_button(self) -> Locator:
        return self.password_panel.locator("button[type='submit']")

    @property
    def username_field(self) -> Locator:
        return self.login_panel.locator("input[name='username']")

    def fill_form_and_submit(self, username, password) -> None:
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.keep_login_checkbox.click()
        self.login_submit.click()
        self.page.wait_for_load_state()

    def navigate(self) -> None:
        """Navigate to the login page."""
        self.page.goto(f"{self.base_url}/auth/login")
        self.page.wait_for_load_state()
