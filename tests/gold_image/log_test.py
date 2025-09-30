from datetime import datetime, timedelta
import pytest
from helpers import files
from helpers import ubuntu


@pytest.mark.gold_image
class TestLog:
    def setup_class(self):
        # pylint: disable=attribute-defined-outside-init
        self.apps = {
            "base_dir": "/wneclient/apps",
            # These are the apps that are expected
            # to have recently modified logs
        }

    def get_log(self, name, ssh):
        """Gets all logs with the specified name
        Args:
            name (str): log name (omitting .log extension)
        Returns:
            list: List of logs with that name
        """
        return ubuntu.execute_cmd_remote(f"find /wneclient/apps -path *{name}.log", ssh).split("\n")

    @pytest.mark.parametrize("log_file", files.parametrize("gold_image:required_logs"))
    def test_log_exists(self, log_file, ssh_host):
        """Checks if a specific log exists in the filesystem
        Args:
            log_file (str): Log file name (omitting .log extension)
        """
        logs = self.get_log(log_file, ssh_host)

        assert len(logs) > 0, f"Could not find required log {log_file}.log"

        for log in logs:
            assert ubuntu.is_file_exist_remote(log, ssh_host)

    @pytest.mark.parametrize("log_file", files.parametrize("gold_image:required_logs_modified"))
    def test_modified_date(self, log_file, ssh_host):
        """A log should be constantly updated, therefore it's modification date should be recent
        (in this case, less than 1 hour)
        """
        now = datetime.utcnow()

        # Threshold modified time limit that the log is considered invalid
        threshold = timedelta(hours=1)
        logs = self.get_log(log_file, ssh_host)

        assert len(logs) > 0, f"Could not find required log {log_file}.log"

        for log in logs:
            modified_time = (
                ubuntu.execute_cmd_remote(f'stat {log} | grep "Modify"', ssh_host)
                .split("Modify:")[1]
                .split(".")[0]
                .strip()
            )
            modified_time = datetime.strptime(modified_time, "%Y-%m-%d %H:%M:%S")

            assert (
                now - modified_time
            ) <= threshold, f"There was no log changes in {log} within the last hour"
