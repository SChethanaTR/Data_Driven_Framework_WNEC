from pathlib import Path
from decouple import config



# pylint: disable=invalid-name
aws_secrets_status = config("AWS_SECRETS_STATUS", default=None)
ip = config("IP")
username = config("USERID")
password = config("PASSWORD")
api_url = f"http://{ip}/api/v1"
api_username = config("API_USERNAME")
api_password = config("API_PASSWORD")
db_user = config("DB_USER")
db_name = config("DB_NAME")
db_password = config("DB_PASSWORD")
ftp_host = config("FTP_HOST")
ftps_host = config("FTPS_HOST")
smb_username = config("SMB_HOST")
smb_password = config("SMB_PASSWORD")
dist_username = config("DIST_USERNAME")
dist_password = config("DIST_PASSWORD")
gi_version = config("GI_LATEST_VERSION")
rp_api_key = config("RP_API_KEY")
rp_endpoint = config("RP_URL")
rp_project = config("RP_PROJECT")
rp_mode = config("RP_MODE")
rp_launch = config("IP", default="Developer PC")
project_root = Path(__file__).parent
os_version = "Ubuntu 24.04"
host_name = "wneclient"
temp_dir = "temp/"
testdata_dir = "/wneclient/QA/"
region = "eu-west-1"
bucket = "tr-wne-client-autotest-testdata"
customer_name = "GDANSK-V7-TESTBED-01"
cur_page = None
ui_timeout = 30000
app_log_references = {
    "fileprocessor": "File processor sleeping for 15 seconds",
    "filepurger": "Sleeping for 15 minutes",
    "internet_backup": "Waiting 1 minutes for next iteration",
}
