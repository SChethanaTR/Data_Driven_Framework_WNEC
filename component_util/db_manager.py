from helpers.database import Database

db_client = Database()


def get_appsetting(name):
    query = f'select value from app_settings where name="{name}"'
    return db_client.execute_query(query)[0][0]


def get_latest_story_id():
    query = (
        "select story_id from files where video_sd_arrived!='null' order by "
        "arrived_display desc limit 1"
    )
    return db_client.execute_query(query)[0][0]


def is_exist_in_files_table(name):
    query = f'select * from files where nr55_newsml_filename="{name}"'
    return len(db_client.execute_query(query)) == 1


def run_query_result(query):
    return db_client.execute_query(query)[0][0]
