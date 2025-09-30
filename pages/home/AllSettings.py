class AllSettingsPage:
    def __init__(self, page):
        self.page = page

    def get_export_button(self):
        return self.page.locator('//div[@class="row button-bar"]//a//button')

    def get_import_button(self):
        return self.page.locator('//div[@class="row button-bar"]//div//button')