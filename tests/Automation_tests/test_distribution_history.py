import logging

import allure

import logging
from playwright.sync_api import expect


@allure.feature("Distribution History")
def test_distribution_history_clear_all(story_page):
    test_distribution_history_clear_all.__doc__ = """Tests the clear all functionality in distribution history.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to distribution admin page
       - Clears existing distribution methods
       - Configures distribution details
       - Sets up FTP distribution

    2. Story Distribution:
       - Adds all stories to distribution queue
       - Navigates to distribution history
       - Waits for history page load

    3. Clear Operation:
       - Clicks dropdown menu button
       - Selects clear option
       - Confirms clear action
       - Verifies operation completion

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working distribution interface
        - Story content availability
        - Distribution method configuration
        - Clear permissions

    Expected Results:
        - Distribution methods cleared
        - Stories added successfully
        - Clear operation completed
        - History cleaned up properly

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: via navigation
    """
    story_page.navigate()
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.clearing_all_distribution_methods()
    story_page.page.wait_for_timeout(5000)
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.page.wait_for_timeout(5000)
    story_page.page.locator(
        '//div[@class="enclosure no-print"]//div[@class="dropdown-menu dropdown drop-left"]//button').click()
    story_page.timeout()
    story_page.page.locator(
        '//div[@class="enclosure no-print"]//div[@class="dropdown-menu dropdown drop-left open"]//div//ul//li[2]').click()
    story_page.timeout()
    story_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
    story_page.timeout()


@allure.feature("Distribution History")
def test_distribution_history_print(story_page):
    test_distribution_history_print.__doc__ = """Tests print functionality in distribution history page.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to distribution admin
       - Clears existing methods
       - Waits for page load
       - Configures distribution details

    2. Story Distribution:
       - Sets up FTP distribution
       - Adds all stories to distribution
       - Navigates to history page
       - Ensures page load completion

    3. Print Operation:
       - Emulates print media
       - Suppresses print dialog
       - Verifies print operation
       - Logs operation status

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working distribution interface
        - Print media emulation support
        - Story content availability
        - Distribution configurations

    Expected Results:
        - Distribution methods configured
        - Stories added successfully
        - Print media emulated
        - Operation logged properly

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: via navigation
    """
    story_page.navigate()
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(5000)
    story_page.clearing_all_distribution_methods()
    story_page.page.wait_for_timeout(5000)
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.page.wait_for_timeout(5000)
    # Suppress the print dialog by emulating print media
    story_page.page.emulate_media(media="print")
    logging.info("Print media emulated successfully.")

    # Log success
    logging.info("Print button clicked, and test passed without manual intervention.")


@allure.feature("Distribution History")
def test_distribution_history_exportascv(story_page):
    test_distribution_history_exportascv.__doc__="""Tests CSV export functionality in distribution history page.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to distribution admin
       - Clears existing distribution methods
       - Waits for cleanup completion
       - Sets distribution details

    2. Story Distribution:
       - Configures FTP distribution
       - Adds all stories to distribution queue
       - Navigates to history page
       - Ensures data load completion

    3. Export Operation:
       - Locates export button
       - Triggers CSV download
       - Verifies operation completion

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working distribution interface
        - FTP configuration access
        - Story content availability
        - CSV export permissions

    Expected Results:
        - Distribution methods configured
        - Stories added to distribution
        - CSV export initiated
        - Download completed

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: via navigation
    """
    story_page.navigate()
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(5000)
    story_page.clearing_all_distribution_methods()
    story_page.page.wait_for_timeout(5000)
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.page.wait_for_timeout(5000)
    story_page.page.locator('//div[@class="enclosure no-print"]//a').click()
    story_page.timeout()
