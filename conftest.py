import json
from pathlib import Path
import paramiko
import pytest
import env
from component_util import api_util, db_manager
from component_util.file_distributor import FileDistributor
from helpers import docker_apps
from helpers.api import API
from pages import (
    FileDistributorPage,
    AboutPage,
    AdminPlayoutPage,
    ConnectionTestPage,
    AllSettingsPage,
    FileLogsPage,
    FileProcessorPage,
    LinkedBoxesPage,
    LoginPage,
    PushClientPage,
    ServicesPage,
    SoftwareUpgradesPage,
    UserManagementPage,
    StoryPage,
    UserInterfacePage,
    HistoryPage,
)
from pages.home import HistoryPage
from pages.home.admin_playout import AdminPlayoutPage
from pages.home.filedistribution import FileDistributorPage
from pages.home.about_page import AboutPage
from pages.home.story import StoryPage
from pages.home.user_management import UserManagementPage
from pages.home.UI import UserInterfacePage
from pages.home.history import HistoryPage
from pages.home.advance_search import AdvanceSearchPage
from pages.home.auth import AuthPage
from pages.home.advance_search import AdvanceSearchPage
from pages.home.live import LivePage
from pages.home.my_video import MyVideoPage
from pages.home.settings import SettingsPage
from pages.home.playout import PlayoutPage
from pages.home.file_logs import FileLogsPage

pytest_plugins = ["plugins.aws_secrets", "fixtures.reportportal"]


######################## Session Scoped Fixture ##################################
# pylint: disable=unused-argument
@pytest.fixture(scope="session", autouse=True)
def check_if_secrets_are_loaded():
    if env.aws_secrets_status and not Path("..env").exists():
        pytest.fail(f"[AWS Secrets ERROR] {env.aws_secrets_status}")


@pytest.fixture(scope="session")
def newsroom_user(test_setup):
    tokenized_user = API(
        api_util.auto_newsroom_user["username"], api_util.auto_newsroom_user["password"]
    )
    tokenized_user.user_setup()
    return tokenized_user


@pytest.fixture(name="production_user", scope="session")
def fixture_production_user(test_setup):
    tokenized_user = API(
        api_util.auto_production_user["username"],
        api_util.auto_production_user["password"],
    )
    tokenized_user.user_setup()
    return tokenized_user


@pytest.fixture(name="ssh_host", scope="session")
def fixture_ssh_host(ip_address=env.ip, username=env.username, password=env.password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)
    yield ssh
    ssh.close()


@pytest.fixture(name="test_setup", scope="session", autouse=True)
def fixture_test_setup():
    users_id_list = []
    api_agent = API()
    FileDistributor().remove_all_disribution_process()
    for user_payload in api_util.user_payload_list:
        if not api_util.is_user_exist(user_payload["username"]):
            response, status = api_agent.post("/users", user_payload)
            assert status == 200, "New user create post request failed"
            assert (
                    "id" in response
            ), f'Unable to setup {user_payload["username"]}, error response: {response["error"]}'
            users_id_list.append(response["id"])
    production_user = {"cookies": []}
    with open("withoutLogin.json", "w") as f:
        json.dump(production_user, f)
    yield
    FileDistributor().remove_all_disribution_process()
    api_util.import_setting()
    for user_id in users_id_list:
        api_agent.delete(f"users/{user_id}")


######################## Function Scoped Fixture ##################################
@pytest.fixture
def add_story_to_distribution():
    fd = FileDistributor()
    story_id = db_manager.get_latest_story_id()
    api_agent = API()
    api_util.delete_distribution_process_by_name("testAutoFTP")
    response, status = fd.create_distribution_process("ftp")
    process_id = response[-1]["id"]
    assert status == 200, "Unable to create distribution process"
    response, status = api_agent.post("/distributionfiles", {"story_id": story_id})
    assert status == 200, "Unable to add file for distribution"
    yield
    api_agent.delete(f"/distributionprocesses/{process_id}")


@pytest.fixture(name="admin_user")
def fixture_admin_user(test_setup):
    tokenized_user = API(api_util.auto_admin_user["username"], api_util.auto_admin_user["password"])
    tokenized_user.user_setup()
    return tokenized_user


@pytest.fixture
def my_video_added(request):
    user = request.getfixturevalue(request.param)
    story_id = db_manager.get_latest_story_id()
    response, status = user.post("/uservideos", {"story_id": story_id})
    assert status == 200, "Unable to add latest story to my video"
    edit_number = db_manager.run_query_result(
        f"select edit_number from files where story_id = '{story_id}'"
    )
    yield edit_number
    user.delete(f'/uservideos/{response["list"][-1]["user_video_id"]}')


@pytest.fixture
def clear_my_videos_queue(request):
    user = request.getfixturevalue(request.param)
    response, status = user.delete("/uservideos")
    assert status == 200, "Unable to delete my video"
    return response


def pytest_exception_interact(node, call, report):
    if report.failed and env.cur_page:
        try:
            sc_name = f'{node.funcargs["request"].path.stem}.png'
            sc_path = Path().joinpath(env.project_root, "temp", "screenshot", sc_name)
            env.cur_page.screenshot(path=sc_path, full_page=True)
            with open(sc_path, "rb") as image_file:
                file_data = image_file.read()
                node.funcargs["rp_logger"].info(
                    "Failure screenshot ",
                    attachment={"name": sc_name, "data": file_data, "mime": "image/png"},
                )
        except Exception as e:
            # TODO: Review reason why sometimes is a function (I guess when not using browser) and we can't get screenshot, probably on pytest-bdd test cases
            print(e)
            # node.funcargs["rp_logger"].info(e)
    env.cur_page = None


@pytest.fixture
def restore_setting():
    api_util.import_setting()


@pytest.fixture
def resume_internet_backup_service(ssh_host):
    yield
    docker_apps.resume("internet_backup")


@pytest.fixture
def set_channel1_file_playout():
    response, status = API().put("playout/channels/1", {"source": "file"})
    assert status == 200, f"Unable set file playout on channel1 with error {response}"


@pytest.fixture
def sftp_host(ssh_host):
    sftp = ssh_host.open_sftp()
    yield sftp
    sftp.close()


######################## Page Fixture ##################################
@pytest.fixture
def admin_playout_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield AdminPlayoutPage(context)
    context.close()


@pytest.fixture
def user_management_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield UserManagementPage(context)
    context.close()


@pytest.fixture
def user_interface_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield UserInterfacePage(context)
    context.close()


@pytest.fixture
def advance_search_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield AdvanceSearchPage(context)
    context.close()


@pytest.fixture
def auth_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield AuthPage(context)
    context.close()


@pytest.fixture
def fd_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield FileDistributorPage(context)
    context.close()


@pytest.fixture
def file_logs_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield FileLogsPage(context)
    context.close()


@pytest.fixture
def history_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield HistoryPage(context)
    context.close()


@pytest.fixture
def live_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield LivePage(context)
    context.close()


@pytest.fixture
def my_videos_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield MyVideoPage(context)
    context.close()


@pytest.fixture()
def setting_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield SettingsPage(context)
    context.close()


@pytest.fixture()
def playout_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield PlayoutPage(context)
    context.close()


@pytest.fixture()
def story_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield StoryPage(context)
    context.close()


@pytest.fixture()
def about_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield AboutPage(context)
    context.close()


@pytest.fixture()
def software_upgrades_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield SoftwareUpgradesPage(context)
    context.close()


@pytest.fixture()
def history_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield HistoryPage(context)
    context.close()


@pytest.fixture()
def file_logs(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield FileLogsPage(context)
    context.close()


@pytest.fixture()
def play_out_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield PlayoutPage(context)
    context.close()


@pytest.fixture()
def file_processor_page(browser, admin_user, request):
    storage_state = f"{request.param}.json" if hasattr(request, "param") else "autoAdmin.json"
    context = browser.new_context(storage_state=storage_state)
    yield FileProcessorPage(context)
    context.close()
