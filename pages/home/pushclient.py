class PushClientPage:
    def __init__(self, page):
        self.page = page

    def get_push_client_username(self):
        return self.page.locator('//div[@class="row"]//input[@name="PushClient.UserName"]')

    def get_push_client_password(self):
        return self.page.locator('//div[@class="row"]//input[@name="PushClient.Password"]')

    def get_proxy_name(self):
        return self.page.locator('//div[@class="row"]//input[@name="PushClient.Proxy"]')

    def get_proxy_username(self):
        return self.page.locator('//div[@class="row"]//input[@name="PushClient.ProxyUser"]')

    def get_proxy_password(self):
        return self.page.locator('//div[@class="row"]//input[@name="changeProxyPassword"]')

    def reset_button(self):
        return self.page.locator('//div[@class="row button-bar"]//button[1]')

    def update_settings(self):
        return self.page.locator('//div[@class="row button-bar"]//button[2]')