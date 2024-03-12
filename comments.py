import os
import tempfile
from google.cloud.sql.connector import Connector


class Comments:
    def __init__(self):
        self.connection = None

    def connect(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
            temp_file_path = temp_file.name

        # Use the temporary file path as the value for GOOGLE_APPLICATION_CREDENTIALS
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

        instance_connection_name = os.environ[
            "MYSQL_CONNECTION_STRING"
        ]
        db_user = os.environ["SQL_USERNAME"]
        db_pass = os.environ["SQL_PASSWORD"]
        db_name = os.environ["SQL_DATABASE"]

        self.connection = Connector().connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )

    def add_user_comment(self, comment: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO user_comments (comment_text)
            VALUES (%s)
            """,
            (comment,)
        )
        self.connection.commit()
        cursor.close()

    def get_user_comments(self, limit=10):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT comment_text, created_at FROM user_comments
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,)
        )
        comments = cursor.fetchall()
        cursor.close()
        return comments

    def close(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection to MySQL database closed.")
