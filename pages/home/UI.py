import logging
import string
import subprocess

from playwright.sync_api import expect
from playwright.sync_api._generated import Locator

from pages.base import Base


class UserInterfacePage(Base):

    def timeout(self):
        self.page.wait_for_timeout(5000)

    def navigate(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/stories#list")
        self.page.wait_for_load_state()

    def favorite_icon(self):
        return self.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][1]')

    def my_videos(self):
        return self.page.locator('//ul[@class="tab vertical"]//li[6]')

    def add_to_playlist(self):
        return self.page.locator('//div[@class="td actions no-print"]//div[@class="flashing-indicators-holder"][2]')

    def playout_opt_1(self):
        return self.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[1]')

    def playout_opt_2(self):
        return self.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[2]')

    def playout_opt_3(self):
        return self.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[3]')

    def playout_opt_4(self):
        return self.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[4]')

    def slug_name(self):
        return self.page.locator('//div[@class="td source-id-slug justified"]//div[@class="column"]//div[@class="row"]//button[1]')

    def po_page(self):
        return self.page.locator('//ul[@class="tab vertical"]//li[4]')

    def upcoming_videos(self):
        return self.page.locator('//div[@class="scrollable"]//div[@data-name="playlist-1"]//div//div//a//div//span[1]')

    def clearing_videos(self):
        return self.page.locator('//div[@class="scrollable"]//div[@data-name="playlist-1"]//div//button[@class="btn-action tooltip no-print"]')

    def get_Content_Source_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]')

    def get_CS_Live_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]//div//ul//li[2]')

    def confirm_content_source_change(self):
        return self.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]')

    def get_mode_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="mode"]')

    def add_playlist_button(self):
        return self.page.locator('//tr[@class="event-row selectable-row"]//td[7]//div[@class="actions"]//div//div//button[@class="btn-action tooltip"]')

    def opt1_add_to_playlist(self):
        return self.page.locator('//tr[@class="event-row selectable-row"]//td[7]//div[@class="actions"]//div//div//div//ul//li[1]')

    def print_sdi_channel_page(self):
        return self.page.locator('//div[@class="main"]//h3//button')

    def livepage_first_row(self):
        return self.page.locator('//tr[@class="event-row selectable-row selected"]//td[2]//button')








