class ServicesPage:
    def __init__(self, page):
        self.page = page

    def get_restart_all(self):
        return self.page.locator('//div[@class="row"]//div[2]//button[@class="btn inv-bg label icon"]')

    def get_Suspend_all(self):
        return self.page.locator('//div[@class="row"]//div[3]//button[@class="btn inv-bg label icon"]')

    def get_Reset_Hardware(self):
        return self.page.locator('//div[@class="row"]//div[4]//button[@class="btn inv-bg label icon"]')

    def get_file_purger_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][1]//div[@class="flashing-indicators-holder"][2]')

    def get_file_purger_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][1]//div[@class="flashing-indicators-holder"][1]')

    def get_kenkast_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][2]//div[@class="flashing-indicators-holder"][1]')

    def get_kenkast_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][2]//div[@class="flashing-indicators-holder"][2]')

    def get_wne_player_1_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][3]//div[@class="flashing-indicators-holder"][1]')

    def get_wne_player_1_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][3]//div[@class="flashing-indicators-holder"][2]')

    def get_wne_player_2_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][4]//div[@class="flashing-indicators-holder"][1]')

    def get_wne_player_2_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][4]//div[@class="flashing-indicators-holder"][2]')

    def get_wne_player_3_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][5]//div[@class="flashing-indicators-holder"][1]')

    def get_wne_player_3_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][5]//div[@class="flashing-indicators-holder"][2]')

    def get_wne_player_4_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][6]//div[@class="flashing-indicators-holder"][1]')

    def get_wne_player_4_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][6]//div[@class="flashing-indicators-holder"][2]')

    def get_health_reporter_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][7]//div[@class="flashing-indicators-holder"][1]')

    def get_health_reporter_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][7]//div[@class="flashing-indicators-holder"][2]')

    def get_file_distributor_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][8]//div[@class="flashing-indicators-holder"][1]')

    def get_file_distributor_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][8]//div[@class="flashing-indicators-holder"][2]')

    def get_wne_upgrader_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][9]//div[@class="flashing-indicators-holder"][1]')

    def get_wne_upgrader_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][9]//div[@class="flashing-indicators-holder"][2]')

    def get_wne_file_processor_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][10]//div[@class="flashing-indicators-holder"][1]')

    def get_wne_file_processor_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][10]//div[@class="flashing-indicators-holder"][2]')

    def get_pushclient_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][11]//div[@class="flashing-indicators-holder"][1]')

    def get_pushclient_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][11]//div[@class="flashing-indicators-holder"][12]')

    def get_ui_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][12]//div[@class="flashing-indicators-holder"][1]')

    def get_ui_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][12]//div[@class="flashing-indicators-holder"][2]')

    def get_database_manager_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][13]//div[@class="flashing-indicators-holder"][1]')

    def get_database_manager_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][13]//div[@class="flashing-indicators-holder"][2]')

    def get_teamviewer_manager_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][14]//div[@class="flashing-indicators-holder"][1]')

    def get_teamviewer_manager_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][14]//div[@class="flashing-indicators-holder"][2]')

    def get_database_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][15]//div[@class="flashing-indicators-holder"][1]')

    def get_database_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][15]//div[@class="flashing-indicators-holder"][2]')

    def get_internet_backup_restart(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][16]//div[@class="flashing-indicators-holder"][1]')

    def get_internet_backup_suspend(self):
        return self.page.locator('//div[@class="with-actions expandable-grid list"]//div[@class="td action-wrapper"][16]//div[@class="flashing-indicators-holder"][2]')
