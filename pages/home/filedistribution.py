class FileDistributorPage:
    def __init__(self, page):
        self.page = page

    def get_client_name(self):
        return self.page.locator('//article[@class="status-about column"]//div[1]//dl//dd[1]').text_content()

    def add_new(self):
        return self.page.locator(
            '//div[@class="main"]//article[@class="admin-distribution"]//div[@class="row button-bar"]//button[@class="btn inv-bg label icon"][1]')

    def export_all(self):
        return self.page.locator('//div[@class="row button-bar"]//button[2]')

    def import_fd(self):
        return self.page.locator('//div[@class="row button-bar"]//button[1]').nth(2)

    def name_distribution(self):
        return self.page.locator('//div[@class="row"]//input[@name="name"]')

    def get_manual(self):
        return self.page.locator('//form[@class="edit-distribution"]//div[1]//label[@data-name="manual"]')

    def get_automatic(self):
        return self.page.locator('//form[@class="edit-distribution"]//div[1]//label[3]').first

    def get_SD_videos(self):
        return self.page.locator('//div//label[@data-name="accepts_sd_videos"]')

    def get_HD_Videos(self):
        return self.page.locator('//div//label[@data-name="accepts_hd_videos"]')

    def get_scripts(self):
        return self.page.locator('//div//label[@data-name="accepts_scripts"]')

    def get_distribution_method(self):
        return self.page.locator('//div[@data-name="distribution_method"]')

    def ftp_distribution_method(self):
        return self.page.locator('//div[@data-name="distribution_method"]//div//ul//li[1]')

    def ftps_distribution_method(self):
        return self.page.locator('//div[@data-name="distribution_method"]//div//ul//li[2]')

    def sftp_distribution_method(self):
        return self.page.locator('//div[@data-name="distribution_method"]//div//ul//li[3]')

    def smb_distribution_method(self):
        return self.page.locator('//div[@data-name="distribution_method"]//div//ul//li[4]')

    def legacy_mode(self):
        return self.page.locator('//label[@data-name="legacy_mode"]')

    def login(self):
        return self.page.locator('//ul[@class="tab horizontal inheader hnav"]//li[3]//div//button')

    def get_hamburger(self):
        self.page.click('//header[@class="inv-bg no-print"]//ul//li[4]//div//button[@class="dropdown-toggle"]')

    def file_distributor_button(self):
        self.page.click('//div//ul[@class="inv-bg groups"]//li[2]//ul//li[4]')

    def ftp_host(self):
        return self.page.locator(
            '//div//details[2]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="uri"]')

    def ftp_target_directory(self):
        return self.page.locator(
            '//div//details[2]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="remote_base_directory"]')

    def ftp_username_method_distributions(self):
        return self.page.locator(
            '//div//details[2]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="username"]')

    def ftp_password_method_distributions(self):
        return self.page.locator(
            '//div//details[2]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="password"]')

    def save_distributions(self):
        return self.page.locator('//div[@class="row button-bar"]//button[@class="btn label"]')

    def ftp_location_details(self):
        return self.page.locator('//div//details[2]')

    def ftps_location_details(self):
        return self.page.locator('//div//details[3]')

    def sftp_location_details(self):
        return self.page.locator('//div//details[4]')

    def sftp_host(self):
        return self.page.locator('//div//details[4]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="uri"]')

    def sftp_target_directory(self):
        return self.page.locator('//div//details[4]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="remote_base_directory"]')

    def sftp_username_method_distributions(self):
        return self.page.locator('//div//details[4]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="username"]')

    def sftp_password_method_distributions(self):
        return self.page.locator('//div//details[4]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="password"]')

    def ftps_host(self):
        return self.page.locator('//div//details[3]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="uri"]')

    def ftps_target_directory(self):
        return self.page.locator('//div//details[3]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="remote_base_directory"]')

    def ftps_username_method_distributions(self):
        return self.page.locator('//div//details[3]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="username"]')

    def ftps_password_method_distributions(self):
        return self.page.locator('//div//details[3]//div[@class="connections row"]//div//label//div[@class="row"]//input[@name="password"]')

    def smb_target_directory_path(self):
        return self.page.locator('//div//details[@class="details"]//label//div//input[@name="target_directory"]')

    def smb_username(self):
        return self.page.locator('//div//details[5]//div//label[@data-name="username"]')

    def smb_password(self):
        return self.page.locator('//div//details[5]//div//label[@data-name="password"]')

    def smb_network_locations(self):
        return self.page.locator('//div//details[5]')

    def stories_tab(self):
        return self.page.locator('//div[@class="column nav no-print"]//ul//li[1]')

    def histories_tab(self):
        return self.page.locator('//div[@class="column nav no-print"]//ul//li[5]')

    def distribution_history(self):
        return self.page.locator('//div[@class="main"]//ul//li[2]')

    def fd_icon(self):
        return self.page.locator('//div[@class = "actions"]//div[2]//button')


