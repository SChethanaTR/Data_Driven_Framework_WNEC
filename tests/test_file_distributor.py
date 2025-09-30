import logging
import os

import pytest

from helpers.database import Database
from pages.home.filedistribution import FileDistributorPage
import pytest
import time
from playwright.sync_api import sync_playwright


def test_manual_Core_ftp_functionality(login, data_loader):
    db_client = Database()
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("FTP")  # Corrected method call
    time.sleep(5)
    # file_distributor_page.get_manual().click()  # Corrected method call
    # time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_location_details().click()
    time.sleep(5)
    file_distributor_page.ftp_host().fill("10.99.13.11")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_target_directory().fill("/testJakub")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_username_method_distributions().fill("wneqa")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_password_method_distributions().fill("wneqa123")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.fd_icon().nth(1).click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)
    db_client.execute_query(f'select * from distribution_configuration_ftp')


def test_manual_Core_ftps_functionality(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("FTPS")  # Corrected method call
    time.sleep(5)
    # file_distributor_page.get_manual().click()  # Corrected method call
    # time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_location_details().click()
    time.sleep(5)
    file_distributor_page.ftps_host().fill("10.99.13.124")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_target_directory().fill("/ubuntuFTPS")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_username_method_distributions().fill("wneqa")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_password_method_distributions().fill("wneqa123")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.fd_icon().nth(1).click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)


def test_manual_Core_sftp_functionality(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("SFTP")  # Corrected method call
    time.sleep(5)
    # file_distributor_page.get_manual().click()  # Corrected method call
    # time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_location_details().click()
    time.sleep(5)
    file_distributor_page.sftp_host().fill("10.99.13.11")  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_target_directory().fill("/wneclient/data/QA/sftp/sk_11july")  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_username_method_distributions().fill("wnecadmin")  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_password_method_distributions().fill("Offence-Tire-1850-Wnev7")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.fd_icon().nth(1).click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)


def test_manual_Core_smb_functionality(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("SMB")  # Corrected method call
    time.sleep(5)
    # file_distributor_page.get_manual().click()  # Corrected method call
    # time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_network_locations().click()
    time.sleep(5)
    file_distributor_page.smb_target_directory_path().fill("10.99.13.11/share/sk_temp")  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_username().fill("wneclient")  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_password().fill("reuters")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.fd_icon().nth(1).click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)


def test_automatic_Core_ftp_functionality(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("Automatic FTP")  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_automatic().click()
    time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_location_details().click()
    time.sleep(5)
    file_distributor_page.ftp_host().fill("10.99.13.11")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_target_directory().fill("/testJakub")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_username_method_distributions().fill("wneqa")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_password_method_distributions().fill("wneqa123")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)


def test_automatic_Core_ftps_functionality(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("Automatic FTPS")  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_automatic().click()
    time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_location_details().click()
    time.sleep(5)
    file_distributor_page.ftps_host().fill("10.99.13.124")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_target_directory().fill("/ubuntuFTPS")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_username_method_distributions().fill("wneqa")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftps_password_method_distributions().fill("wneqa123")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)


def test_automatic_Core_sftp_functionality(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("Automatic SFTP")  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_automatic().click()
    time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_location_details().click()
    time.sleep(5)
    file_distributor_page.sftp_host().fill("10.99.13.11")  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_target_directory().fill("/wneclient/data/QA/sftp/sk_11july")  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_username_method_distributions().fill("wnecadmin")  # Corrected method call
    time.sleep(5)
    file_distributor_page.sftp_password_method_distributions().fill("Offence-Tire-1850-Wnev7")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)


def test_automatic_Core_smb_functionality(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("Automatic SMB")  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_automatic().click()
    time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_network_locations().click()
    time.sleep(5)
    file_distributor_page.smb_target_directory_path().fill("10.99.13.11/share/sk_temp")  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_username().fill("wneclient")  # Corrected method call
    time.sleep(5)
    file_distributor_page.smb_password().fill("reuters")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.histories_tab().click()
    time.sleep(2)
    file_distributor_page.distribution_history().click()
    time.sleep(5)


def test_Interoperability_with_other_component_FileDistributor_Admin_Section_Story_page(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    file_distributor_page.add_new().click()
    time.sleep(5)
    file_distributor_page.name_distribution().fill("FTPs")  # Corrected method call
    time.sleep(5)
    # file_distributor_page.get_manual().click()  # Corrected method call
    # time.sleep(5)
    file_distributor_page.get_SD_videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_HD_Videos().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_scripts().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.get_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_distribution_method().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_location_details().click()
    time.sleep(5)
    file_distributor_page.ftp_host().fill("10.99.13.11")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_target_directory().fill("/testJakub")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_username_method_distributions().fill("wneqa")  # Corrected method call
    time.sleep(5)
    file_distributor_page.ftp_password_method_distributions().fill("wneqa123")  # Corrected method call
    time.sleep(5)
    file_distributor_page.save_distributions().click()  # Corrected method call
    time.sleep(5)
    file_distributor_page.stories_tab().click()
    time.sleep(2)
    file_distributor_page.fd_icon().nth(1).click()
    time.sleep(2)

    indicator_locator = page.locator('//div[@class="indicator small-tip tip-align-left ok-indicator"]').first

    # Wait for the indicator to appear
    indicator_locator.wait_for(state='visible', timeout=5000)  # Adjust the timeout as necessary

    # Assert that the indicator with the tick icon is visible
    assert indicator_locator.is_visible(), "Indicator with tick icon should be visible after clicking the file distributor icon"


def test_Interoperability_with_other_components_FileDistributor_Admin_Section_Buttons_Export(login, data_loader):
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    download_path = "/Users/s.chethana/PycharmProjects/Wnec_DataDrivenTesting/Download"
    os.makedirs(download_path, exist_ok=True)
    with page.expect_download() as download_info:
        file_distributor_page.export_all().click()

    # Get the download object
    download = download_info.value

    # Save the downloaded file to the specified path
    download.save_as(os.path.join(download_path, download.suggested_filename))

    # Verify the file exists
    downloaded_file_path = os.path.join(download_path, download.suggested_filename)
    assert os.path.exists(downloaded_file_path), f"File was not downloaded: {downloaded_file_path}"


def test_Interoperability_with_other_components_FileDistributor_Admin_Section_Buttons_Import(login, data_loader):#doesnt work
    page = login
    file_distributor_page = FileDistributorPage(page)
    file_distributor_page.get_hamburger()
    file_distributor_page.file_distributor_button()
    time.sleep(5)
    json_file_path = "/Users/s.chethana/PycharmProjects/Wnec_DataDrivenTesting/Import_Files/import_distribution_process.json"

    assert os.path.exists(json_file_path), f"File does not exist: {json_file_path}"
    with page.expect_file_chooser() as fc_info:
        page.click(file_distributor_page.import_fd())  # Replace with the actual selector for the import button
    file_chooser = fc_info.value
    file_chooser.set_files(json_file_path)

    # Wait for the import to complete (adjust the wait time as necessary)
    page.wait_for_timeout(10000)  # Wait for 10 seconds, adjust as necessary

    # Verify that the import was successful
    success_message_locator = page.locator('text=Import successful')  # Replace with the actual success message locator
    assert success_message_locator.is_visible(), "Import was not successful"


