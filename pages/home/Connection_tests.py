class ConnectionTestPage:
    def __init__(self, page):
        self.page = page

    def get_test_CDN_Connection(self):
        return self.page.locator('//div[@class="row"]//button[1]')

    def get_test_DNS_Connection(self):
        return self.page.locator('//div[@class="row"]//button[2]')
