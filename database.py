import psycopg2
from psycopg2.extras import RealDictCursor
import os

class DatabaseConnection:
    def __init__(self):
        if os.environ.get('APP_SETTINGS') == 'testing':
            self.conn = psycopg2.connect(dbname="ireporter_testdb",
                                         password="123",
                                         host="localhost", port="5432",
                                         user="phiona")
        else:
            self.conn = psycopg2.connect(dbname="ireporter_db", password="123",
                                         host="localhost", port="5432",
                                         user="phiona")

        self.cur = self.conn.cursor()
        self.conn.autocommit = True
    
    def create_incident_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS incidents(incident_id SERIAL PRIMARY KEY NOT NULL,
                  createdOn DATE NOT NULL, created_by VARCHAR(25)
                  NOT NULL, incident_type VARCHAR(100) NOT NULL, title VARCHAR(250)
                  NOT NULL, description VARCHAR(250) NOT NULL,
                  location VARCHAR(100) NOT NULL, status VARCHAR(10) NOT NULL,
                  images VARCHAR(255) NOT NULL, videos VARCHAR(255) NOT NULL, comments VARCHAR(250));"""
        self.cur.execute(sql)

    def create_user_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY NOT NULL,
                  firstname VARCHAR(25) NOT NULL, lastname VARCHAR(25) NOT NULL,
                  othernames VARCHAR(25) NOT NULL, email VARCHAR(25) NOT NULL UNIQUE,
                  password VARCHAR(25) NOT NULL, phonenumber VARCHAR(25) NOT NULL,
                  username VARCHAR(10) NOT NULL,
                  registered_on DATE NOT NULL, is_admin VARCHAR  NOT NULL);"""
        self.cur.execute(sql)
   
    def edit_incident(self,  attribute, value, records):
        query = f"""UPDATE incidents SET {attribute} ='{value}' WHERE incidents = '{incidents}' """
        self.cur.execute(query)
        return'update successfully'

    def drop_tables(self, table_name):
        """ Drops the tables that exist in the database"""
        sql = """ DROP TABLE {} CASCADE; """
        self.cur.execute(sql.format(table_name))

    def close_DB(self):
        self.conn.close()


dbconn = DatabaseConnection()
dbconn.create_incident_table()
dbconn.close_DB()