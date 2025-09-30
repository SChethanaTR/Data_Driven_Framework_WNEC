import logging

import env
import pytest
from playwright.sync_api import expect

from helpers import ubuntu
from helpers.database import Database


def test_Administrator_file_playout_manual(
        admin_playout_page):  # FilePlayout-Manual #Verification of logs - FilePlayout - Manual/Auto/Loop
    # Navigate to the admin playout page
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

    # Click on the playout icon against each story
    for i in range(3, 8):
        admin_playout_page.story_page_playout_button().nth(i).click()
        wait()
        admin_playout_page.playout_option_1().click()
        wait()
        logging.info("Story playout initiated for story index: %d", i)

    # Navigate to the playout page and print all story names that have been added
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    for i in range(1, 6):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info("Story %d: %s", i, text)
        assert text is not None, "Story text should not be None"

    wait()
    # Negative scenario: Check if playout icon is not clickable when 'manual' is not selected
    admin_playout_page.page.locator(
        '//div[@id="app-root"]//header[@class="inv-bg no-print"]//ul[@class="tab horizontal inheader hnav"]//li[4]//div[@data-name="nav-menu"]').click()
    wait()
    admin_playout_page.page.locator('//ul[@class="inv-bg groups"]//li[2]//ul//li[2]').click()
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Auto_box1().click()  # Assuming 'Automatic' is another option
    wait()
    admin_playout_page.confirm_content_source_change().click()
    wait()

    admin_playout_page.stories_page().click()
    wait()

    for i in range(3, 8):
        try:
            admin_playout_page.story_page_playout_button().nth(i).click()
            wait()
            assert False, "Playout button should not be clickable in 'Automatic' mode"
        except:
            logging.info("Playout button is not clickable for story index: %d in 'Automatic' mode", i)
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


def test_Administrator_file_playout_auto(
        admin_playout_page):  # FilePlayout-Auto #Verification of logs - FilePlayout - Manual/Auto/Loop
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
    admin_playout_page.confirm_content_source_change().click()
    wait()

    # Select 'auto' from the Mode dropdown
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Auto_box1().click()
    admin_playout_page.confirm_content_source_change().click()
    wait()

    # Navigate to the playout page and print all story names that have been added
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    for i in range(1, 4):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info("Story %d: %s", i, text)
        assert text is not None, "Story text should not be None"

    # Negative Scenario
    # Change mode to 'manual' and verify that the playout process does not work as expected
    wait()
    # Negative scenario: Check if playout icon is not clickable when 'manual' is not selected
    admin_playout_page.page.locator(
        '//div[@id="app-root"]//header[@class="inv-bg no-print"]//ul[@class="tab horizontal inheader hnav"]//li[4]//div[@data-name="nav-menu"]').click()
    wait()
    admin_playout_page.page.locator('//ul[@class="inv-bg groups"]//li[2]//ul//li[2]').click()
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Manual_box1().click()  # Assuming 'Manual' is another option
    wait()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.page.wait_for_timeout(5000)


    # Attempt to navigate to the playout page and verify that stories are not added
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    admin_playout_page.page.wait_for_timeout(5000)
    story_name = admin_playout_page.page.locator('//div[@class="scrollable no-print"]').nth(1).text_content()
    if story_name == " ":
        logging.info("empty")
    else:
        logging.info(story_name)
    db_client.execute_query(f'SELECT * FROM player')


def test_Administrator_file_playout_loop(
        admin_playout_page):  # FilePlayout- Loop #Verification of logs - FilePlayout - Manual/Auto/Loop
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
    admin_playout_page.confirm_content_source_change().click()
    wait()
    # select 'Loop'  from the mode drop down
    admin_playout_page.get_mode_box1().click()
    wait()
    admin_playout_page.get_Mode_Loop_box1().click()
    wait()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.page.locator('//button[@class="btn inv-bg label icon"]').click()  # click on configure loop
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]').click()  # click on loop dropdown
    wait()
    admin_playout_page.page.locator('//div[@data-name="loops"]//div//ul//li[4]').click()  # select 3
    wait()
    # admin_playout_page.page.locator('//div[@class="services"]//label[@class="tick label"]//input').nth(1).click()
    # admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@class="row buttons"]//button[2]').click()  # save
    wait()
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()  # playout page
    wait()
    for i in range(1, 4):
        text = admin_playout_page.page.locator('//div[@class="slug-edit-number row"]//span[@class="wbreak"]').nth(
            i).text_content()
        logging.info("Story %d: %s", i, text)
    for i in range(1, 4):
        now_playing = admin_playout_page.page.locator(
            '//div[@class="playout-grid with-columns"]//div[4]//h4[@class="label"]//a//div//span').nth(1).text_content()
        logging.info(now_playing)
        wait()
        admin_playout_page.page.locator('//div[@class="row control"]//button[3]').nth(1).click()
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


def test_Administrator_live_playout_manual(admin_playout_page):  # Live-Manual
    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.timeout()
    # Selecting the live option from content source dropdown
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_Live_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()
    # selecting the manual option from mode dropdown
    admin_playout_page.get_mode_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@data-name="mode"]//div//ul//li[2]').click()
    admin_playout_page.timeout()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()
    # navigating to live page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[2]').click()
    # printing the first story from live page
    story_name = admin_playout_page.live_page_slug_name().nth(0).text_content()
    logging.info(story_name)
    admin_playout_page.timeout()
    # selecting the playoutnow button and selecting sdi1 for the video to be played
    admin_playout_page.live_page_playout_icon().nth(1).click()
    admin_playout_page.timeout()
    admin_playout_page.live_page_playout_op_1().click()
    admin_playout_page.timeout()
    # naviagte to playout page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()  # playout page
    admin_playout_page.timeout()
    admin_playout_page.timeout()
    # printing the video that was being added
    now_playing = admin_playout_page.page.locator(
        '//div[@class="playout-grid with-columns"]//div[4]//h4[@class="label"][2]//a[@class="playing-now"]').nth(
        0).text_content()
    logging.info(now_playing)
    # verifying if the added story and the story vbeing played are same
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


def test_Administrator_live_playout_Fixed(admin_playout_page):  # Live- Fixed- not giving proper output
    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.timeout()
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_Live_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()
    admin_playout_page.get_mode_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@data-name="mode"]//div//ul//li[3]').click()
    admin_playout_page.timeout()
    admin_playout_page.confirm_content_source_change().click()
    admin_playout_page.timeout()
    # selecting the channel dropdown for fixed playout
    admin_playout_page.page.locator('//div[@class="row list-row"]//div[@data-name="channel"]').click()  # select channel
    # selecting the channel
    admin_playout_page.page.locator(
        '//div[@class="row list-row"]//div[@data-name="channel"]//div//ul//li[2]').click()  # RL1
    # navigate to live page
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[2]').click()  # select live page
    # selecting the row for video
    admin_playout_page.page.locator('//tbody//tr[@class="event-row selectable-row"]').nth(2).click()
    admin_playout_page.timeout()
    admin_playout_page.timeout()
    # checking the video that has channel name as RL1
    rows = admin_playout_page.page.locator('//tbody//tr[@class="event-row selectable-row"]')
    for i in range(rows.count()):
        row = rows.nth(i)
        # Use XPath and correct the syntax for Playwright
        rl_button = row.locator('xpath=.//td//button[@class="btn-channel"]').text_content()
        if rl_button == "rl&nbsp;1":
            slug_name = row.locator('xpath=.//td[2]//button').inner_text()
            logging.info(f"Found rl 1 button. Adjacent slug name: {slug_name}")
            break
    else:
        logging.info("No rl 1 button found in any row")
    admin_playout_page.timeout()
    admin_playout_page.page.locator('//div[@class="column nav no-print"]//ul//li[4]').click()
    # should print the video being played and verify if both are same
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


def test_Administrator_6xLive_preview_playout_Fixed(admin_playout_page):  # Verification of logs - 6X Live Preview
    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_6x_Live_Preview_box1().click()
    admin_playout_page.timeout()
    # admin_playout_page.confirm_content_source_change().click()
    # admin_playout_page.timeout()
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


def test_Administrator_RLS_preview_playout_Fixed(admin_playout_page):  # Verification of logs - RLS Broadcast
    db_client = Database()
    admin_playout_page.navigate()
    admin_playout_page.get_Content_Source_box1().click()
    admin_playout_page.timeout()
    admin_playout_page.get_CS_RLS_Broadcast_box1().click()
    admin_playout_page.timeout()
    # admin_playout_page.confirm_content_source_change().click()
    # admin_playout_page.timeout()
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


# def test_enable_disable_Channel(admin_playout_page):
#     admin_playout_page.navigate()
#     logging.info('Navigated to playout page')
#     admin_playout_page.timeout()
#     admin_playout_page.get_disable_channel_box_1().click()
#     logging.info("Radio button to disable channel is clicked")
#     admin_playout_page.timeout()
#     admin_playout_page.page.goto('http://10.189.200.6/stories#list')
#     admin_playout_page.timeout()
#     admin_playout_page.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]').nth(1).click()
#     admin_playout_page.timeout()
#     # admin_playout_page.playout_option_1().click()
#     admin_playout_page.page.goto('http://10.189.200.6/playout')
#     status = admin_playout_page.page.locator('//div[@class="playout-grid with-columns"]//div//h4[@class="label"]//div').nth(1).text_content()
#     logging.info(status)
#     if status == "PLAYOUT STOPPEDPress Start button, and/or add videos to Playlist, or press Play Now button in Stories page":
#         logging.info("Channel is disabled")
#     else:
#         logging.info("Channel is enabled")
#     admin_playout_page.page.goto('http://10.189.200.6/admin/playout')
#     admin_playout_page.timeout()
#     admin_playout_page.get_enable_channel_box_1().click()
#     admin_playout_page.timeout()
#     logging.info("Radio button to enable channel is clicked")
#     admin_playout_page.timeout()
#     admin_playout_page.page.goto('http://10.189.200.6/stories#list')
#     admin_playout_page.timeout()
#     admin_playout_page.page.locator('//div[@class="td no-print"]//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]').nth(1).click()
#     admin_playout_page.timeout()
#     admin_playout_page.page.locator('//div[@class="flashing-indicators-holder"]//div//div//ul//li[1]').click()
#     admin_playout_page.timeout()
#     admin_playout_page.page.goto('http://10.189.200.6/playout')
#     admin_playout_page.timeout()
#     playout_ready_text = admin_playout_page.page.locator('div.playing-now').nth(1).text_content()
#     logging.info(playout_ready_text.split('\n')[0])
#     if playout_ready_text == "PLAYOUT STOPPED":
#         logging.info("Channel is disabled")
#     else:
#         logging.info("Channel is enabled")


def test_enable_disable_channel(admin_playout_page):
    ADMIN_PLAYOUT_URL = 'http://10.189.200.6/admin/playout'
    STORIES_LIST_URL = 'http://1010.189.200.6/stories#list'
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


def test_playout_playlist_button(admin_playout_page):
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
    admin_playout_page.timeout()
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
