class SoftwareUpgradesPage:
    def __init__(self, page):
        self.page = page

    def get_upload_software(self):
        return self.page.locator('//div[@class="upload"]')

    def get_rollback_to_previous_version(self):
        return self.page.locator('//div[@class="actions"]//button[1]')

    def get_schedule_rollback_to_previous_version(self):
        return self.page.locator('//div[@class="actions"]//button[2]')

    def get_current_SW_version(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[1]//td[1]').text_content()

    def get_current_SW_Status(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[1]//td[2]').text_content()

    def get_current_release_note(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[1]//td[3]').text_content()

    def get_current_cut_off_date(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[1]//td[4]').text_content()

    def get_current_schedule_start(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[1]//td[5]').text_content()

    def get_current_actions(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[1]//td[6]').text_content()

    def get_rollback_SW_version(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[2]//td[1]').text_content()

    def get_rollback_SW_Status(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[2]//td[2]').text_content()

    def get_rollback_release_note(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[2]//td[3]').text_content()

    def get_rollback_cut_off_date(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[2]//td[4]').text_content()

    def get_rollback_schedule_start(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[2]//td[5]').text_content()

    def get_rollback_actions(self):
        return self.page.locator('//div[@class="upgrades"]//table//tbody//tr[2]//td[6]').text_content()



