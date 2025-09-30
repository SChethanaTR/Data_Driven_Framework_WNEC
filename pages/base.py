from playwright.sync_api import BrowserContext, Locator, Page
import env


class Base:
    def __init__(self, context: BrowserContext, page: Page = None):
        self.context = context
        self.base_url = f"http://{env.ip}"
        self.page = page if page else self.context.new_page()
        self.page.set_default_timeout(env.ui_timeout)
        env.cur_page = self.page

    @property
    def change_password_button(self) -> Locator:
        return self.page.locator("//a[text()='Change password']")

    @property
    def confirmation_dialog(self):
        return self.page.locator("dialog.inv-bg")

    @property
    def cancel_popup_button(self):
        return self.page.locator(".btn-sec.label")

    @property
    def accept_popup_button(self):
        return self.page.locator(".btn.inv-bg.label")

    @property
    def login_dropdown(self) -> Locator:
        return self.page.locator("div[class='dropdown-menu']").first

    @property
    def login_button(self) -> Locator:
        return self.page.locator("//a[starts-with(text(),'Log in to')]")

    @property
    def logout_button(self) -> Locator:
        return self.page.locator("//a[starts-with(text(),'Log out')]")

    @property
    def search_bar(self):
        return self.page.locator("input[placeholder='Search Stories']")

    @property
    def search_button(self):
        return self.page.locator("//button[text()='Search']").first

    @property
    def clear_search_button(self):
        return self.page.locator("//button[text()='Clear Search']")

    @property
    def save_search_button(self):
        return self.page.locator("//button[text()='Save Search']")

    @property
    def advance_search_button(self):
        return self.page.locator("//a[text()='Advanced Search']")

    @property
    def navigation_menu(self) -> Locator:
        return self.page.locator("[data-name='nav-menu']")

    @property
    def logo(self):
        return self.page.locator("img[alt='Reuters logo']")

    @property
    def help_header(self):
        return self.page.locator("a[href='https://liaison.reuters.com/page/wne-technical-notes']")

    @property
    def playout_side_panel(self):
        return self.page.locator("aside")

    @property
    def menu_status(self):
        return self.navigation_menu.locator("//a[text()='STATUS']")

    @property
    def menu_about(self):
        return self.navigation_menu.locator("//a[text()='About']")

    @property
    def menu_services(self):
        return self.navigation_menu.locator("//a[text()='Services']")

    @property
    def menu_software_upgrade(self):
        return self.navigation_menu.locator("//a[text()='Software Upgrades']")

    @property
    def menu_file_logs(self):
        return self.navigation_menu.locator("//a[text()='File Logs']")

    @property
    def menu_device_status(self):
        return self.navigation_menu.locator("//a[text()='Device Status']")

    @property
    def menu_host_info(self):
        return self.navigation_menu.locator("//a[text()='Host Info']")

    @property
    def menu_admin(self):
        return self.navigation_menu.locator("//a[text()='ADMIN']")

    @property
    def menu_playout(self):
        return self.navigation_menu.locator("//a[text()='Playout']")

    @property
    def menu_user_management(self):
        return self.navigation_menu.locator("//a[text()='User Management']")

    @property
    def menu_file_distribution(self):
        return self.navigation_menu.locator("//a[text()='File Distribution']")

    @property
    def menu_kencast(self):
        return self.navigation_menu.locator("//a[text()='Kencast Administration']")

    @property
    def menu_settings(self):
        return self.navigation_menu.locator("//a[text()='SETTINGS']")

    @property
    def menu_file_processor(self):
        return self.navigation_menu.locator("//a[text()='File Processor']")

    @property
    def menu_playout_setting(self):
        return self.navigation_menu.locator("//a[text()='Playout']")

    @property
    def menu_internet_backup(self):
        return self.navigation_menu.locator("//a[text()='Internet Backup']")

    @property
    def menu_test_connection(self):
        return self.navigation_menu.locator("//a[text()='Connection Tests']")

    @property
    def menu_push_client(self):
        return self.navigation_menu.locator("//a[text()='Push Client']")

    @property
    def menu_linked_box(self):
        return self.navigation_menu.locator("//a[text()='Linked Boxes']")

    @property
    def menu_advance(self):
        return self.navigation_menu.locator("//a[text()='Advanced']")

    @property
    def menu_all_setting(self):
        return self.navigation_menu.locator("//a[text()='All Settings']")


    @property
    def confirmation_dialog_advanced_search(self):
        return self.page.locator('//main[@class = "search"]')