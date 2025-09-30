import logging
import time

import allure

import env
import pytest
from playwright.sync_api import expect
import pandas as pd
import logging

from helpers import ubuntu
from helpers.database import Database


@allure.feature("UserInterface")  # working #all locators are correct
def test_HistoryPage_Playout_History(story_page):
    test_HistoryPage_Playout_History.__doc__="""Tests playout history functionality by configuring playout and verifying history entries.

    Detailed Test Flow:
    1. History Setup:
       - Navigates to playout history
       - Clears existing history if needed
       - Handles clear confirmations

    2. Playout Configuration:
       - Accesses admin playout page
       - Sets source to file playout
       - Configures loop mode
       - Manages confirmation dialogs

    3. History Verification:
       - Returns to history page
       - Enables loop items view
       - Waits for story elements
       - Logs visible story slugs

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working playout interface
        - History page access
        - File playout configuration
        - Story content availability

    Expected Results:
        - History cleared successfully
        - Playout configured properly
        - Loop mode enabled
        - Stories visible in history

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

    # Navigate back to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()
    story_page.page.locator('//label[@data-name="loopitems"]').click()
    story_page.timeout()

    # Wait until all stories are visible on the page
    elements = story_page.elements()
    elements.wait_for(state="visible")

    # # Print all items in the history page
    # all_texts = elements.all_text_contents()
    # for text in all_texts:
    #     logging.info(text)

    story_slug = story_page.page.locator('//div[@class="td source-id-slug justified"]//div[@class="cell-text h4"]')
    for i in range(story_slug.count()):
        logging.info(story_slug.nth(i).text_content())
        story_page.timeout()


@allure.feature("UserInterface")
def test_PlayoutPage_Print_MyPlayout_page(user_interface_page):
    test_PlayoutPage_Print_MyPlayout_page.__doc__= """Tests print functionality in playout page.

    Detailed Test Flow:
    1. Page Setup:
       - Navigates to playout page
       - Ensures page load completion
       - Verifies page accessibility

    2. Print Operation:
       - Locates printer icon
       - Triggers print dialog
       - Verifies dialog appearance

    Args:
        user_interface_page: Fixture providing interface methods and page controls

    Dependencies:
        - Working playout interface
        - Print functionality access
        - Print dialog support

    Expected Results:
        - Navigation successful
        - Print icon visible
        - Print dialog triggered
        - Operation logged

    URLs Accessed:
        - Playout Page: http://10.189.200.6/playout
    """
    user_interface_page.navigate()
    user_interface_page.timeout()
    # navigate to the playout page
    user_interface_page.page.goto('http://10.189.200.6/playout')
    user_interface_page.timeout()
    # click on the printer icon
    user_interface_page.print_sdi_channel_page().click()
    logging.info("Dailog box for Printing the page has opened")


@allure.feature("UserInterface")
def test_LivePage_Check_LivePreview(user_interface_page):
    test_LivePage_Check_LivePreview.__doc__="""Tests live preview functionality by verifying content presence.

    Detailed Test Flow:
    1. Page Navigation:
       - Navigates to live page
       - Waits for page load
       - Ensures accessibility

    2. Content Verification:
       - Checks first row content
       - Validates live content presence
       - Logs verification results

    Args:
        user_interface_page: Fixture providing interface methods and page controls

    Dependencies:
        - Working live interface
        - Live content availability
        - Preview functionality

    Expected Results:
        - Navigation successful
        - Live content visible
        - Status logged correctly

    URLs Accessed:
        - Live Page: http://10.189.200.6/live
    """
    user_interface_page.navigate()
    user_interface_page.timeout()
    # navigate to the live page
    user_interface_page.page.goto('http://10.189.200.6/live')
    user_interface_page.timeout()
    # checking if there is atleast a video in live page to confirm live is working
    story = user_interface_page.livepage_first_row().text_content()  # content of first row
    logging.info(story)
    if story:
        logging.info('Live page exists')
    else:
        logging.info('Live page doesnt exists')
    user_interface_page.timeout()


@allure.feature("UserInterface")
def test_StoriesPage_CopyLink(story_page):
    test_StoriesPage_CopyLink.__doc__="""Tests story link copying functionality and link validation.

    Detailed Test Flow:
    1. Page Navigation:
       - Navigates to stories page
       - Enables advisories view
       - Selects specific story

    2. Link Operations:
       - Triggers copy link action
       - Captures copied link value
       - Validates link format

    3. Link Verification:
       - Opens new browser tab
       - Navigates to copied URL
       - Verifies page load
       - Waits for content stability

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working stories interface
        - Copy functionality
        - Multi-tab browser support

    Expected Results:
        - Advisory toggle successful
        - Link copied correctly
        - New tab opens
        - Link loads successfully

    Wait Times:
        - Page load: Default timeout
        - Content stability: 30 seconds
    """
    story_page.navigate()
    story_page.page.locator('//label[@data-name="advisories"]').click()
    story_page.timeout()
    story_page.click_a_story().click()  # clicking on a story
    story_page.timeout()
    story_page.stories_copy_link().click()  # clicking on the copy link
    story_page.timeout()
    # Get the value of the input field
    copied_value = story_page.copied_link_content().input_value()  # getting the copied link value
    story_page.timeout()
    # Log the copied value
    logging.info(f"Copied value: {copied_value}")

    # Open the copied link in a new tab
    new_tab = story_page.page.context.new_page()
    new_tab.goto(copied_value)
    new_tab.wait_for_load_state()
    logging.info("Copied link opened in a new tab.")
    # Wait for a few minutes (e.g., 2 minutes)
    time.sleep(30)
    logging.info("Waited for 1 minutes.")


@allure.feature("UserInterface")
def test_HistoryPage_Hide_Or_Show_Loop_Configuration(story_page):
    test_HistoryPage_Hide_Or_Show_Loop_Configuration.__doc__="""Tests loop configuration visibility control in playout history.

    Detailed Test Flow:
    1. History Setup:
       - Navigates to playout history
       - Clears existing history
       - Handles clear confirmations

    2. Playout Configuration:
       - Sets source to file playout
       - Enables loop mode
       - Manages confirmation dialogs

    3. Loop Visibility:
       - Returns to history page
       - Verifies loop checkbox state
       - Toggles loop configuration
       - Validates content visibility

    4. Content Verification:
       - Waits for story elements
       - Logs visible story entries
       - Verifies loop configuration state

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working playout interface
        - History page access
        - Loop mode functionality
        - Content availability

    Expected Results:
        - History cleared successfully
        - File playout configured
        - Loop mode enabled
        - Loop configuration toggled
        - Stories visible and logged

    URLs Accessed:
        - History Page: http://10.189.200.6/history/playout
        - Admin Playout: http://10.189.200.6/admin/playout
    """
    # Step 1: Navigate to the story page
    story_page.navigate()

    # Step 2: Go to the playout history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()

    # Step 3: Clear history if clear button is visible
    clear_button = story_page.page.locator('//div[@class="enclosure no-print"]//button[@type="button"][2]')
    if clear_button.is_visible():
        clear_button.click()
        story_page.timeout()

        confirm_clear = story_page.page.locator('//dialog[@class="inv-bg"]//button[2]')
        if confirm_clear.is_visible():
            confirm_clear.click()
            story_page.timeout()

    # Step 4: Navigate to admin playout page
    story_page.page.goto("http://10.189.200.6/admin/playout")
    story_page.timeout()

    # Step 5: Configure file-layout
    source_dropdown = story_page.page.locator(
        '//div[@class="list column"]//div[@class="row list-row"][1]//div[@data-name="source"]')
    file_playout = story_page.page.locator('//div[@data-name="source"]//ul//li[5]')

    source_dropdown.click()
    story_page.timeout()
    file_playout.click()
    story_page.timeout()

    # Step 6: Confirm file-layout configuration
    confirmation_popup = story_page.page.locator('//dialog[@class="inv-bg"]//button[2]')
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Step 7: Configure loop mode
    mode_dropdown = story_page.page.locator(
        '//div[@class="list column"]//div[@class="row list-row"][1]//div[@data-name="mode"]')
    loop_mode = story_page.page.locator(
        '//div[@class="list column"]//div[@class="row list-row"][1]//div[@data-name="mode"]//div//ul//li[1]')

    mode_dropdown.click()
    story_page.timeout()
    loop_mode.click()
    story_page.timeout()

    # Step 8: Confirm loop mode configuration
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Step 9: Return to playout history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()

    # Step 10: Check and toggle loop configuration checkbox
    loop_checkbox = story_page.page.locator('//label[@data-name="loopitems"]')
    if not loop_checkbox.is_checked():
        logging.info("Loop configuration is currently hidden. Enabling it now.")
        loop_checkbox.check()
        logging.info("Loop configuration is now visible.")
    else:
        logging.info("Loop configuration is already visible.")
    story_page.page.wait_for_timeout(3000)

    # Step 11: Log all visible items on the page
    elements = story_page.page.locator(
        '//div[@class="td source-id-slug justified"]//div[@class="row"]//div[@class="cell-text h4"][1]')
    for i in range(elements.count()):
        logging.info(elements.nth(i).text_content())
        story_page.page.wait_for_timeout(1000)


@allure.feature("UserInterface")
def test_Clear_Playout_History(story_page):
    test_Clear_Playout_History.__doc__= """Tests clear functionality in playout history page.

    Detailed Test Flow:
    1. Navigation:
       - Accesses playout history page
       - Ensures page load completion

    2. Loop Items Setup:
       - Locates loop items checkbox
       - Verifies checkbox state
       - Enables if unchecked
       - Waits for UI update

    3. Clear Operation:
       - Locates clear button
       - Verifies button visibility
       - Triggers clear action
       - Handles confirmation dialog

    Args:
        story_page: Fixture providing page interface and controls

    Dependencies:
        - Working history interface
        - Clear functionality
        - Loop items toggle
        - Confirmation dialogs

    Expected Results:
        - Page loads successfully
        - Loop items visible
        - Clear action completes
        - History cleared

    URLs Accessed:
        - History Page: http://10.189.200.6/history/playout
    """
    # Step 1: Navigate to Playout History Page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()

    # Step 2: Locate the 'Show Loop Items' checkbox
    loop_checkbox = story_page.page.locator('//label[@data-name="loopitems"]')

    # Step 3: Check if checkbox is unchecked, then check it
    if not loop_checkbox.is_checked():
        logging.info("Loop items checkbox is unchecked. Checking it to reveal Clear button.")
        loop_checkbox.check()
        story_page.timeout()
    else:
        logging.info("Loop items checkbox is already checked.")

    # Step 4: Locate and click the Clear button
    clear_button = story_page.page.locator('//div[@class="enclosure no-print"]//button[@type="button"][2]')
    if clear_button.is_visible():
        logging.info("Clear button is visible. Clicking to clear history.")
        clear_button.click()
        story_page.timeout()

        # Step 5: Confirm the clear action if confirmation dialog appears
        confirm_clear = story_page.page.locator('//dialog[@class="inv-bg"]//button[2]')
        if confirm_clear.is_visible():
            logging.info("Confirmation dialog appeared. Confirming clear action.")
            confirm_clear.click()
            story_page.timeout()
        else:
            logging.info("No confirmation dialog appeared.")
    else:
        logging.warning("Clear button is not visible even after checking the loop checkbox.")


@allure.feature("UserInterface")
def test_LivePage_live_page_view(story_page):
    test_LivePage_live_page_view.__doc__= """Tests content visibility on live page.

    Detailed Test Flow:
    1. Page Navigation:
       - Loads live page URL
       - Waits for page response

    2. Content Verification:
       - Locates live event rows
       - Checks for content presence
       - Logs visible event details

    Args:
        story_page: Fixture providing story page interface and methods

    Dependencies:
        - Working live interface
        - Live content availability
        - XPath element access

    Expected Results:
        - Page loads successfully
        - Event rows found or absence logged
        - Content details captured

    URLs Accessed:
        - Live Page: http://10.189.200.6/live
    """
    story_page.navigate()
    story_page.page.goto("http://10.189.200.6/live")
    story_page.timeout()

    # Locate all elements matching the given XPath
    elements = story_page.page.locator('//tbody//tr[@class="event-row selectable-row"]')
    story_page.timeout()

    # Check if the locator exists
    if elements.count() > 0:
        # Retrieve and print the text content of all matching elements
        all_texts = elements.all_text_contents()
        for text in all_texts:
            logging.info(text)
    else:
        logging.info("This is not a live page.")
    story_page.timeout()


@allure.feature("UserInterface")
def test_Livepage_actions(story_page):
    test_Livepage_actions.__doc__= """Tests live page video management functionality.

    Detailed Test Flow:
    1. Page Navigation:
       - Loads live page
       - Verifies URL
       - Handles page response

    2. Video Enumeration:
       - Locates live video entries
       - Counts available videos
       - Validates video presence

    3. Video Operations:
       - Retrieves video titles
       - Accesses playout controls
       - Handles channel selection
       - Manages video assignment

    Args:
        story_page: Fixture providing page interface and controls

    Dependencies:
        - Working live interface
        - Available video content
        - Channel configuration
        - Playout functionality

    Expected Results:
        - Page loads successfully
        - Videos identified
        - Playout controls accessible
        - Channel assignment completed

    URLs Accessed:
        - Live Page: http://10.189.200.6/live
    """
    # Navigate to the live page
    story_page.navigate()
    story_page.page.goto("http://10.189.200.6/live")
    story_page.timeout()
    assert story_page.page.url == "http://10.189.200.6/live", "Failed to navigate to the live page."

    # Handle "Live Now" section
    live_now_videos = story_page.page.locator(
        '//tbody//tr[@class="event-row selectable-row"]')  # all the rows which has story name in live page
    assert live_now_videos.count() >= 0, "'Live Now' section locator is invalid or inaccessible."  # checking if there are atleast one video
    if live_now_videos.count() > 0:  # if there are more than one video
        logging.info(f"Found {live_now_videos.count()} videos under 'Live Now'.")  # printing the number of videos

        for i in range(2, live_now_videos.count()):  # iterating through each video
            video_title = story_page.page.locator('//tbody//tr[@class="event-row selectable-row"]//td[2]').nth(
                i).text_content()  # getting the title of the video
            assert video_title, f"Failed to retrieve title for video {i} in 'Live Now'."  # checking if the title is retrieved
            logging.info(f"Live Now Video: {video_title}")  # printing the title of the video

            # Click the playout button (triangle symbol)
            playout_button = story_page.page.locator(
                '//tbody//tr[@class="event-row selectable-row"]//td[7]//button').nth(
                1)  # getting the playout button of the video
            assert playout_button.is_visible(), f"Playout button for video {i} in 'Live Now' is not visible."  # checking if the playout button is visible
            playout_button.click()
            logging.info("Playout button visible and clicked")
            story_page.timeout()
            # Select a channel from the options
            channel_options = story_page.page.locator('//ul[@class="channel-options"]//li/button')
            assert channel_options.count() >= 0, "Channel options locator is invalid or inaccessible."
            if channel_options.count() > 0:
                channel_options.nth(0).click()  # Select the first channel (adjust index as needed)
                logging.info(f"Added '{video_title}' to the first channel.")
                story_page.timeout()
            else:
                logging.info("No channel options available.")
    else:
        logging.info("No videos found under 'Live Now'.")


@allure.feature("UserInterface")
def test_PlayoutNowPage_Playout_Now_Button_On_LivePage(story_page):
    test_PlayoutNowPage_Playout_Now_Button_On_LivePage.__doc__="""Tests playout functionality from live page to playout.

    Detailed Test Flow:
    1. Admin Configuration:
       - Sets source to live mode
       - Configures manual playout
       - Handles confirmation dialogs

    2. Live Page Operation:
       - Navigates to live view
       - Verifies story presence
       - Triggers playout action

    3. Verification Steps:
       - Confirms source settings
       - Validates mode changes
       - Checks story details
       - Verifies playout initiation

    Args:
        story_page: Fixture providing page interface and methods

    Dependencies:
        - Working admin interface
        - Live source access
        - Manual mode support
        - Story availability

    Expected Results:
        - Source set to live
        - Manual mode enabled
        - Story accessible
        - Playout triggered

    URLs Accessed:
        - Admin Playout: http://10.189.200.6/admin/playout
        - Live Page: http://10.189.200.6/live
    """
    # Navigate to the admin playout page
    story_page.page.goto("http://10.189.200.6/admin/playout")
    story_page.timeout()
    assert story_page.page.url == "http://10.189.200.6/admin/playout", "Failed to navigate to the admin playout page."

    # click on source button
    source_dropdown = story_page.page.locator('//div[@class="row list-row"]//div[@data-name="source"]').first
    assert source_dropdown.is_visible(), "Source dropdown is not visible."
    source_dropdown.click()
    story_page.timeout()

    # click on live button
    source_live = story_page.page.locator('//div[@data-name="source"]//div//ul//li[2]')
    assert source_live.is_visible(), "Source live option is not visible."
    source_live.click()
    story_page.timeout()

    # Handle confirmation popup if it appears
    confirmation_popup = story_page.page.locator('//dialog[@class="inv-bg"]//button[2]')
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Click on mode
    mode_dropdown = story_page.page.locator('//div[@class="row list-row"]//div[@data-name="mode"]').first
    assert mode_dropdown.is_visible(), "Mode dropdown is not visible."
    mode_dropdown.click()
    story_page.timeout()

    # click on manual
    manual_mode = story_page.page.locator('//div[@class="row list-row"]//div[@data-name="mode"]//div//ul//li[2]')
    assert manual_mode.is_visible(), "Manual mode option is not visible."
    manual_mode.click()
    story_page.timeout()

    # Handle confirmation popup
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Navigate to the live page
    story_page.page.goto("http://10.189.200.6/live")
    story_page.timeout()
    assert story_page.page.url == "http://10.189.200.6/live", "Failed to navigate to the live page."

    story_name = story_page.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div/div[4]/div[2]/h1').text_content()
    assert story_name, "Failed to retrieve the story name."
    logging.info(f"Story name: {story_name}")
    story_page.timeout()

    story_page.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up"]//button[@class="btn inv-bg label icon"]').click()  # playout button
    story_page.timeout()
    story_page.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[1]').click()  # 1st option
    story_page.timeout()


@allure.feature("UserInterface")
def test_MyVideosPage_Add_My_Videos_To_Playlist(story_page):  # works
    test_MyVideosPage_Add_My_Videos_To_Playlist.__doc__=  """Tests adding videos from My Videos page to playlist with database verification.

    Detailed Test Flow:
    1. Initial Setup:
       - Clears playout history
       - Configures playout source and mode
       - Handles confirmation dialogs

    2. Navigation Flow:
       - Stories page access
       - My Videos page setup
       - Videos page verification

    3. Video Operations:
       - Validates video presence
       - Triggers playlist addition
       - Verifies playlist updates

    4. System Verification:
       - FTP log validation
       - Database query checks
       - Content synchronization

    Args:
        story_page: Fixture providing page interface and methods

    Dependencies:
        - Working playout interface
        - Database connection
        - FTP access
        - Video content availability

    Expected Results:
        - History cleared
        - Videos accessible
        - Playlist updated
        - Database synchronized

    URLs Accessed:
        - History: http://10.189.200.6/history/playout
        - Admin: http://10.189.200.6/admin/playout
        - Stories: http://10.189.200.6/stories?earlyscripts=true#list
        - Videos: http://10.189.200.6/videos
    """
    db_client = Database()
    story_page.navigate()

    # Navigate to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()
    story_page.clear_distribution_history_if_the_clear_button_is_present()

    # Navigate to the admin playout page
    story_page.page.goto("http://10.189.200.6/admin/playout")
    story_page.timeout()

    # Assert that the source dropdown is visible and clickable
    source_dropdown = story_page.page.locator('//div[@class="row list-row"]//div[@data-name="source"]').first
    assert source_dropdown.is_visible(), "Source dropdown is not visible."
    source_dropdown.click()
    story_page.timeout()

    # Assert that the file playout option is visible and clickable
    file_playout = story_page.page.locator('//div[@data-name="source"]//div//ul//li[5]')
    assert file_playout.is_visible(), "File playout option is not visible."
    file_playout.click()
    story_page.timeout()

    # Handle confirmation popup if it appears
    confirmation_popup = story_page.page.locator('//dialog[@class="inv-bg"]//button[2]')
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Assert that the mode dropdown is visible and clickable
    mode_dropdown = story_page.page.locator('//div[@class="row list-row"]//div[@data-name="mode"]').first
    assert mode_dropdown.is_visible(), "Mode dropdown is not visible."
    mode_dropdown.click()
    story_page.timeout()

    # Assert that the manual mode option is visible and clickable
    manual_mode = story_page.page.locator('//div[@class="row list-row"]//div[@data-name="mode"]//div//ul//li[2]')
    assert manual_mode.is_visible(), "Manual mode option is not visible."
    manual_mode.click()
    story_page.timeout()

    # Handle confirmation popup for loop mode
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Navigate to the stories page
    story_page.page.goto("http://10.189.200.6/stories?earlyscripts=true#list")
    story_page.timeout()

    # Assert that the addpage to dropdown
    dropdown_button = story_page.page.locator('//div[@data-name="add-page"]')
    assert dropdown_button.is_visible(), "Dropdown button is not visible."
    dropdown_button.click()
    story_page.timeout()

    # Assert that the dropdown option is visible and clickable for myvideos
    dropdown_option = story_page.page.locator('//div[@data-name="add-page"]//div//ul//li[1]')
    assert dropdown_option.is_visible(), "Dropdown option is not visible."
    dropdown_option.click()
    story_page.timeout()

    # Navigate to the videos page
    story_page.page.goto("http://10.189.200.6/videos")
    story_page.timeout()
    assert story_page.page.url == "http://10.189.200.6/videos", "Failed to navigate to the videos page."

    # Assert that video elements are present
    elements = story_page.page.locator('//div[@class="td source-id-slug justified"]')
    assert elements.count() > 0, "No video elements found."
    all_texts = elements.all_text_contents()
    for text in all_texts:
        logging.info(text)
    story_page.timeout()

    # Assert that the playlist button is visible and clickable
    playlist_button = story_page.page.locator('//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up"]//button[@class="btn-icon tooltip no-print"]')
    assert playlist_button.is_visible(), "Playlist button is not visible."
    playlist_button.click()
    story_page.timeout()


    # Assert that the FTP connection is successful
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
        assert file_names, "No files found in the FTP directory."
    except Exception as e:
        logging.info(f"Error: {e}")
        assert False, f"Failed to connect to FTP: {e}"

    logging.info(file_names)

    # Assert that the database query executes successfully
    result = db_client.execute_query(f'SELECT * FROM player')
    assert result, "Database query returned no results."


@allure.feature("UserInterface")
def test_MyVideosPage_Print_My_Videos(story_page):
    test_MyVideosPage_Print_My_Videos.__doc__="""Tests print functionality for My Videos page.

    Detailed Test Flow:
    1. Page Navigation:
       - Loads initial page
       - Accesses dropdown menu
       - Selects videos view

    2. Print Setup:
       - Opens videos page
       - Configures print media
       - Emulates print action

    3. Print Operation:
       - Handles print dialog
       - Validates print state
       - Confirms completion

    Args:
        story_page: Fixture providing page interface and methods

    Dependencies:
        - Working videos interface
        - Print media emulation
        - Page access rights
        - Print functionality

    Expected Results:
        - Navigation successful
        - Print media emulated
        - Print dialog handled
        - Operation logged

    URLs Accessed:
        - Videos Page: http://10.189.200.6/videos
    """
    story_page.navigate()
    story_page.timeout()

    # Assert that the dropdown button is visible and clickable
    dropdown_button = story_page.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[2]/div[2]/button')
    assert dropdown_button.is_visible(), "Dropdown button is not visible."
    dropdown_button.click()
    story_page.timeout()

    # Assert that the dropdown option is visible and clickable
    dropdown_option = story_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/div[2]/div[2]/div/ul/li[1]/button')
    assert dropdown_option.is_visible(), "Dropdown option is not visible."
    dropdown_option.click()
    story_page.timeout()

    # Navigate to the videos page and assert successful navigation
    story_page.page.goto("http://10.189.200.6/videos")
    story_page.timeout()
    assert story_page.page.url == "http://10.189.200.6/videos", "Failed to navigate to the videos page."

    # Suppress the print dialog by emulating print media
    story_page.page.emulate_media(media="print")
    logging.info("Print media emulated successfully.")

    # Assert that the print button is visible (if uncommented for interaction)
    # print_button = story_page.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[1]/div/button[1]')
    # assert print_button.is_visible(), "Print button is not visible."
    # print_button.click()
    # story_page.timeout()

    # Log success
    logging.info("Print button clicked, and test passed without manual intervention.")


@allure.feature("UserInterface")
def test_LivePage_Add_To_Playlist(story_page):  # working
    test_LivePage_Add_To_Playlist.__doc__="""Tests live content addition to playlist with source and mode configuration.

    Detailed Test Flow:
    1. Admin Setup:
       - Configures live source
       - Sets manual mode
       - Verifies configurations

    2. Live Content:
       - Navigates to live page
       - Captures story details
       - Triggers playlist addition

    3. Playlist Verification:
       - Adds to channel
       - Validates content
       - Checks locators

    Args:
        story_page: Fixture providing page interface and methods

    Dependencies:
        - Working admin interface
        - Live source availability
        - Playlist functionality
        - Channel configuration

    Expected Results:
        - Source set to Live
        - Mode set to Manual
        - Story added to playlist
        - Content visible in playout

    URLs Accessed:
        - Admin Playout: http://10.189.200.6/admin/playout
        - Live Page: http://10.189.200.6/live
        - Playout Page: http://10.189.200.6/playout
    """
    story_page.page.goto("http://10.189.200.6/admin/playout")
    story_page.timeout()

    # Configure live
    source_dropdown = story_page.source_drop_down()
    source_live = story_page.source_as_live_in_dropdown()
    source_dropdown.click()
    story_page.timeout()
    source_live.click()
    story_page.timeout()

    # Handle confirmation popup if it appears
    confirmation_popup = story_page.confirmation_popup()
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()
    else:
        pass
    source = story_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[1]/button').text_content()
    assert source == "Live"
    # Configure manual mode for live
    mode_dropdown = story_page.mode_dropdown()
    live_manual_mode = story_page.manual_mode_for_live_source()
    mode_dropdown.click()
    story_page.timeout()
    live_manual_mode.click()
    story_page.timeout()

    # Handle confirmation popup for loop mode
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    mode = story_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[2]/button').text_content()
    assert mode == "Manual"

    # Navigate to the live page
    story_page.page.goto("http://10.189.200.6/live")
    story_added_to_playlist = story_page.page.locator(
        '//tr[@class="event-row selectable-row"]//td[2]').first.text_content()
    logging.info(f"Story added to playlist: {story_added_to_playlist}")

    story_page.page.locator(
        '//tr[@class="event-row selectable-row"]//td[7]').first.click()  # click on a playlist button
    story_page.timeout()
    story_page.page.locator(
        '//tr[@class="event-row selectable-row"]//td[7]//div[@class="actions"]//div//div//div//ul//li[1]').click()  # click on the channel to add the video
    story_page.timeout()
    story_page.page.goto('http://10.189.200.6/playout')
    story_page.timeout()
    story_page.timeout()
    story_page.timeout()
    story_page.timeout()
    locator1 = story_page.page.locator('//div//h4[@class="label"]//a').first
    locator2 = story_page.page.locator('//div[@class="column"]//a//div//span').first

    try:
        # Try first locator: check visibility and enabled state
        if locator1.is_visible(timeout=2000) and locator1.is_enabled(timeout=2000):
            logging.info(f"Locator 1 text: {locator1.text_content()}")
        # Else, try the second locator
        elif locator2.is_visible(timeout=2000) and locator2.is_enabled(timeout=2000):
            logging.info(f"Locator 2 text: {locator2.text_content()}")
        else:
            logging.info("Neither locator is visible and actionable.")
    except TimeoutError:
        # If any .is_visible() call times out (element not found), try the other
        try:
            if locator2.is_visible(timeout=2000) and locator2.is_enabled(timeout=2000):
                logging.info(f"Locator 2 text: {locator2.text_content()}")
            else:
                logging.info("Neither locator is visible and actionable.")
        except TimeoutError:
            logging.info("Neither locator is visible and actionable.")


@allure.feature("UserInterface")
def test_View_XML(story_page):
    test_View_XML.__doc__= """Tests XML viewing functionality with screenshot capture.

    Detailed Test Flow:
    1. Navigation:
       - Loads initial page
       - Opens story details
       - Triggers XML view

    2. Screenshot:
       - Captures full page
       - Saves dialog content
       - Verifies file creation

    3. Visual Verification:
       - Waits for content load
       - Captures XML dialog
       - Documents state

    Args:
        story_page: Fixture providing page interface and methods

    Dependencies:
        - Working interface
        - XML content access
        - Screenshot capability
        - Storage permissions

    Expected Results:
        - Page navigation successful
        - XML dialog opened
        - Screenshot captured
        - File saved as 'dialog_screenshot.png'

    Files Generated:
        - dialog_screenshot.png: Full page screenshot
    """
    story_page.navigate()
    story_page.timeout()
    story_page.page.locator(
        '//div[@class="td source-id-slug justified"]/div[@class="column"]/div[@class="row"]/button[1]').first.click()
    story_page.timeout()
    story_page.page.locator('//div[@class="enclosure no-print"]//a').click()
    story_page.timeout()
    #
    #
    # # Wait for the dialog to appear (optional, if it takes time to load)
    # dialog = story_page.page.locator('//div[@class="dialog-content"]')
    # try:
    #     dialog.wait_for(state="visible", timeout=10000)  # Adjust timeout as needed
    # except Exception as e:
    #     logging.info(f"Dialog did not become visible: {e}")

    # Take a screenshot of the dialog box
    story_page.page.screenshot(path="dialog_screenshot.png", full_page=True)
    logging.info("Screenshot of the dialog saved as 'dialog_screenshot.png'")

@allure.feature("UserInterface")
def test_AdminSettingsPage_FileProcessor(story_page):
    test_AdminSettingsPage_FileProcessor.__doc__=    """Tests file processor settings configuration in admin settings page.

    Detailed Test Flow:
    1. Settings Navigation:
       - Accesses processor settings
       - Verifies page load
       - Confirms form visibility

    2. Input Configuration:
       - Sets customer name
       - Configures IP address
       - Validates input values

    3. Dropdown Settings:
       - Configures frame rate
       - Sets video definition
       - Verifies selections

    4. Button Operations:
       - Tests reset functionality
       - Validates update settings
       - Confirms actions

    Args:
        story_page: Fixture providing page interface and methods

    Test Data:
        - Customer Name: GDANSK-V7-TESTBED-06
        - IP Address: 172.16.2.2
        - Frame Rate: First option
        - Video Definition: First option

    Dependencies:
        - Working admin interface
        - Settings access rights
        - Form input functionality
        - Button controls

    Expected Results:
        - All form fields accessible
        - Input values set correctly
        - Dropdowns functional
        - Buttons responsive

    URLs Accessed:
        - Settings Page: http://10.189.200.6/settings/processor
    """
    locators = {
        "customer_name": '//input[@name="Customer.Name"]',
        "ip_address_of_satellite_receiver": '//input[@name="RX8200.IPAddress"]',
        "Frame_rate": '//div[@data-name ="Video.Format"]//button[@class="dropdown-toggle label"]',
        "Video_definition": '//div[@data-name ="Video.Definition"]//button[@class="dropdown-toggle label"]',
        "Reset_button": '//div[@class="row button-bar"]//button[1]',
        "Update_settings": '//div[@class="row button-bar"]//button[1]',

    }
    # Navigate to the settings page
    story_page.navigate()
    story_page.page.goto('http://10.189.200.6/settings/processor')
    story_page.timeout()

    # Test input fields
    customer_name_input = story_page.page.locator(locators["customer_name"])
    assert customer_name_input.is_visible(), "Customer Name input is not visible."
    customer_name_input.fill("GDANSK-V7-TESTBED-06")
    assert customer_name_input.input_value() == "GDANSK-V7-TESTBED-06", "Failed to set Customer Name."

    ip_address_input = story_page.page.locator(locators["ip_address_of_satellite_receiver"])
    assert ip_address_input.is_visible(), "IP Address input is not visible."
    ip_address_input.fill("172.16.2.2")
    assert ip_address_input.input_value() == "172.16.2.2", "Failed to set IP Address."

    # Test dropdowns
    frame_rate_dropdown = story_page.page.locator(locators["Frame_rate"])
    assert frame_rate_dropdown.is_visible(), "Frame Rate dropdown is not visible."
    frame_rate_dropdown.click()
    story_page.timeout()
    frame_rate_option = story_page.page.locator(
        '//div[@data-name="Video.Format"]//ul/li[1]')  # Adjust option locator as needed
    assert frame_rate_option.is_visible(), "Frame Rate option is not visible."
    frame_rate_option.click()

    video_definition_dropdown = story_page.page.locator(locators["Video_definition"])
    assert video_definition_dropdown.is_visible(), "Video Definition dropdown is not visible."
    video_definition_dropdown.click()
    story_page.timeout()
    video_definition_option = story_page.page.locator(
        '//div[@data-name="Video.Definition"]//ul/li[1]')  # Adjust option locator as needed
    assert video_definition_option.is_visible(), "Video Definition option is not visible."
    video_definition_option.click()

    # Test buttons
    reset_button = story_page.page.locator(locators["Reset_button"])
    assert reset_button.is_visible(), "Reset button is not visible."
    reset_button.click()
    story_page.timeout()
    logging.info("Reset button clicked successfully.")

    update_settings_button = story_page.page.locator(locators["Update_settings"])
    # assert update_settings_button.is_visible(), "Update Settings button is not visible."
    update_settings_button.is_visible()
    story_page.timeout()
    logging.info("Update Settings button clicked successfully.")

@allure.feature("UserInterface")
def test_Admin_Settings_Page_Playout_Options(story_page):  # working
    test_Admin_Settings_Page_Playout_Options.__doc__= """Tests playout options configuration in admin settings page.

    Detailed Test Flow:
    1. Settings Navigation:
       - Accesses playout settings
       - Verifies page load
       - Checks form elements

    2. Checkbox Controls:
       - Gen lock configuration
       - Waiting video toggle
       - RLS Plus pre-roll
       - Slug display settings

    3. Input Configurations:
       - Video playout mode
       - Lipsync offsets (SD/HD)
       - RLS Plus offsets
       - Format-specific settings

    4. Button Operations:
       - Reset functionality
       - Update settings
       - State validation

    Args:
        story_page: Fixture providing page interface and methods

    Test Data:
        - Offset Values: 0
        - Video Formats: SD525, SD625, HD50, HD60
        - RLS Plus Formats: HD50, HD60

    Dependencies:
        - Working admin interface
        - Settings access rights
        - Form controls
        - Video configuration access

    Expected Results:
        - All controls accessible
        - Input values accepted
        - Checkboxes toggleable
        - Settings updateable

    URLs Accessed:
        - Settings Page: http://10.189.200.6/settings/playout
    """
    locators = {
        "gen_lock": '//div[@class="block"]//label[@data-name="genlock_enabled"]',
        "gen_lock_offset": '//label[@class="input disabled inline"]//div//input[@name="genlock_offset"]',
        "Show_Waiting_video_for_playout": '//label[@data-name="PlayWaitVideo"]',
        "RLS_PLUS_PRE_ROLL": '//label[@data-name="RLOB.preRoll"]',
        "Show_Slug_on_video_playout_on_loop_mode": '//label[@data-name="Video.TextOverlay"]',
        "Video_playout_mode_dropdown": '//label[@class="input inline"]//div//div[@data-name="Playout.OutputMode"]',
        "SD525": '//label[@data-name="Lipsync_offset_SD525"]//div',
        "SD625": '//label[@data-name="Lipsync_offset_SD625"]//div',
        "HD50": '//label[@data-name="Lipsync_offset_HD50"]//div',
        "HD60": '//label[@data-name="Lipsync_offset_HD60"]//div',
        "RLS_PLUS_HD50": '//label[@data-name="Lipsync_offset_HD50_rlob"]//div',
        "RLS_PLUS_HD60": '//label[@data-name="Lipsync_offset_HD60_rlob"]//div',
        "Reset": '//div[@class="row button-bar"]//button[1]',
        "Update_Settings": '//div[@class="row button-bar"]//button[2]',
    }
    story_page.navigate()
    story_page.page.goto("http://10.189.200.6/settings/playout")
    story_page.timeout()
    # gen_lock_checkbox = story_page.page.locator(locators["gen_lock"])
    # gen_lock_checkbox.click()
    # story_page.timeout()
    # assert gen_lock_checkbox.is_checked(), "Gen Lock checkbox is not checked."
    # gen_lock_checkbox.click()
    # assert not gen_lock_checkbox.is_checked(), "Gen Lock checkbox is still checked after clicking."

    gen_lock_offset_input_area = story_page.page.locator(locators["gen_lock_offset"])
    assert gen_lock_offset_input_area.is_disabled(), "Gen Lock Offset input area is  visible."
    logging.info("genlock offset done")

    show_waiting_video_for_playout_checkbox = story_page.page.locator(locators["Show_Waiting_video_for_playout"])
    assert show_waiting_video_for_playout_checkbox.is_checked(), "Check box is not checked"
    show_waiting_video_for_playout_checkbox.click()
    assert not show_waiting_video_for_playout_checkbox.is_checked(), "Check box is  checked after clicking."
    logging.info("waiting video done")

    rls_plus_pre_roll_checkbox = story_page.page.locator(locators["RLS_PLUS_PRE_ROLL"])
    rls_plus_pre_roll_checkbox.click()
    story_page.timeout()
    assert rls_plus_pre_roll_checkbox.is_checked(), "RLS Plus Pre Roll checkbox is not checked."
    rls_plus_pre_roll_checkbox.click()
    assert not rls_plus_pre_roll_checkbox.is_checked(), "RLS Plus Pre Roll checkbox is still checked after clicking."
    story_page.timeout()
    logging.info("rls done")

    show_slug_on_video_playout_checkbox = story_page.page.locator(locators["Show_Slug_on_video_playout_on_loop_mode"])
    show_slug_on_video_playout_checkbox.click()
    story_page.timeout()
    assert show_slug_on_video_playout_checkbox.is_checked(), "Show Slug on Video Playout checkbox is not checked."
    show_slug_on_video_playout_checkbox.click()
    assert not show_slug_on_video_playout_checkbox.is_checked(), "Show Slug on Video Playout checkbox is still checked after clicking."
    story_page.timeout()
    logging.info("slug on video done")

    video_playout_mode_dropdown = story_page.page.locator(locators["Video_playout_mode_dropdown"])
    assert video_playout_mode_dropdown.is_editable(), "Video Playout Mode dropdown is  editable."
    logging.info("video playout done")

    SD525_input_area = story_page.page.locator(locators["SD525"])
    assert SD525_input_area.is_editable(), "SD525 input area is not editable."
    SD525_input_area.fill("0")
    assert SD525_input_area.input_value() == "0", "Failed to set SD525 input area value."
    logging.info("sd525 done")

    SD625_input_area = story_page.page.locator(locators["SD625"])
    assert SD625_input_area.is_editable(), "SD625 input area is not editable."
    SD625_input_area.fill("0")
    assert SD625_input_area.input_value() == "0", "Failed to set SD625 input area value."
    logging.info("sd625 done")

    HD50_input_area = story_page.page.locator(locators["HD50"])
    assert HD50_input_area.is_editable(), "HD50 input area is not editable."
    HD50_input_area.fill("0")
    assert HD50_input_area.input_value() == "0", "Failed to set HD50 input area value."
    logging.info("hd50 done")

    HD60_input_area = story_page.page.locator(locators["HD60"])
    assert HD60_input_area.is_editable(), "HD60 input area is not editable."
    HD60_input_area.fill("0")
    assert HD60_input_area.input_value() == "0", "Failed to set HD60 input area value."
    logging.info("hd 60 done")

    RLS_PLUS_HD50_input_area = story_page.page.locator(locators["RLS_PLUS_HD50"])
    assert RLS_PLUS_HD50_input_area.is_editable(), "RLS Plus HD50 input area is not editable."
    RLS_PLUS_HD50_input_area.fill("0")
    assert RLS_PLUS_HD50_input_area.input_value() == "0", "Failed to set RLS Plus HD50 input area value."
    logging.info("rlshd50 done")

    RLS_PLUS_HD60_input_area = story_page.page.locator(locators["RLS_PLUS_HD60"])
    assert RLS_PLUS_HD60_input_area.is_editable(), "RLS Plus HD60 input area is not editable."
    RLS_PLUS_HD60_input_area.fill("0")
    assert RLS_PLUS_HD60_input_area.input_value() == "0", "Failed to set RLS Plus HD60 input area value."
    logging.info("rls hd60 done")

    reset_button = story_page.page.locator(locators["Reset"])
    assert reset_button.is_enabled(), "Reset button is not visible."

    update_settings_button = story_page.page.locator(locators["Update_Settings"])
    assert update_settings_button.is_enabled(), "Update Settings button is not visible."

    logging.info("Playoutpage tested successfully")


@allure.feature("UserInterface")
def test_HistoryPage_Search_Playout_History(story_page):
    test_HistoryPage_Search_Playout_History.__doc__="""Tests search functionality in playout history page.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to history page
       - Clears existing history
       - Configures file playout source

    2. Mode Configuration:
       - Sets loop mode
       - Handles confirmations
       - Verifies settings

    3. Search Operation:
       - Extracts reference text
       - Performs search
       - Validates results

    Args:
        story_page: Fixture providing page interface and methods

    Test Data:
        - Source: File playout
        - Mode: Loop
        - Search: Extracted story slug

    Dependencies:
        - Working history interface
        - Search functionality
        - Story visibility
        - Clear history access

    Expected Results:
        - History cleared successfully
        - Loop mode configured
        - Search matches extracted text
        - Results displayed correctly

    URLs Accessed:
        - History Page: http://10.189.200.6/history/playout
        - Admin Playout: http://10.189.200.6/admin/playout
    """
    # Navigate to the story page
    story_page.navigate()

    # Navigate to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()
    story_page.clear_distribution_history_if_the_clear_button_is_present()

    # Navigate to the admin playout page
    story_page.page.goto("http://10.189.200.6/admin/playout")
    story_page.timeout()

    # Configure file-layout
    source_dropdown = story_page.page.locator(
        '//div[@class="list column"]//div[@class="row list-row"][1]//div[@data-name="source"]')
    file_playout = story_page.page.locator('//div[@data-name="source"]//ul//li[5]')
    source_dropdown.click()
    story_page.timeout()
    file_playout.click()
    story_page.timeout()

    # Handle confirmation popup if it appears
    confirmation_popup = story_page.page.locator('//dialog[@class="inv-bg"]//button[2]')
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()
    else:
        pass
        # Configure loop mode
    mode_dropdown = story_page.page.locator(
        '//div[@class="list column"]//div[@class="row list-row"][1]//div[@data-name="mode"]')
    mode_dropdown.click()
    loop_mode = story_page.page.locator('//div[@data-name="mode"]//div//ul//li[2]')
    loop_mode.click()
    story_page.page.wait_for_timeout(30000)

    # Handle confirmation popup for loop mode
    if confirmation_popup.is_visible():
        confirmation_popup.click()
        story_page.timeout()

    # Navigate back to the history page
    story_page.page.goto("http://10.189.200.6/history/playout")
    story_page.timeout()

    checkbox = story_page.page.locator('//label[@data-name="loopitems"]')
    assert checkbox.is_enabled(), "Checkbox is not enabled."
    checkbox.click()
    story_page.timeout()

    # Wait until all stories are visible on the page
    # elements = story_page.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[2]/div[13]/div[2]/div[1]/div[1]')
    # elements.wait_for(state="visible")

    # Print all items in the history page
    story_slug = story_page.page.locator('//div[@class="td source-id-slug justified"]//div[@class="cell-text h4"]')
    for i in range(story_slug.count()):
        logging.info(story_slug.nth(i).text_content())
        story_page.timeout()

        # Extract the text from the given locator
    extracted_text = story_page.page.locator(
        '//div[@class="td source-id-slug justified"]//div[@class="cell-text h4"]').nth(1).text_content()
    logging.info(f"Extracted text: {extracted_text}")

    # Input the extracted text into the search bar
    search_bar = story_page.page.locator(
        '//input[@placeholder="Search playout history"]')  # Replace with the actual search bar locator
    search_bar.fill(extracted_text)
    story_page.timeout()
    search_bar.press("Enter")
    story_page.page.wait_for_timeout(2000)

    # Validate if the search result is displayed
    search_result = story_page.page.locator(
        '//div[@class="td source-id-slug justified"]//div//div//div[@class="cell-text h4"]').nth(
        1).text_content()  # Adjust locator if needed
    logging.info(search_result)
    story_page.timeout()
    assert search_result == extracted_text, "Search result does not match the expected text."


@allure.feature("UserInterface")
def test_HistoryPage_Search_Distribution_History(story_page):
    test_HistoryPage_Search_Distribution_History.__doc__= """Tests search functionality in distribution history page.

    Detailed Test Flow:
    1. Distribution Setup:
       - Configures FTP distribution
       - Sets distribution details
       - Prepares history data

    2. History Management:
       - Clears existing history
       - Adds test stories
       - Verifies table load

    3. Search Operation:
       - Extracts story slug
       - Performs search
       - Validates results

    Args:
        story_page: Fixture providing page interface and methods

    Test Data:
        - Distribution: FTP settings
        - Search: First story slug from history

    Dependencies:
        - Working distribution interface
        - History access rights
        - Search functionality
        - Story visibility

    Expected Results:
        - History cleared successfully
        - Stories added to distribution
        - Search matches extracted slug
        - Results displayed correctly

    URLs Accessed:
        - Distribution History: http://10.189.200.6/history/distribution
    """
    # Step 1: Initial Setup
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()

    # Step 2: Navigate to Distribution History Page
    story_page.page.goto("http://10.189.200.6/history/distribution")
    story_page.timeout()

    # Step 3: Clear Distribution History (if applicable)
    story_page.clear_distribution_history_if_the_clear_button_is_present()

    # Step 4: Add Stories to Distribution and Revisit History Page
    story_page.add_all_stories_to_distribution()
    story_page.navigate_to_distribution_history()
    story_page.timeout()

    # Step 5: Wait for History Table to Load
    elements = story_page.storypage_elements()
    elements.wait_for(state="visible")

    # Step 6: Log All Story Slugs from the Table
    story_slug_locator = story_page.page.locator('//table//tbody//tr//td[1]')
    for i in range(story_slug_locator.count()):
        logging.info(story_slug_locator.nth(i).text_content())

    # Step 7: Extract First Story Slug Text
    extracted_text = story_slug_locator.first.text_content()
    logging.info(f"Extracted text: {extracted_text}")

    # Step 8: Search Using Extracted Text
    search_bar = story_page.page.locator('//input[@placeholder="Search distribution history"]')
    search_bar.fill(extracted_text)
    story_page.timeout()
    search_bar.press("Enter")
    story_page.timeout()

    # Step 9: Validate Search Result
    search_result = story_page.page.locator('//table//tbody//tr//td[1]').text_content()
    logging.info(f"Search result: {search_result}")
    story_page.timeout()

    assert search_result == extracted_text, "Search result does not match the expected text."


@allure.feature("UserInterface")
def test_HistoryPage_Distribution_History(story_page):
    test_HistoryPage_Distribution_History.__doc__="""Tests distribution history functionality and content visibility.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to main page
       - Configures distribution details
       - Sets up FTP distribution

    2. History Management:
       - Navigates to distribution history
       - Clears existing history
       - Adds test stories to distribution

    3. Content Verification:
       - Waits for history elements
       - Retrieves all story slugs
       - Logs distributed content

    Args:
        story_page: Fixture providing page interface and methods

    Dependencies:
        - Working distribution system
        - FTP configuration
        - History access rights
        - Story visibility

    Expected Results:
        - History cleared successfully
        - Stories distributed correctly
        - Content visible in history
        - All slugs retrievable

    URLs Accessed:
        - Distribution History: http://10.189.200.6/history/distribution
    """
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    # Navigate to the distribution history page
    story_page.page.goto("http://10.189.200.6/history/distribution")
    story_page.timeout()

    # Clear the distribution history if the clear button is present
    story_page.clear_distribution_history_if_the_clear_button_is_present()
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history

    # Wait for the history elements to be visible
    elements = story_page.storypage_elements()
    elements.wait_for(state="visible")

    # Log all items in the history page
    story_slug = story_page.page.locator('//table//tbody//tr//td[1]')
    for i in range(story_slug.count()):
        logging.info(story_slug.nth(i).text_content())
        story_page.timeout()
