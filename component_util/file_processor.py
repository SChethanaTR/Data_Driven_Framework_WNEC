import time
from component_util import db_manager
from helpers import strings, s3
from helpers.api import API
from helpers import ubuntu
from helpers.database import Database
import env


# Invalid test files from FileProcessor/InvalidFile/ AWS bucket
INVALID_FILE_1 = "2013-05-10T065249Z_2_WNE95LN7J_RTRWNEC_0_3993-LIN-TEST-TITLE.XML"
INVALID_FILE_2 = (
    "2013-06-17T032754Z_1_WNE96GP30_RTRWNEC_0_0000-ADVISORY-CCTV-NEWSCONTENT-"
    "FOR-MONDAY-JUNE-17-2013-ADVISORY-3-AFTERNOON.XML"
)
INVALID_FILE_3 = "2022-03-11T094127Z_1_WD394211032022RP1_RTRWNEC_0_3942-TEST-INVALID.XML"
INVALID_FILE_4 = "2022-03-12T064455Z_3_WD413812032022RP1_RTRWNEC_0_4138-EMPTY-TITLE.XML"

# Valid test files from FileProcessor/ValidFile/ AWS bucket
VALID_FILE_1 = "2013-05-10T065249Z_1_WNE95FEJT_RTRWNEC_0_4992-LIN-TEST-TITLE.XML"
VALID_FILE_2 = "2023-07-22T061504Z_2_WDIKZSYG9_RTRWNEC_0_6612-GREECE-HEATWAVE-TOURISM-IMPACT.XML"
VALID_FILE_3 = (
    "2023-06-26T165902Z_1_ADIH62K3M_RTRWNEC_0_0000-ADVISORY-LIVE-WITHDRAWAL-COLORADO-SHOOTING.XML"
)
VALID_FILE_4 = "2022-03-12T064455Z_3_WD413812032022RP1_RTRWNEC_0_4138-TEST-TITLE.XML"
VALID_FILE_V7 = "2023-08-02T053142Z_4_RW162702082023RP1_RTRMADC_0_ASIA-WEATHER-KHANUN-JAPAN-UGC.XML"


class FileProcessor:
    INVALID_OUTPUT_FOLDER = "/wneclient/data/Invalid/"
    VALID_OUTPUT_FOLDER = "/wneclient/data/Video/"
    INVALID_TEST_DATA_FOLDER = "FileProcessor/InvalidFile/"
    VALID_TEST_DATA_FOLDER = "FileProcessor/Valid/"
    STORY_TO_INGEST_TEST_DATA_FOLDER = "FileProcessor/StoriesToIngest/"
    STORY_TO_INGEST = "2023-05-15T113753Z_6_RW255215052023RP1_RTRMADC_0_TURKEY-ELECTION-OGAN.XML"
    VALID_TEST_DATA_LIST = [VALID_FILE_1, VALID_FILE_4, VALID_FILE_3, VALID_FILE_2]
    INVALID_TEST_DATA_LIST = [
        INVALID_FILE_1,
        INVALID_FILE_2,
        INVALID_FILE_3,
        INVALID_FILE_4,
    ]
    INPUT_FOLDER_SATELLITE = "/wneclient/data/RVN/"
    INPUT_FOLDER_CDN = "/wneclient/data/RVN-CDN/"
    if db_manager.get_appsetting("supportV7Script") == "true":
        INPUT_FOLDER_SATELLITE = "/wneclient/data/RVN-SCRIPTS/"
        VALID_TEST_DATA_LIST.append(VALID_FILE_V7)

    def ingest_story(self, ssh_host, file_name):
        file_path = "testdata/" + self.STORY_TO_INGEST_TEST_DATA_FOLDER + file_name
        file_path_box = env.testdata_dir + file_path
        if not ubuntu.is_file_exist_remote(file_path_box, ssh_host):
            s3.copy(file_path, file_path_box, ssh_host=ssh_host)
        new_usn = f"AU{strings.random_digit(12)}RP1"
        old_usn = file_name.split("_")[2]
        new_file_name = file_name.replace(old_usn, new_usn)
        new_file_path_box = file_path_box.replace(old_usn, new_usn)
        ubuntu.is_execute_cmd_successful_remote(
            f"cp -r {file_path_box} {new_file_path_box}", ssh_host
        )
        assert ubuntu.is_execute_cmd_successful_remote(
            f"sed -i 's/{old_usn}/{new_usn}/g' {new_file_path_box}", ssh_host
        ), "Unable to update file with new usn_id"
        assert ubuntu.is_execute_cmd_successful_remote(
            f"cp -r {new_file_path_box} {self.INPUT_FOLDER_SATELLITE + new_file_name}",
            ssh_host,
        ), f"Unable to copy {new_file_name} in {self.INPUT_FOLDER_SATELLITE}"
        time.sleep(30)
        ubuntu.delete_file_remote(new_file_path_box, ssh_host)
        return new_usn

    def add_file_to_distribution(self, usn_id):
        payload = {"story_id": f"tag:reuters.com,2023:newsml_{usn_id}"}
        return API().post("/distributionfiles", payload)

    def delete_ingest_file_from_database_if_exist(self, file_name):
        db_client = Database()
        db_client.execute_query(f'delete from files where nr55_newsml_filename="{file_name}"')
