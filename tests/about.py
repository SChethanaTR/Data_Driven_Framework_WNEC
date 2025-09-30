import pytest


@pytest.fixture(scope="session")
def browser():
    browser = Browser()
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def data_loader():
    return DataLoader('/Users/s.chethana/PycharmProjects/Wnec_DataDrivenTesting/data/test_data.json')


def test_about_page(browser, data_loader):
    page = browser.page
    about_page = AboutPage(page)

    page.goto('http://10.99.13.216/status/about')
    client_name = about_page.get_client_name()
    client_pc_serial_number = about_page.get_Client_PC_Serial_Number()
    host_id = about_page.get_host_id()
    host_name = about_page.get_host_name()
    client_pc_type = about_page.get_Client_PC_Type()
    time = about_page.get_time()
    user_id = about_page.get_Get_User_ID()
    installed_patches = about_page.get_installed_patches()
    rec_mac_address = about_page.get_Receiver_MAC_Address()
    software_version = about_page.get_software_version()

    assert client_name == data_loader.get_data('WNE Client Name')
    assert client_pc_serial_number == data_loader.get_data('WNE Client PC Serial Number')
    assert host_id == data_loader.get_data('Host ID')
    assert host_name == data_loader.get_data('Host Name')
    assert client_pc_type == data_loader.get_data('WNE Client PC Type')
    assert time == data_loader.get_data('Time')
    assert user_id == data_loader.get_data('Guest User ID')
    assert installed_patches == data_loader.get_data('Installed Patches')
    assert rec_mac_address == data_loader.get_data('WNE Receiver MAC Address')
    assert software_version == data_loader.get_data('Version')
