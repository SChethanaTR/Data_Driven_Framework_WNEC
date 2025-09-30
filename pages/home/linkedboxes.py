class LinkedBoxesPage:
    def __init__(self, page):
        self.page = page

    def get_allow_access_from_other_boxes(self):
        return self.page.locator('//div[@class="block"]//label[@data-name="allowAccess"]')

    def control_other_box(self):
        return self.page.locator('//div[@class="block"]//label[@data-name="hasLinked"]')

    def reset_button(self):
        return self.page.locator('//div[@class="row button-bar"]//button[1]')

    def update_settings(self):
        return self.page.locator('//div[@class="row button-bar"]//button[2]')
