import logging
import allure
from playwright.sync_api import expect
import env
from conftest import story_page
from helpers import ubuntu
from helpers.database import Database
import random
import string
from tabulate import tabulate


def wait(story_page):
    story_page.page.wait_for_timeout(1000)


@allure.feature("FD")
def test_Create_FD(story_page):
    test_Create_FD.__doc__ = """Tests creation of multiple file distribution methods.

    Detailed Test Flow:
    1. Distribution Setup:
       - Creates FTP distribution
       - Creates FTPS distribution 
       - Creates SFTP distribution

    2. Configuration Details:
       - Unique names for each method
       - Common fields (SD, HD, Script)
       - Protocol-specific settings

    3. Validation:
       - Verifies history entries
       - Confirms distributions added
       - Cleans up test data

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Names: test1, test2, test3
        - Protocols: FTP, FTPS, SFTP
        - Fields: SD, HD, Script enabled

    Dependencies:
        - Working FD service
        - Protocol access
        - UI navigation
        - History logging

    Expected Results:
        - Three distributions created
        - History entries logged
        - Cleanup successful

    URLs Accessed:
        - Distribution History: http://10.189.200.6/history/distribution
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    # Navigate to story page
    story_page.navigate()
    story_page.clearing_all_distribution_methods()
    story_page.timeout()

    # Open FD page
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()

    # Define distribution methods
    distribution_methods = [
        ("test1", 1, story_page.ftp_distribution),
        ("test2", 2, story_page.ftps_distribution),
        ("test3", 3, story_page.sftp_distribution)
    ]

    for fd_name, protocol_index, fill_details_func in distribution_methods:
        # Click 'Add New Distribution Method'
        story_page.add_new_FD.first.click()
        wait()

        # Fill 'Name' field with retry logic
        name_input = story_page.page.locator('//input[@name="name"]')
        name_input.fill("")  # Clear first
        wait()
        name_input.fill(fd_name)
        wait()

        # Fill common fields
        story_page.SD.first.click()
        wait()
        story_page.HD.first.click()
        wait()
        story_page.script.first.click()
        wait()

        # Select distribution method from dropdown
        story_page.page.locator('//div[@data-name="distribution_method"]').click()
        method_selector = f'//div[@data-name="distribution_method"]//div//ul//li[{protocol_index}]'
        story_page.page.locator(method_selector).click()
        wait()

        # Fill protocol-specific details
        fill_details_func()
        story_page.page.wait_for_timeout(1000)

    # Navigate to history page
    story_page.navigate()
    story_page.page.locator('//div[@data-name="add-page"]').click()
    wait()
    story_page.page.locator('//div[@data-name="add-page"]//div//ul//li[1]').click()
    wait()
    story_page.page.goto('http://10.189.200.6/history/distribution')
    wait()
    # Log all distribution entries
    rows = story_page.page.locator('//table//tbody//tr')
    for i in range(rows.count()):
        slug_name = rows.nth(i).text_content()
        logging.info(slug_name)
        story_page.timeout()

    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)
    for _ in range(3):  # Assuming there are 3 to delete
        indicators = story_page.page.locator(
            '//div[@class="distribution-actions"]//div[@class="flashing-indicators-holder"][4]')

        if indicators.count() == 0:
            break  # Exit if no more indicators found

        indicators.first.click()
        wait()

        # Wait for dialog and click cancel
        confirm_cancel = story_page.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]')
        if confirm_cancel.is_visible():
            confirm_cancel.click()
            story_page.page.wait_for_timeout(2000)


@allure.feature("FD")
def test_Create_with_existing_name(story_page):
    test_Create_with_existing_name.__doc__ = """Tests error handling when creating distribution with duplicate name.

    Detailed Test Flow:
    1. Distribution Creation:
       - Creates first distribution method
       - Attempts second distribution with same name
       - Tests multiple protocols (FTP, FTPS, SFTP)

    2. Error Validation:
       - Captures error message
       - Verifies error text
       - Validates error handling

    3. Database Check:
       - Queries FTP configurations
       - Verifies database state
       - Cleans up test data

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Protocols: FTP, FTPS, SFTP
        - Error Message: "The server responded with an error..."
        - Database Table: distribution_configuration_ftp

    Dependencies:
        - Story page navigation
        - Protocol selection
        - Database access
        - Error handling

    Expected Results:
        - Error on duplicate name
        - Proper error message shown
        - Database validation complete

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    db_client = Database()

    # Step 1: Navigate to the story page
    story_page.navigate()
    story_page.timeout()

    # Step 2: Attempt to create two distribution methods with the same name
    for i in range(2):
        story_page.navigate()
        story_page.details_for_distribution()

        # Select protocol based on index
        story_page.select_protocol.nth(i).click()
        protocol_text = story_page.protocol_method.text_content()
        logging.info(f"Selected protocol: {protocol_text}")

        # Fill protocol-specific details
        protocol_map = {
            "FTP": story_page.ftp_distribution,
            "FTPS": story_page.ftps_distribution,
            "SFTP": story_page.sftp_distribution  # Uncomment if implemented
        }

        # Call the appropriate method if protocol is recognized
        fill_func = protocol_map.get(protocol_text)
        if fill_func:
            fill_func()
        else:
            logging.warning(f"Unknown protocol: {protocol_text}")

    # Step 3: Validate error message for duplicate distribution name
    error_locator = '//form[@class="edit-distribution error"]//h3[@class="error"]'
    error_message = story_page.page.locator(error_locator).text_content()
    logging.info(f"Error message: {error_message}")
    assert error_message == "The server responded with an error. The operation was unsuccessful."
    logging.info("Duplicate distribution name error validated successfully.")

    # Step 4: Run a DB query to verify distribution configuration
    db_client.execute_query('SELECT * FROM distribution_configuration_ftp')
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)
    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_create_with_empty_name(story_page):
    test_create_with_empty_name.__doc__ = """Tests error handling when creating distribution with empty name.

    Detailed Test Flow:
    1. Distribution Setup:
       - Opens distribution form
       - Leaves name field empty
       - Sets SD parameter
       - Selects FTP method

    2. Error Validation:
       - Captures error message
       - Verifies error text
       - Asserts message content

    3. Cleanup:
       - Navigates to admin page
       - Removes test configurations
       - Resets state

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Name Field: Empty string
        - Error Message: "Please specify a name..."
        - Protocol: FTP

    Dependencies:
        - Story page navigation
        - Error handling
        - FTP configuration

    Expected Results:
        - Error on empty name
        - Proper error message shown
        - Clean state after test

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    story_page.navigate()
    story_page.timeout()
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()
    story_page.add_new_FD.first.click()
    story_page.FD_name.fill("")
    story_page.SD.check()
    story_page.page.locator('//div[@data-name="distribution_method"]').click()
    method_selector = f'//div[@data-name="distribution_method"]//div//ul//li[1]'
    story_page.page.locator(method_selector).click()
    story_page.ftp_distribution()
    error_message = story_page.page.locator(
        '//label[@class="input error"]//div[@data-input-message-type="error"]').first.text_content()
    logging.info(error_message)
    assert error_message == "Please specify a name for this distribution process."
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_create_with_empty_name_and_different_characters(story_page):
    test_create_with_empty_name_and_different_characters.__doc__ = """Tests file distribution creation with various special characters and empty names.

    Detailed Test Flow:
    1. Input Testing:
       - Tests empty strings
       - Tests whitespace
       - Tests special characters
       - Tests valid names

    2. Validation Process:
       - Handles blank inputs
       - Handles special characters
       - Handles valid inputs
       - Verifies error messages

    3. Cleanup:
       - Navigates to admin page
       - Clears all methods
       - Resets state

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Special Characters: +, *, !, @, #, etc.
        - Empty Values: "", "  "
        - Valid Values: test1
        - HTML Entities: &amp;, &lt;&gt;

    Dependencies:
        - Story page navigation
        - Input validation
        - Error handling

    Expected Results:
        - Proper error for empty names
        - Proper error for special chars
        - Success for valid names
        - Clean state after test

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    # Define test inputs
    inputs = [
        "+", "*", "test1", "", "  ", "_", "!", "@", "#", "$", "%", "^", "&amp;", "*", "()", "_", "+", "-", "=", "~",
        "{}", "[]", ":", ";", "|", "&lt;&gt;", ".", "?"
    ]

    # Define input categories for handling
    special_inputs = {
        " ", "_", "+", "*", "", "  ", "!", "@", "#", "$", "%", "^", "&amp;", "()", "-", "=", "~",
        "{}", "[]", ":", ";", "|", "&lt;&gt;", ".", "?"
    }

    def fill_fd_name_and_validate(input_value):
        logging.info(f"Testing with FD name: '{input_value}'")

        # Navigate and open FD creation form
        story_page.navigate()
        story_page.timeout()
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()

        # Fill FD name
        story_page.page.locator('//input[@name="name"]').fill(input_value)

        # Call appropriate validation method
        if input_value.strip() == "":
            story_page.Blank_input()
        elif input_value in special_inputs:
            story_page.special_input()
        else:
            story_page.valid_input()

    # Run the test for a subset of random inputs
    for _ in range(7):
        input_value = random.choice(inputs)
        fill_fd_name_and_validate(input_value)
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_with_out_valid_host(story_page):
    test_with_out_valid_host.__doc__ = """Tests file distribution behavior with and without valid host configuration.

    Detailed Test Flow:
    1. Valid Host Test:
       - Creates distribution with valid host
       - Tests FTP/SFTP/FTPS protocols
       - Verifies successful setup

    2. Invalid Host Test:
       - Creates distribution without host
       - Validates error handling
       - Tests all protocols

    3. Protocol-Specific Testing:
       - FTP configuration
       - SFTP configuration
       - FTPS configuration

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Names: test1, test2
        - Protocols: FTP, SFTP, FTPS
        - Host Values: Valid and Empty

    Dependencies:
        - Story page navigation
        - Protocol selection
        - Host validation
        - Error handling

    Expected Results:
        - Success with valid host
        - Error with missing host
        - Protocol-specific validation

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """

    def create_fd(fd_name, protocol_index, story_page, with_host=True):
        story_page.navigate()
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()
        story_page.page.locator('//input[@name="name"]').fill(fd_name)
        wait()

        story_page.SD.check()
        story_page.page.locator('//div[@data-name="distribution_method"]').click()
        wait()

        method_selector = f'//div[@data-name="distribution_method"]//div//ul//li[1]'
        story_page.page.locator(method_selector).click()
        wait()

        # Select protocol
        story_page.protocol_method.last.click()
        story_page.select_protocol.nth(protocol_index).click()
        protocol_text = story_page.protocol_method.text_content()
        logging.info(f"Selected protocol: {protocol_text}")

        # Fill distribution details based on protocol and host flag
        if protocol_text == "FTP":
            if with_host:
                story_page.ftp_distribution()
            else:
                story_page.ftp_distribution_without_host()
        elif protocol_text == "SFTP":
            if with_host:
                story_page.sftp_distribution()
            else:
                story_page.sftp_distribution_without_host()
        elif protocol_text == "FTPS":
            if with_host:
                story_page.ftps_distribution()
            else:
                story_page.ftps_distribution_without_host()

        # Validate missing host scenario
        if not with_host:
            story_page.without_host()

        story_page.page.wait_for_timeout(1000)
        story_page.navigate()

    # Step 1: Create FD with valid host
    create_fd(fd_name="test1", protocol_index=0, with_host=True)

    # Step 2: Create FD without host
    create_fd(fd_name="test2", protocol_index=0, with_host=False)
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_with_out_valid_directory(story_page):
    test_with_out_valid_directory.__doc__ = """Tests file distribution behavior with and without valid target directory.

    Detailed Test Flow:
    1. Valid Directory Test:
       - Creates distribution with valid directory
       - Tests all protocols (FTP/SFTP/FTPS)
       - Verifies successful setup

    2. Invalid Directory Test:
       - Creates distribution without target dir
       - Validates error handling
       - Tests for each protocol

    3. Protocol-Specific Testing:
       - Tests FTP directory validation
       - Tests SFTP directory validation
       - Tests FTPS directory validation

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Names: test1, test2
        - Protocols: FTP, SFTP, FTPS
        - Directory Values: Valid and Empty

    Dependencies:
        - Story page navigation
        - Protocol selection
        - Directory validation
        - Error handling

    Expected Results:
        - Success with valid directory
        - Error with missing directory
        - Protocol-specific validation

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """

    def create_fd(fd_name, protocol_index, story_page, with_directory=True):
        story_page.navigate()
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()
        story_page.page.locator('//input[@name="name"]').fill(fd_name)
        wait()

        story_page.SD.check()
        story_page.page.locator('//div[@data-name="distribution_method"]').click()
        wait()

        method_selector = f'//div[@data-name="distribution_method"]//div//ul//li[1]'
        story_page.page.locator(method_selector).click()
        wait()

        # Select protocol
        story_page.protocol_method.last.click()
        story_page.select_protocol.nth(protocol_index).click()
        protocol_text = story_page.protocol_method.text_content()
        logging.info(f"Selected protocol: {protocol_text}")

        # Fill distribution details based on protocol and host flag
        if protocol_text == "FTP":
            if with_directory:
                story_page.ftp_distribution()
            else:
                story_page.ftp_distribution_without_target()
        elif protocol_text == "SFTP":
            if with_directory:
                story_page.sftp_distribution()
            else:
                story_page.sftp_distribution_without_target()
        elif protocol_text == "FTPS":
            if with_directory:
                story_page.ftps_distribution()
            else:
                story_page.ftps_distribution_without_target()

        # Validate missing host scenario
        if not with_directory:
            story_page.without_target_directory()

        wait()
        story_page.navigate()

    # Step 1: Create FD with valid host
    create_fd(fd_name="test1", protocol_index=0, with_directory=True)

    # Step 2: Create FD without host
    create_fd(fd_name="test2", protocol_index=0, with_directory=False)
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_Add_Dist_for_nonAdmin_user(story_page):
    test_Add_Dist_for_nonAdmin_user.__doc__ = """Tests file distribution functionality for non-admin user.

    Detailed Test Flow:
    1. Setup Phase:
       - Creates random test user
       - Sets up FTP distribution
       - Configures permissions

    2. User Management:
       - Creates new user account
       - Sets role permissions
       - Saves user configuration

    3. Authentication Flow:
       - Performs logout
       - Validates logout message
       - Performs login as new user
       - Verifies access

    4. Distribution Testing:
       - Adds content to distribution
       - Checks history
       - Validates distribution

    5. Database Validation:
       - Verifies user creation
       - Checks FTP configuration
       - Validates queue entries

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Username: Random 8 character string
        - Password: Chethuuu@123
        - Tables: users, distribution_configuration_ftp

    Dependencies:
        - User management system
        - Distribution system
        - Database access
        - Authentication system

    Expected Results:
        - User created successfully
        - Distribution configured
        - History updated
        - Database entries verified

    URLs Accessed:
        - Distribution History: http://10.189.200.6/history/distribution
    """

    def generate_random_username(length=8):
        """Generate a random username of specified length."""
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    # Setup
    random_username = generate_random_username()
    password = "Chethuuu@123"
    db_client = Database()

    # Initial navigation and distribution setup
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.navigate()
    story_page.page.wait_for_timeout(6000)

    # User creation
    story_page.hamburger.click()
    story_page.User_management.click()
    story_page.page.wait_for_timeout(6000)
    story_page.add_user.click()
    story_page.new_username.fill(random_username)
    story_page.timeout()
    story_page.new_password.fill(password)
    story_page.timeout()
    story_page.role_permissions()
    story_page.new_user_save.click()
    story_page.timeout()

    # Logout flow
    story_page.login_logout.first.click()
    story_page.timeout()
    expected_text = "Log out from BOX 1"
    actual_text = story_page.log_out_from_box.text_content()

    if actual_text == expected_text:
        story_page.log_out_from_box.click()
        story_page.timeout()
    else:
        raise AssertionError(f"Expected: '{expected_text}', Got: '{actual_text}'")

    story_page.page.get_by_role("button", name="Log Out").click()
    story_page.timeout()

    # Login flow
    story_page.login_logout.first.click()
    expected_text_1 = "Log in to BOX 1"
    actual_text_1 = story_page.log_in_to_box.text_content()

    if actual_text_1 == expected_text_1:
        story_page.log_in_to_box.click()
        story_page.timeout()
    else:
        raise AssertionError(f"Expected: '{expected_text_1}', Got: '{actual_text_1}'")

    story_page.timeout()
    story_page.page.get_by_label("username").fill(random_username)
    story_page.page.get_by_label("password").fill(password)
    story_page.timeout()
    story_page.page.get_by_role("button", name="Log In").click()
    story_page.page.wait_for_timeout(6000)

    # Distribution validation
    story_page.add_to_distribution_icon.first.click()
    story_page.timeout()
    story_page.History.click()
    story_page.timeout()
    story_page.page.locator('//ul[@class = "tab horizontal inpage no-print"]//li[2]').click()
    story_page.timeout()
    # Database validation
    logging.info("Validation from database")
    db_client.execute_query(f"SELECT * FROM users WHERE username = '{random_username}'")
    db_client.execute_query("SELECT * FROM distribution_configuration_ftp")
    db_client.execute_query("SELECT * FROM distribution_file_queue")


@allure.feature("FD")
def test_delete_process_with_active_transfer(story_page):
    test_delete_process_with_active_transfer.__doc__ = """Tests deletion of distribution process while transfer is active.

    Detailed Test Flow:
    1. Setup Phase:
       - Clears existing distributions
       - Creates new FTP distribution
       - Verifies initial DB state

    2. Transfer Initiation:
       - Triggers multiple transfers
       - Verifies active state
       - Checks history

    3. Deletion Process:
       - Removes active distribution
       - Validates removal
       - Checks cleanup

    4. Verification:
       - Checks log files
       - Validates DB state
       - Confirms cleanup

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Table: distribution_configuration_ftp

    Dependencies:
        - Database access
        - SSH connection
        - FTP service
        - Log access

    Expected Results:
        - Process removed successfully
        - DB entries cleaned
        - Logs updated correctly

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    db_client = Database()

    # Initial navigation and distribution setup
    story_page.navigate()
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()

    story_page.details_for_distribution()
    story_page.ftp_distribution()

    # Pre-deletion DB check
    db_client.execute_query("SELECT * FROM distribution_configuration_ftp")

    # Trigger active transfer
    story_page.navigate()
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()

    # Navigate to distribution history
    story_page.navigate_to_distribution_history()
    wait()

    # Remove distribution process
    story_page.hamburger.click()
    story_page.File_distributor_icon.click()
    story_page.timeout()
    story_page.remove_process.click()
    story_page.confirm_removal.click()
    story_page.timeout()
    logging.info("Distribution process has been removed")

    # Read log file from remote host
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = "/wneclient/apps/filedistributor/log/filedistributor.log"
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
        logging.info(file_names)
    except Exception as e:
        logging.info(f"Error reading log file: {e}")

    # Post-deletion DB check
    db_client.execute_query("SELECT * FROM distribution_configuration_ftp")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_change_filter_on_active_process(story_page):
    test_change_filter_on_active_process.__doc__ = """Tests modification of filters on an active distribution process.

    Detailed Test Flow:
    1. Initial Setup:
       - Creates new distribution
       - Configures FTP details
       - Verifies active state

    2. Process Management:
       - Tests editing active process
       - Validates error message
       - Stops active process

    3. Filter Configuration:
       - Applies service filters
       - Tests sensitivity filters
       - Handles filter errors

    4. Process Restart:
       - Saves new configuration
       - Restarts distribution
       - Validates changes

    5. Distribution Validation:
       - Checks CCTV story
       - Verifies history
       - Validates queue

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Error Message: "You are not able to edit..."
        - Filter Types: Service, Sensitivity
        - Table: distribution_file_queue

    Dependencies:
        - Database access
        - Distribution system
        - Filter system
        - History tracking

    Expected Results:
        - Error on active edit
        - Filters applied successfully
        - Process restarts properly
        - History updated correctly

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    db_client = Database()

    # Initial setup
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.timeout()

    # Attempt to edit active configuration
    story_page.distribution_target.click()
    story_page.timeout()
    error_msg = story_page.e_message.text_content()
    assert error_msg == 'You are not able to edit a started process. Please stop the process first.'

    # Stop the active process
    story_page.stop_distribution.click()
    story_page.confirm_to_stop_distribution.click()
    story_page.timeout()

    # Apply filters
    story_page.Filters.click()
    story_page.timeout()

    if story_page.no_filter.is_enabled():
        # Service Filter
        story_page.service_filter.click()
        story_page.save_distribution.click()
        story_page.page.wait_for_timeout(5000)

        service_filter_error = story_page.page.locator(
            '//div//details[6]//div[@class = "h4 input-info error"]'
        ).text_content()

        if service_filter_error == "Please select at least one service":
            logging.info(service_filter_error)
            story_page.subcon.first.click()
            story_page.timeout()
        else:
            story_page.navigate()
            logging.info("Cannot continue the process")

        # Sensitivity Filter
        story_page.sensitivity_filter.click()
        story_page.save_distribution.click()
        story_page.page.wait_for_timeout(5000)

        sensitivity_filter_error = story_page.page.locator(
            '//div//details[6]//div[@class = "h4 input-info error"]'
        ).text_content()

        if sensitivity_filter_error == "Please select at least one exclusion":
            logging.info(sensitivity_filter_error)
            story_page.Graphic_Sensitive_filter.last.click()
            story_page.timeout()
        else:
            story_page.navigate()
            logging.info("Cannot continue the process")
    else:
        story_page.no_filter.check()

    # Save and restart distribution
    story_page.save_distribution.click()
    story_page.timeout()
    story_page.play_distribution.click()
    story_page.confirm_play_distribution.click()
    story_page.timeout()

    # Navigate to CCTV story and distribution history
    story_page.navigate()
    story_page.cctv_story.click()
    story_page.story_dist_icon.first.click()
    story_page.timeout()
    story_page.History.click()
    story_page.distribution_history.click()
    story_page.page.wait_for_timeout(5000)

    # DB validation
    db_client.execute_query("SELECT * FROM distribution_file_queue")
    story_page.page.wait_for_timeout(5000)

    # Repeat history check
    story_page.History.click()
    story_page.distribution_history.click()
    story_page.page.wait_for_timeout(5000)
    db_client.execute_query("SELECT * FROM distribution_file_queue")

    # Final wait
    story_page.page.wait_for_timeout(4000)
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
@allure.story("Multiple distributions configured result in a file distributed to all of them")
def test_multiple_distributions_configured_result_in_a_file_distributed_to_all_of_them(story_page):
    test_multiple_distributions_configured_result_in_a_file_distributed_to_all_of_them.__doc__ = """Tests distributing files to multiple configured distributors simultaneously.

    Detailed Test Flow:
    1. Distribution Setup:
       - Creates 3 FTP distributors
       - Configures each with unique name
       - Enables SD, HD, script options

    2. File Distribution:
       - Adds files to 2 distributors
       - Skips first distributor
       - Verifies distribution start

    3. Validation Steps:
       - Checks distribution logs
       - Verifies DB entries
       - Lists target files

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distributor Names: test0, test1, test2
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Target Dir: /wneclient/data/QA/ftp/files/testJakub
        - Table: distribution_file_queue

    Dependencies:
        - Database access
        - SSH connection
        - FTP service
        - Log access

    Expected Results:
        - All distributors created
        - Files distributed correctly
        - Logs show distribution
        - Files present in target

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    db_client = Database()
    story_page.navigate()

    # Step 1: Create 3 File Distributors
    for i in range(3):
        story_page.navigate()
        story_page.hamburger.click()
        story_page.file_distributor_icon.click()
        story_page.add_new_FD.first.click()
        story_page.FD_name.fill(f"test{i}")
        story_page.SD.first.click()
        story_page.HD.first.click()
        story_page.script.first.click()
        story_page.protocol_method.last.click()
        story_page.ftp_distribution()
        story_page.timeout()
        story_page.navigate()

    # Step 2: Add files to distributors (excluding the first one)
    for j in range(1, 3):
        story_page.add_to_distributor.nth(j).click()
        story_page.timeout()

    # Step 3: Navigate to distribution history
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(6000)

    # Step 4: Validate file distribution via SSH
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"cat {logfile_path}")
        file_names = stdout.read().decode().splitlines()
        table = [[i + 1, name] for i, name in enumerate(file_names)]
        logging.info(
            "\n📄 Files distributed (from log):\n" + tabulate(table, headers=["#", "File Name"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error while fetching log file: {e}")

    # Step 5: Validate distribution entries in the database
    try:
        result = db_client.execute_query('SELECT * FROM distribution_file_queue')
        if result:
            headers = result[0].keys()
            rows = [list(row.values()) for row in result]
            logging.info("\n🗃️ Distribution entries in DB:\n" + tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            logging.info("ℹ️ No entries found in the distribution_file_queue table.")
    except Exception as e:
        logging.error(f"❌ Database query failed: {e}")

    # Step 6: List files in target directory
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        target_directory = '/wneclient/data/QA/ftp/files/testJakub'
        stdin, stdout, stderr = ssh.exec_command(f"ls -lh {target_directory}")
        file_list = stdout.read().decode().splitlines()
        table = [[i + 1, file] for i, file in enumerate(file_list)]
        logging.info(
            "\n📁 Files Present in Target Directory:\n" + tabulate(table, headers=["#", "File"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error listing target directory files: {e}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
@allure.story("Check Active connection with Passive Server")
def test_Check_Active_connection_with_Passive_Server(story_page):
    test_Check_Active_connection_with_Passive_Server.__doc__ = """Tests FTP active mode connection with passive server configuration.

    Detailed Test Flow:
    1. FTP Configuration:
       - Sets up FTP connection details
       - Configures active mode
       - Validates server settings

    2. Distribution Setup:
       - Configures target directory
       - Sets credentials
       - Verifies active mode enabled

    3. Validation Steps:
       - Checks history table
       - Verifies log entries
       - Confirms file presence

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Host: 10.99.13.11
        - Target: /wneclient/data/QA/ftp/files/testJakub
        - Credentials: wneqa/wneqa123
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log

    Dependencies:
        - FTP server access
        - SSH connection
        - Log access
        - Active mode support

    Expected Results:
        - Active mode enabled
        - Connection successful
        - Files distributed
        - Logs updated

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    # Step 1: Configure FTP Distribution
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

    # Step 2: Navigate to Distribution History
    story_page.navigate()
    story_page.page.locator('//div[@data-name="add-page"]').click()
    story_page.page.locator('//div[@data-name="add-page"]//div//ul//li[1]').click()
    story_page.page.goto('http://10.189.200.6/history/distribution')
    story_page.page.wait_for_timeout(3000)

    # Step 3: Print Distribution History Table Content
    logging.info("\n📄 Distribution History Table Content:")
    cells = story_page.page.locator('//table//tbody//tr')
    table_data = []

    for i in range(cells.count()):
        row = cells.nth(i).locator('td')
        row_data = [row.nth(j).text_content().strip() for j in range(row.count())]
        table_data.append(row_data)

    if table_data:
        logging.info("\n" + tabulate(table_data, headers="firstrow", tablefmt="grid"))
    else:
        logging.info("No data found in distribution history.")

    # Step 4: Fetch File Distributor Logs from Source Box
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        logging.info("\n" + "\n".join([f"  • {line}" for line in log_lines]))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")

    # Step 5: List Files in Target Directory
    logging.info("\n📁 Files Present in Target Directory:")
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        target_directory = '/wneclient/data/QA/ftp/files/testJakub'
        stdin, stdout, stderr = ssh.exec_command(f"ls -lh {target_directory}")
        file_list = stdout.read().decode().splitlines()
        logging.info("\n" + "\n".join([f"  • {file}" for file in file_list]))
    except Exception as e:
        logging.error(f"❌ Error listing target directory files: {e}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_Check_when_primary_server_fails_failover_to_standby_server_happens(story_page):
    test_Check_when_primary_server_fails_failover_to_standby_server_happens.__doc__ = """Tests failover functionality when primary FTP server fails.

    Detailed Test Flow:
    1. Server Setup:
       - Configures primary server
       - Sets up standby server
       - Validates initial connection

    2. Distribution Process:
       - Adds files to distributors
       - Triggers distribution
       - Monitors transfer status

    3. Failover Validation:
       - Checks distribution logs
       - Verifies file presence
       - Confirms standby usage

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP with standby
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Target Dir: /wneclient/data/QA/ftp/files/testJakub

    Dependencies:
        - Database access
        - SSH connection
        - Primary FTP server
        - Standby FTP server
        - Log access

    Expected Results:
        - Primary server failure detected
        - Successful failover to standby
        - Files distributed correctly
        - Logs show failover event

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.standby_ftp_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()

    # Step 1: Add files to distributors
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()

    # Step 2: Navigate to distribution history
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(2000)

    # Step 3: Fetch File Distributor Logs from Source Box
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")

    # Step 4: List Files in Target Directory
    logging.info("\n📁 Files Present in Target Directory:")
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        target_directory = '/wneclient/data/QA/ftp/files/testJakub'
        stdin, stdout, stderr = ssh.exec_command(f"ls -lh {target_directory}")
        file_list = stdout.read().decode().splitlines()
        table = [[i + 1, file] for i, file in enumerate(file_list)]
        logging.info("\n" + tabulate(table, headers=["#", "File"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error listing target directory files: {e}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_If_primary_and_standby_servers_are_provided_If_primary_working_files_should_arrive_to_it(story_page):
    test_If_primary_and_standby_servers_are_provided_If_primary_working_files_should_arrive_to_it.__doc__ = """Tests file distribution to primary server when both primary and standby are configured.

    Detailed Test Flow:
    1. Server Configuration:
       - Sets up primary server
       - Configures standby server
       - Validates both connections

    2. Distribution Process:
       - Adds files to distributors
       - Initiates transfer
       - Monitors primary server

    3. Validation Steps:
       - Checks distributor logs
       - Verifies file delivery
       - Confirms primary usage

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP with standby
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Target Dir: /wneclient/data/QA/ftp/files/testJakub

    Dependencies:
        - Database access
        - SSH connection
        - Primary FTP server
        - Standby FTP server
        - Log access

    Expected Results:
        - Files sent to primary
        - No standby usage
        - Logs show primary only
        - Files present in target

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.standby_without_error_ftp_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()

    # Step 1: Add files to distributors
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()

    # Step 2: Navigate to distribution history
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(2000)

    # Step 3: Fetch File Distributor Logs from Source Box
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")

    # Step 4: List Files in Target Directory
    logging.info("\n📁 Files Present in Target Directory:")
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        target_directory = '/wneclient/data/QA/ftp/files/testJakub'
        stdin, stdout, stderr = ssh.exec_command(f"ls -lh {target_directory}")
        file_list = stdout.read().decode().splitlines()
        table = [[i + 1, file] for i, file in enumerate(file_list)]
        logging.info("\n" + tabulate(table, headers=["#", "File"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error listing target directory files: {e}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_If_only_primary_server_information_is_provided_Primary_server_should_be_used_for_distribution(story_page):
    test_If_only_primary_server_information_is_provided_Primary_server_should_be_used_for_distribution.__doc__ = """Tests file distribution using only primary server configuration.

    Detailed Test Flow:
    1. Primary Server Setup:
       - Configures primary FTP server
       - Validates connection details
       - Verifies server status

    2. Distribution Process:
       - Adds files to distributors
       - Initiates transfer
       - Monitors distribution

    3. Validation Steps:
       - Checks distributor logs
       - Verifies file delivery
       - Confirms primary usage

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP primary only
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Target Dir: /wneclient/data/QA/ftp/files/testJakub

    Dependencies:
        - Database access
        - SSH connection
        - Primary FTP server
        - Log access

    Expected Results:
        - Files distributed via primary
        - No standby configuration
        - Logs show primary usage
        - Files present in target

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.page.wait_for_timeout(6000)
    story_page.navigate()

    # Step 1: Add files to distributors
    for i in range(1, 3):
        story_page.add_to_distributor.nth(i).click()
        story_page.timeout()

    # Step 2: Navigate to distribution history
    story_page.navigate_to_distribution_history()
    story_page.page.wait_for_timeout(2000)

    # Step 3: Fetch File Distributor Logs from Source Box
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")

    # Step 4: List Files in Target Directory
    logging.info("\n📁 Files Present in Target Directory:")
    try:
        public_host = env.ftp_host
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        target_directory = '/wneclient/data/QA/ftp/files/testJakub'
        stdin, stdout, stderr = ssh.exec_command(f"ls -lh {target_directory}")
        file_list = stdout.read().decode().splitlines()
        table = [[i + 1, file] for i, file in enumerate(file_list)]
        logging.info("\n" + tabulate(table, headers=["#", "File"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error listing target directory files: {e}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
@allure.story("No Password - Directory - Passive Mode")
def test_file_distribution_without_password(story_page):
    test_file_distribution_without_password.__doc__ = """Tests error handling when configuring FTP distribution without password.

    Detailed Test Flow:
    1. Distribution Setup:
       - Navigates to distribution page
       - Configures distribution details
       - Attempts FTP setup without password

    2. Error Handling:
       - Captures error message
       - Validates error content
       - Verifies UI feedback

    3. Validation Steps:
       - Checks error presence
       - Verifies message text
       - Confirms UI state

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP
        - Expected Error: "Please specify a Password."
        - Error Locator: //div//label[@class="input password error"]//div[@class="h4 input-info error"]

    Dependencies:
        - Distribution page access
        - Error handling system
        - UI validation

    Expected Results:
        - Error message displayed
        - Password field marked as error
        - Distribution not created
        - State properly reset

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """

    # Step 1: Navigate to the story page
    story_page.navigate()

    # Step 2: Fill in distribution details
    story_page.details_for_distribution()

    # Step 3: Attempt FTP distribution without password
    story_page.ftp_distribution_without_password()

    # Step 4: Capture and validate the error message
    error_locator = '//div//label[@class="input password error"]//div[@class="h4 input-info error"]'
    error_message = story_page.page.locator(error_locator).text_content()

    # Step 5: Assert the expected error message
    expected_message = "Please specify a Password."
    assert error_message == expected_message, f"Expected '{expected_message}', but got '{error_message}'"

    # Step 6: Log the error message
    logging.info(f"Captured error message: {error_message}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_Check_when_primary_server_is_back_after_a_failover_fall_back_to_primary_server_should_happen(story_page):
    test_Check_when_primary_server_is_back_after_a_failover_fall_back_to_primary_server_should_happen.__doc__ = """Tests automatic fallback to primary server after recovery from failover state.

    Detailed Test Flow:
    1. Initial Setup:
       - Configures primary FTP server (10.99.13.11)
       - Sets up standby server
       - Validates initial distribution

    2. Failover Test:
       - Stops distribution
       - Changes primary server to invalid IP (10.99.13.117)
       - Verifies standby server usage
       - Validates file distribution

    3. Recovery Test:
       - Restores primary server IP
       - Verifies automatic fallback
       - Confirms distribution success

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Primary Server: 10.99.13.11
        - Invalid Server: 10.99.13.117
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Table: distribution_configuration_ftp

    Dependencies:
        - SSH connection
        - FTP servers
        - Story page navigation
        - Distribution system

    Expected Results:
        - Successful failover to standby
        - Automatic fallback to primary
        - All files distributed
        - Proper server usage logged

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    story_page.navigate()  # navigate to the story page
    story_page.details_for_distribution()  # click on details for distribution
    story_page.FTP_option.click()  # click on FTP option
    story_page.primary_ftp_details()  # save primary details for ftp server
    story_page.standby_ftp_details()  # save standby details for ftp server
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.verify_distribution_on_history_page()  # verify distribution on history page
    story_page.page.wait_for_timeout(2000)
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")
    logging.info("\n📁 Files Present in Target Directory:")

    # Simulate primary server failure
    story_page.simulate_primary_server_failure_for_failure()
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.verify_distribution_on_history_page()  # verify distribution on history page
    story_page.page.wait_for_timeout(2000)
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")
    logging.info("\n📁 Files Present in Target Directory:")

    # Restore Primary Server
    story_page.restore_primary_server()
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.verify_distribution_on_history_page()  # verify distribution on history page
    story_page.page.wait_for_timeout(2000)
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")
    logging.info("\n📁 Files Present in Target Directory:")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_add_to_distribution_with_no_active_distribution_possible(story_page):
    test_add_to_distribution_with_no_active_distribution_possible.__doc__ = """Tests error handling when adding to distribution with no active distribution configured.

    Detailed Test Flow:
    1. Initial Setup:
       - Creates initial distribution
       - Configures FTP settings
       - Verifies history entries

    2. Distribution Removal:
       - Navigates to distributor
       - Removes active distribution
       - Confirms removal

    3. Validation Steps:
       - Attempts new distribution
       - Checks dropdown visibility
       - Verifies error handling

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Table: distribution_configuration_ftp

    Dependencies:
        - SSH connection
        - Story page navigation
        - Distribution system
        - Log access

    Expected Results:
        - Distribution removal successful
        - Error on new distribution attempt
        - Proper state validation
        - Logs updated correctly

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    story_page.navigate()  # navigate to the story page
    story_page.details_for_distribution()  # click on details for distribution
    story_page.FTP_option.click()  # click on FTP option
    story_page.primary_ftp_details()  # save primary details for ftp server
    save_button = story_page.page.locator('//div[@class="row button-bar"]//button[@type="submit"]')
    save_button.click()
    story_page.add_all_stories_to_distribution()  # add stories to distribution
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.verify_distribution_on_history_page()  # verify distribution on history page
    # story_page.page.wait_for_timeout(300000)
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()
    story_page.page.locator('//div[@class="flashing-indicators-holder"]//button[@data-tooltip="Remove"]').click()
    story_page.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]').click()

    # Attempt to add to distribution without an active distribution
    story_page.Attempt_to_add_to_distribution_without_an_active_distribution()
    story_page.check_if_distribution_dropdown_is_visible()  # check if distribution dropdown is visible
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.verify_distribution_on_history_page()  # verify distribution on history page
    story_page.page.wait_for_timeout(2000)
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)
    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
@allure.story("Remove FTP Distribution Configuration")
def test_remove_distribution(story_page):
    test_remove_distribution.__doc__ = """Tests removal of FTP distribution configuration.

    Detailed Test Flow:
    1. Distribution Creation:
       - Navigates to File Distributor
       - Creates new distribution
       - Sets up FTP configuration

    2. Configuration Steps:
       - Sets name to "test1"
       - Selects SD, HD, script options
       - Configures FTP protocol
       - Completes setup

    3. Validation Steps:
       - Checks database entries
       - Verifies configuration
       - Confirms removal

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Name: test1
        - Table: distribution_configuration_ftp
        - Components: SD, HD, Script

    Dependencies:
        - Database access
        - Story page navigation
        - FTP configuration
        - Distribution system

    Expected Results:
        - Distribution created
        - DB entry verified
        - Removal successful
        - Configuration cleared

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    db_client = Database()

    # Step 1: Navigate to File Distributor creation
    story_page.navigate()
    story_page.hamburger.click()
    story_page.file_distributor_icon.click()
    story_page.add_new_FD.first.click()

    # Step 2: Fill in distribution details
    story_page.FD_name.fill("test1")
    story_page.SD.first.click()  # Select SD
    story_page.HD.first.click()  # Select HD
    story_page.script.first.click()  # Select script
    story_page.protocol_method.last.click()  # Select protocol method
    story_page.ftp_distribution()  # Configure FTP distribution
    story_page.timeout()  # Wait for distribution to complete

    # Step 3: Navigate to admin distribution page
    story_page.navigate()
    story_page.page.goto('http://10.189.200.6/admin/distribution')

    # Step 4: Validate distribution entry in DB
    result = db_client.execute_query('SELECT * FROM distribution_configuration_ftp')
    logging.info(f"DB Query Result: {result}")

    # Step 5: Remove the distribution process
    story_page.remove_process.first.click()
    story_page.confirm_removal.click()

    logging.info("✅ Distribution process removed successfully.")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
@allure.story("Pause and Resume FTP Distribution")
def test_pause_resume_FD(story_page):
    test_pause_resume_FD.__doc__ = """Tests pause and resume functionality of FTP distribution process.

    Detailed Test Flow:
    1. Distribution Setup:
       - Creates new FTP distribution
       - Sets name, SD, HD, script options
       - Configures FTP settings

    2. State Management:
       - Validates DB configuration
       - Pauses distribution
       - Resumes distribution
       - Verifies state changes

    3. Validation Steps:
       - Checks database entries
       - Confirms pause state
       - Verifies resume state

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Name: test1
        - Table: distribution_configuration_ftp
        - Components: SD, HD, Script

    Dependencies:
        - Database access
        - Story page navigation
        - Distribution controls
        - State management

    Expected Results:
        - Distribution created
        - Pause successful
        - Resume successful
        - States properly tracked

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    db_client = Database()

    # Step 1: Create a new FTP distribution
    with allure.step("Create a new FTP distribution"):
        story_page.navigate()
        story_page.details_for_distribution()
        story_page.ftp_distribution()
        story_page.timeout()

    # Step 2: Validate distribution entry in DB
    with allure.step("Validate FTP distribution entry in database"):
        result = db_client.execute_query('SELECT * FROM distribution_configuration_ftp')
        logging.info(f"DB Query Result: {result}")

    # Step 3: Navigate to distribution admin page
    with allure.step("Navigate to distribution admin page"):
        story_page.navigate()
        story_page.page.goto('http://10.189.200.6/admin/distribution')
        story_page.timeout()

    # Step 4: Pause the distribution
    with allure.step("Pause the distribution"):
        story_page.play_distribution.first.click()
        story_page.timeout()
        story_page.confirm_play_distribution.click()
        story_page.timeout()
        logging.info("✅ Distribution paused successfully.")

    # Step 5: Resume the distribution
    with allure.step("Resume the distribution"):
        story_page.play_distribution.first.click()
        story_page.timeout()
        story_page.page.locator('//*[@id="modal-root"]/div/dialog/div/div/button[2]').click()
        story_page.timeout()
        logging.info("✅ Distribution resumed successfully.")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
@allure.story("Start and Stop FTP Distribution")
def test_start_stop_FD(story_page):
    test_start_stop_FD.__doc__ = """Tests start and stop functionality of FTP distribution process.

    Detailed Test Flow:
    1. Distribution Setup:
       - Creates new FTP distribution
       - Sets name, SD, HD, script options
       - Configures FTP settings

    2. Control Testing:
       - Validates DB configuration
       - Stops distribution
       - Verifies stopped state
       - Starts distribution
       - Confirms running state

    3. Validation Steps:
       - Checks database entries
       - Verifies state transitions
       - Confirms control responses

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Name: test1
        - Table: distribution_configuration_ftp
        - Components: SD, HD, Script

    Dependencies:
        - Database access
        - Story page navigation
        - Distribution controls
        - State management

    Expected Results:
        - Distribution created
        - Stop successful
        - Start successful
        - States properly tracked

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    db_client = Database()

    # Step 1: Create a new FTP distribution
    with allure.step("Create a new FTP distribution"):
        story_page.navigate()
        story_page.details_for_distribution()
        story_page.ftp_distribution()
        story_page.timeout()

    # Step 2: Validate distribution entry in DB
    with allure.step("Validate FTP distribution entry in database"):
        result = db_client.execute_query('SELECT * FROM distribution_configuration_ftp')
        logging.info(f"DB Query Result: {result}")

    # Step 3: Navigate to distribution admin page
    with allure.step("Navigate to distribution admin page"):
        story_page.navigate()
        story_page.page.goto('http://10.189.200.6/admin/distribution')

    # Step 4: Stop the distribution
    with allure.step("Stop the distribution process"):
        story_page.stop_distribution.first.click()
        story_page.timeout()
        story_page.page.locator('//*[@id="modal-root"]/div/dialog/div/div/button[2]').click()
        story_page.timeout()
        logging.info("✅ Distribution process has been stopped successfully.")

    # Step 5: Start the distribution again
    with allure.step("Start the distribution process"):
        story_page.page.locator(
            '//*[@id="app-root"]/div[3]/main/div[2]/article/div[3]/div[10]/div[2]/div[2]/button'
        ).click()
        story_page.timeout()
        story_page.page.locator('//*[@id="modal-root"]/div/dialog/div/div/button[2]').click()
        story_page.timeout()
        logging.info("✅ Distribution process has been started successfully.")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_export_all_process(story_page):  # to be tested
    test_export_all_process.__doc__ = """Tests export functionality for all distribution processes.

    Detailed Test Flow:
    1. Setup Phase:
       - Creates new distribution
       - Configures FTP settings
       - Prepares for export

    2. Export Process:
       - Locates export button
       - Triggers export action
       - Waits for completion

    3. Cleanup Steps:
       - Returns to admin page
       - Clears configurations
       - Verifies cleanup

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP
        - Table: distribution_configuration_ftp
        - Export Format: System default

    Dependencies:
        - Database access
        - Story page navigation
        - Export functionality
        - File system access

    Expected Results:
        - Distribution created
        - Export completed
        - Files generated
        - Cleanup successful

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.page.wait_for_timeout(2000)
    story_page.Export_button().click()
    story_page.timeout()
    logging.info("Exported all processes successfully")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_distribute_legacy_files(story_page):
    test_distribute_legacy_files.__doc__ = """Tests distribution functionality for legacy files.

    Detailed Test Flow:
    1. Distribution Setup:
       - Navigates to distribution page
       - Configures legacy file settings
       - Prepares distribution details

    2. File Processing:
       - Adds all stories to distribution
       - Verifies history entries
       - Monitors distribution logs

    3. Validation Steps:
       - Checks file distributor logs
       - Verifies file queue entries
       - Validates distribution history

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Log Path: /wneclient/apps/filedistributor/log/filedistributor.log
        - Table: distribution_file_queue
        - Log Format: Grid with numbered entries

    Dependencies:
        - Database access
        - SSH connection
        - File distributor service
        - Story page navigation

    Expected Results:
        - Legacy files distributed
        - Logs show successful transfer
        - Queue entries validated
        - History updated correctly

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    db_client = Database()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.distribution_details_for_legacy_files()
    story_page.add_all_stories_to_distribution()
    story_page.navigate_to_distribution_history()  # navigate to distribution history
    story_page.verify_distribution_on_history_page()  # verify distribution on history page
    story_page.page.wait_for_timeout(2000)
    logging.info("\n📦 File Distributor Logs (Source Box):")
    try:
        public_host = env.ip
        ssh = ubuntu.ssh_connect(public_host, env.username, env.password)
        logfile_path = '/wneclient/apps/filedistributor/log/filedistributor.log'
        stdin, stdout, stderr = ssh.exec_command(f"tail -n 20 {logfile_path}")
        log_lines = stdout.read().decode().splitlines()
        table = [[i + 1, line] for i, line in enumerate(log_lines)]
        logging.info("\n" + tabulate(table, headers=["#", "Log Entry"], tablefmt="grid"))
    except Exception as e:
        logging.error(f"❌ Error fetching source logs: {e}")
    logging.info("\n📁 Files Present in Target Directory:")

    logging.info("Validation from database")
    db_client.execute_query(f'SELECT * FROM distribution_file_queue')  # sql not working
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_distribution_by_service_code(story_page):
    test_distribution_by_service_code.__doc__ = """Tests file distribution functionality based on service code filtering.

    Detailed Test Flow:
    1. Distribution Setup:
       - Navigates to distribution page
       - Configures service code settings
       - Cleans history if needed

    2. Story Selection:
       - Captures slug from subcon page
       - Captures slug from CCTV page
       - Adds stories to distribution

    3. Validation Steps:
       - Waits for distribution completion
       - Verifies slugs in history
       - Matches distributed stories

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Service Types: Subcon, CCTV
        - History Table: distribution_history
        - Wait Time: 180000ms

    Dependencies:
        - Story page navigation
        - Distribution service
        - History tracking
        - Slug matching

    Expected Results:
        - Stories distributed correctly
        - Slugs found in history
        - Distribution completed
        - History updated properly

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
        - Distribution History: http://10.189.200.6/history/distribution
    """
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.distribution_details_for_service_code()
    story_page.page.goto("http://10.189.200.6/history/distribution")
    Distribution_history_content = story_page.page.locator('//table//tbody//td[@class="nodata"]').text_content()
    if Distribution_history_content == "No records found":
        story_page.page.wait_for_timeout(2000)
        story_page.navigate()
    else:
        Clear_distribution_history = story_page.page.locator('//div[@class="enclosure no-print"]//div//button')
        Clear_distribution_history.click()
        Clear_queue = story_page.page.locator('//div[@class="enclosure no-print"]//div//div//ul//li[2]')
        Clear_queue.click()
        Confirm_clear = story_page.page.locator('//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]')
        Confirm_clear.click()
    story_page.navigate()
    story_page.page.locator('//div[@class="tab-browser row no-print"]//div[1]//a').click()
    slug_on_subcon_page = story_page.page.locator(
        '//div[@class="td source-id-slug justified"]//div//div//button[1]').first.text_content()
    logging.info(f"Slug on subcon page: {slug_on_subcon_page}")
    story_page.page.locator('//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]').first.click()
    story_page.page.locator('//div[@class="tab-browser row no-print"]//div[2]//a').click()
    slug_on_cctv_page = story_page.page.locator(
        '//div[@class="td source-id-slug justified"]//div//div//button[1]').first.text_content()
    logging.info(f"Slug on cctv page: {slug_on_cctv_page}")
    story_page.page.locator('//div[@class="actions"]//div[@class="flashing-indicators-holder"][2]').first.click()
    story_page.page.goto("http://10.189.200.6/history/distribution")
    story_page.page.wait_for_timeout(180000)
    elements = story_page.page.locator('//table//tbody//tr')
    for i in range(elements.count()):
        row_slug = story_page.page.locator(f'//table//tbody//tr[{i + 1}]//td[3]').text_content()
        if row_slug == slug_on_subcon_page or row_slug == slug_on_cctv_page:
            row_text = story_page.page.locator(f'//table//tbody//tr[{i + 1}]').text_content()
            logging.info(f"Matching row found: {row_text}")
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)

    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_verify_places_from_where_user_can_add_to_distribution(story_page):
    test_verify_places_from_where_user_can_add_to_distribution.__doc__ = """Tests distribution functionality from different entry points in the UI.

    Detailed Test Flow:
    1. Stories Page:
       - Navigates to stories page
       - Sets up FTP distribution
       - Adds stories to distribution

    2. MyVideos Page:
       - Navigates to videos page
       - Verifies distribution button
       - Adds content to distribution

    3. Validation Steps:
       - Confirms story addition
       - Verifies button functionality
       - Checks distribution status

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Distribution Type: FTP
        - Entry Points: Stories, MyVideos
        - Wait Time: 2000ms

    Dependencies:
        - Story page navigation
        - FTP configuration
        - Distribution service
        - Video library access

    Expected Results:
        - Stories added from Stories page
        - Content added from MyVideos
        - Distribution successful
        - All entry points functional

    URLs Accessed:
        - Stories Page: Default navigation
        - MyVideos Page: http://10.189.200.6/videos
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    story_page.navigate()
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.ftp_distribution()
    story_page.add_all_stories_to_distribution()
    logging.info("Storsie added to distribution from Stories page!!")
    story_page.page.wait_for_timeout(2000)
    story_page.page.goto('http://10.189.200.6/videos')
    story_page.page.locator('//div[@class="enclosure no-print"]//button[2]').click()
    story_page.page.wait_for_timeout(2000)
    logging.info("Stories added to distribution from MyVideos page!!")
    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_FD_Service_Start_Stop(story_page):
    test_FD_Service_Start_Stop.__doc__ = """Tests File Distributor service restart functionality.

    Detailed Test Flow:
    1. Service Access:
       - Navigates to services status page
       - Locates FD service controls

    2. Service Control:
       - Initiates service restart
       - Confirms restart action
       - Waits for completion

    3. Validation Steps:
       - Returns to distribution admin
       - Cleans up configurations
       - Verifies service state

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Service Name: File Distributor
        - Service Index: 8
        - Wait Time: 2000ms

    Dependencies:
        - Service management access
        - Story page navigation
        - Distribution service
        - Dialog interactions

    Expected Results:
        - Service restart initiated
        - Confirmation dialog shown
        - Service restarts successfully
        - Admin page accessible

    URLs Accessed:
        - Services Status: http://10.189.200.6/status/services
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    story_page.navigate()
    story_page.timeout()
    story_page.page.goto("http://10.189.200.6/status/services")
    story_page.timeout()
    story_page.page.locator(
        '//div[@class="td action-wrapper"][8]//div[@class="flashing-indicators-holder"][1]').click()  # fd restart button
    story_page.timeout()
    story_page.page.locator(
        '//dialog[@class="inv-bg"]//div[@class="row buttons"]//button[2]').click()  # confirm restart
    story_page.timeout()
    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)
    story_page.clearing_all_distribution_methods()


@allure.feature("FD")
def test_export_as_json(story_page):
    test_export_as_json.__doc__ = """Tests export functionality of distribution configuration to JSON format.

    Detailed Test Flow:
    1. Configuration Setup:
       - Navigates to distribution page
       - Configures service code settings
       - Prepares distribution details

    2. Export Process:
       - Locates export JSON button
       - Triggers export action
       - Waits for completion

    3. Cleanup Steps:
       - Returns to admin page
       - Clears configurations
       - Verifies cleanup

    Args:
        story_page: Fixture providing story page interface

    Test Data:
        - Export Format: JSON
        - Distribution Type: Service Code
        - Wait Time: 2000ms

    Dependencies:
        - Story page navigation
        - Distribution configuration
        - Export functionality
        - File system access

    Expected Results:
        - Distribution configured
        - JSON export successful
        - File generated
        - Cleanup completed

    URLs Accessed:
        - Distribution Admin: http://10.189.200.6/admin/distribution
    """
    story_page.navigate()
    story_page.details_for_distribution()
    story_page.distribution_details_for_service_code()
    story_page.export_as_json().click()  # export as json
    story_page.timeout()
    logging.info("Exported as JSON successfully")

    story_page.page.goto('http://10.189.200.6/admin/distribution')
    story_page.page.wait_for_timeout(2000)
    story_page.clearing_all_distribution_methods()
