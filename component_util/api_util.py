import json
from helpers.api import API
import env


auto_admin_user = {
    "username": "autoAdmin",
    "password": f"{env.api_password}QA@123",
    "privileges": [1],
}
auto_production_user = {
    "username": "autoProduction",
    "password": f"{env.api_password}QA@123",
    "privileges": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
}
auto_newsroom_user = {
    "username": "autoNewsRoom",
    "password": f"{env.api_password}QA@123",
    "privileges": [],
}
user_payload_list = [auto_admin_user, auto_production_user, auto_newsroom_user]


def delete_user_by_username(username):
    response, status = API().get("/users")
    assert status == 200, "Unable to get users list"
    for user in response[::-1]:
        if user["username"] == username:
            API().delete(f'users/{user["id"]}')
            break


def is_user_exist(username):
    response, status = API().get("/users")
    assert status == 200, "Unable to get users list"
    for user in response[::-1]:
        if user["username"] == username:
            return True
    return False


def delete_distribution_process_by_name(name):
    response, status = API().get("/distributionprocesses")
    assert status == 200, "Unable to get distribution processes list"
    for process in response[::-1]:
        if process["name"] == name:
            API().delete(f'/distributionprocesses/{process["id"]}')
            break


def import_setting():
    try:
        api_agent = API()
        default_setting_json = f'testdata/Settings/defaultSettingsBox{env.ip.split(".")[3]}.json'
        with open(default_setting_json, "r") as f:
            payload = json.load(f)
        response = api_agent.session.put(api_agent.endpoint_to_url("/appsettings"), json=payload)
        assert response.status_code == 200, "Unable to restore setting"
    except Exception as e:
        print(e)
