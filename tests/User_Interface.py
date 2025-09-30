import logging

import env
import pytest
from playwright.sync_api import expect
import pandas as pd

# def test_UI_Add_To_Playlist(user_interface_page):
#     user_interface_page.navigate()
#     user_interface_page.timeout()
#     for i in range(1, 4):
#         user_interface_page.favorite_icon().nth(i).click()
#         user_interface_page.timeout()
#     user_interface_page.my_videos().click()
#     for i in range(1, 4):
#         slug_name = user_interface_page.slug_name().nth(i).text_content()
#         logging.info(slug_name)
#         user_interface_page.timeout()
#         user_interface_page.add_to_playlist().nth(i).click()
#         user_interface_page.timeout()
#         user_interface_page.playout_opt_1().click()
#         user_interface_page.timeout()
#     user_interface_page.po_page().click()
#     for i in range(user_interface_page.upcoming_videos().count()):
#         upcoming_videos = user_interface_page.upcoming_videos().nth(i).text_content()
#         logging.info(upcoming_videos)

import logging

from helpers import ubuntu
from helpers.database import Database


def test_UI_Add_To_Playlist_from_myvideos(user_interface_page):#UI/MyVideos: Add to Playlist
    db_client = Database()
    # Navigate to the user interface page
    user_interface_page.navigate()

    # Add first three favorite videos
    for i in range(0, 4):
        user_interface_page.favorite_icon().nth(i).click()
        user_interface_page.timeout()

    # clearing the playlist
    user_interface_page.po_page().click()
    user_interface_page.timeout()
    while True:
        # Fetch all elements at once instead of counting and using nth
        playlist_button_selector = "//div[@class='scrollable']//div[@data-name='playlist-1']//div//button[@class='btn-action tooltip no-print']"
        playlist_buttons = user_interface_page.page.query_selector_all(playlist_button_selector)

        # Break the loop if no more buttons are found
        if not playlist_buttons:
            break

        # Process the first button found
        button = playlist_buttons[0]
        if button.is_visible():
            button.click()

            # Wait for the dialog and ensure it is visible
            dialog_selector = "//dialog[@class='inv-bg']//div//div[@class='row buttons']//button[2]"
            user_interface_page.page.wait_for_selector(dialog_selector, state="visible")

            # Click the second button in the dialog
            user_interface_page.page.locator(dialog_selector).click()

            # Implement a delay or wait for a specific condition to ensure the UI has updated
            user_interface_page.timeout()

            logging.info("Deleted one item")
            # Navigate to "My Videos" section

        user_interface_page.my_videos().click()
        # Process and add first three videos from "My Videos" to the playlist
        for i in range(0, 4):
            # Get the slug name of the video
            slug_name = user_interface_page.slug_name().nth(i).text_content()
            logging.info(f"Slug Name: {slug_name}")
            user_interface_page.timeout()

            # Add video to the playlist
            user_interface_page.add_to_playlist().nth(i).click()
            user_interface_page.timeout()

            # Select first playout option
            user_interface_page.playout_opt_1().click()
            user_interface_page.timeout()

            # Navigate to the PO page
    user_interface_page.po_page().click()
    user_interface_page.timeout()
    for i in range(1, 4):
        upcoming_videos = user_interface_page.upcoming_videos().nth(i).text_content()
        logging.info(upcoming_videos)
        user_interface_page.timeout()
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


def test_UI_Playout_Now(user_interface_page):#UI/Live: Playout Now
    db_client = Database()
    def wait():
        """Short helper function to reduce redundancy and improve readability."""
        user_interface_page.timeout()

    # Navigate to the admin playout page
    user_interface_page.navigate()
    wait()
    user_interface_page.page.goto('http://10.189.200.6/admin/playout')

    # Select the content source and confirm
    user_interface_page.get_Content_Source_box1().click()
    wait()
    user_interface_page.get_CS_Live_box1().click()
    wait()
    user_interface_page.confirm_content_source_change().click()
    wait()

    # Change the mode and confirm
    user_interface_page.get_mode_box1().click()
    wait()
    user_interface_page.page.locator('//div[@data-name="mode"]//div//ul//li[2]').click()
    wait()
    user_interface_page.confirm_content_source_change().click()
    wait()

    # Navigate to the live page and interact with specific elements
    user_interface_page.page.goto('http://10.189.200.6/live')
    wait()
    user_interface_page.page.locator(
        '//div[@class="row action-bar-wrapper"]//div[@class="flashing-indicators-holder"]//div//button').click()
    wait()
    user_interface_page.page.locator(
        '//div[@class="row action-bar-wrapper"]//div[@class="flashing-indicators-holder"]//div//div//ul//li[1]').click()
    wait()

    # Fetch and log the story being played
    story_being_played = user_interface_page.page.locator('//div[@class="event-details"]//h1').text_content()
    logging.info(f"Story being played: {story_being_played}")
    wait()

    # Navigate back to playout and verify the story
    user_interface_page.page.goto('http://10.189.200.6/playout')
    wait()
    user_interface_page.timeout()
    now_playing = user_interface_page.page.locator('a.playing-now > div.wbreak').nth(1).text_content()
    logging.info(now_playing)
    user_interface_page.timeout()
    assert story_being_played == now_playing
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


def test_add_videos_to_playlist_from_Live(user_interface_page):#UI/Live: Add to Playlist
    # user_interface_page.timeout()
    # user_interface_page.page.goto('http://10.189.200.6/admin/playout')
    # user_interface_page.get_Content_Source_box1().click()
    # user_interface_page.timeout()
    # user_interface_page.get_CS_Live_box1().click()
    # user_interface_page.timeout()
    # user_interface_page.confirm_content_source_change().click()
    # user_interface_page.timeout()
    # user_interface_page.get_mode_box1().click()
    # user_interface_page.timeout()
    # user_interface_page.page.locator('//div[@data-name="mode"]//div//ul//li[2]').click()
    # user_interface_page.timeout()
    # user_interface_page.confirm_content_source_change().click()
    # user_interface_page.timeout()
    # user_interface_page.page.goto('http://10.189.200.6/live')
    # for i in range(1, 4):
    #     user_interface_page.add_playlist_button().nth(i).click()
    #     user_interface_page.timeout()
    #     user_interface_page.opt1_add_to_playlist().click()
    #     user_interface_page.timeout()
    db_client = Database()
    def wait_for_page():
        user_interface_page.timeout()

    # Navigate to the playout admin page
    user_interface_page.page.goto('http://10.189.200.6/admin/playout')
    wait_for_page()

    # Select content source
    user_interface_page.get_Content_Source_box1().click()
    wait_for_page()
    user_interface_page.get_CS_Live_box1().click()
    wait_for_page()
    user_interface_page.confirm_content_source_change().click()
    wait_for_page()

    # Change mode
    user_interface_page.get_mode_box1().click()
    wait_for_page()
    user_interface_page.page.locator('//div[@data-name="mode"]//div//ul//li[2]').click()
    wait_for_page()
    user_interface_page.confirm_content_source_change().click()
    wait_for_page()

    # Navigate to the live page
    user_interface_page.page.goto('http://10.189.200.6/live')

    # Add videos to the playlist
    for i in range(1, 4):
        user_interface_page.add_playlist_button().nth(i).click()
        wait_for_page()
        user_interface_page.opt1_add_to_playlist().click()
        wait_for_page()
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


def test_print_my_videos(user_interface_page):#UI/MyVideos: Print
    user_interface_page.navigate()
    user_interface_page.timeout()
    #navigate to myvideos page
    user_interface_page.page.goto('http://10.189.200.6/videos')
    user_interface_page.timeout()
    #click on the printer icon
    user_interface_page.page.locator(
        '//div[@class="enclosure no-print"]//button[@class="btn-icon tooltip no-print"]').nth(1).click()
    logging.info("Dailog box for Printing the page has opened")


def test_print_my_playout_page(user_interface_page):#UI/Playout: Print
    user_interface_page.navigate()
    user_interface_page.timeout()
    #navigate to the playout page
    user_interface_page.page.goto('http://10.189.200.6/playout')
    user_interface_page.timeout()
    #click on the printer icon
    user_interface_page.page.locator('//div[@class="main"]//h3//button').click()
    logging.info("Dailog box for Printing the page has opened")


def test_live_preview(user_interface_page):#UI/Live: Live Preview
    user_interface_page.navigate()
    user_interface_page.timeout()
    #navigate to the live page
    user_interface_page.page.goto('http://10.189.200.6/live')
    user_interface_page.timeout()
    #checking if there is atleast a video in live page to confirm live is working
    story = user_interface_page.page.locator('//tr[@class="event-row selectable-row selected"]//td[2]//button').text_content()
    logging.info(story)
    if story:
        logging.info('Live page exists')
    else:
        logging.info('Live page doesnt exists')
    user_interface_page.timeout()



