import logging
import string
import subprocess

from playwright.sync_api import expect
from playwright.sync_api._generated import Locator

from pages.base import Base


class HistoryPage(Base):

    def timeout(self):
        self.page.wait_for_timeout(5000)

    def navigate_playout_history(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/history/playout")
        self.page.wait_for_load_state()

    def navigate_distribution_history(self) -> None:
        self.page.goto(f"{self.base_url}/history/distribution")
        self.page.wait_for_load_state()


