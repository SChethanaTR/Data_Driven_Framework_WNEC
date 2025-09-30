import logging
import mysql.connector
import env

logging.basicConfig(level=logging.INFO)


# pylint: disable=too-few-public-methods
class Database:
    def __init__(self, host=env.ip, user=env.db_user, passwd=env.db_password, database=env.db_name):
        self.db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        self.cursor = self.db.cursor()

    # pylint: disable=logging-fstring-interpolation
    def execute_query(self, query: str, params: tuple = None):
        """Executes a SQL statement on the database
        Args:
        query (str): The SQL string
        params (tuple): The parameters for the query (optional)
        Returns:
        list: A list of tuples with all rows of a query result set.
        """
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            self.db.commit()
            for row in result:
                logging.info(row)
            return result
        except mysql.connector.Error as error:
            logging.error(f"Error executing query: {query}. Error message: {error}")
            return None
