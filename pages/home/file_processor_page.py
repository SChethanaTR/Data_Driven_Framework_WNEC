class FileProcessorPage:
    def __init__(self, page):
        self.page = page

    def get_fp_name(self):
        return self.page.locator('//div[@class="row"]//input[@name="Customer.Name"]')

    def get_ip_add_satellite(self):
        return self.page.locator('//label[@data-name="RX8200.IPAddress"]//div//input')

    def get_frame_rate_dropdown(self):
        return self.page.locator('//div[@class="row"]//div[@data-name="Video.Format"]')

    def get_frame_rate_29(self):
        return self.page.locator('//div[@class="row"]//div[@data-name="Video.Format"]//div//ul//li[1]')

    def get_frame_rate_25(self):
        return self.page.locator('//div[@class="row"]//div[@data-name="Video.Format"]//div//ul//li[2]')

    def get_video_definition_dropdown(self):
        return self.page.locator('//div[@class="row"]//div[@data-name="Video.Definition"]')

    def get_video_definition_Sd(self):
        return self.page.locator('//div[@class="row"]//div[@data-name="Video.Definition"]//div//ul//li[1]')

    def get_video_definition_HD(self):
        return self.page.locator('//div[@class="row"]//div[@data-name="Video.Definition"]//div//ul//li[2]')

    def get_video_definition_SDHD(self):
        return self.page.locator('//div[@class="row"]//div[@data-name="Video.Definition"]//div//ul//li[3]')

    def get_upload_license(self):
        return self.page.locator('//div[@class="upload"]')

    def reset_button(self):
        return self.page.locator('//div[@class="row button-bar"]//button[1]')

    def update_settings_button(self):
        return self.page.locator('//div[@class="row button-bar"]//button[2]')

    def internet_backup_enabled_button(self):
        return self.page.locator('//div[@class="block"]//label[2][@data-name="CDNR.Enabled"]')

    def internet_backup_username(self):
        return self.page.locator('//div[@class="block"]//label[3][@data-name="CDNR.UserName"]')

    def get_change_password(self):
        return self.page.locator('//div[@class="block"]//label[4][@data-name="changePassword"]')

    def proxy_address(self):
        return self.page.locator('//div[@class="block"]//label[1][@data-name="CDNR.Proxy"]')

    def proxy_username(self):
        return self.page.locator('//div[@class="block"]//label[2][@data-name="CDNR.ProxyUsername"]')

    def proxy_changePassword(self):
        return self.page.locator('//div[@class="block"]//label[3][@data-name="changeProxyPassword"]')

    def internet_backup_reset_button(self):
        return self.page.locator('//div[@class="row button-bar"]//button[1]')

    def internet_backup_update_settings(self):
        return self.page.locator('//div[@class="row button-bar"]//button[2]')




