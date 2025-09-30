from pathlib import Path
from datetime import datetime, timedelta
from wait_for import wait_for
import time

import env
from helpers import ubuntu


class Wait:
    def for_file(
        self,
        path: str,
        to_exist=True,
        timeout: int = 60,
        delay: float = 0.5,
        ssh_host=None,
    ):  # pylint: disable=too-many-arguments
        """Wait for a file to be created or removed
        Args:
            path (str): Full path of the file
            to_exist (bool, optional): Wait for file to exist (set false to wait for
            it being deleted). Defaults to True.
            timeout (int, optional): Max waiting time in seconds. Defaults to 60.
            delay (float, optional): Interval between checks in seconds. Defaults to 0.5.
            ssh_host (SSHClient) : ssh client object
        Returns:
            tuple: (True/False, time it took)
        """
        fail_condition = not to_exist
        func = ubuntu.is_file_exist_remote if ssh_host else Path(path).exists
        print(f"Waiting for {path} to exist {to_exist}")
        return wait_for(
            func,
            func_args=[path, ssh_host],
            fail_condition=fail_condition,
            timeout=timeout,
            delay=delay,
        )

    def for_app(self, app: str, timeout: int = 60, delay: float = 0.5, ssh_host=None):
        """Wait for a container to be fully restarted
        Args:
            app (str): Full path of the file
            timeout (int, optional): Max wainting time in seconds. Defaults to 60.
            delay (float, optional): Interval between checks in seconds. Defaults to 0.5.
        Returns:
            tuple: (True/False, time it took)
        """
        __tracebackhide__ = True  # pylint: disable=unused-variable)

        # Reference datetime (Apps use UTC for their logs)
        now = datetime.utcnow()

        # Finds the logs of this app
        log_path = f"/wneclient/apps/{app}/log/{app}.log"
        if not log_path:
            raise FileNotFoundError(f"No logs were found for app {app}")

        def check_app_restart(
            log_path: list,
            reference_string: str,
            reference_date: datetime,
            ssh_host=None,
        ):
            """Determines the last time an app restarted based on it's log lines
            Note that this only works in logs that contain a timestamp
            Args:
                log_path (list): The log files path of this app
                reference_string (str): The string search, what determines with app was restarted
                reference_date (datetime): Limit time, anything before this datetime will be ignored
            Returns:
                bool: If the app is restarted or not
            """

            # push-client uses a dd-mm-yy format, all other use a ISO format (yyyy-mm-dd)
            date_formats = ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S")
            if ssh_host:
                lines = ubuntu.execute_cmd_remote(f"tail -n 400 {log_path}", ssh_host).split("\n")
            else:
                with open(log_path) as file:
                    lines = file.readlines()
            # Reads lines from most recent to oldest
            lines.reverse()
            # Read every line
            for line in lines:
                line_date = None
                # Tries to convert the first characters in a date format
                for date_format in date_formats:
                    try:
                        line_date = datetime.strptime(line[:19], date_format)
                    except ValueError:
                        continue
                    else:
                        break
                # Stop if we go too far back into the log (with a margin)
                if line_date < reference_date - timedelta(seconds=20):
                    break
                # If the reference string is found, return and end
                if reference_string in line:
                    return True
            return False

        return wait_for(
            check_app_restart,
            func_args=[log_path, env.app_log_references[app], now, ssh_host],
            timeout=timeout,
            delay=delay,
            message=f'Confirm that "{app}" restarted',
        )

