from playwright.sync_api._generated import Locator
from pages.base import Base


class FileLogsPage(Base):
    @property
    def file_log_page(self) -> Locator:
        return self.page.locator(".status-logs.column")

    @property
    def all_application_tab(self) -> Locator:
        return self.file_log_page.locator("//a[text()='All Applications']")

    @property
    def file_distributor_tab(self) -> Locator:
        return self.file_log_page.locator("//a[text()='File Distributor']")

    @property
    def file_processor_tab(self) -> Locator:
        return self.file_log_page.locator("//a[text()='File Processor']")

    @property
    def file_purger_tab(self) -> Locator:
        return self.file_log_page.locator("//a[text()='File Purger']")

    @property
    def log_search_bar(self):
        return self.file_log_page.locator("[name='search']")

    @property
    def log_search_button(self):
        return self.file_log_page.locator("//button[text()='Search']").first

    @property
    def log_clear_search_button(self):
        return self.file_log_page.locator("//button[text()='Clear Search']")

    @property
    def history_search(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//input').last

    @property
    def history_search_button(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//button').last

    @property
    def download_All_button(self):
        return self.file_log_page.locator('//div[@class = "action-row"]//a')

    def navigate(self) -> None:
        self.page.goto(f"{self.base_url}/status/logs")
        self.page.wait_for_load_state()

    @property
    def file_processor_history_search(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//input').last

    @property
    def file_purger_history_search(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//input').last

    @property
    def file_processor_history_search_button(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//button').last

    @property
    def file_purger_history_search_button(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//button').last

    @property
    def file_dist_history_search(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//input').last

    @property
    def file_dist_history_search_button(self):
        return self.file_log_page.locator('//form[@class = "search-bar no-print"]//button').last

    def navigate_file_logs(self) -> None:
        self.page.goto(f"{self.base_url}/status/logs")
        self.page.wait_for_load_state()

    def navigate_file_distributor(self) -> None:
        self.page.goto(f"{self.base_url}/status/logs?type=distributor")
        self.page.wait_for_load_state()

    def navigate_file_processor(self) -> None:
        self.page.goto(f"{self.base_url}/status/logs?type=processor")
        self.page.wait_for_load_state()

    def navigate_file_purger(self) -> None:
        self.page.goto(f"{self.base_url}/status/logs?type=purger")
        self.page.wait_for_load_state()
