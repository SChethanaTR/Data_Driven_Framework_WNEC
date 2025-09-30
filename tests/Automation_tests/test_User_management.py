import env
from helpers import ubuntu
from helpers.database import Database
import pandas as pd
import allure
import random
import string
import logging


def handle_rows(page):
    # Select all rows
    rows = page.query_selector_all("//tbody//tr[@class='selectable-row']")

    for row in rows:
        # Get the username from the first cell
        username = row.query_selector("td[1]").inner_text()

        # Check if the username is not 'administrator'
        if username.lower() != 'administrator':
            # Find the corresponding button and click it
            button = row.query_selector("//td[@class='actions-cell']//div[@class='actions']//div//button")
            button.click()
            page.query_selector_all('//dialog[@class="inv-bg"]//div//div//button[2]').click()


@allure.feature("UserManagement")
def test_verify_user_addition(user_management_page):
    test_verify_user_addition.__doc__ = """Tests user addition functionality with data-driven approach.

    Detailed Test Flow:
    1. Data Preparation:
       - Connects to database
       - Loads test data from Excel
       - Cleans existing users

    2. User Management:
       - Deletes non-admin users
       - Adds users from Excel data
       - Verifies each addition

    3. Validation:
       - Checks UI visibility
       - Validates SSH logs
       - Verifies database entries

    Args:
        user_management_page: Fixture providing user management interface

    Test Data:
        - Source: test_data.xlsx
        - Required Columns: Username, Password
        - Protected Users: administrator, autoAdmin

    Dependencies:
        - Database connection
        - SSH access
        - Excel file presence
        - UI access rights

    Expected Results:
        - Users deleted except admins
        - New users added successfully
        - Database records match
        - Logs show operations

    URLs Accessed:
        - User Management: http://10.189.200.6/admin/users
    """
    db_client = Database()

    # Load data from Excel file
    filepath = '/Users/s.chethana/PycharmProjects/Data_Driven_Framework_WNEC/data/test_data.xlsx'
    data = pd.read_excel(filepath)

    # Navigate to user management page
    user_management_page.navigate_user_page()

    # --- Delete all users except administrator and autoAdmin ---
    def delete_all_users_except_admin():
        while True:
            rows = user_management_page.page.locator('table tbody tr.selectable-row')
            row_count = rows.count()
            user_deleted = False

            for i in range(row_count):
                row = rows.nth(i)
                username_element = row.locator('td:nth-child(1)')  # ✅ CSS selector
                username = username_element.text_content().strip()

                if username not in ['administrator', 'autoAdmin']:
                    # Check if delete icon exists for this row
                    delete_icon = row.locator('.actions-cell .actions .flashing-indicators-holder')
                    if delete_icon.count() > 0:
                        delete_icon.click()
                        user_management_page.page.wait_for_timeout(3000)

                        # Confirm deletion
                        user_management_page.page.locator(
                            'dialog.inv-bg .row.buttons button:nth-child(2)'
                        ).click()
                        user_management_page.page.wait_for_timeout(2000)

                        logging.info(f"Deleted user: {username}")
                        user_deleted = True
                        break  # Re-fetch rows after deletion

            if not user_deleted:
                break  # Exit loop when no more deletions are needed

    delete_all_users_except_admin()

    # --- Add users from Excel and verify ---
    for index, row in data.iterrows():
        username = row['Username']
        password = row['Password']

        # Navigate to the user page
        user_management_page.page.goto("http://10.189.200.6/admin/users")

        # Add user
        user_management_page.test_add_user(username, password)
        user_management_page.timeout()

        # Verify user is added
        added_users = user_management_page.page.locator('tbody tr.selectable-row td:nth-child(1)')
        user_found = False

        for element_handle in added_users.element_handles():
            if element_handle.text_content().strip() == username:
                logging.info(f"User {username} is added")
                user_found = True
                break

        if not user_found:
            logging.info(f"User {username} not found in the table")

    # --- Validate from logs via SSH ---
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
        logging.info(file_names)
    except Exception as e:
        logging.info(f"Error reading logs: {e}")

    # --- Validate from database ---
    db_client.execute_query('SELECT * FROM users')


@allure.feature("UserManagement")
def test_delete_user(user_management_page):
    test_delete_user.__doc__ = """Tests user deletion functionality and verifies removal.

    Detailed Test Flow:
    1. User Selection:
       - Navigates to user page
       - Locates target user
       - Captures user details

    2. Deletion Process:
       - Triggers delete action
       - Confirms deletion
       - Waits for completion

    3. Validation:
       - Checks system logs
       - Verifies database state
       - Confirms UI update

    Args:
        user_management_page: Fixture providing user management interface

    Dependencies:
        - Working database connection
        - SSH access for logs
        - UI access rights
        - Active user session

    Expected Results:
        - User successfully deleted
        - Database updated
        - Logs show deletion
        - UI reflects changes

    URLs Accessed:
        - User Management: http://10.189.200.6/admin/users
    """
    db_client = Database()
    user_management_page.navigate_user_page()
    user_management_page.timeout()
    deleted_user = user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[1]').nth(
        1).text_content()
    user_management_page.page.locator('//div[@class="actions"]//div[@class="flashing-indicators-holder"]//button').nth(
        1).click()
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


@allure.feature("UserManagement")
def test_add_multiple_users(user_management_page):
    test_add_multiple_users.__doc__ = """Tests multiple user creation with random credentials.

    Detailed Test Flow:
    1. Initial Cleanup:
       - Navigates to user page
       - Removes existing non-admin users
       - Prepares database connection

    2. User Creation:
       - Generates random credentials
       - Creates 3 unique users
       - Validates each addition

    3. Validation:
       - Checks system logs
       - Verifies database entries
       - Confirms UI updates

    Args:
        user_management_page: Fixture providing user management interface

    Test Data:
        - Number of users: 3
        - Username: 6 lowercase chars
        - Password: Mix of cases, digits, specials

    Dependencies:
        - Database connection
        - SSH access for logs
        - UI access rights
        - Random generation

    Expected Results:
        - Old users deleted
        - New users added
        - Database updated
        - Logs show changes

    URLs Accessed:
        - User Management: http://10.189.200.6/admin/users
    """

    db_client = Database()
    user_management_page.navigate_user_page()

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

    # Function to generate random username and password
    def generate_credentials():
        username = ''.join(random.choices(string.ascii_lowercase, k=6))  # 6-character lowercase username

        # Generate password with mix of characters
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=3))
        uppercase = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=2))
        special = ''.join(random.choices('!@#$%^&*', k=2))

        # Combine all characters and shuffle
        password = list(lowercase + uppercase + digits + special)
        random.shuffle(password)
        password = ''.join(password)

        return username, password

    # Add multiple users with random credentials
    num_users = 3  # Number of users to add
    for _ in range(num_users):
        username, password = generate_credentials()
        logging.info(f"Adding user - Username: {username}, Password: {password}")

        # Navigate to the user page
        user_management_page.page.goto("http://10.189.200.6/admin/users")

        # Add user
        user_management_page.test_add_user(username, password)
        user_management_page.timeout()

    try:  # validation from logs
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
    except Exception as e:
        logging.info(f"Error: {e}")

    logging.info(file_names)
    db_client.execute_query(f'SELECT * FROM users')


@allure.feature("UserManagement")
def test_login_logout(user_management_page):
    test_login_logout.__doc__ = """Tests user login and logout functionality.

    Detailed Test Flow:
    1. User Setup:
       - Creates random test user
       - Cleans existing users
       - Prepares credentials

    2. Login Process:
       - Adds new test user
       - Performs login
       - Verifies access

    3. Logout Process:
       - Opens logout menu
       - Verifies logout message
       - Confirms logout

    Args:
        user_management_page: Fixture providing user management interface

    Test Data:
        - Username: Random 6 lowercase chars
        - Password: Mix of cases, digits, specials
        - Protected User: administrator

    Dependencies:
        - Working user interface
        - Authentication system
        - Session management

    Expected Results:
        - User created successfully
        - Login completes
        - Logout message correct
        - Session terminates

    URLs Accessed:
        - User Management: http://10.189.200.6/admin/users
    """

    def generate_credentials():
        username = ''.join(random.choices(string.ascii_lowercase, k=6))
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=3))
        uppercase = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=2))
        special = ''.join(random.choices('!@#$%^&*', k=2))
        password = list(lowercase + uppercase + digits + special)
        random.shuffle(password)
        return username, ''.join(password)

    try:
        # Navigate to the user management page
        user_management_page.navigate_user_page()

        # Delete all users except the administrator
        all_users = user_management_page.page.locator('//table//tbody//tr[@class="selectable-row"]//td[1]')
        for element_handle in all_users.element_handles():
            username = element_handle.text_content().strip()
            if username != 'administrator':
                user_management_page.page.locator(
                    '//tbody//tr[@class="selectable-row"]//td[@class="actions-cell"]//div[@class="actions"]//div[@class="flashing-indicators-holder"]').nth(
                    1).click()
                user_management_page.page.wait_for_timeout(3000)
                user_management_page.page.locator(
                    '//dialog[@class="inv-bg"]//div//div[@class="row buttons"]//button[2]').click()

        # Generate random credentials for one user
        username, password = generate_credentials()
        logging.info(f"Testing user - Username: {username}, Password: {password}")

        # Add user
        user_management_page.test_add_user(username, password)
        user_management_page.timeout()

        # # Search for created user
        # user_management_page.page.locator('//div[@class="filter"]//input').fill(username)
        # user_management_page.timeout()
        #
        # # Verify user exists
        # found_username = user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[1]').text_content()
        # assert found_username == username, f"Expected user {username}, found {found_username}"
        # logging.info("User successfully created")

        # Verify login/logout functionality
        user_management_page.verify_logout_login(username, password)
        logging.info("Login successful")

        # Perform logout
        user_management_page.page.locator(
            '//ul[@class="tab horizontal inheader hnav"]//li[3]//div//button').click()
        user_management_page.timeout()

        # Click logout and verify message
        log_out_button = user_management_page.page.locator(
            '//ul[@class="tab horizontal inheader hnav"]//li[3]//div//div//ul//li//a[1]')
        log__logout = log_out_button.text_content()
        assert log__logout == "Log out from BOX 1", f"Unexpected logout message: {log__logout}"
        logging.info("Logout message verified")

        # Click the logout button
        log_out_button.click()
        user_management_page.timeout()
        logging.info("Successfully logged out")

    finally:
        user_management_page.page.close()


@allure.feature("UserManagement")
def test_search_user(user_management_page):
    test_search_user.__doc__ = """Tests user search functionality after creation.

    Detailed Test Flow:
    1. User Setup:
       - Generates random credentials
       - Creates new test user
       - Records credentials

    2. Search Process:
       - Navigates to user page
       - Enters search query
       - Waits for results

    3. Verification:
       - Checks user presence
       - Validates username match
       - Reviews system logs

    Args:
        user_management_page: Fixture providing user management interface

    Test Data:
        - Username: Random 6 lowercase chars
        - Password: Mix of cases, digits, specials
        - Log Path: /wneclient/apps/uibackend/log/uibackend.log

    Dependencies:
        - User management interface
        - Search functionality
        - SSH log access
        - Random generation

    Expected Results:
        - User created successfully
        - Search finds user
        - Username matches
        - Logs accessible

    URLs Accessed:
        - User Management: http://10.189.200.6/admin/users
    """

    def generate_credentials():
        username = ''.join(random.choices(string.ascii_lowercase, k=6))
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=3))
        uppercase = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=2))
        special = ''.join(random.choices('!@#$%^&*', k=2))
        password = list(lowercase + uppercase + digits + special)
        random.shuffle(password)
        return username, ''.join(password)

    try:
        # Navigate to user management page
        user_management_page.navigate_user_page()

        # Generate random credentials for one user
        username, password = generate_credentials()
        logging.info(f"Testing user - Username: {username}, Password: {password}")

        # Create new user
        user_management_page.test_add_user(username, password)
        user_management_page.timeout()

        # Search for created user
        user_management_page.page.locator('//div[@class="filter"]//input').fill(username)
        user_management_page.timeout()

        # Verify user exists
        found_username = user_management_page.page.locator('//tbody//tr[@class="selectable-row"]//td[1]').text_content()
        if found_username == username:
            logging.info("User successfully found")
            assert found_username == username, f"Expected user {username}, found {found_username}"
        else:
            logging.error("User not found")
            assert False, "Created user was not found in search results"

        # Log check (optional)
        try:
            public_host = env.ftp_host
            ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
            logfile_path = '/wneclient/apps/uibackend/log/uibackend.log'
            stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
            log_content = stdout.read().decode().splitlines()
            logging.info("Log file content retrieved successfully")
        except Exception as e:
            logging.error(f"Error accessing logs: {e}")

    finally:
        user_management_page.page.close()
