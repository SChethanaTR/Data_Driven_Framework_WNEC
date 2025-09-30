import logging

import allure

import logging
from playwright.sync_api import expect





@allure.feature("History")
def test_playout_print(story_page):
    test_playout_print.__doc__=  """Tests print functionality in playout history with loop mode configuration.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to playout history
       - Clears existing search filters
       - Handles confirmation dialogs

    2. Playout Configuration:
       - Sets content source to file playout
       - Configures loop mode
       - Handles confirmation popups
       - Validates mode settings

    3. Loop Settings:
       - Returns to history page
       - Checks loop checkbox state
       - Enables loop configuration if needed
       - Triggers print action

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working playout interface
        - Print functionality
        - Loop mode access
        - History page access

    Expected Results:
        - Clear operation successful
        - File playout configured
        - Loop mode enabled
        - Print dialog triggered

    URLs Accessed:
        - History Page: http://10.189.200.6/history/playout
        - Admin Playout: http://10.189.200.6/admin/playout
    """
    story_page.navigate()

    # Navigate to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()

    # Check if the clear button is present
    clear_button = story_page.clear_search_button()
    if clear_button.is_visible():
        clear_button.click()
        story_page.timeout()
        # Confirm clearing if confirmation dialog appears
        confirm_clear = story_page.confirm_clear_button()
        if confirm_clear.is_visible():
            confirm_clear.click()
            story_page.timeout()

    # Navigate to the admin playout page
    story_page.page.goto("http://10.189.200.6/admin/playout")
    story_page.timeout()

    # Configure file-layout
    source_dropdown = story_page.source_drop_down()
    file_playout = story_page.file_playout()
    source_dropdown.click()
    story_page.timeout()
    file_playout.click()
    story_page.timeout()

    # Handle confirmation popup if it appears
    confirmation_popup = story_page.confirmation_popup()
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()
    else:
        pass
        # Configure loop mode
    mode_dropdown = story_page.mode_dropdown()
    loop_mode = story_page.loop_mode()
    mode_dropdown.click()
    story_page.timeout()
    loop_mode.click()
    story_page.timeout()

    # Handle confirmation popup for loop mode
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Navigate to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()
    loop_checkbox = story_page.page.locator('//label[@data-name="loopitems"]')
    if not loop_checkbox.is_checked():
        logging.info("Loop configuration is currently hidden. Enabling it now.")
        loop_checkbox.check()
        logging.info("Loop configuration is now visible.")
    else:
        logging.info("Loop configuration is already visible.")
    story_page.page.wait_for_timeout(3000)
    story_page.page.locator('//div[@class="enclosure no-print"]//button[@class="btn-icon tooltip no-print"]').nth(1).click()
    story_page.page.wait_for_timeout(3000)




@allure.feature("History")
def test_playout_export_as_cv(story_page):
    test_playout_export_as_cv.__doc__="""Tests CSV export functionality in playout history with loop mode configuration.

    Detailed Test Flow:
    1. History Page Setup:
       - Navigates to playout history
       - Clears existing search filters
       - Handles clear confirmation dialogs

    2. Playout Configuration:
       - Switches to admin playout page
       - Sets content source to file playout
       - Handles source confirmation popup
       - Configures loop mode setting
       - Manages mode confirmation dialogs

    3. Export Operation:
       - Returns to history page
       - Verifies loop checkbox state
       - Enables loop items if needed
       - Triggers CSV export via button click

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working playout interface
        - CSV export functionality
        - Loop mode access
        - History page access

    Expected Results:
        - Clear filters successful
        - File playout configured
        - Loop mode enabled
        - CSV export initiated

    URLs Accessed:
        - History Page: http://10.189.200.6/history/playout
        - Admin Playout: http://10.189.200.6/admin/playout
    """
    story_page.navigate()

    # Navigate to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()

    # Check if the clear button is present
    clear_button = story_page.clear_search_button()
    if clear_button.is_visible():
        clear_button.click()
        story_page.timeout()
        # Confirm clearing if confirmation dialog appears
        confirm_clear = story_page.confirm_clear_button()
        if confirm_clear.is_visible():
            confirm_clear.click()
            story_page.timeout()

    # Navigate to the admin playout page
    story_page.page.goto("http://10.189.200.6/admin/playout")
    story_page.timeout()

    # Configure file-layout
    source_dropdown = story_page.source_drop_down()
    file_playout = story_page.file_playout()
    source_dropdown.click()
    story_page.timeout()
    file_playout.click()
    story_page.timeout()

    # Handle confirmation popup if it appears
    confirmation_popup = story_page.confirmation_popup()
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()
    else:
        pass
        # Configure loop mode
    mode_dropdown = story_page.mode_dropdown()
    loop_mode = story_page.loop_mode()
    mode_dropdown.click()
    story_page.timeout()
    loop_mode.click()
    story_page.timeout()

    # Handle confirmation popup for loop mode
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()


    # Navigate to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()
    loop_checkbox = story_page.page.locator('//label[@data-name="loopitems"]')
    if not loop_checkbox.is_checked():
        logging.info("Loop configuration is currently hidden. Enabling it now.")
        loop_checkbox.check()
        logging.info("Loop configuration is now visible.")
    else:
        logging.info("Loop configuration is already visible.")
    story_page.page.wait_for_timeout(3000)
    story_page.page.locator('//div[@class="enclosure no-print"]//a').click()
    story_page.timeout()











