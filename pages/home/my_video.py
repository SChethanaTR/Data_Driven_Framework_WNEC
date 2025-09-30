import logging
import string
import subprocess

from playwright.sync_api import expect
from playwright.sync_api._generated import Locator

from pages.base import Base


class MyVideoPage(Base):

    def timeout(self):
        self.page.wait_for_timeout(5000)

    def navigate_user_page(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/admin/users")
        self.page.wait_for_load_state()
