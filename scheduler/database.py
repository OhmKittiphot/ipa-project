import os

import mysql.connector


def get_router_info():
    db_host = os.environ.get("DB_HOST")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")

    connection = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database=db_name
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM routers")
    routers = cursor.fetchall()
    cursor.close()
    connection.close()

    return routers


if __name__ == "__main__":
    get_router_info()
