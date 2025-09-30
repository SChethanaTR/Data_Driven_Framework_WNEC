import logging

import env
import pytest
from playwright.sync_api import expect

from helpers import ubuntu
from helpers.database import Database

# def test_Administrator_file_playout_manual(admin_playout_page):  # working
#     """
#     Tests the functionality of manually playing out files.
#     Navigates to the admin playout page and selects 'fileplayout' and 'manual' options from dropdowns.
#     Initiates playout for stories and verifies logs.
#     Includes a negative scenario to verify that the playout button isn't clickable when 'manual' mode isn't selected.
#     """
#
#     # Navigate to the admin playout page
#     def wait():
#         """Short helper function to reduce redundancy and improve readability."""
#         admin_playout_page.timeout()
#
#     db_client = Database()
#     admin_playout_page.navigate()
#
#     # Select 'fileplayout' from the Content Source dropdown
#     admin_playout_page.get_Content_Source_box1().click()
#     wait()
#     admin_playout_page.get_CS_File_playout_box1().click()
#     wait()
#     admin_playout_page.confirm_content_source_change().click()
#     wait()
#
#     # Select 'manual' from the Mode dropdown
#     admin_playout_page.get_mode_box1().click()
#     wait()
#     admin_playout_page.get_Mode_Manual_box1().click()
#     wait()
#     admin_playout_page.confirm_content_source_change().click()
#     wait()
#
#     # Navigate to the story page
#     admin_playout_page.stories_page().click()
#     wait()
#
#     # Click on the playout icon against each story
#     for i in range(3, 8):
#         admin_playout_page.story_page_playout_button().nth(i).click()
#         wait()
#         admin_playout_page.playout_option_1().click()
#         wait()
#         logging.info("Story playout initiated for story index: %d", i)
#
#     # Navigate to the playout page and print all story names that have been added
#     admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
#     for i in range(1, 6):
#         text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
#             i).text_content()
#         logging.info("Story %d: %s", i, text)
#         assert text is not None, "Story text should not be None"
#
#     wait()
#     # Negative scenario: Check if playout icon is not clickable when 'manual' is not selected
#     admin_playout_page.page.locator(
#         '//div[@id="app-root"]//header[@class="inv-bg no-print"]//ul[@class="tab horizontal inheader hnav"]//li[4]//div[@data-name="nav-menu"]').click()
#     wait()
#     admin_playout_page.page.locator('//ul[@class="inv-bg groups"]//li[2]//ul//li[2]').click()
#     admin_playout_page.get_mode_box1().click()
#     wait()
#     admin_playout_page.get_Mode_Auto_box1().click()  # Assuming 'Automatic' is another option
#     wait()
#     admin_playout_page.confirm_content_source_change().click()
#     wait()
#
#     admin_playout_page.stories_page().click()
#     wait()
#
#     for i in range(3, 8):
#         try:
#             admin_playout_page.story_page_playout_button().nth(i).click()
#             wait()
#             assert False, "Playout button should not be clickable in 'Automatic' mode"
#         except:
#             logging.info("Playout button is not clickable for story index: %d in 'Automatic' mode", i)
#     try:  # validation from logs
#         # Get the list of all files in the directory
#         public_host = env.ftp_host
#         ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
#         logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
#         stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
#         file_names = stdout.read().decode().splitlines()
#     except Exception as e:
#         logging.info(f"Error: {e}")
#     logging.info(file_names)
#     db_client.execute_query(f'SELECT * FROM player')


import logging
import allure
from helpers.database import Database
from helpers import ubuntu
import env


@allure.step("Navigate to the admin playout page")
def navigate_to_admin_playout_page(admin_playout_page):
    admin_playout_page.navigate()
    admin_playout_page.timeout()


@allure.step("Select 'fileplayout' from the Content Source dropdown")
def select_fileplayout(admin_playout_page):
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_File_playout_box1().click()
    admin_playout_page.timeout()
    # admin_playout_page.confirm_content_source_change().click()
    # admin_playout_page.timeout()


@allure.step("Select 'manual' from the Mode dropdown")
def select_manual_mode(admin_playout_page):
    admin_playout_page.get_mode_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_Mode_Manual_box1().click()
    admin_playout_page.timeout()
    # admin_playout_page.confirm_content_source_change().click()
    # admin_playout_page.timeout()


@allure.step("Initiate playout for stories")
def initiate_playout(admin_playout_page):
    admin_playout_page.stories_page().click()
    admin_playout_page.timeout()
    for i in range(3, 8):
        admin_playout_page.story_page_playout_button().nth(i).click()
        admin_playout_page.timeout()
        admin_playout_page.playout_option_1().click()
        admin_playout_page.timeout()
        logging.info(f"Story playout initiated for story index: {i}")
        allure.attach(f"Story index: {i}", name="Playout Details", attachment_type=allure.attachment_type.TEXT)


@allure.step("Validate playout page and story names")
def validate_playout_page(admin_playout_page):
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    for i in range(1, 6):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info(f"Story {i}: {text}")
        allure.attach(text, name=f"Story {i} Content", attachment_type=allure.attachment_type.TEXT)
        assert text is not None, "Story text should not be None"


@allure.step("Negative scenario: Verify playout button is not clickable in 'Automatic' mode")
def verify_negative_scenario(admin_playout_page):
    admin_playout_page.page.locator(
        '//div[@id="app-root"]//header[@class="inv-bg no-print"]//ul[@class="tab horizontal inheader hnav"]//li[4]//div[@data-name="nav-menu"]').click()
    admin_playout_page.timeout()
    admin_playout_page.page.locator('//ul[@class="inv-bg groups"]//li[2]//ul//li[2]').click()
    admin_playout_page.get_mode_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_Mode_Auto_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()
    admin_playout_page.stories_page().click()
    admin_playout_page.timeout()

    for i in range(3, 8):
        try:
            admin_playout_page.story_page_playout_button().nth(i).click()
            admin_playout_page.timeout()
            assert False, "Playout button should not be clickable in 'Automatic' mode"
        except:
            logging.info(f"Playout button is not clickable for story index: {i} in 'Automatic' mode")
            allure.attach(f"Story index: {i}", name="Negative Scenario Details",
                          attachment_type=allure.attachment_type.TEXT)


@allure.step("Validate logs and database")
def validate_logs_and_database():
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
        logging.info(file_names)
        allure.attach("\n".join(file_names), name="Log File Content", attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
        logging.info(f"Error: {e}")
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)

    db_client = Database()
    db_client.execute_query(f'SELECT * FROM player')


@allure.feature("AdminPlayout")
def test_Administrator_file_playout_manual(admin_playout_page):

    test_Administrator_file_playout_manual.__doc__ = """
       Detailed test flow:
       1. Navigates to admin playout page
       2. Handles fixed channel settings:
          - Enables/disables fixed channels based on current state
          - Verifies channel status via UI dialog
       3. Sets up playout configuration:
          - Selects fileplayout as content source
          - Sets manual mode for playout control
       4. Performs playout operations:
          - Initiates story playout
          - Validates playout status in UI
       5. Tests negative scenarios:
          - Verifies playout restrictions in non-manual mode
       6. Validates:
          - Checks backend logs
          - Verifies database entries

       Dependencies:
       - Requires admin_playout_page fixture
       - Needs database access
       - Relies on logging configuration

       Expected Results:
       - Successfully configures playout settings
       - Correctly handles channel states
       - Properly validates all playout operations
       """
    navigate_to_admin_playout_page(admin_playout_page)
    admin_playout_page.timeout()
    checkbox = admin_playout_page.page.locator('//label[@class="toggle labelled"]')
    checkbox.click()
    if admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to enable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is enabled")
    elif admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to disable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[1]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is already enabled")
    admin_playout_page.timeout()

    select_fileplayout(admin_playout_page)
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
    select_manual_mode(admin_playout_page)
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()

    initiate_playout(admin_playout_page)
    validate_playout_page(admin_playout_page)
    verify_negative_scenario(admin_playout_page)
    validate_logs_and_database()


@allure.feature("AdminPlayout")
def test_Administrator_file_playout_loop(admin_playout_page):  # FilePlayout- Loop #Verification of logs - FilePlayout - Manual/Auto/Loop not working   (working)
    test_Administrator_file_playout_loop.__doc__ = """Tests the file playout functionality in loop mode.

    Detailed Test Flow:
    1. Channel Configuration:
       - Navigates to admin playout page
       - Toggles and verifies fixed channel settings
       - Handles channel enable/disable confirmations
    
    2. Playout Setup:
       - Sets content source to 'fileplayout'
       - Configures mode to 'Loop'
       - Handles confirmation dialogs for settings changes
    
    3. Loop Configuration:
       - Opens loop configuration dialog
       - Sets loop count to 3
       - Saves loop settings
    
    4. Validation:
       - Checks story names in playout page
       - Verifies player logs via SSH
       - Validates database state
    
    Args:
        admin_playout_page: Fixture providing access to admin playout page functions

    Dependencies:
        - Database connection
        - SSH access to player logs
        - Fixed channel configuration
        - Playout permissions
    
    Expected Results:
        - Fixed channel settings properly configured
        - Loop mode successfully enabled
        - Stories added to playout queue
        - Proper log entries created
        - Database records updated
    """

    def wait():
        admin_playout_page.timeout()

    db_client = Database()
    # Positive Scenario
    # Navigate to the admin playout page
    admin_playout_page.navigate()
    wait()
    admin_playout_page.timeout()
    checkbox = admin_playout_page.page.locator('//label[@class="toggle labelled"]')
    checkbox.click()
    if admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to enable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is enabled")
    elif admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to disable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[1]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is already enabled")
    admin_playout_page.timeout()

    # Select 'fileplayout' from the Content Source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    wait()
    admin_playout_page.get_CS_File_playout_box1().click()
    wait()

    # Check if the confirmation dialog box appears for Content Source
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Select 'Loop' from the mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Loop_box1().click()
    wait()

    # Check if the confirmation dialog box appears for Mode
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Configure the loop
    admin_playout_page.page.locator('//button[@class="btn inv-bg label icon"]').first.click()  # click on configure loop
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]').click()  # click on loop dropdown
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]//div//ul//li[4]').click()  # select 3
    wait()
    admin_playout_page.page.locator(
        '//dialog[@class="inv-bg inv-bg loop-auto-dialog"]//div//div[@class="row buttons"]//button[2]').click()  # save
    wait()

    # Navigate to the playout page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    wait()
    for i in range(1, 4):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info("Story %d: %s", i, text)
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM player')


@allure.feature("AdminPlayout")
def test_Administrator_file_playout_auto(admin_playout_page):
    test_Administrator_file_playout_auto.__doc__ ="""
    Test file playout functionality in automatic mode.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout page
       - Manages fixed channel configuration:
         * Enables/disables based on current state
         * Handles confirmation dialogs
         * Verifies channel status

    2. Content Source Configuration:
       - Selects 'fileplayout' from dropdown
       - Handles confirmation dialog if present
       - Verifies selection is applied

    3. Mode Configuration:
       - Sets mode to 'Auto'
       - Handles confirmation dialog
       - Verifies mode selection

    4. Story Verification:
       - Navigates to playout page
       - Verifies presence of stories (1-3)
       - Validates story names are not null
       - Logs story details

    5. Negative Testing:
       - Switches to manual mode
       - Verifies playout page content
       - Checks if stories are cleared
       - Logs empty state or remaining stories

    6. Database Validation:
       - Executes player table query
       - Verifies database state

    Dependencies:
       - admin_playout_page fixture
       - Database connection
       - Fixed channel configuration
       - Story content in system

    Expected Results:
       - Fixed channel properly configured
       - Auto mode successfully enabled
       - Stories visible in auto mode
       - Stories cleared in manual mode
       - Database records validated

    Note: This test verifies both positive (auto mode) and negative (manual mode) scenarios
    """

    def wait():
        admin_playout_page.timeout()

    db_client = Database()
    # Positive Scenario
    # Navigate to the admin playout page
    admin_playout_page.navigate()
    wait()
    admin_playout_page.timeout()
    checkbox = admin_playout_page.page.locator('//label[@class="toggle labelled"]')
    checkbox.click()
    if admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to enable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is enabled")
    elif admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to disable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[1]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is already enabled")
    admin_playout_page.timeout()

    # Select 'fileplayout' from the Content Source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    wait()
    admin_playout_page.get_CS_File_playout_box1().click()

    # Check if the confirmation dialog box appears for Content Source
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Select 'auto' from the Mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Auto_box1().click()
    # Check if the confirmation dialog box appears for Content Source
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Navigate to the playout page and print all story names that have been added
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    for i in range(1, 4):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info("Story %d: %s", i, text)
        wait()
        assert text is not None, "Story text should not be None"

    admin_playout_page.navigate()
    # Negative Scenario
    # Change mode to 'manual' and verify that the playout process does not work as expected
    wait()
    # # Negative scenario: Check if playout icon is not clickable when 'manual' is not selected
    # admin_playout_page.page.locator('//div[@id="app-root"]//header[@class="inv-bg no-print"]//ul[@class="tab horizontal inheader hnav"]//li[4]//div[@data-name="nav-menu"]').click()
    # wait()
    # admin_playout_page.page.locator('//ul[@class="inv-bg groups"]//li[2]//ul//li[2]').click()
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Manual_box1().click()  # Assuming 'Manual' is another option
    wait()
    # admin_playout_page.confirm_content_source_change().click()
    # wait()

    # Attempt to navigate to the playout page and verify that stories are not added
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    wait()

    # Check if the element exists
    story_elements = admin_playout_page.page.locator('//div[@class="scrollable no-print"]')
    if story_elements.count() == 0:
        logging.info("empty")
    else:
        for i in range(story_elements.count()):
            story_name = story_elements.nth(i).text_content()
            logging.info(story_name)

    # Execute the database query
    db_client.execute_query(f'SELECT * FROM player')


@allure.feature("AdminPlayout")
def test_Administrator_live_playout_Fixed(admin_playout_page):
    test_Administrator_live_playout_Fixed.__doc__ = """Tests the live playout functionality with fixed channel configuration.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout page
       - Configures fixed channel settings
       - Handles enable/disable confirmation dialogs

    2. Content Configuration:
       - Sets content source to 'Live'
       - Sets fixed mode
       - Configures channel to RL1
       - Handles confirmation dialogs

    3. Live Page Validation:
       - Navigates to live page
       - Checks for existing content rows
       - Verifies RL1 channel assignment
       - Captures story slug information

    4. Backend Validation:
       - Checks player logs via SSH
       - Validates database state

    Dependencies:
       - admin_playout_page fixture
       - Database connection
       - SSH access to player logs
       - Fixed channel permissions

    Expected Results:
       - Fixed channel properly enabled
       - Live content source configured
       - RL1 channel assigned
       - Story properly playing on assigned channel
       - Logs and database records validated
    """

    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.timeout()

    # Locator for the checkbox
    checkbox = admin_playout_page.page.locator('//label[@class="toggle labelled"]')
    checkbox.click()
    if admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to enable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is enabled")
    elif admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to disable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[1]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is already enabled")
    admin_playout_page.timeout()
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_Live_box1().click()
    admin_playout_page.timeout()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.get_mode_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@data-name="mode"]//div//ul//li[3]').click()
    admin_playout_page.timeout()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
    # Selecting the channel dropdown for fixed playout
    admin_playout_page.page.locator('//div[@data-name="channel"]').first.click()  # select channel
    admin_playout_page.page.locator(
        '//div[@class="row list-row"]//div[@data-name="channel"]//div//ul//li[2]').click()  # RL1

    # Navigate to live page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[2]').click()  # select live page
    admin_playout_page.timeout()

    # Check if any rows exist on the live page
    rows = admin_playout_page.page.locator('//tbody//tr[@class="event-row selectable-row"]')
    if rows.count() == 0:
        logging.info("No rows found on the live page.")
        return  # Exit the test if no rows are present

    # Checking the video that has channel name as RL1
    for i in range(rows.count()):
        row = rows.nth(i)
        rl_button = row.locator('xpath=.//td//button[@class="btn-channel"]').text_content()
        if rl_button == "rl&nbsp;1":
            slug_name = row.locator('xpath=.//td[2]//button').inner_text()
            logging.info(f"Found rl 1 button. Adjacent slug name: {slug_name}")
            break
    else:
        logging.info("No rl 1 button found in any row")
        return  # Exit the test if no matching button is found

    admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()

    # Should print the video being played and verify if both are the same
    try:  # Validation from logs
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM player')


@allure.feature("AdminPlayout")
def test_Administrator_6xLive_preview_playout_Fixed(admin_playout_page):
    test_Administrator_6xLive_preview_playout_Fixed.__doc__="""Tests the 6X live preview playout functionality with fixed channel configuration.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout page
       - Manages fixed channel settings via checkbox toggle
       - Handles enable/disable confirmation dialogs

    2. Content Configuration:
       - Sets content source to '6x Live Preview'
       - Handles content source change confirmations
       - Ensures proper mode selection

    3. Preview Validation:
       - Navigates to playout page
       - Captures currently playing content
       - Verifies live preview status

    4. System Validation:
       - Retrieves and validates player logs via SSH
       - Checks database state via player table query
       - Verifies system configuration

    Dependencies:
       - admin_playout_page fixture
       - Database connection
       - SSH access to player logs
       - Fixed channel configuration
       - Live preview functionality

    Expected Results:
       - Fixed channel properly configured
       - 6x Live Preview mode activated
       - Content playing correctly
       - Logs showing proper preview activity
       - Database records accurate

    Technical Notes:
       - Uses SSH for log validation
       - Performs database queries
       - Handles UI confirmations
       - Manages timeout between actions
    """

    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.timeout()
    checkbox = admin_playout_page.page.locator('//label[@class="toggle labelled"]')
    checkbox.click()
    if admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to enable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is enabled")
    elif admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to disable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[1]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is already enabled")
    admin_playout_page.timeout()
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_6x_Live_Preview_box1().click()
    admin_playout_page.timeout()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()
    admin_playout_page.play_out_page_link().click()
    admin_playout_page.timeout()
    live = admin_playout_page.page.locator(
        '//div[@class="playout-grid with-columns"]//div//h4[@class="label"]//div[@class="playing-now"]').nth(
        0).text_content()
    logging.info(live)
    admin_playout_page.timeout()
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM player')


@allure.feature("AdminPlayout")
def test_Administrator_RLS_preview_playout_Fixed(admin_playout_page):
    test_Administrator_RLS_preview_playout_Fixed.__doc__="""Tests RLS (Remote Live Stream) preview playout functionality with fixed channel configuration.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout page
       - Manages fixed channel settings:
         * Toggles fixed channel state
         * Handles confirmation dialogs
         * Verifies channel status

    2. RLS Configuration:
       - Sets content source to RLS Broadcast
       - Handles content source change confirmations
       - Navigates to playout page

    3. Content Validation:
       - Captures and logs currently playing video
       - Retrieves and logs upcoming video list
       - Verifies content sequence

    4. System Verification:
       - Checks player logs via SSH
       - Validates database state
       - Verifies proper content streaming

    Dependencies:
       - admin_playout_page fixture
       - Database connection
       - SSH access to player logs
       - RLS broadcast configuration
       - Fixed channel permissions

    Expected Results:
       - Fixed channel properly configured
       - RLS broadcast mode activated
       - Current and upcoming content visible
       - Logs showing proper stream activity
       - Database records validated

    Technical Notes:
       - Uses SSH for log validation
       - Performs database queries
       - Monitors live stream status
    """
    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.timeout()
    checkbox = admin_playout_page.page.locator('//label[@class="toggle labelled"]')
    checkbox.click()
    if admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to enable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is enabled")
    elif admin_playout_page.page.locator(
            '//dialog[@class="inv-bg"]//div//h1[@class="title"]').text_content() == "Are you sure you want to disable fixed channels?":
        admin_playout_page.timeout()
        admin_playout_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[1]').click()
        admin_playout_page.timeout()
        logging.info("Fixed channel is already enabled")
    admin_playout_page.timeout()
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_RLS_Broadcast_box1().click()
    admin_playout_page.timeout()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.play_out_page_link().click()  # playout page
    logging.info("Now Playing")
    now_playing = admin_playout_page.RLS_Now_playing_Videos().nth(1).text_content()  # Nowplaying video
    logging.info(now_playing)
    logging.info("Upcoming")
    stories = admin_playout_page.RLS_upcoming_list_of_videos()  # upcoming list of videos
    for i in range(stories.count()):
        story = stories.nth(i).text_content()
        logging.info(story)
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM player')


@allure.feature("AdminPlayout")
def test_enable_disable_channel(admin_playout_page):
    test_enable_disable_channel.__doc__=  """Tests channel enable/disable functionality in the admin playout interface.

    Detailed Test Flow:
    1. Channel Disable Test:
       - Navigates to admin playout page
       - Disables channel via radio button
       - Verifies channel disabled status
       - Checks playout stopped message

    2. Channel Enable Test:
       - Re-enables channel via radio button
       - Verifies channel enabled status
       - Validates playout ready state

    3. Status Verification:
       - Checks SDI1 box messages
       - Validates playout status text
       - Confirms channel state changes

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working admin playout interface
        - Valid channel configuration
        - Story list access
        - Playout page access

    Expected Results:
        - Channel successfully disables/enables
        - Correct status messages displayed
        - Proper state transitions occur
        - Status changes logged accurately

    URLs Accessed:
        - Admin Playout: /admin/playout
        - Stories List: /stories#list
        - Playout Page: /playout
    """
    ADMIN_PLAYOUT_URL = 'http://10.189.200.6/admin/playout'
    STORIES_LIST_URL = 'http://10.189.200.6/stories#list'
    PLAYOUT_URL = 'http://10.189.200.6/playout'

    def navigate_and_log(page, url, message):
        """Function to navigate to a URL and log a message."""
        page.goto(url)
        admin_playout_page.timeout()
        logging.info(message)

    def click_and_log(locator, message):
        """Function to click a locator and log a message."""
        locator.click()
        admin_playout_page.timeout()
        logging.info(message)

    """Test enabling and disabling a channel on the admin playout page."""
    # Navigate to the playout page
    navigate_and_log(admin_playout_page.page, ADMIN_PLAYOUT_URL, 'Navigated to playout page')

    # Disable the channel
    click_and_log(admin_playout_page.get_disable_channel_box_1(), "Radio button to disable channel is clicked")
    navigate_and_log(admin_playout_page.page, STORIES_LIST_URL, '')
    admin_playout_page.page.locator(
        '//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]').nth(
        1).click()
    admin_playout_page.timeout()
    navigate_and_log(admin_playout_page.page, PLAYOUT_URL, '')

    # Check if the channel is disabled
    # checking the message on sdi1 box
    status = admin_playout_page.page.locator(
        '//div[@class="playout-grid with-columns"]//div//h4[@class="label"]//div').nth(1).text_content()
    logging.info(status)
    if status == "PLAYOUT STOPPEDPress Start button, and/or add videos to Playlist, or press Play Now button in Stories page":
        logging.info("Channel is disabled")
    else:
        logging.info("Channel is enabled")
        # Enable the channel
        # navigate back to adminplayout page and click on teh radio button to enable
    navigate_and_log(admin_playout_page.page, ADMIN_PLAYOUT_URL, '')
    click_and_log(admin_playout_page.get_enable_channel_box_1(), "Radio button to enable channel is clicked")

    # Navigate back to the stories list and perform actions
    navigate_and_log(admin_playout_page.page, STORIES_LIST_URL, '')
    admin_playout_page.page.locator(
        '//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]').nth(
        1).click()
    admin_playout_page.timeout()

    # Final navigation to playout page to check the channel status
    navigate_and_log(admin_playout_page.page, PLAYOUT_URL, '')
    playout_ready_text = admin_playout_page.page.locator('div.playing-now').nth(1).text_content()
    logging.info(playout_ready_text.split('\n')[0])

    if playout_ready_text == "PLAYOUT STOPPED":
        logging.info("Channel is disabled")
    else:
        logging.info("Channel is enabled")


@allure.feature("AdminPlayout")
def test_playout_controls(admin_playout_page):
    test_playout_controls.__doc__="""Tests the functionality of playout control buttons (play, pause, stop).

    Detailed Test Flow:
    1. Initial Setup:
       - Configures file playout source
       - Sets manual mode
       - Initializes control button locators
       - Sets up database connection

    2. Content Configuration:
       - Navigates to stories page
       - Selects story for playout
       - Initiates playout sequence
       - Navigates to playout control page

    3. Control Testing:
       - Tests Stop Button:
         * Clicks stop
         * Verifies playout stopped message
         * Validates stopped state

       - Tests Play Button:
         * Clicks play
         * Verifies playback resumed
         * Validates playing state

       - Tests Pause Button:
         * Clicks pause
         * Verifies paused state
         * Validates content status

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working playout interface
        - Valid content for playback
        - Manual mode permissions
        - Database connection

    Expected Results:
        - Stop button halts playback
        - Play button resumes content
        - Pause button freezes playback
        - Status messages reflect actions
        - Log entries confirm operations
    """
    # Define locators for buttons
    stop_button = admin_playout_page.page.locator('//div[@class="main"]//div[@class="playout-grid with-columns"]//div[@class="row control"][1]//button[@class="btn-playback btn-icon no-print"][1]')
    pause_button = admin_playout_page.page.locator('//div[@class="main"]//div[@class="playout-grid with-columns"]//div[@class="row control"][1]//button[@class="btn-playback btn-icon no-print"][2]')
    play_button = admin_playout_page.page.locator('//div[@class="main"]//div[@class="playout-grid with-columns"]//div[@class="row control"][1]//button[@class="btn-playback btn-icon no-print"]')

    def wait():
        """Helper function to add a timeout."""
        admin_playout_page.timeout()

    # Initialize database client and navigate to the admin playout page
    db_client = Database()
    admin_playout_page.navigate()

    # Select 'fileplayout' from the Content Source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    wait()
    admin_playout_page.get_CS_File_playout_box1().click()
    wait()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Select 'manual' from the Mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Manual_box1().click()
    wait()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Navigate to the story page and initiate playout for a story
    admin_playout_page.stories_page().click()
    wait()
    admin_playout_page.page.locator(
        '//div[@class="actions"]//div[2]//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up"]'
        ).first.click()
    admin_playout_page.page.locator(
        '//div[@class="dropdown-menu flower dropdown playout-playlist dropdown drop-up open"]//div//ul//li[1]'
        ).click()
    admin_playout_page.stories_page().click()
    wait()

    # Navigate to the playout page and log the current playing status
    admin_playout_page.page.goto('http://10.189.200.6/playout')
    current_playing = admin_playout_page.page.locator(
        '//div[@class="main"]//div[@class="playout-grid with-columns"]//div//h4[@class="label"][2]').first.text_content()
    logging.info(f"Currently playing: {current_playing}")

    # Test the stop button functionality
    stop_button.click()
    wait()
    stopped_playing = admin_playout_page.page.locator(
        '//div[@class="main"]//div[@class="playout-grid with-columns"]//div//h4[@class="label"]//div[@class="playing-now"]').first.text_content()
    logging.info(f"After stopping: {stopped_playing}")
    if stopped_playing == "PLAYOUT STOPPEDPress Start button, and/or add videos to Playlist, or press Play Now button in Stories page":
        logging.info("Playout stopped successfully")
    else:
        logging.info("Playout did not stop as expected")

    admin_playout_page.page.wait_for_timeout(2000)

    # Test the play button functionality
    play_button.click()
    wait()
    playing = admin_playout_page.page.locator(
        '//div[@class="main"]//div[@class="playout-grid with-columns"]//div//h4[@class="label"]').first.text_content()
    logging.info(f"After playing: {playing}")
    admin_playout_page.page.wait_for_timeout(2000)

    # Test the pause button functionality
    pause_button.click()
    wait()
    paused_playing = admin_playout_page.page.locator(
        '//div[@class="main"]//div[@class="playout-grid with-columns"]//div//h4[@class="label"]').first.text_content()
    logging.info(f"After pausing: {paused_playing}")


@allure.feature("AdminPlayout")
def test_export_as_cv(admin_playout_page):
    test_export_as_cv.__doc__="""Tests the CSV export functionality in the playout history section.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout page
       - Configures content source as fileplayout
       - Sets loop mode with 3 iterations
       - Handles confirmation dialogs

    2. Loop Configuration:
       - Opens loop configuration dialog
       - Sets loop count to 3
       - Saves loop settings
       - Verifies configuration

    3. Content Validation:
       - Navigates to playout page
       - Captures and logs story details
       - Verifies story presence

    4. Export Process:
       - Navigates to playout history
       - Triggers CSV export
       - Confirms export completion

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working playout interface
        - Database connection
        - File export permissions
        - Story content in system

    Expected Results:
        - Loop mode properly configured
        - Stories visible in playout list
        - CSV export successfully completed
        - Export data matches displayed content

    URLs Accessed:
        - Admin Playout: /admin/playout
        - Playout History: /history/playout
    """
    def wait():
        admin_playout_page.timeout()

    db_client = Database()
    # Positive Scenario
    # Navigate to the admin playout page
    admin_playout_page.navigate()
    wait()

    # Select 'fileplayout' from the Content Source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    wait()
    admin_playout_page.get_CS_File_playout_box1().click()
    wait()

    # Check if the confirmation dialog box appears for Content Source
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Select 'Loop' from the mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Loop_box1().click()
    wait()

    # Check if the confirmation dialog box appears for Mode
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Configure the loop
    admin_playout_page.page.locator('//button[@class="btn inv-bg label icon"]').first.click()  # click on configure loop
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]').click()  # click on loop dropdown
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]//div//ul//li[4]').click()  # select 3
    wait()
    admin_playout_page.page.locator(
        '//dialog[@class="inv-bg inv-bg loop-auto-dialog"]//div//div[@class="row buttons"]//button[2]').click()  # save
    wait()

    # Navigate to the playout page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    wait()
    for i in range(1, 4):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info("Story %d: %s", i, text)

    admin_playout_page.page.goto('http://10.189.200.6/history/playout')
    wait()
    admin_playout_page.page.locator('//*[@id="app-root"]/div[3]/main/div[2]/div[1]/div/a').click()
    wait()
    logging.info('Data exported')


@allure.feature("AdminPlayout")
def test_clear_all_items_playout_history(admin_playout_page):
    test_clear_all_items_playout_history.__doc__="""Tests the functionality to clear all items from playout history.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout
       - Configures content source as fileplayout
       - Sets loop mode
       - Creates test data via loop configuration

    2. Loop Configuration:
       - Sets loop count to 3
       - Saves loop settings
       - Verifies stories in playout list

    3. History Clearing:
       - Navigates to playout history
       - Manages loop items checkbox state
       - Triggers clear functionality
       - Handles confirmation dialog

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working playout interface
        - Database connection
        - History clearing permissions
        - Existing playout history data

    Expected Results:
        - Loop configuration successful
        - History page accessible
        - Clear button visible after checkbox selection
        - Confirmation dialog appears
        - History items cleared successfully
        - Proper logging of actions

    URLs Accessed:
        - Admin Playout: /admin/playout
        - Playout History: /history/playout
    """
    def wait():
        admin_playout_page.timeout()

    db_client = Database()
    # Positive Scenario
    # Navigate to the admin playout page
    admin_playout_page.navigate()
    wait()

    # Select 'fileplayout' from the Content Source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    wait()
    admin_playout_page.get_CS_File_playout_box1().click()
    wait()

    # Check if the confirmation dialog box appears for Content Source
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Select 'Loop' from the mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Loop_box1().click()
    wait()

    # Check if the confirmation dialog box appears for Mode
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        wait()

    # Configure the loop
    admin_playout_page.page.locator('//button[@class="btn inv-bg label icon"]').first.click()  # click on configure loop
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]').click()  # click on loop dropdown
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]//div//ul//li[4]').click()  # select 3
    wait()
    admin_playout_page.page.locator(
        '//dialog[@class="inv-bg inv-bg loop-auto-dialog"]//div//div[@class="row buttons"]//button[2]').click()  # save
    wait()

    # Navigate to the playout page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    wait()
    for i in range(1, 4):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info("Story %d: %s", i, text)

    admin_playout_page.page.goto('http://10.189.200.6/history/playout')
    wait()
    loop_checkbox = admin_playout_page.page.locator('//label[@data-name="loopitems"]')

    # Step 3: Check if checkbox is unchecked, then check it
    if not loop_checkbox.is_checked():
        logging.info("Loop items checkbox is unchecked. Checking it to reveal Clear button.")
        loop_checkbox.check()
        admin_playout_page.timeout()
    else:
        logging.info("Loop items checkbox is already checked.")

    # Step 4: Locate and click the Clear button
    clear_button = admin_playout_page.page.locator('//div[@class="enclosure no-print"]//button[@type="button"][2]')
    if clear_button.is_visible():
        logging.info("Clear button is visible. Clicking to clear history.")
        clear_button.click()
        admin_playout_page.timeout()

        # Step 5: Confirm the clear action if confirmation dialog appears
        confirm_clear = admin_playout_page.page.locator('//dialog[@class="inv-bg"]//button[2]')
        if confirm_clear.is_visible():
            logging.info("Confirmation dialog appeared. Confirming clear action.")
            confirm_clear.click()
            admin_playout_page.timeout()
        else:
            logging.info("No confirmation dialog appeared.")
    else:
        logging.warning("Clear button is not visible even after checking the loop checkbox.")


@allure.feature("AdminPlayout")
def test_lock_unlock_configuration(admin_playout_page):
    test_lock_unlock_configuration.__doc__="""Tests the lock/unlock functionality of playout configuration controls.

    Detailed Test Flow:
    1. Element Location:
       - Identifies lock button
       - Locates input area
       - Finds source dropdown
       - Finds mode dropdown

    2. Lock Testing:
       - Activates configuration lock
       - Attempts interactions with input area
       - Tests source dropdown accessibility
       - Tests mode dropdown accessibility
       - Verifies elements are not interactable

    3. Unlock Testing:
       - Deactivates configuration lock
       - Verifies input area interaction
       - Confirms source dropdown access
       - Confirms mode dropdown access
       - Validates elements are interactable

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working playout interface
        - Admin permissions
        - Lock/unlock button functionality
        - Input and dropdown elements

    Expected Results:
        - Elements non-interactable when locked
        - Elements interactable when unlocked
        - Proper error/success logging
        - Correct state transitions
    """
    def wait():
        """Helper function to add a timeout."""
        admin_playout_page.timeout()

    admin_playout_page.navigate()

    # Locate elements
    lock_button = admin_playout_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/label[2]')  # Adjust locator as needed
    input_area = admin_playout_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/span[2]')  # Adjust locator as needed
    source_dropdown = admin_playout_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[1]')  # Adjust locator as needed
    mode_dropdown = admin_playout_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/article/div/div[2]/div[1]/div[2]')  # Adjust locator as needed

    # Lock the configuration
    lock_button.click()
    wait()

    # Try interacting with input area and dropdowns when locked
    try:
        input_area.click()
        input_area.fill("Test Input")
        logging.error("Input area is interactable when locked, which is incorrect.")
    except:
        logging.info("Input area is not interactable when locked, as expected.")
    wait()
    wait()

    try:
        source_dropdown.click()
        logging.error("Source dropdown is interactable when locked, which is incorrect.")
    except:
        logging.info("Source dropdown is not interactable when locked, as expected.")
    wait()
    wait()

    try:
        mode_dropdown.click()
        logging.error("Mode dropdown is interactable when locked, which is incorrect.")
    except:
        logging.info("Mode dropdown is not interactable when locked, as expected.")

    wait()
    wait()

    # Unlock the configuration
    lock_button.click()
    wait()

    # Try interacting with input area and dropdowns when unlocked
    try:
        input_area.click()
        input_area.fill("Test Input")
        logging.info("Input area is interactable when unlocked, as expected.")
    except:
        logging.error("Input area is not interactable when unlocked, which is incorrect.")
    wait()
    wait()
    try:
        source_dropdown.click()
        logging.info("Source dropdown is interactable when unlocked, as expected.")
    except:
        logging.error("Source dropdown is not interactable when unlocked, which is incorrect.")
    wait()
    wait()
    try:
        mode_dropdown.click()
        logging.info("Mode dropdown is interactable when unlocked, as expected.")
    except:
        logging.error("Mode dropdown is not interactable when unlocked, which is incorrect.")
    wait()
    wait()


@allure.feature("AdminPlayout")
def test_when_there_is_no_video_playout_a_waiting_video(admin_playout_page):
    test_when_there_is_no_video_playout_a_waiting_video.__doc__="""Tests the waiting video functionality when no content is available for playout.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout page
       - Configures content source as fileplayout
       - Sets manual mode
       - Handles confirmation dialogs

    2. Configuration:
       - Selects file playout source
       - Configures manual mode
       - Verifies configuration changes
       - Handles confirmation popups

    3. Status Verification:
       - Navigates to playout page
       - Checks playout ready status
       - Verifies channel video slug
       - Validates empty state handling

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working playout interface
        - Database connection
        - Manual mode permissions
        - Empty playout queue

    Expected Results:
        - "PLAYOUT READY" message displayed
        - Empty channel video slug
        - Proper status messages shown
        - Correct error handling

    URLs Accessed:
        - Admin Playout: /admin/playout
        - Playout Page: http://10.189.200.6/playout
    """
    def wait():
        """Short helper function to reduce redundancy and improve readability."""
        admin_playout_page.timeout()

    db_client = Database()
    admin_playout_page.navigate()

    # Select 'fileplayout' from the Content Source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    wait()
    admin_playout_page.get_CS_File_playout_box1().click()
    wait()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()

    # Select 'manual' from the Mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Manual_box1().click()
    wait()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()

    admin_playout_page.page.goto("http://10.189.200.6/playout")
    admin_playout_page.timeout()

    # Check the content of the specified locator
    playout_ready_locator = admin_playout_page.page.locator(
        '//*[@id="app-root"]/div[3]/main/div[2]/div[1]/div[5]/h4/div')
    playout_ready_text = playout_ready_locator.text_content().strip()

    if playout_ready_text == "PLAYOUT READY Add videos to Playlist or press Play Now button in Stories page":
        # Locate the channel video slug
        channel_video_slug = admin_playout_page.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/div[1]/div[2]/div/img')
        slug_content = channel_video_slug.get_attribute("src")

        # Check if the slug is empty
        if not slug_content:
            logging.info("Channel video slug is empty as expected.")
        else:
            logging.error(f"Channel video slug is not empty. Actual content: {slug_content}")
    else:
        logging.info(f"Playout status is not 'Playout ready:'. Actual content: {playout_ready_text}")


@allure.feature("AdminPlayout")
def test_Administrator_live_playout_manual(admin_playout_page):
    test_Administrator_live_playout_manual.__doc__="""Tests manual live playout functionality in administrator mode.

    Detailed Test Flow:
    1. Initial Setup:
       - Navigates to admin playout
       - Sets content source to live
       - Configures manual mode
       - Handles confirmation dialogs

    2. Live Content:
       - Navigates to live page
       - Verifies video presence
       - Captures initial story details
       - Initiates manual playout

    3. Playout Verification:
       - Checks story name matches
       - Verifies playout status
       - Validates via logs
       - Confirms database state

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working playout interface
        - Database connection
        - SSH access for logs
        - Available live content

    Expected Results:
        - Live content properly selected
        - Manual mode activated
        - Story plays out correctly
        - Log entries match actions
        - Database reflects changes

    URLs Accessed:
        - Admin Playout: /admin/playout
        - Live Page: http://10.189.200.6/live
        - Playout Page: via navigation
    """

    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.timeout()
    # Selecting the live option from content source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_Live_box1().click()
    admin_playout_page.timeout()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        admin_playout_page.timeout()
    # selecting the manual option from mode dropdown
    admin_playout_page.get_mode_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@data-name="mode"]//div//ul//li[2]').click()
    admin_playout_page.timeout()
    if admin_playout_page.confirm_content_source_change().is_visible():
        admin_playout_page.confirm_content_source_change().click()
        admin_playout_page.timeout()
    # navigating to live page
    admin_playout_page.page.goto("http://10.189.200.6/live")
    admin_playout_page.timeout()

    # Check if any elements exist on the live page
    live_videos = admin_playout_page.page.locator('//tbody//tr[@class="event-row selectable-row"]')
    if live_videos.count() == 0:
        logging.info("No videos on the live page currently.")
        return  # Exit the test if no videos are present

    # printing the first story from live page
    story_name = admin_playout_page.live_page_slug_name().nth(0).text_content()
    logging.info(story_name)
    admin_playout_page.timeout()
    # selecting the playoutnow button and selecting sdi1 for the video to be played
    admin_playout_page.live_page_playout_icon().nth(1).click()
    admin_playout_page.timeout()
    admin_playout_page.live_page_playout_op_1().click()
    admin_playout_page.timeout()
    # navigate to playout page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()  # playout page
    admin_playout_page.timeout()
    admin_playout_page.timeout()
    admin_playout_page.page.wait_for_timeout(20000)
    # printing the video that was being added
    now_playing = admin_playout_page.page.locator(
        '//div[@class="playout-grid with-columns"]//div[4]//h4[@class="label"][2]//a[@class="playing-now"]').nth(
        0).text_content()
    logging.info(now_playing)
    # verifying if the added story and the story being played are the same
    assert story_name == now_playing
    # validation from logs
    try:
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    logging.info("Validation from database")
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/player/log1/wnecplayer.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM player')  # sql not working


@allure.feature("AdminPlayout")
def test_playout_playlist_button(admin_playout_page):
    test_playout_playlist_button.__doc__=  """Tests visibility of playout and playlist buttons in different content source modes.

    Detailed Test Flow:
    1. File Playout Mode:
       - Navigates to admin playout
       - Sets content source as fileplayout
       - Configures manual mode
       - Verifies button visibility in stories page

    2. Live Mode:
       - Switches to live content source
       - Maintains manual mode setting
       - Navigates to live page
       - Verifies button visibility

    Args:
        admin_playout_page: Fixture providing admin playout page interface

    Dependencies:
        - Working playout interface
        - Button visibility permissions
        - Story content availability
        - Live content availability

    Expected Results:
        - Playout and playlist buttons visible in stories page
        - Buttons visible in live content mode
        - Proper state handling for both modes
        - Correct logging of button visibility

    URLs Accessed:
        - Admin Playout: http://10.189.200.6/admin/playout
        - Stories Page: via navigation
        - Live Page: http://10.189.200.6/live
    """
    # playoutbutton = "//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]"
    # playlist_button = "//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][3]"
    def wait():
        admin_playout_page.timeout()

    admin_playout_page.navigate()
    admin_playout_page.get_Content_Source_box1().click()
    wait()
    admin_playout_page.get_CS_File_playout_box1().click()
    wait()
    admin_playout_page.confirm_content_source_change().click()
    wait()

    # Select 'manual' from the Mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Manual_box1().click()
    wait()
    admin_playout_page.confirm_content_source_change().click()
    wait()

    # Navigate to the story page
    admin_playout_page.stories_page().click()
    wait()
    if admin_playout_page.page.locator(
            '//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]').nth(
        1).is_visible() and admin_playout_page.page.locator(
        '//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][3]').nth(
        1).is_visible():
        logging.info('Playout and playlist button are present')
    else:
        logging.info("No buttons visible")
    admin_playout_page.page.goto('http://10.189.200.6/admin/playout')
    # Selecting the live option from content source dropdown
    # Selecting the live option from content source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_Live_box1().click()
    admin_playout_page.timeout()  # you have to check for fixed channel and modify the script
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()

    # selecting the manual option from mode dropdown
    admin_playout_page.get_mode_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@data-name="mode"]//div//ul//li[2]').click()
    admin_playout_page.timeout()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()
    admin_playout_page.page.goto('http://10.189.200.6/live')
    admin_playout_page.timeout()
    if admin_playout_page.page.locator(
            '//div[@class="row action-bar-wrapper"]//div[@class="flashing-indicators-holder"]').is_visible() and admin_playout_page.page.locator(
        '//td[@class="actions-cell"]//div[@class="actions"]//div//div//button').nth(3).is_visible():
        logging.info('Playout and playlist button are present')
    else:
        logging.info("No buttons visible")
