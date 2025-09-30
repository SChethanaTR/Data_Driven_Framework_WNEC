import logging
import re
import pytest
from playwright.sync_api import expect
from component_util import db_manager
from conftest import my_video_added
from pages.home import my_video


def test_file_logs(file_logs):
    file_logs.navigate()
    file_logs.page.wait_for_timeout(3000)
    file_logs.all_application_tab.click()
    message = file_logs.page.locator('//div[@class = "expandable-grid"]//div[6]').text_content()
    logging.info(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.history_search.type(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.history_search_button.click()
    file_logs.page.wait_for_timeout(3000)
    file_logs.download_All_button.click()
    file_logs.page.wait_for_timeout(3000)
    file_logs.navigate_file_distributor()
    file_logs.page.wait_for_timeout(3000)
    file_logs.navigate_file_purger()
    file_logs.page.wait_for_timeout(3000)
    file_logs.navigate_file_purger()
    file_logs.page.wait_for_timeout(3000)


def test_search_file_distributor(file_logs):
    file_logs.navigate_file_distributor()
    file_logs.page.wait_for_timeout(3000)
    message = file_logs.page.locator('//div[@class = "expandable-grid"]//div[6]').text_content()
    logging.info(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.file_dist_history_search.type(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.file_dist_history_search_button.click()


def test_search_file_processor(file_logs):
    file_logs.navigate_file_processor()
    file_logs.page.wait_for_timeout(3000)
    message = file_logs.page.locator('//div[@class = "expandable-grid"]//div[6]').text_content()
    logging.info(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.file_processor_history_search.type(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.file_processor_history_search_button.click()


def test_search_file_purger(file_logs):
    file_logs.navigate_file_purger()
    file_logs.page.wait_for_timeout(3000)
    message = file_logs.page.locator('//div[@class = "expandable-grid"]//div[6]').text_content()
    logging.info(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.file_purger_history_search.type(message)
    file_logs.page.wait_for_timeout(3000)
    file_logs.file_purger_history_search_button.click()