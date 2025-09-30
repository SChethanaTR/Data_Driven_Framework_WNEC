import logging
import string
import subprocess

from playwright.sync_api import expect
from playwright.sync_api._generated import Locator

from pages.base import Base


class AdminPlayoutPage(Base):

    def get_disable_channel_box_1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//label[@data-tooltip="Disable channel"]')

    def get_enable_channel_box_1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//label[@data-tooltip="Enable channel"]')

    def get_disable_channel_box_2(self):
        return self.page.locator('//div[@class="list column"]//div[2]//label[@data-tooltip="Disable channel"]')

    def get_disable_channel_box_3(self):
        return self.page.locator('//div[@class="list column"]//div[3]//label[@data-tooltip="Disable channel"]')

    def get_disable_channel_box_4(self):
        return self.page.locator('//div[@class="list column"]//div[4]//label[@data-tooltip="Disable channel"]')

    def get_SDI_Box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//span[@class="editable input displaying"]')

    def get_SDI_Box2(self):
        return self.page.locator('//div[@class="list column"]//div[2]//span[@class="editable input displaying"]')

    def get_SDI_Box3(self):
        return self.page.locator('//div[@class="list column"]//div[3]//span[@class="editable input displaying"]')

    def get_SDI_Box4(self):
        return self.page.locator('//div[@class="list column"]//div[4]//span[@class="editable input displaying"]')

    def get_Fixed_Channel(self):
        return self.page.locator('//div[@class="row"]//label[@class="toggle labelled"]')

    def get_Content_Source_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]')

    def get_mode_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="mode"]')

    def get_mode_box2(self):
        return self.page.locator('//div[@class="list column"]//div[2]//div[@data-name="mode"]')

    def get_mode_box3(self):
        return self.page.locator('//div[@class="list column"]//div[3]//div[@data-name="mode"]')

    def get_mode_box4(self):
        return self.page.locator('//div[@class="list column"]//div[4]//div[@data-name="mode"]')

    def get_CS_Live_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]//div//ul//li[2]')

    def get_CS_6x_Live_Preview_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]//div//ul//li[3]')

    def get_CS_RLS_Broadcast_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]//div//ul//li[4]')

    def get_CS_File_playout_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]//div//ul//li[5]')

    def get_CS_Sent_from_connect_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]//div//ul//li[6]')

    def get_Mode_Loop_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="mode"]//div//ul//li[2]')

    def get_Mode_Auto_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="mode"]//div//ul//li[3]')

    def get_Mode_Manual_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="mode"]//div//ul//li[4]')

    def lock_configuration_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//label[@class="lock"]')

    def lock_configuration_box2(self):
        return self.page.locator('//div[@class="list column"]//div[2]//label[@class="lock"]')

    def lock_configuration_box3(self):
        return self.page.locator('//div[@class="list column"]//div[3]//label[@class="lock"]')

    def lock_configuration_box4(self):
        return self.page.locator('//div[@class="list column"]//div[4]//label[@class="lock"]')

    def content_source_box1(self):
        return self.page.locator('//div[@class="list column"]//div[1]//div[@data-name="source"]')

    def content_source_box2(self):
        return self.page.locator('//div[@class="list column"]//div[2]//div[@data-name="source"]')

    def content_source_box3(self):
        return self.page.locator('//div[@class="list column"]//div[3]//div[@data-name="source"]')

    def content_source_box4(self):
        return self.page.locator('//div[@class="list column"]//div[4]//div[@data-name="source"]')

    def confirm_content_source_change(self):
        return self.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]')


    def stories_page(self):
        return self.page.locator('//div[@class="column nav no-print"]//ul//li[1]')

    def story_page_playout_button(self):
        return self.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][3]')

    def playout_option_1(self):
        return self.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][3]//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[1]')

    def playout_option_2(self):
        return self.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][3]//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[2]')

    def playout_option_3(self):
        return self.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][3]//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[3]')

    def playout_option_4(self):
        return self.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][3]//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[4]')

    def play_out_page(self):
        return self.page.locator('//div[@class="column nav no-print"]//ul//li[4]')

    def live_page_playout_icon(self):
        return self.page.locator('//td[@class="actions-cell"]//div[@class="actions"]//div[@class="flashing-indicators-holder"]') #multiple playout icons

    def live_page_slug_name(self):
        return self.page.locator('//tr[@class="event-row selectable-row"]//td[2]') #has multiple slug names

    def live_page_playout_op_1(self):
        return self.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[1]')

    def RLS_upcoming_list_of_videos(self):
        return self.page.locator('//div[@data-name="playlist-1"]//div[@class="row list-row"]//div[@class="column"]//a')

    def RLS_Now_playing_Videos(self):
        return self.page.locator('//div//h4[@class="label"]//div[@class="playing-now"]')

    def play_out_page_link(self):
        return self.page.locator('//div[@class="column nav no-print"]//ul//li[4]')

    def Select_Source_as_Fileplayout(self):
        # Select 'fileplayout' from the Content Source dropdown
        self.get_Content_Source_box1().click()
        self.timeout()
        self.get_CS_File_playout_box1().click()
        self.confirm_content_source_change().click()
        self.timeout()

    def Select_Mode_as_Auto(self):
        # Select 'auto' from the Mode dropdown
        self.get_mode_box1().click()
        self.timeout()
        self.get_Mode_Auto_box1().click()
        self.confirm_content_source_change().click()
        self.timeout()
        self.page.wait_for_timeout(5000)




    def timeout(self):
        self.page.wait_for_timeout(5000)

    def navigate(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/admin/playout")
        self.page.wait_for_load_state()


