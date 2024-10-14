import os
import mysql.connector
from dotenv import load_dotenv


class DBOperations:


    def create_connection(self):
        try:
            # establishing connection
            ROOT_DIR = os.getcwd()
            ENV_FILE_PATH = os.path.join(ROOT_DIR, '.env')

            # loading the .env file path
            load_dotenv(dotenv_path=ENV_FILE_PATH)
            
            # Retrieve credentials from environment variables
            host = os.getenv('HOST')
            user = os.getenv('USER')
            password = os.getenv('PASSWORD')
            database = os.getenv('DATABASE')
            
            # Establish connection
            conn = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
                )
            
            return conn
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            raise e
        
    def create_database(self, database_name="passwords_db"):
        try:
            conn = self.create_connection()
            query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
            
            with conn as conn:
                cursor = conn.cursor()
                cursor.execute(query)  # Execute the query
                print(f"Database '{database_name}' created.")
        except Exception as e:
            print(f"Error creating database: {e}")
            raise e


    def create_table(self, table_name="passwords_info"):
        try:
            conn = self.create_connection()
            query = (f"""CREATE TABLE IF NOT EXISTS {table_name}
                        (
                        ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        website TEXT NOT NULL,
                        username VARCHAR(200),
                        password VARCHAR(50)
                    );""")
        except Exception as e:
            raise e
        
        with conn as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            # print("Tables are created.")


    def create_record(self, data, table_name="passwords_info"):
        try:
            # Extract data
            website = data['website']
            username = data['username']
            password = data['password']
            
            # Establish connection to the database
            conn = self.create_connection()
            
            # Prepare SQL query
            query = f'''
            INSERT INTO {table_name} (website, username, password) 
            VALUES (%s, %s, %s);
            '''
            
            # Execute the query
            with conn as conn:
                cursor = conn.cursor()
                cursor.execute(query, (website, username, password))
                conn.commit()  # Commit the changes
                # print("Saved the records:", (website, username, password))

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        
    def show_record(self, table_name="passwords_info"):
        try:
            conn = self.create_connection()
            query = f'''SELECT * FROM {table_name};'''
            
            with conn as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                list_record = cursor.fetchall()
                return list_record

        except Exception as e:
            raise e
        
    def update_record(self, data, table_name="passwords_info"):
        try:
            ID = data['ID']
            website = data['website']
            username = data['username']
            password = data['password']
            conn = self.create_connection()
            query = f'''UPDATE {table_name} SET website = %s, username = %s, 
            password = %s WHERE ID = %s;
            '''
            with conn as conn:
                cursor = conn.cursor()
                cursor.execute(query, (website, username, password, ID))
                conn.commit()  # Commit the changes
        except Exception as e:
            raise e

    def delete_record(self, ID, table_name="passwords_info"):
        try:
            conn = self.create_connection()
            query = f'''DELETE FROM {table_name} WHERE ID = %s;
            '''
            with conn as conn:
                cursor = conn.cursor()
                cursor.execute(query, (ID,))
                conn.commit()  # Commit the changes
        except Exception as e:
            raise e
        