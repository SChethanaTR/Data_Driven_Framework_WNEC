class AboutPage:
    def __init__(self, page):
        self.page = page

    def get_client_name(self):
        return self.page.locator('//article[@class="status-about column"]//div[1]//dl//dd[1]').text_content()

    def get_Client_PC_Serial_Number(self):
        return self.page.locator('//article[@class="status-about column"]//div[1]//dl//dd[2]').text_content()

    def get_Client_PC_Type(self):
        return self.page.locator('//article[@class="status-about column"]//div[1]//dl//dd[3]').text_content()

    def get_Receiver_MAC_Address(self):
        return self.page.locator('//article[@class="status-about column"]//div[1]//dl//dd[4]').text_content()

    def get_Get_User_ID(self):
        return self.page.locator('//article[@class="status-about column"]//div[1]//dl//dd[5]').text_content()

    def get_host_name(self):
        return self.page.locator('//article[@class="status-about column"]//div[2]//dl//dd[1]').text_content()

    def get_host_id(self):
        return self.page.locator('//article[@class="status-about column"]//div[2]//dl//dd[2]').text_content()

    def get_time(self):
        return self.page.locator('//article[@class="status-about column"]//div[2]//dl//dd[3]').text_content()

    def get_software_version(self):
        return self.page.locator('//article[@class="status-about column"]//div[3]//dl//dd[1]').text_content()

    def get_installed_patches(self):
        return self.page.locator('//article[@class="status-about column"]//div[3]//dl//dd[2]').text_content()


    # Add more methods for interactions as needed