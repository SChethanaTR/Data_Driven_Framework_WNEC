import logging
import string
import subprocess

from playwright.sync_api import expect
from playwright.sync_api._generated import Locator
from tabulate import tabulate

from pages.base import Base


class StoryPage(Base):
    @property
    def add_to_distribution_button(self) -> Locator:
        return self.stories_view.locator("button[data-name='folder-button']").first

    @property
    def expanded_story_distribution_button(self) -> Locator:
        return self.stories_view.locator(".td.no-print.expanded  button[data-name='folder-button']")

    @property
    def expanded_story_my_video_button(self) -> Locator:
        return self.stories_view.locator(
            ".td.no-print.expanded  button[data-name='favourite-button']"
        )

    @property
    def stories_view(self) -> Locator:
        return self.page.locator("main[class='stories']")

    @property
    def story_detail_grid(self) -> Locator:
        return self.stories_view.locator(".story-details.grid-container")

    @property
    def prev_page_button(self):
        return self.page.locator("//button[text()='Prev']")

    @property
    def next_page_button(self):
        return self.page.locator("//button[text()='Next']")

    @property
    def current_page_display(self):
        return self.page.locator(".editable.input")

    @property
    def current_page_input(self):
        return self.page.locator("input[name='page']")

    @property
    def per_page_dropdown(self):
        return self.page.locator(".page-switch.no-print .dropdown-toggle.label div")

    @property
    def page_input(self):
        return self.page.locator('//div[@class = "page-switch no-print"]//span')

    @property
    def arrived_video_icon(self):
        return self.stories_view.locator("[data-tooltip^='Video']").first

    @property
    def arrived_script_icon(self):
        return self.stories_view.locator("[data-tooltip^='Script']").first

    @property
    def add_to_myvideo_button(self):
        return self.stories_view.locator("[data-name='favourite-button']").first

    @property
    def add_to_playout_button(self) -> Locator:
        return self.stories_view.locator("[data-tooltip^='Playout']").first

    @property
    def add_to_playlist_button(self) -> Locator:
        return self.stories_view.locator("[data-tooltip$='Playlist']").first

    @property
    def story_id(self) -> Locator:
        return self.stories_view.locator(".btn-link.h4.bold").first

    @property
    def id_slug_component(self):
        return self.stories_view.locator(
            '//div[@class ="td source-id-slug justified"]//div[@class = "column"]//div//button[1]').first
        # return self.stories_view.locator(".td.source-id-slug.justified").first

    @property
    def list_view_button(self):
        return self.stories_view.locator(".switch [data-tooltip^='List'] a")

    @property
    def grid_view_button(self):
        return self.stories_view.locator("[aria-label='Grid view']")

    @property
    def sort_dropdown_button(self):
        return self.stories_view.locator("[data-name='sort']")

    @property
    def print_detail_button(self):
        return self.story_detail_grid.locator("[data-tooltip^='Print']")

    @property
    def add_my_video_detail_button(self):
        return self.story_detail_grid.locator("[data-tooltip$='Videos']")

    @property
    def copy_link_button(self):
        return self.story_detail_grid.locator("[data-tooltip$='Link']")

    @property
    def view_xml_button(self):
        return self.story_detail_grid.locator("[data-tooltip$='XML']")

    @property
    def story_duration(self):
        return self.stories_view.locator("div.duration")

    @property
    def hd_tag(self):
        return self.stories_view.locator(".hd")

    @property
    def advisory_checkbox(self):
        return self.stories_view.locator("input[name=advisories]+span")

    @property
    def early_access_script_checkbox(self):
        return self.stories_view.locator("input[name=earlyscripts]+span")

    @property
    def all_story_tab(self):
        return self.stories_view.locator("a[name='all']")

    def get_script_filename_from_story_detail(self) -> string:
        self.story_detail_grid.locator("div[name='xml-file']").wait_for()
        return self.story_detail_grid.locator("div[name='xml-file']").first.text_content().strip()

    def get_sd_video_filename_from_story_detail(self) -> string:
        self.story_detail_grid.locator("div[name='sd-file']").wait_for()
        return self.story_detail_grid.locator("div[name='sd-file']").first.text_content().strip()

    def get_hd_video_filename_from_story_detail(self) -> string:
        self.story_detail_grid.locator("div[name='hd-file']").wait_for()
        return self.story_detail_grid.locator("div[name='hd-file']").first.text_content().strip()

    def navigate(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/stories")
        self.page.wait_for_load_state()

    def navigate_playout(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/admin/playout")
        self.page.wait_for_load_state()

    def navigate_distribution_history(self) -> None:
        """Navigate to the story page."""
        self.page.goto(f"{self.base_url}/history/distribution")
        self.page.wait_for_load_state()

    def open_recent_story_detail_grid(self) -> string:
        return self.stories_view.locator(
            "//button[@class='btn-link h4 bold' and text()!='Advisory']"
        ).first.click()

    @property
    def input_page_number(self):
        return self.page.locator('//span[@class = "editable input displaying"]')

    @property
    def print_page(self):
        return self.page.get_by_role("button", name="Print Page")

    @property
    def my_video_option(self):
        return self.page.locator('//div[@class = "column nav no-print"]//ul//li[6]')

    @property
    def playlist_icon(self):
        return self.page.locator('//div[@class = "enclosure no-print"]//div')

    @property
    def print_icon(self):
        return self.page.locator('//div[@class = "enclosure no-print"]//button[1]').last

    @property
    def clear_icon(self):
        return self.page.locator('//div[@class = "enclosure no-print"]//button[2]')

    @property
    def add_page_to(self):
        return self.page.locator('//div[@data-name = "add-page"]')

    @property
    def add_page_to_distribution(self):
        return self.page.locator('//div//ul//li[1]').last

    @property
    def slug_My_video(self):
        return self.page.locator('//div//button[@class = "btn-link h4"]')

    @property
    def myvideo_clear_dialog_box(self):
        return self.page.locator('//dialog[@class = "inv-bg"]//div//div//button[2]')

    @property
    def myvideo_clear_option(self):
        return self.page.locator('//div[@class = "enclosure no-print"]//button[2]')

    @property
    def add_page_to_my_videos(self):
        return self.page.locator('//div//ul//li[2]').last

    @property
    def print_page_icon(self):
        return self.page.locator('//button[@class = "btn-sec label icon inpage btn-print no-print"]')

    @property
    def advanced_search_link(self):
        return self.page.locator('//a[@href = "/search" ]')

    @property
    def services(self):
        return self.page.locator('//input[@name = "all"]')

    @property
    def aspect_ratio(self):
        return self.page.locator('//input[@value = "widescreen"]')

    @property
    def reset_values(self):
        return self.page.locator('//button[@class = "btn-sec label"]')

    @property
    def search_services(self):
        return self.page.locator('//div[@class = "row-wrap"]//label[2]')

    @property
    def stories_added_by_time(self):
        return self.page.locator('//div[@data-name = "interval"]')

    @property
    def exclusions(self):
        return self.page.locator('//div[@class = "column"]//label[1]').last

    @property
    def My_videos(self):
        return self.page.locator('//a[@href="/videos"]')

    @property
    def Show_Advisories(self):
        return self.page.locator('//label[@data-name = "advisories"]')

    @property
    def Show_early_access_scripts(self):
        return self.page.locator('//label[@data-name = "earlyscripts"]')

    @property
    def copy_link(self):
        return self.page.locator('//div[@class = "enclosure no-print"]//button[2]')

    @property
    def Close_copy_link(self):
        return self.page.locator('//div[@class = "row buttons"]//button')

    @property
    def XML(self):
        return self.page.locator('//div[@class = "enclosure no-print"]//a')

    @property
    def Slug(self):
        return self.page.locator('//div[@class = "th row"]//button[1]')

    @property
    def ID(self):
        return self.page.locator('//div[@class = "th row"]//button[2]')

    @property
    def Headline(self):
        return self.page.locator('//div[@class = "expandable-grid list"]//div[4]')

    @property
    def Arrived(self):
        return self.page.locator('//div[@class = "expandable-grid list"]//div[5]')

    @property
    def print_icon(self):
        return self.page.locator('//button[@class = "btn-icon tooltip no-print"]').first

    @property
    def Stories(self):
        return self.page.locator('//ul[@class = "tab vertical"]//li[1]')

    @property
    def Live(self):
        return self.page.locator('//ul[@class = "tab vertical"]//li[2]')

    @property
    def Story_Advisories(self):
        return self.page.locator('//ul[@class = "tab vertical"]//li[3]')

    @property
    def Story_playout_comp(self):
        return self.page.locator('//ul[@class = "tab vertical"]//li[4]')

    @property
    def History(self):
        return self.page.locator('//ul[@class = "tab vertical"]//li[5]')

    @property
    def MyVideos(self):
        return self.page.locator('//ul[@class = "tab vertical"]//li[6]')

    @property
    def AllStories(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[1]')

    @property
    def Reuters(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[2]')

    @property
    def ANI(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[3]')

    @property
    def CCTV(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[4]')

    @property
    def HollywoodTV(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[5]')

    @property
    def StatsPerform(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[6]')

    @property
    def VNR(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[7]')

    @property
    def Sent_from_connect(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print no-print"]//li[8]')

    @property
    def search_stories(self):
        return self.page.locator('//input[@type= "search"]')

    @property
    def search_stories_button(self):
        return self.page.locator('//form[@class = "search-bar no-print"]//button')

    @property
    def search_distribution_history(self):
        return self.page.locator('//input[@type = "search"]').last

    @property
    def search_distribution_history_button(self):
        return self.page.locator('//form[@class = "search-bar no-print"]//button').last

    @property
    def sort_by(self):
        return self.page.locator('//div[@class = "main"]//div[@class = "story-actions no-print"]//div[2]')

    @property
    def direction(self):
        return self.page.locator('//div[@class = "main"]//div[@class = "story-actions no-print"]//div[3]')

    @property
    def sort_by_options(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li')

    @property
    def direction_options(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li')

    @property
    def fixed_channels(self):
        return self.page.locator('//label[@class = "toggle labelled"]')

    @property
    def playout_dialog_box(self):
        return self.page.locator('//dialog[@class = "inv-bg"]//div//div//button[2]')

    @property
    def content_source(self):
        return self.page.locator('//div[@class = "list column"]//div[1]//div[@class = "dropdown-menu dropdown"]').first

    @property
    def mode_options(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li')

    @property
    def content_source_options(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li')

    @property
    def playout_mode(self):
        return self.page.locator('//div[@class = "list column"]//div[1]//div[@class = "dropdown-menu dropdown"]').last

    @property
    def UI_input(self):
        return self.page.locator('//div[@class = "list column"]//div[1]//span[@class = "editable input displaying"]')

    @property
    def add_to_my_video_icon(self):
        return self.page.locator('//div[@class = "enclosure no-print"]//div').first

    @property
    def show_advisories(self):  # returns the first petal of the first video
        return self.page.locator('//div[@class = "story-actions no-print"]//label[1]')

    @property
    def favorite_icon(self):  # returns the first petal of the first video
        return self.page.locator(
            '//div[@class = "flashing-indicators-holder"]//button[@data-name = "favourite-button"]')

    @property
    def add_to_distributor(self):
        return self.page.locator('//div[@class = "actions"]//div[2]//button')

    @property
    def slug_of_story_added(self):
        return self.page.locator(
            '//div[@class = "td source-id-slug justified"]//div[@class = "column"]//div[@class = "row"]//button[@class = "btn-link h4"]')

    @property
    def name_of_the_slug_distributed(self):
        return self.page.locator('//tbody//tr//td[1]')

    @property
    def hamburger(self):
        return self.page.locator('//div[@class = "dropdown-menu admin"]')

    @property
    def file_distributor_icon(self):
        return self.page.locator('//ul[@class = "inv-bg groups"]//li[2]//ul//li[4]')

    @property
    def add_new_FD(self):
        return self.page.locator('//div[@class = "row button-bar"]//button[1]')

    @property
    def FD_name(self):
        return self.page.locator('//input[@name= "name"]')

    @property
    def SD(self):
        return self.page.locator('//form[@class="edit-distribution"]//div//label[@data-name="accepts_sd_videos"]')

    @property
    def HD(self):
        return self.page.locator('//form[@class="edit-distribution"]//div//label[@data-name="accepts_hd_videos"]')

    @property
    def script(self):
        return self.page.locator('//form[@class="edit-distribution"]//div//label[@data-name="accepts_scripts"]')

    @property
    def FTP_Details(self):
        return self.page.locator('//div//details[2]')

    @property
    def FTPS_Details(self):
        return self.page.locator("//details[./summary/div/h2[text()='FTPS LOCATION DETAILS']]")

    @property
    def SFTP_Details(self):
        return self.page.locator('//div//details[4]')

    @property
    def SMB_Details(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li[4]')

    @property
    def SMB_Target_Directory(self):
        return self.page.locator(
            '//div//label[@class = "input"]//div[@class = "row"]//input[@name = "target_directory"]')

    @property
    def SMB_Domain(self):
        return self.page.locator('//div//label[@class = "input"]//div[@class = "row"]//input[@name = "domain"]')

    @property
    def SMB_Username(self):
        return self.page.locator('//div//label[@class = "input"]//div[@class = "row"]//input[@name = "username"]').last

    @property
    def SMB_Password(self):
        return self.page.locator('//label[@data-name = "password"]//div//input[@type = "password"]')

    @property
    def host(self):
        return self.page.locator('//input[@name = "uri"]')

    @property
    def target_director(self):
        return self.page.locator('//input[@name = "remote_base_directory"]').first

    @property
    def FD_username(self):
        return self.page.locator('//input[@name = "username"]')

    @property
    def FD_password(self):
        return self.page.locator('//input[@name = "password"]')

    @property
    def save_FD(self):
        return self.page.locator('//div//button[@type = "submit"]')

    @property
    def playout_icon(self):
        return self.page.locator('//div[@class = "actions"]//div[3]')

    @property
    def first_channel_patel(self):  # returns the first petal of the first video
        return self.page.locator(".petal").first

    @property
    def playout_show_loop_item(self):
        return self.page.locator('//div[@class = "main"]//label')

    @property
    def protocol_method(self):
        # This locator targets the specific dropdown option containing the text "FTP"
        return self.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/form/div[1]/div/button/div')
        # Fetch and return the text content of the FTP option

    @property
    def FTP_option(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li[1]')

    @property
    def FTPS_option(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li[2]')

    @property
    def SFTP_option(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li[3]')

    def prev_next(self):
        self.current_page_input.fill('5')
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(3000)
        assert self.current_page_display.text_content() == "5"
        self.page.wait_for_timeout(3000)
        self.prev_page_button.click()
        self.page.wait_for_timeout(3000)
        assert self.current_page_display.text_content() == "4"
        self.page.wait_for_timeout(3000)
        self.next_page_button.click()
        self.page.wait_for_timeout(3000)
        assert self.current_page_display.text_content() == "5"
        self.current_page_display.click()
        self.current_page_input.clear()
        self.current_page_input.fill('250')
        expect(self.next_page_button).to_be_disabled()

    def add_to_distribution(self):
        text = self.id_slug_component.text_content()
        print(text)
        self.add_page_to.click()
        self.page.wait_for_timeout(3000)
        self.add_page_to_distribution.click()
        self.page.wait_for_timeout(3000)
        self.History.click()
        self.page.wait_for_timeout(3000)
        self.navigate_distribution_history()
        self.page.wait_for_timeout(3000)
        self.search_distribution_history.fill(text)
        self.search_distribution_history_button.click()
        self.page.wait_for_timeout(3000)
        self.navigate()
        self.page.wait_for_timeout(3000)
        self.add_page_to.click()
        self.page.wait_for_timeout(3000)
        self.add_page_to_my_videos.click()
        self.page.wait_for_timeout(3000)
        self.MyVideos.click()
        self.page.wait_for_timeout(3000)
        self.search_stories.click()
        self.page.wait_for_timeout(3000)
        self.search_stories.fill(text)
        self.page.wait_for_timeout(3000)
        self.search_stories_button.click()
        self.page.wait_for_timeout(15000)

    def timeout(self):
        self.page.wait_for_timeout(3000)

    def add_new_file_distributor(self):
        self.hamburger.click()  # hamburger
        self.timeout()
        self.file_distributor_icon.click()  # filedistributor icon
        self.timeout()
        self.add_new_FD.first.click()
        self.timeout()
        self.FD_name.fill("test1")  # input
        self.SD.first.click()  # SD
        self.HD.first.click()
        self.script.first.click()
        self.timeout()
        self.FTP_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.117')
        self.timeout()
        self.target_director.first.fill('/wneclient/data/QA/ftp/files/testJakub')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()
        self.navigate()
        for i in range(1, 4):
            self.add_to_distributor.nth(i).click()
            self.page.wait_for_timeout(3000)
        self.page.locator('//ul[@class = "tab vertical"]//li[5]').click()
        self.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()
        self.timeout()

    def ftps_distribution(self):
        # self.FTPS_option.click()
        self.timeout()
        self.FTPS_Details.click()
        self.timeout()
        self.host.first.fill('10.60.11.28')
        self.timeout()
        self.target_director.first.fill('/')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        self.page.wait_for_timeout(6000)

    def ftp_distribution(self):
        # self.FTP_option.click()
        # self.timeout()
        self.FTP_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.11')
        self.timeout()
        self.target_director.first.fill('/wneclient/data/QA/ftp/files/testJakub')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()

    def sftp_distribution(self):
        self.page.wait_for_timeout(6000)
        self.SFTP_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.11')
        self.timeout()
        self.target_director.first.fill('/wneclient/data/QA/sftp/sk_11july')
        self.timeout()
        self.FD_username.first.fill('wnecadmin')
        self.timeout()
        self.FD_password.first.fill('Offence-Tire-1850-Wnev7')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()

    def add_to_Playout_distribution(self):
        self.hamburger.click()  # hamburger
        self.timeout()
        self.file_distributor_icon.click()  # filedistributor icon
        self.timeout()
        self.add_new_FD.first.click()
        self.timeout()
        self.FD_name.fill("test1")  # input
        self.SD.first.click()  # SD
        self.HD.first.click()
        self.script.first.click()
        self.timeout()
        self.FTP_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.117')
        self.timeout()
        self.target_director.first.fill('/wneclient/data/QA/ftp/files/testJakub')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()
        self.navigate()
        for i in range(1, 4):
            self.playout_icon.nth(i).click()
            self.timeout()
            self.first_channel_patel.click()
            self.timeout()
        self.page.locator('//ul[@class = "tab vertical"]//li[5]').click()
        self.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[1]').click()
        self.page.wait_for_timeout(6000)
        self.playout_show_loop_item.click()
        self.timeout()

    def clear_distribution_history(self):
        self.page.locator('//ul[@class = "tab vertical"]//li[5]').click()
        self.page.wait_for_timeout(3000)
        self.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()
        self.page.wait_for_timeout(3000)
        self.page.locator(
            '//div[@class = "enclosure no-print"]//div[@class = "dropdown-menu dropdown drop-left"]//button[@class = "btn-action tooltip"]').click()
        self.page.wait_for_timeout(3000)
        self.page.locator(
            '//div[@class = "enclosure no-print"]//div[@class = "dropdown-menu dropdown drop-left open"]//div//ul//li[2]').click()
        self.page.wait_for_timeout(3000)
        self.page.locator('//dialog[@class = "inv-bg"]//div//div[@class = "row buttons"]//button[2]').click()

    @property
    def select_protocol(self):
        return self.page.locator('//div[@class = "dropdown-menu dropdown open"]//div//ul//li')

    @property
    def check_advisory(self):
        return self.page.locator('//label[@class = "checkbox label"]')

    @property
    def User_management(self):
        return self.page.locator('//ul[@class = "inv-bg groups"]//li[2]//ul//li[3]')

    @property
    def File_distributor(self):
        return self.page.locator('//ul[@class = "inv-bg groups"]//li[2]//ul//li[4]')

    @property
    def add_user(self):
        return self.page.locator('//button[@class = "btn inv-bg label icon"]')

    def navigate_to_distribution_history(self):
        self.page.locator('//ul[@class = "tab vertical"]//li[5]').click()
        self.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()

    def add_page_to_distribution_fd(self) -> string:
        return self.stories_view.locator(
            "//button[@data-tooltip='Only videos that have arrived are added to the distribution']"
        ).first.click()

    def error_message(self):
        error = self.page.locator('//label[@class = "input error"]//div[@class = "h4 input-info error"]').text_content()
        logging.info(error)
        assert error == "Name must contain only letters, numbers and whitespaces."

    def blank_error_message(self):
        error = self.page.locator('//label[@class = "input error"]//div[@class = "h4 input-info error"]').text_content()
        logging.info(error)
        assert error == "Please specify a name for this distribution process."

    def special_input(self):
        # self.FD_name.fill("")
        self.SD.first.click()
        self.protocol_method.last.click()
        self.select_protocol.first.click()
        text = self.protocol_method.text_content()
        logging.info(text)
        if text == "FTP":
            self.ftp_distribution()
            self.error_message()
        elif text == "SFTP":
            self.sftp_distribution()
            self.error_message()
        else:
            self.ftps_distribution()
            self.error_message()
        self.page.wait_for_timeout(6000)

    def Blank_input(self):
        # self.FD_name.fill("")
        self.SD.first.click()
        self.protocol_method.last.click()
        self.select_protocol.first.click()
        text = self.protocol_method.text_content()
        logging.info(text)
        if text == "FTP":
            self.ftp_distribution()
            self.blank_error_message()
        elif text == "SFTP":
            self.sftp_distribution()
            self.blank_error_message()
        else:
            self.ftps_distribution()
            self.blank_error_message()
        self.page.wait_for_timeout(6000)

    def valid_input(self):
        # self.FD_name.fill("")
        self.SD.first.click()
        self.protocol_method.last.click()
        self.select_protocol.first.click()
        text = self.protocol_method.text_content()
        logging.info(text)
        if text == "FTP":
            self.ftp_distribution()
        elif text == "SFTP":
            self.sftp_distribution()
        else:
            self.ftps_distribution()
        self.navigate()
        self.check_advisory.first.click()
        self.page.wait_for_timeout(6000)

    def ftp_distribution_without_host(self):
        # self.FTP_option.click()
        # self.timeout()
        self.FTP_Details.click()
        self.timeout()
        self.host.first.fill('')
        self.timeout()
        self.target_director.first.fill('/wneclient/data/QA/ftp/files/testJakub')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()

    def ftps_distribution_without_host(self):
        # self.FTPS_option.click()
        self.timeout()
        self.FTPS_Details.click()
        self.timeout()
        self.host.first.fill('')
        self.timeout()
        self.target_director.first.fill('/wneclient/data/QA/ftps/files/ubuntuFTPS')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        self.page.wait_for_timeout(6000)

    def sftp_distribution_without_host(self):
        self.page.wait_for_timeout(6000)
        self.SFTP_Details.click()
        self.timeout()
        self.host.first.fill('')
        self.timeout()
        self.target_director.first.fill('/wneclient/data/QA/sftp/ubuntuSFTP')
        self.timeout()
        self.FD_username.first.fill('wnecadmin')
        self.timeout()
        self.FD_password.first.fill('Offence-Tire-1850-Wnev7')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()

    def without_host(self):
        error_msg = self.page.locator(
            '//div//label[@class = "input error"]//div[@class= "h4 input-info error"]').text_content()
        logging.info(error_msg)
        assert error_msg == "Please specify a valid Host."

    def ftp_distribution_without_target(self):
        # self.FTP_option.click()
        # self.timeout()
        self.FTP_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.117')
        self.timeout()
        self.target_director.first.fill('')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        if self.target_director.text_content() == "":
            self.without_target_directory()

    def ftps_distribution_without_target(self):
        # self.FTPS_option.click()
        self.timeout()
        self.FTPS_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.117')
        self.timeout()
        self.target_director.first.fill('')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.timeout()
        self.save_FD.last.click()
        if self.target_director.text_content() == "":
            self.without_target_directory()

    def sftp_distribution_without_target(self):
        self.page.wait_for_timeout(6000)
        self.SFTP_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.117')
        self.timeout()
        self.target_director.first.fill('')
        self.timeout()
        self.FD_username.first.fill('wnecadmin')
        self.timeout()
        self.FD_password.first.fill('Offence-Tire-1850-Wnev7')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()
        if self.target_director.text_content() == "":
            self.without_target_directory()

    def without_target_directory(self):
        error_msg = self.page.locator(
            '//label[@class = "input error"]//div[@class = "h4 input-info error"]').text_content()
        logging.info(error_msg)
        assert error_msg == "Please specify a valid Remote Base Directory."

    @property
    def new_username(self):
        return self.page.locator('//dialog[@class = "inv-bg user-edit-dialog"]//input[@name = "newUsername"]')

    @property
    def new_password(self):
        return self.page.locator('//dialog[@class = "inv-bg user-edit-dialog"]//input[@name = "newPassword"]')

    def role_permissions(self):
        self.page.locator('//div[@class = "privileges-field"]//ul//li[2]').first.click()  # add to distribution
        self.timeout()
        self.page.locator('//div[@class = "privileges-field"]//ul//li[3]').first.click()  # distribution history
        self.timeout()

    @property
    def new_user_save(self):
        return self.page.locator('//div[@class = "row buttons"]//button[2]')

    @property
    def log_out_from_box(self):
        return self.page.locator('//ul//li//a[@data-nav-name= "Log out from BOX 1"]')

    @property
    def log_in_to_box(self):
        return self.page.locator('//ul//li//a[@data-nav-name= "Log in to BOX 1"]')

    @property
    def login_logout(self):
        return self.page.locator('//button[@class = "dropdown-toggle"]')

    @property
    def add_to_distribution_icon(self):
        return self.page.locator('//div[@class = "td no-print"]//div[@class = "actions"]//div[1]')

    @property
    def File_distributor_icon(self):
        return self.page.locator('//ul[@class = "inv-bg groups"]//li[2]//ul//li[4]')

    @property
    def remove_process(self):
        return self.page.locator('//div[@class = "distribution-actions"]//div[4]//button')

    @property
    def confirm_removal(self):
        return self.page.locator('//dialog[@class = "inv-bg"]//div//div[@class = "row buttons"]//button[2]')

    ####
    @property
    def distribution_target(self):
        return self.page.locator('//div[@class = "td target error-tip"]')

    @property
    def e_message(self):
        return self.page.locator('//form[@class = "edit-distribution disabled"]//h3')

    @property
    def stop_distribution(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/div[3]/div[10]/div[2]/div[3]/button')

    @property
    def confirm_to_stop_distribution(self):
        return self.page.locator('//dialog[@class = "inv-bg"]//div//div//button[2]')

    @property
    def Filters(self):
        return self.page.locator('//div//details[6]//summary//div')

    @property
    def no_filter(self):
        return self.page.locator('//div//details[6]//div//div[@class = "filter row"]').first

    @property
    def service_filter(self):
        return self.page.locator('//label[@data-name = "service_filter"]')

    @property
    def subcon(self):
        return self.page.locator('//div[@class = "row"]//ul//li[1]')

    @property
    def sensitivity_filter(self):
        return self.page.locator('//label[@data-name = "sensitivity_filter"]')

    @property
    def Graphic_Sensitive_filter(self):
        return self.page.locator('//ul[@class = "multiselect"]//li[1]')

    @property
    def save_distribution(self):
        return self.page.locator('//div[@class = "row button-bar"]//button[@class = "btn label"]')

    @property
    def play_distribution(self):
        return self.page.locator('//div[@class = "distribution-actions"]//div[2]')

    @property
    def confirm_play_distribution(self):
        return self.page.locator('//dialog[@class = "inv-bg"]//div//div//button[2]')

    @property
    def cctv_story(self):
        return self.page.locator('//div[@class = "tab-browser row no-print"]//div[2]')

    @property
    def story_dist_icon(self):
        return self.page.locator('//div[@class = "td no-print"]//div[@class = "actions"]//div[2]')

    @property
    def distribution_history(self):
        return self.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]')

    def details_for_distribution(self):
        self.hamburger.click()
        self.file_distributor_icon.click()
        self.add_new_FD.first.click()
        self.FD_name.fill("test1")  # using f-string to create different names
        self.SD.first.click()  # SD
        self.HD.first.click()
        self.script.first.click()
        self.protocol_method.last.click()
        self.timeout()

    def details_for_distribution_different_methods(self, test_num):
        self.hamburger.click()
        self.file_distributor_icon.click()
        self.add_new_FD.first.click()
        self.FD_name.fill(f"test{test_num}")  # using f-string to create different names
        self.SD.first.click()  # SD
        self.HD.first.click()
        self.script.first.click()
        self.protocol_method.last.click()
        self.timeout()

    @property
    def standby_url(self):
        return self.page.locator('//div//input[@name = "standby_uri"]').first

    @property
    def standby_target_directory(self):
        return self.page.locator('//div[@class = "row"]//input[@name = "standby_remote_base_directory"]').first

    @property
    def standby_username(self):
        return self.page.locator('//div[@class = "row"]//input[@name = "standby_username"]').first

    @property
    def standby_password(self):
        return self.page.locator('//div[@class = "row"]//input[@name = "standby_password"]').first

    def standby_ftp_distribution(self):
        self.FTP_Details.click()
        self.host.first.fill('10.99.13.116')
        self.timeout()
        self.target_director.first.fill('/testJakub')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.standby_url.fill("10.99.13.11")
        self.timeout()
        self.standby_target_directory.fill("/testJakub")
        self.timeout()
        self.standby_username.fill("wneqa")
        self.timeout()
        self.standby_password.fill("wneqa123")
        self.timeout()
        self.save_distribution.click()
        self.timeout()

    def standby_without_error_ftp_distribution(self):
        self.FTP_Details.click()
        self.host.first.fill('10.99.13.11')
        self.timeout()
        self.target_director.first.fill('/testJakub')
        self.timeout()
        self.FD_username.first.fill('wneqa')
        self.timeout()
        self.FD_password.first.fill('wneqa123')
        self.standby_url.fill("10.99.13.11")
        self.timeout()
        self.standby_target_directory.fill("/testJakub")
        self.timeout()
        self.standby_username.fill("wneqa")
        self.timeout()
        self.standby_password.fill("wneqa123")
        self.timeout()
        self.save_distribution.click()
        self.timeout()

    import subprocess

    import subprocess

    def print_ssh_logs(self, ip_address, username, password):
        # Using sshpass to provide the password (sshpass must be installed on your system)
        # WARNING: This is insecure as it exposes the password to the process table and history logs.
        command = f"ssh {username}@{ip_address}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            logging.info(f"Output: {output.decode()}")
        else:
            logging.info(f"Error: {error.decode()}")

    def ftp_distribution_without_password(self):
        self.page.wait_for_timeout(6000)
        self.FTP_Details.click()
        self.timeout()
        self.host.first.fill('10.99.13.11')
        self.timeout()
        self.target_director.first.fill('/testJakub')
        self.timeout()
        self.FD_username.first.fill('wnecadmin')
        self.timeout()
        self.FD_password.first.fill('')
        self.timeout()
        self.save_FD.last.click()
        self.timeout()

    def distribution_name(self):
        return self.page.locator('//label[@data-name="name"]//div//input')

    def get_add_files_manually(self):
        return self.page.locator('//div//label[@data-name="manual"][1]')

    def get_Add_files_automatically(self):
        return self.page.locator('//div//label[@data-name="manual"][2]')

    def sd_videos(self):
        return self.page.locator('//div//label[@data-name="accepts_sd_videos"][1]')

    def hd_videos(self):
        return self.page.locator('//div//label[@data-name="accepts_sd_videos"][2]')

    def scripts(self):
        return self.page.locator('//div//label[@data-name="accepts_sd_videos"][3]')

    def distribution_method_dropdown(self):
        return self.page.locator('//div//div[@data-name="distribution_method"]')

    def ftp_dropdown(self):
        return self.page.locator('//div//div[@class="dropdown-menu dropdown open"]//div//ul//li[1]')

    def ftp_host_details(self):
        return self.page.locator(
            '//div//details[@class="details"][2]//div[@class="connections row"]//div//label[@data-name="uri"]//div//input[@name="uri"]')

    def ftp_target_directory_Details(self):
        return self.page.locator(
            '//div//details[@class="details"][2]//div[@class="connections row"]//div//label[@data-name="remote_base_directory"]//div//input[@name="remote_base_directory"]')

    def ftp_username(self):
        return self.page.locator(
            '//div//details[@class="details"][2]//div[@class="connections row"]//div//label[@data-name="username"]//div//input[@name="username"]')

    def ftp_password(self):
        return self.page.locator(
            '//div//details[@class="details"][2]//div[@class="connections row"]//div//label[@data-name="password"]//div//input[@name="password"]')

    def ftps_dropdown(self):
        return self.page.locator('//div//div[@class="dropdown-menu dropdown open"]//div//ul//li[2]')

    def ftps_host_details(self):
        return self.page.locator(
            '//div//details[@class="details"][3]//div[@class="connections row"]//div//label[@data-name="uri"]//div//input[@name="uri"]')

    def ftps_target_directory_Details(self):
        return self.page.locator(
            '//div//details[@class="details"][3]//div[@class="connections row"]//div//label[@data-name="remote_base_directory"]//div//input[@name="remote_base_directory"]')

    def ftps_username(self):
        return self.page.locator(
            '//div//details[@class="details"][3]//div[@class="connections row"]//div//label[@data-name="username"]//div//input[@name="username"]')

    def ftps_password(self):
        return self.page.locator(
            '//div//details[@class="details"][3]//div[@class="connections row"]//div//label[@data-name="password"]//div//input[@name="password"]')

    def sftp_dropdown(self):
        return self.page.locator('//div//div[@class="dropdown-menu dropdown open"]//div//ul//li[3]')

    def sftp_host_details(self):
        return self.page.locator(
            '//div//details[@class="details"][4]//div[@class="connections row"]//div//label[@data-name="uri"]//div//input[@name="uri"]')

    def sftp_target_directory_Details(self):
        return self.page.locator(
            '//div//details[@class="details"][4]//div[@class="connections row"]//div//label[@data-name="remote_base_directory"]//div//input[@name="remote_base_directory"]')

    def sftp_username(self):
        return self.page.locator(
            '//div//details[@class="details"][4]//div[@class="connections row"]//div//label[@data-name="username"]//div//input[@name="username"]')

    def sftp_password(self):
        return self.page.locator(
            '//div//details[@class="details"][4]//div[@class="connections row"]//div//label[@data-name="password"]//div//input[@name="password"]')

    def smb_dropdown(self):
        return self.page.locator('//div//div[@class="dropdown-menu dropdown open"]//div//ul//li[4]')

    def smb_target_Directory_path(self):
        return self.page.locator('//div//details[5]//div//label[@data-name = "target_directory"]//div//input')

    def smb_domain(self):
        return self.page.locator('//details[@class="details"]//div//label[@data-name ="domain"]//div//input')

    def smb_username(self):
        return self.page.locator('//div//details[5]//div//label[@data-name = "username"]//div//input')

    def smb_password(self):
        return self.page.locator('//div//details[5]//div//label[@data-name = "password"]//div//input')

    def start_distribution(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/div[3]/div[10]/div[2]/div[2]/button')

    def confirm_start_stop_distribution(self):
        return self.page.locator('//*[@id="modal-root"]/div/dialog/div/div/button[2]')

    def export_all_processes(self):
        return self.page.locator(
            '//article[@class="admin-distribution"]//div[@class="row button-bar"]//button[2][@class="btn inv-bg label icon"]')

    def click_a_story(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[3]/div[10]/div[2]/div[1]/button[1]')

    def stories_copy_link(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[3]/div[15]/div/div/div[2]/div/button[2]')

    def copied_link_content(self):
        return self.page.locator('//*[@id="modal-root"]/div/dialog/div/label/div/input')

    def clear_search_button(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[1]/div/button[2]')

    def confirm_clear_button(self):
        return self.page.locator('//*[@id="modal-root"]/div/dialog/div/div/button[2]')

    def source_drop_down(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[1]/button')

    def file_playout(self):
        return self.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[1]/div/ul/li[5]/button')

    def confirmation_popup(self):
        return self.page.locator('//*[@id="modal-root"]/div/dialog/div/div/button[2]')

    def mode_dropdown(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[2]/button')

    def loop_mode(self):
        return self.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[2]/div/ul/li[2]/button')

    def elements(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[2]/div[13]/div[2]/div[1]/div[1]')

    def clear_history(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[1]/div/button[2]')

    def confirm_clear(self):
        return self.page.locator('//*[@id="modal-root"]/div/dialog/div/div/button[2]')

    def add_page_to_dropdown(self):
        self.page.locator('//div[@data-name="add-page"]').click()

    def add_page_to_FD_dropdown(self):
        self.page.locator('//div[@data-name="add-page"]//div//ul//li[1]').click()

    def storypage_elements(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/table/tbody/tr[1]/td[1]/h2')

    def source_as_live_in_dropdown(self):
        return self.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[1]/div/ul/li[2]/button')

    def manual_mode_for_live_source(self):
        return self.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[2]/div/ul/li[2]/button')

    def primary_ftp_details(self):
        ftp_location_details = self.page.locator('//div//details[@class="details"][2]')
        primary_host = self.page.locator('//input[@name="uri"]').first
        primary_target_directory = self.page.locator('//input[@name="remote_base_directory"]').first
        primary_username = self.page.locator('//input[@name="username"]').first
        primary_password = self.page.locator('//input[@name="password"]').first
        ftp_location_details.click()
        primary_host.fill("10.99.13.11")
        primary_target_directory.fill("/wneclient/data/QA/ftp/files/testJakub")
        primary_username.fill("wneqa")
        primary_password.fill("wneqa123")

    def standby_ftp_details(self):
        secondary_host = self.page.locator('//input[@name="standby_uri"]').first
        secondary_target_directory = self.page.locator('//input[@name="standby_remote_base_directory"]').first
        secondary_username = self.page.locator('//input[@name="standby_username"]').first
        secondary_password = self.page.locator('//input[@name="standby_password"]').first
        secondary_host.fill("10.99.13.11")
        secondary_target_directory.fill("/wneclient/data/QA/ftp/files/testJakub")
        secondary_username.fill("wneqa")
        secondary_password.fill("wneqa123")
        save_button = self.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
        save_button.click()

    def add_all_stories_to_distribution(self):
        self.navigate()
        self.add_page_to_dropdown()
        self.page.wait_for_timeout(2000)
        self.add_page_to_FD_dropdown()
        self.page.wait_for_timeout(2000)

    def verify_distribution_on_history_page(self):
        History_page_link = self.page.locator('//ul[@class="tab vertical"]//li[5]')
        Distribution_history_link = self.page.locator('//ul[@class="tab horizontal inpage no-print"]//li[2]')
        History_page_link.click()
        Distribution_history_link.click()
        self.page.wait_for_timeout(2000)
        cells = self.page.locator('//tbody//tr//td')
        cell_count = cells.count()

        for i in range(cell_count):
            text = cells.nth(i).text_content()
            logging.info(f"Cell {i + 1}: {text}")

    def simulate_primary_server_failure(self):
        ftp_location_details = self.page.locator('//div//details[@class="details"][2]')
        primary_host = self.page.locator('//input[@name="uri"]').first
        primary_target_directory = self.page.locator('//input[@name="remote_base_directory"]').first
        primary_username = self.page.locator('//input[@name="username"]').first
        primary_password = self.page.locator('//input[@name="password"]').first
        ftp_location_details.click()
        primary_host.fill("10.99.13.117")
        self.page.wait_for_timeout(2000)
        primary_target_directory.fill("/wneclient/data/QA/ftp/files/testJakub")
        primary_username.fill("wneqa")
        primary_password.fill("wneqa123")
        self.page.wait_for_timeout(2000)
        save_button = self.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
        save_button.click()
        self.page.wait_for_timeout(2000)

    def details_for_automatic_distribution(self):
        self.hamburger.click()
        self.file_distributor_icon.click()
        self.add_new_FD.first.click()
        self.FD_name.fill("test2")  # using f-string to create different names
        automatic_method = self.page.locator('//div//label[@data-name="manual"][2]')
        automatic_method.click()
        self.SD.first.click()  # SD
        self.HD.first.click()
        self.script.first.click()
        self.protocol_method.last.click()
        self.timeout()

    def automatic_primary_ftp_details(self):
        ftp_location_details = self.page.locator('//div//details[2]')
        primary_host = self.page.locator('//input[@name="uri"]').first
        primary_target_directory = self.page.locator('//input[@name="remote_base_directory"]').first
        primary_username = self.page.locator('//input[@name="username"]').first
        primary_password = self.page.locator('//input[@name="password"]').first
        ftp_location_details.click()
        primary_host.fill("10.99.13.11")
        primary_target_directory.fill("/wneclient/data/QA/ftp/files/testJakub")
        primary_username.fill("wneqa")
        primary_password.fill("wneqa123")

    def check_if_distribution_dropdown_is_visible(self):
        self.navigate()

        # Step 1: Click the dropdown to reveal options
        dropdown = self.page.locator('//div[@data-name="add-page"]')
        dropdown.click()

        # Step 2: Locate all <li> elements inside the dropdown
        options_locator = self.page.locator('//div[@data-name="add-page"]//div//ul//li')
        option_texts = options_locator.all_text_contents()

        # Step 3: Log all options
        logging.info("Dropdown options available:")
        for i, text in enumerate(option_texts, start=1):
            logging.info(f"Option {i}: {text}")

        # Step 4: Assert that "Distribution" is NOT present
        if "Distribution" not in option_texts:
            logging.info("✅ 'Distribution' option is not available in the dropdown.")
        else:
            raise AssertionError("'Distribution' option should not be visible in the dropdown.")

        # Optional: Wait for visual confirmation
        self.page.wait_for_timeout(2000)

    def Export_button(self):
        return self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/div[1]/button[2]')

    def distribution_details_for_legacy_files(self):
        ftp_location_details = self.page.locator('//div//details[@class="details"][2]')
        primary_host = self.page.locator('//input[@name="uri"]').first
        primary_target_directory = self.page.locator('//input[@name="remote_base_directory"]').first
        primary_username = self.page.locator('//input[@name="username"]').first
        primary_password = self.page.locator('//input[@name="password"]').first
        legacy_files_checkbox = self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/form/div[1]/label[7]')
        save_button = self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/form/div[3]/button')
        ftp_location_details.click()
        primary_host.fill("10.99.13.11")
        primary_target_directory.fill("/wneclient/data/QA/ftp/files/testJakub")
        primary_username.fill("wneqa")
        primary_password.fill("wneqa123")
        self.page.wait_for_timeout(2000)
        legacy_files_checkbox.click()
        self.page.wait_for_timeout(2000)
        save_button.click()

    def distribution_details_for_service_code(self):
        ftp_location_details = self.page.locator('//div//details[@class="details"][2]')
        primary_host = self.page.locator('//input[@name="uri"]').first
        primary_target_directory = self.page.locator('//input[@name="remote_base_directory"]').first
        primary_username = self.page.locator('//input[@name="username"]').first
        primary_password = self.page.locator('//input[@name="password"]').first
        legacy_files_checkbox = self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/form/div[1]/label[7]')
        filters_drop_down = self.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/form/div[2]/details[6]/summary/div')
        subcon_filter = self.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/form/div[2]/details[6]/div/div[2]/div/ul/li[1]')
        save_button = self.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/article/form/div[3]/button')
        ftp_location_details.click()
        primary_host.fill("10.99.13.11")
        primary_target_directory.fill("/wneclient/data/QA/ftp/files/testJakub")
        primary_username.fill("wneqa")
        primary_password.fill("wneqa123")
        self.page.wait_for_timeout(2000)
        legacy_files_checkbox.click()
        self.page.wait_for_timeout(2000)
        filters_drop_down.click()
        subcon_filter.click()
        save_button.click()

    def export_as_json(self):
        return self.page.locator('//div[@class="distribution-actions"]//div[@class="flashing-indicators-holder"][1]')

    def clearing_all_distribution_methods(self):
        while True:
            indicators = self.page.locator(
                '//div[@class="distribution-actions"]//div[@class="flashing-indicators-holder"][4]'
            )

            count = indicators.count()
            if count == 0:
                break  # No more indicators to process

            # Always click the first one to avoid stale references
            indicators.first.click()
            self.page.wait_for_timeout(1000)

            # Wait for dialog and click cancel
            confirm_cancel = self.page.locator(
                '//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]'
            )

            if confirm_cancel.is_visible():
                confirm_cancel.click()
                self.page.wait_for_timeout(2000)

    def clear_distribution_history_if_the_clear_button_is_present(self):
        clear_button = self.clear_history()
        if clear_button.is_visible():
            clear_button.click()
            self.timeout()
            confirm_clear = self.confirm_clear()
            if confirm_clear.is_visible():
                confirm_clear.click()
                self.timeout()

    def story_slug_locator(self):
        return self.page.locator('//table//tbody//tr//td[1]')

    def search_bar(self):
        return self.page.locator('//input[@placeholder="Search distribution history"]')

    def search_result(self):
        return self.page.locator('//table//tbody//tr//td[1]')

    def simulate_primary_server_failure_for_failure(self):
        self.navigate()  # navigate to the story page
        self.hamburger.click()
        self.file_distributor_icon.click()
        self.page.locator('//button[@data-tooltip="Stop"]').click()
        self.page.wait_for_timeout(2000)
        self.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]').click()
        self.page.locator('//div[@class="td name error-tip"]').click()
        self.page.wait_for_timeout(2000)
        self.page.locator('//div//details[@class="details"][2]').click()
        self.page.locator('//input[@name="uri"]').first.clear()
        self.page.wait_for_timeout(2000)
        self.page.locator('//input[@name="uri"]').first.fill("10.99.13.117")
        save_button = self.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
        save_button.click()
        self.page.wait_for_timeout(2000)
        self.page.locator('//button[@data-tooltip="Start"]').click()
        self.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]').click()
        self.page.wait_for_timeout(2000)

    def restore_primary_server(self):
        self.navigate()  # navigate to the story page
        self.hamburger.click()
        self.file_distributor_icon.click()
        self.page.locator('//button[@data-tooltip="Stop"]').click()
        self.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]').click()
        self.page.wait_for_timeout(2000)
        self.page.locator('//div[@class="td name error-tip"]').click()
        self.page.locator('//div//details[@class="details"][2]').click()
        self.page.wait_for_timeout(2000)
        self.page.locator('//input[@name="uri"]').first.clear()
        self.page.locator('//input[@name="uri"]').first.fill("10.99.13.11")
        self.page.wait_for_timeout(2000)
        save_button = self.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
        save_button.click()
        self.page.locator('//button[@data-tooltip="Start"]').click()
        self.page.wait_for_timeout(2000)
        self.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]').click()

    def Attempt_to_add_to_distribution_without_an_active_distribution(self):
        self.page.wait_for_timeout(2000)
        self.navigate()  # navigate to the story page
        self.page.wait_for_timeout(2000)
        self.details_for_automatic_distribution()
        self.FTP_option.click()  # click on FTP option
        self.automatic_primary_ftp_details()  # save primary details for ftp server
        save_button = self.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
        save_button.click()
