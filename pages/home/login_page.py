# pages/login_page.py

class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self, LoginUsername, Password):
        self.page.click('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//button[@class="dropdown-toggle"]')
        self.page.click('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//div//ul//li//a')
        self.page.fill('//div[@class="main"]//form//label//div//input[@name="username"]', LoginUsername)
        self.page.fill('//div[@class="main"]//form//label//div//input[@name="password"]', Password)
        self.page.click('//div[@class="submit-area"]//button')

