import logging
import string
import subprocess

from playwright.sync_api import expect
from playwright.sync_api._generated import Locator

from pages.base import Base


class UserManagementPage(Base):

    def timeout(self):
        self.page.wait_for_timeout(5000)

    def navigate_user_page(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/admin/users")
        self.page.wait_for_load_state()

    def get_filter_search(self):
        return self.page.locator('//div[@class="filter"]')

    def get_add_user(self):
        return self.page.locator("//button[@class='btn inv-bg label icon']")

    def get_edit_user(self):
        return self.page.locator('//button[@class="btn-action tooltip"]')

    def get_username(self):
        return self.page.locator('//tbody//tr[@class="selectable-row"]//td[1]').text_content()

    def get_priviliges(self):
        return self.page.locator('//tbody//tr[@class="selectable-row"]//td[2]').text_content()

    def get_hamburger(self):
        self.page.click('//header[@class="inv-bg no-print"]//ul//li[4]//div//button[@class="dropdown-toggle"]')

    def get_user_management(self):
        self.page.click('//header[@class="inv-bg no-print"]//ul//li[4]//div//ul//li[2]//ul//li[3]')

    def fill_username(self, username):
        self.page.fill('//div[@class="row"]//input[@name="newUsername"]', username)
        return username

    def fill_password(self, password):
        self.page.fill('//div[@class="row"]//input[@name="newPassword"]', password)
        return password

    def admin_privilge(self):
        return self.page.locator('//div[@class="privileges-field"]//div[@class="admin"]')

    def check_privilege_1(self):
        self.page.check('//div[@class="privileges-field"]//ul[1]//li[1]//label')

    def check_privilege_2(self):
        self.page.check('//div[@class="privileges-field"]//ul[1]//li[2]//label')

    def click_save(self):
        self.page.click('//div[@class="row buttons"]//button[2]')

    # def test_add_user(self, username, password):
    #     self.timeout()
    #     self.get_add_user().click()
    #     self.fill_username(username)
    #     self.fill_password(password)
    #     self.admin_privilge().click()
    #     self.timeout()
    #     self.click_save()
    #     self.timeout()
    #     #logout
    #     self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//button').click()
    #     self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//div//ul//li//a[1]').click()
    #     self.page.locator('//form[@class="panel logout"]//button').click()
    #
    #     #login
    #     self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//button').click()
    #     self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//ul//li//a').click()
    #     self.page.locator('//input[@name="username"]').fill(username)
    #     self.page.locator('//input[@name="password"]').fill(password)
    #     self.page.locator('//div[@class="submit-area"]//button').click()

    def test_add_user(self, username, password):
        self.timeout()
        self.get_add_user().click()
        self.fill_username(username)
        self.fill_password(password)
        self.admin_privilge().click()
        self.timeout()
        self.click_save()
        self.timeout()

    def verify_logout_login(self, username, password):
        # self.timeout()
        # self.get_add_user().click()#adding a user
        # self.fill_username(username)
        # self.fill_password(password)
        # self.admin_privilge().click()
        # self.timeout()
        # self.click_save()
        # self.timeout()

        # Logout
        self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//button').click()#administrator button
        self.timeout()
        self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//div//ul//li//a[1]').click()#logoutfrombox1
        self.timeout()
        self.page.locator('//form[@class="panel logout"]//button').click()#logging out
        self.timeout()
        # Verify or correct the URL after logout
        #self.page.wait_for_url("http://10.99.13.11/missing")  # Wait for the unexpected URL
        # self.page.goto("http://10.99.13.11/stories#list")  # Navigate to a known login page
        # self.timeout()
        # Login
        # self.timeout()
        self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//button//div').click()#click on login button
        self.timeout()
        login_link = self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//ul//li//a[@data-nav-name="Log in to BOX 1"]')
        self.timeout()
        login_link.click()
        self.timeout()
        # Wait for the login inputs to be visible and then fill them
        self.page.locator('//input[@name="username"]').fill(username)
        self.timeout()
        self.page.locator('//input[@name="password"]').fill(password)
        self.timeout()

        # Click the login button
        self.page.locator('//div[@class="submit-area"]//button').click()

        # Verify successful login by checking for a URL change or a specific element that only appears on a successful login
        # self.page.wait_for_url(
        #     "http://10.99.13.11/stories#list")  # Adjust the URL to match the expected landing page after login

        # Optionally, you can add assertions here to ensure that the login was successful
        #assert "Dashboard" in self.page.locator('//title').textContent(), "Login failed. Dashboard not found."







