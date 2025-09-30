import logging
import os
import random
import re

import pandas as pd
import pytest
from playwright.sync_api import expect

import conftest
import env
from component_util import db_manager
from collections import Counter
from conftest import story_page
from env import password
from helpers import ubuntu
# import mysql.connector
from helpers.database import Database


def test_FD_Create_dist_using_UI(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.timeout()
    for i in range(0, 3):
        story_page.details_for_distribution(i+1)
        story_page.select_protocol.nth(i).click()
        text = story_page.protocol_method.text_content()
        logging.info(text)
        logging.info("ABCDDD")
        if text == "FTP":
            story_page.ftp_distribution()
        elif text == "SFTP":
            story_page.sftp_distribution()
        else:
            story_page.ftps_distribution()
        story_page.navigate()
        story_page.check_advisory.first.click()
        story_page.page.wait_for_timeout(6000)
        if text == "FTP":
            logging.info("Distribution History is empty")
        elif text == "SFTP":
            story_page.clear_distribution_history()
        else:
            story_page.clear_distribution_history()
        story_page.page.wait_for_timeout(3000)
        story_page.navigate()
        for j in range(0, 3):
            story_page.add_to_distributor.nth(j).click()
            text1 = story_page.slug_of_story_added.nth(j).text_content()
            logging.info(text1)
            story_page.page.wait_for_timeout(10000)
        logging.info(f"Files added to {text} distribution")
        story_page.navigate_to_distribution_history()
        for k in range(0, 3):  # validation from UI to check if the same stories are being added
            content_added = story_page.name_of_the_slug_distributed.nth(k).text_content()
            logging.info(content_added)
            story_page.page.wait_for_timeout(3000)
        logging.info(f"Files distributed to {text}")
        story_page.timeout()
    story_page.timeout()
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    logging.info("Validation from database")
    db_client.execute_query(f'SELECT * FROM distribution_file_queue')  # sql not working


def test_Create_with_existing_name(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.timeout()
    for i in range(0, 2):
        story_page.navigate()
        story_page.details_for_distribution()
        story_page.select_protocol.nth(i).click()
        text = story_page.protocol_method.text_content()
        logging.info(text)
        if text == "FTP":
            story_page.ftp_distribution()
        # elif text == "SFTP":
        #     story_page.sftp_distribution()
        else:
            story_page.ftps_distribution()
    error = story_page.page.locator('//form[@class = "edit-distribution error"]//h3[@class = "error"]').text_content()
    logging.info(error)
    assert error == "The server responded with an error. The operation was unsuccessful."
    db_client.execute_query(f'SELECT * FROM distribution_configuration_ftp')  # SQL worked

def test_create_with_empty_name_and_different_characters(story_page):
    inputs = ["+", "*", "test1", "", "  ", "_", "!", "@", "#", "$", "%", "^", "&", "*", "()", "_", "+", "-", "=", "~",
              "{}", "[]", ":", ";", "|", "<>", ".", "?"]

    for i in range(7):  # Assuming you want to perform the test with 10 randomly picked inputs
        input_value = random.choice(inputs)
        story_page.navigate()
        story_page.timeout()
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()
        story_page.FD_name.fill(input_value)
        if input_value in [" ", "_", "+", "*", "", "  ", "_", "!", "@", "#", "$", "%", "^", "&", "*", "()", "_", "+",
                           "-", "=", "~", "{}", "[]", ":", ";", "|", "<>", ".", "?"]:
            logging.info(input_value)
            story_page.special_input()
        elif input_value == "":
            logging.info(input_value)
            story_page.Blank_input()
        else:
            logging.info(input_value)
            story_page.valid_input()  # working


def test_without_valid_host(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.timeout()
    for i in range(0, 3):
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()
        story_page.FD_name.fill("test1")
        story_page.SD.first.click()  # SD
        # story_page.HD.first.click()
        # story_page.script.first.click()
        story_page.protocol_method.last.click()
        story_page.select_protocol.nth(i).click()
        text = story_page.protocol_method.text_content()
        logging.info(text)
        if text == "FTP":
            story_page.ftp_distribution_without_host()
            story_page.without_host()
        elif text == "SFTP":
            story_page.sftp_distribution_without_host()
            story_page.without_host()
        else:
            story_page.ftps_distribution_without_host()
            story_page.without_host()
        story_page.navigate()
    db_client.execute_query(f'select * from distribution_configuration_ftp')  # working


def test_without_target_directory(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.timeout()
    for i in range(0, 3):
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()
        story_page.FD_name.fill("test1")
        story_page.SD.first.click()  # SD
        # story_page.HD.first.click()
        # story_page.script.first.click()
        story_page.protocol_method.last.click()
        story_page.select_protocol.nth(i).click()
        text = story_page.protocol_method.text_content()
        logging.info(text)
        if text == "FTP":
            story_page.ftp_distribution_without_target()
        elif text == "SFTP":
            story_page.sftp_distribution_without_target()
        else:
            story_page.ftps_distribution_without_target()
        story_page.navigate()
    db_client.execute_query(f'select * from distribution_configuration_ftp')  # working


def test_Add_Dist_for_nonAdmin_user(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.navigate()
    story_page.page.wait_for_timeout(6000)
    story_page.hamburger.click()
    story_page.User_management.click()
    story_page.page.wait_for_timeout(6000)
    story_page.add_user.click()
    story_page.new_username.fill("CL")
    story_page.timeout()
    story_page.new_password.fill("Chethuuu@123")
    story_page.timeout()
    story_page.role_permissions()
    story_page.new_user_save.click()
    story_page.timeout()
    story_page.login_logout.first.click()
    story_page.timeout()
    expected_text = "Log out from BOX 1"
    if story_page.log_out_from_box.text_content() == expected_text:
        story_page.log_out_from_box.click()
        story_page.timeout()
    else:
        # If the text content is not as expected, raise an AssertionError
        raise AssertionError(
            f"Expected text: '{expected_text}', Actual text: '{story_page.log_out_from_box.text_content()}'")
    story_page.page.get_by_role("button", name="Log Out").click()
    story_page.timeout()
    story_page.login_logout.first.click()
    expected_text_1 = "Log in to BOX 1"
    if story_page.log_in_to_box.text_content() == expected_text_1:
        story_page.log_in_to_box.click()
        story_page.timeout()
    else:
        # If the text content is not as expected, raise an AssertionError
        raise AssertionError(
            f"Expected text: '{expected_text_1}', Actual text: '{story_page.log_in_to_box.text_content()}'")
    # story_page.log_in_to_box.click()
    story_page.timeout()
    story_page.page.get_by_label("username").fill("CL")
    story_page.page.get_by_label("password").fill("Chethuuu@123")
    story_page.timeout()
    story_page.page.get_by_role("button", name="Log In").click()
    story_page.page.wait_for_timeout(6000)
    story_page.add_to_distribution_icon.first.click()
    story_page.timeout()
    story_page.History.click()
    story_page.timeout()
    story_page.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()
    story_page.timeout()
    logging.info("Validation from database")
    db_client.execute_query(f"SELECT *  FROM users WHERE username = 'CL'")
    db_client.execute_query(f'SELECT  *  FROM distribution_configuration_ftp')
    db_client.execute_query(f'SELECT * FROM distribution_file_queue')  # workin


def test_delete_process_with_active_transfer(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    db_client.execute_query(f'select * from distribution_configuration_ftp')
    story_page.navigate()
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(10000)
    story_page.hamburger.click()
    story_page.File_distributor_icon.click()
    story_page.timeout()
    story_page.remove_process.click()
    story_page.confirm_removal.click()
    story_page.timeout()
    logging.info("Distribution process have been removed")
    try:
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    # Query Database After Creation and Deletion
    db_client.execute_query(f'select * from distribution_configuration_ftp')  # worked


def test_change_filter_on_active_process(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.timeout()
    story_page.distribution_target.click()  # to make changes to the active configuration
    story_page.timeout()
    error_msg = story_page.e_message.text_content()
    assert error_msg == 'You are not able to edit a started process. Please stop the process first.'
    story_page.stop_distribution.click()
    story_page.confirm_to_stop_distribution.click()
    story_page.timeout()
    story_page.Filters.click()  # filters
    story_page.timeout()
    if story_page.no_filter.is_enabled():
        story_page.service_filter.click()
        story_page.save_distribution.click()
        story_page.page.wait_for_timeout(5000)
        service_filter_error_message = story_page.page.locator(
            '//div//details[6]//div[@class = "h4 input-info error"]').text_content()
        if service_filter_error_message == "Please select at least one service":
            logging.info(service_filter_error_message)
            story_page.subcon.first.click()
            story_page.timeout()
        else:
            story_page.navigate()
            logging.info("Cant continue the process")
        story_page.sensitivity_filter.click()  # sensitivity
        story_page.save_distribution.click()
        story_page.page.wait_for_timeout(5000)
        sensitivity_filter_error_message = story_page.page.locator(
            '//div//details[6]//div[@class = "h4 input-info error"]').text_content()
        if sensitivity_filter_error_message == "Please select at least one exclusion":
            logging.info(sensitivity_filter_error_message)
            story_page.Graphic_Sensitive_filter.last.click()
            story_page.timeout()
        else:
            story_page.navigate()
            logging.info("Cant continue the process")
    else:
        story_page.no_filter.check()
    story_page.save_distribution.click()  # save
    story_page.timeout()
    story_page.play_distribution.click()  # playing
    story_page.confirm_play_distribution.click()  # confirm play
    story_page.timeout()
    story_page.navigate()
    story_page.cctv_story.click()  # cctv
    # story_page.page.locator('//div[@class = "td no-print"]//div[@class = "actions"]//div[2]').first.click()
    story_page.story_dist_icon.first.click()
    story_page.timeout()
    story_page.History.click()
    story_page.distribution_history.click()  # distribution history
    story_page.page.wait_for_timeout(5000)
    db_client.execute_query(f'SELECT * FROM distribution_file_queue')
    story_page.page.wait_for_timeout(5000)
    story_page.History.click()
    story_page.distribution_history.click()
    story_page.page.wait_for_timeout(5000)
    db_client.execute_query(f'SELECT * FROM distribution_file_queue')
    # assert story_page.page.locator('//div[@class = "nodata"]').text_content() == "No records found"
    story_page.page.wait_for_timeout(4000)  # not working


def test_Multiple_distributions_configured_result_in_a_file_distributed_to_all_of_them(story_page):
    db_client = Database()
    for i in range(0, 3):
        story_page.navigate()
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()
        story_page.FD_name.fill(f"test{i}")
        story_page.SD.first.click()  # SD
        story_page.HD.first.click()
        story_page.script.first.click()
        story_page.protocol_method.last.click()
        story_page.ftp_distribution()
        story_page.timeout()
        story_page.navigate()
    for j in range(1, 3):
        story_page.add_to_distributor.nth(j).click()
        story_page.timeout()
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(6000)
    try:
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    logging.info("Validation from database")
    db_client.execute_query(f'SELECT * FROM distribution_file_queue')  # sql query not working


def test_Check_Active_connection_with_Passive_Server(story_page):
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.FTP_Details.click()
    story_page.timeout()
    story_page.host.first.fill('10.99.13.11')
    story_page.timeout()
    story_page.target_director.first.fill('/wneclient/data/QA/ftp/files/testJakub')
    story_page.timeout()
    story_page.FD_username.first.fill('wneqa')
    story_page.timeout()
    story_page.FD_password.first.fill('wneqa123')
    story_page.timeout()
    expect(story_page.page.locator('//div[@class = "centered row"]//label[@data-name = "active"][2]')).to_be_enabled()
    story_page.save_FD.last.click()
    story_page.timeout()
    try:
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)  # passes


def test_Check_when_primary_server_fails_failover_to_standby_server_happens(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.standby_ftp_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(10000)
    # ssh_password = .env.password
    try:
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    logging.info("Validation through database")
    db_client.execute_query(f'select * from distribution_configuration_ftp')  # working


def test_If_primary_and_standby_servers_are_provided_If_primary_working_files_should_arrive_to_it(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.standby_without_error_ftp_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(10000)
    try:
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    logging.info("Validation through database")
    db_client.execute_query(f'select * from distribution_configuration_ftp')  # working


def test_If_only_primary_server_information_is_provided_Primary_server_should_be_used_for_distribution(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(10000)
    try:
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    logging.info("Verified from terminal Logs")
    db_client.execute_query(f'select * from distribution_configuration_ftp')
    logging.info("Verified from database")  # working


def test_File_distribution_using_the_following_configuration_No_Password_Directory_Passive_mode(story_page):
    # db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution_without_password()
    save_error_message = story_page.page.locator(
        '//div//label[@class = "input password error"]//div[@class = "h4 input-info error"]').text_content()
    assert save_error_message == "Please specify a Password."
    logging.info(save_error_message)  # working


def test_Check_when_primary_server_is_back_after_a_failover_fall_back_to_primary_server_should_happen(story_page):
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.standby_ftp_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(10000)


def test_ftp_Select_services_and_run(story_page):  # not completed
    file_path = "/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx"
    sheet_name = "FileDistribution"
    distribution_name = "FTP"
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    story_page.navigate()
    story_page.timeout()
    story_page.page.goto('http://10.189.200.4/admin/distribution')
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@class="btn inv-bg label icon"]').click()
    story_page.timeout()
    story_page.distribution_name().fill(df[df['Name'] == 'FTP']['Name'].iloc[0])
    story_page.timeout()
    story_page.distribution_method_dropdown().click()
    story_page.timeout()
    logging.info("Dropdown clicked")
    story_page.timeout()
    story_page.ftp_dropdown().click()
    story_page.timeout()
    story_page.page.locator(
        '//form[@class="edit-distribution"]//div//details[@class="details"][2]//summary//div').click()
    story_page.timeout()
    story_page.ftp_host_details().fill(df[df['Name'] == 'FTP']['Host'].iloc[0])
    story_page.timeout()
    story_page.ftp_target_directory_Details().fill(df[df['Name'] == 'FTP']['TargetDirectory'].iloc[0])
    story_page.timeout()
    story_page.ftp_username().fill(df[df['Name'] == 'FTP']['Username'].iloc[0])
    story_page.timeout()
    story_page.ftp_password().fill(df[df['Name'] == 'FTP']['Password'].iloc[0])
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
    story_page.timeout()


def test_ftps_Select_services_and_run(story_page):  # not completed
    file_path = "/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx"
    sheet_name = "FileDistribution"
    distribution_name = "FTPS"
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    story_page.navigate()
    story_page.timeout()
    story_page.page.goto('http://10.189.200.4/admin/distribution')
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@class="btn inv-bg label icon"]').click()
    story_page.timeout()
    story_page.distribution_name().fill(df[df['Name'] == 'FTPS']['Name'].iloc[0])
    story_page.timeout()
    story_page.distribution_method_dropdown().click()
    story_page.timeout()
    logging.info("Dropdown clicked")
    story_page.timeout()
    story_page.ftps_dropdown().click()
    story_page.timeout()
    story_page.page.locator(
        '//form[@class="edit-distribution"]//div//details[@class="details"][3]//summary//div').click()
    story_page.timeout()
    story_page.ftps_host_details().fill(df[df['Name'] == 'FTPS']['Host'].iloc[0])
    story_page.timeout()
    story_page.ftps_target_directory_Details().fill(df[df['Name'] == 'FTPS']['TargetDirectory'].iloc[0])
    story_page.timeout()
    story_page.ftps_username().fill(df[df['Name'] == 'FTPS']['Username'].iloc[0])
    story_page.timeout()
    story_page.ftps_password().fill(df[df['Name'] == 'FTPS']['Password'].iloc[0])
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
    story_page.timeout()


def test_sftp_Select_services_and_run(story_page):  # not completed
    file_path = "/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx"
    sheet_name = "FileDistribution"
    distribution_name = "FTPS"
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    story_page.navigate()
    story_page.timeout()
    story_page.page.goto('http://10.189.200.4/admin/distribution')
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@class="btn inv-bg label icon"]').click()
    story_page.timeout()
    story_page.distribution_name().fill(df[df['Name'] == 'SFTP']['Name'].iloc[0])
    story_page.timeout()
    story_page.distribution_method_dropdown().click()
    story_page.timeout()
    logging.info("Dropdown clicked")
    story_page.timeout()
    story_page.sftp_dropdown().click()
    story_page.timeout()
    story_page.page.locator(
        '//form[@class="edit-distribution"]//div//details[@class="details"][4]//summary//div').click()
    story_page.timeout()
    story_page.sftp_host_details().fill(df[df['Name'] == 'SFTP']['Host'].iloc[0])
    story_page.timeout()
    story_page.sftp_target_directory_Details().fill(df[df['Name'] == 'SFTP']['TargetDirectory'].iloc[0])
    story_page.timeout()
    story_page.sftp_username().fill(df[df['Name'] == 'SFTP']['Username'].iloc[0])
    story_page.timeout()
    story_page.sftp_password().fill(df[df['Name'] == 'SFTP']['Password'].iloc[0])
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
    story_page.timeout()


def test_smb_Select_services_and_run(story_page):
    file_path = "/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx"
    sheet_name = "FileDistribution"
    distribution_name = "FTPS"
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    story_page.navigate()
    story_page.timeout()
    story_page.page.goto('http://10.189.200.4/admin/distribution')
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@class="btn inv-bg label icon"]').click()
    story_page.timeout()
    story_page.distribution_name().fill(df[df['Name'] == 'SMB']['Name'].iloc[0])
    story_page.timeout()
    story_page.distribution_method_dropdown().click()
    story_page.timeout()
    logging.info("Dropdown clicked")
    story_page.timeout()
    story_page.smb_dropdown().click()
    story_page.timeout()
    story_page.page.locator(
        '//form[@class="edit-distribution"]//div//details[@class="details"][5]//summary//div').click()
    story_page.timeout()
    story_page.smb_target_Directory_path().fill(df[df['Name'] == 'SFTP']['TargetDirectory'].iloc[0])
    story_page.timeout()
    story_page.smb_username().fill(df[df['Name'] == 'SFTP']['Username'].iloc[0])
    story_page.timeout()
    story_page.smb_password().fill(df[df['Name'] == 'SFTP']['Password'].iloc[0])
    story_page.timeout()
    story_page.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
    story_page.timeout()
    story_page.page.goto('http://10.189.200.4/admin/distribution')
    story_page.timeout()


def test_hover_element(story_page):
    story_page.navigate()
    story_page.page.wait_for_timeout(5000)
    story_page.page.locator('//div[@class="main"]//div[@class="tab-browser row no-print"]//div[4]').hover()
    story_page.page.wait_for_timeout(5000)
    logging.info(story_page.page.locator('//div[@class="main"]//div[@class="tab-browser row no-print"]//div[4]').text_content())
    story_page.page.wait_for_timeout(5000)
    story_page.page.goto('http://10.189.200.4/admin/playout')
    story_page.page.locator('//article[@class="admin-playout"]//div[@class="box-playout"]//div[@class="list column"]//div//label[@class="toggle"]').nth(1).hover()
    story_page.page.wait_for_timeout(5000)
    logging.info(story_page.page.locator('//article[@class="admin-playout"]//div[@class="box-playout"]//div[@class="list column"]//div//label[@class="toggle"]').nth(1).inner_text())
    story_page.page.wait_for_timeout(5000)