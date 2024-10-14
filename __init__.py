import mysql.connector
print(mysql.connector.__version__)
import sys

def check_mysql_connection(host, port, user, password, database):
    """Checks the MySQL connection parameters and returns a boolean indicating success."""
    try:
        cnx = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py host port username password database")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
    password = sys.argv[4]
    database = sys.argv[5]

    if check_mysql_connection(host, port, user, password, database):
        print("MySQL connection successful!")
    else:
        print("MySQL connection failed.")
