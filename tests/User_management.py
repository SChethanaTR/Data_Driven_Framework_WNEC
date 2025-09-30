import logging

import env
import pytest
from playwright.sync_api import expect
import pandas as pd

from helpers import ubuntu
from helpers.database import Database


def test_add_multiple_users(user_management_page):#UI/Admin: User Management
    db_client = Database()
    # Load data from Excel file
    filepath = '/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx'
    data = pd.read_excel(filepath)
    user_management_page.navigate_user_page()
    # to delete all users except administrator
    all_users = user_management_page.page.locator('//table//tbody//tr[@class="selectable-row"]//td[1]')
    # Check each element's text content
    for element_handle in all_users.element_handles():
        username = element_handle.text_content().strip()
        if username != 'administrator':
            user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[@class="actions-cell"]//div[@class="actions"]//div[@class="flashing-indicators-holder"]').nth(1).click()
            user_management_page.page.wait_for_timeout(3000)
            user_management_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
    # Iterate over each row in the DataFrame
    for index, row in data.iterrows():
        username = row['Username']
        password = row['Password']
        # Navigate to the user page
        user_management_page.page.goto("http://10.189.200.6/admin/users")
        # Add user
        user_management_page.test_add_user(username, password)
        user_management_page.timeout()
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM users')


def test_verify_user_addition(user_management_page):
    db_client = Database()
    # Load data from Excel file
    filepath = '/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx'
    data = pd.read_excel(filepath)
    user_management_page.navigate_user_page()
    # to delete all users except administrator
    all_users = user_management_page.page.locator('//table//tbody//tr[@class="selectable-row"]//td[1]')
    # Check each element's text content
    for element_handle in all_users.element_handles():
        username = element_handle.text_content().strip()
        if username != 'administrator':
            user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[@class="actions-cell"]//div[@class="actions"]//div[@class="flashing-indicators-holder"]').nth(1).click()
            user_management_page.page.wait_for_timeout(3000)
            user_management_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
    # Iterate over each row in the DataFrame
    for index, row in data.iterrows():
        username = row['Username']
        password = row['Password']
        # Navigate to the user page
        user_management_page.page.goto("http://10.189.200.6/admin/users")

        # Add user
        user_management_page.test_add_user(username, password)
        user_management_page.timeout()
        # Retrieve all elements matching the locator
        added_users = user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[1]')

        # Check each element's text content
        user_found = False
        for element_handle in added_users.element_handles():
            if element_handle.text_content().strip() == username:
                logging.info(f"User {username} is added")
                user_found = True
                break
        if not user_found:
            logging.info(f"User {username} not found in the table")
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM users')


def test_login_logout(user_management_page):
    db_client = Database()
    # Load data from Excel file
    filepath = '/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx'
    data = pd.read_excel(filepath)
    user_management_page.navigate_user_page()
    # to delete all users except administrator
    all_users = user_management_page.page.locator('//table//tbody//tr[@class="selectable-row"]//td[1]')
    # Check each element's text content
    for element_handle in all_users.element_handles():
        username = element_handle.text_content().strip()
        if username != 'administrator':
            user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[@class="actions-cell"]//div[@class="actions"]//div[@class="flashing-indicators-holder"]').nth(1).click()
            user_management_page.page.wait_for_timeout(3000)
            user_management_page.page.locator('//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()
    # Iterate over each row in the DataFrame
    for index, row in data.iterrows():
        username = row['Username']
        password = row['Password']
        # Navigate to the user page
        user_management_page.page.goto("http://10.189.200.6/admin/users")
        # Add user
        user_management_page.verify_logout_login(username, password)
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM users')


def test_delete_user(user_management_page):
    db_client = Database()
    user_management_page.navigate_user_page()
    user_management_page.timeout()
    deleted_user = user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[1]').nth(1).text_content()
    user_management_page.page.locator('//div[@class="actions"]//div[@class="flashing-indicators-holder"]//button').nth(1).click()
    user_management_page.timeout()
    user_management_page.page.locator('//dialog[@class="inv-bg"]//div//div//button[2]').click()
    logging.info(deleted_user)
    user_management_page.timeout()
    try:  # validation from logs
        # Get the list of all files in the directory
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")
    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM users')


def test_search_user(user_management_page):
    db_client = Database()
    # Load data from Excel file
    filepath = '/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx'
    data = pd.read_excel(filepath)

    # to delete all users except administrator
    all_users = user_management_page.page.locator('//table//tbody//tr[@class="selectable-row"]//td[1]')
    # Check each element's text content
    for element_handle in all_users.element_handles():
        username = element_handle.text_content().strip()
        if username != 'administrator':
            user_management_page.page.locator(
                '//tbody//tr[@class="selectable-row"]//td[@class="actions-cell"]//div[@class="actions"]//div[@class="flashing-indicators-holder"]').nth(
                1).click()
            user_management_page.page.wait_for_timeout(3000)
            user_management_page.page.locator(
                '//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()


    # Iterate over each row in the DataFrame
    for index, row in data.iterrows():
        username = row['Username']
        password = row['Password']
        # Navigate to the user page
        user_management_page.page.goto("http://10.189.200.6/admin/users")
        # Add user
        user_management_page.test_add_user(username, password)
        user_management_page.timeout()
        user_management_page.page.locator('//div[@class="filter"]//input').fill(username)
        user_management_page.timeout()
        if user_management_page.is_user_present(username):
            print("User present")
        else:
            print("No user found")
        try:  # validation from logs
            # Get the list of all files in the directory
            public_host = env.ftp_host
            ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
            logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
            stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
            file_names = stdout.read().decode().splitlines()
        except Exception as e:
            logging.info(f"Error: {e}")
        logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM users')






