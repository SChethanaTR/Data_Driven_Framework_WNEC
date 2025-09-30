import time
from helpers.api import API
from helpers.wait import Wait


def restart(app: str, ssh_host=None) -> None:
    """Restarts a Docker container app via API call and wait until it's fully
    restarted
    Args:
        app (str): The app name (filepurger, fileprocessor, etc)
    """
    __tracebackhide__ = True  # pylint: disable=unused-variable

    # Some apps change names from Docker to API
    if app == "filepurger":
        service = "purger"
    else:
        service = app

    response, status = API().post(f"/services/{service}", {"operation": "restart"})
    assert status == 200, "Unable to restart service"

    # Wait until it's fully restarted
    Wait().for_app(app, ssh_host=ssh_host)
    return response




def resume(app: str) -> None:
    """Resume a Docker container app via API call
    Args:
        app (str): The app name (filepurger, fileprocessor, etc)
    """

    # Some apps change names from Docker to API
    if app == "filepurger":
        service = "purger"
    else:
        service = app

    response, status = API().put(f"/services/{service}", {"operation": "resume"})
    time.sleep(60)
    assert status == 200, "Unable to resume service"
    return response


def stop(app: str) -> None:
    """Stop Docker container app via API call.
    Args:
        app (str): The app name (filepurger, fileprocessor, etc)
    """

    # Some apps change names from Docker to API
    if app == "filepurger":
        service = "purger"
    else:
        service = app

    response, status = API().put(f"/services/{service}", {"operation": "stop"})
    time.sleep(2)
    assert status == 200, "Unable to stop service"
    return response



