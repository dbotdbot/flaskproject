import datetime
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
	#Create db connection to db (if none exists will create)
	#db_file is the db file with its location
	#will close connection when finished
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	finally:
		conn.close()

def connect_to_db(db_file):
	#returns Connection object of db_file
	try:
		conn = sqlite3.connect(db_file)
		print("Connected to db")
		return conn
	except Error as e:
		print(e)

	return None

def disconnect_from_db(conn):
	#disconnect from db
	try:
		conn.close()
	except Error as e:
		print(e)

def create_table(conn, create_table_sql):
	#creates table based on create_table_sql
	#create_table_sql will be a string with
	#the sql commands all setup
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print (e)

def create_entry(conn, data_to_log):
	sql = ''' INSERT INTO logger(time_data,weight_data,type_date) VALUES(?,?,?) '''
	cur = conn.cursor()
	try:
		cur.execute(sql, data_to_log)
		print("seemed to execute create entry")
		return cur.lastrowid
	except:
		print("some sort of error occured")

def select_all_logs(conn):
	cur = conn.cursor()
	cur.execute("SELECT * FROM logger")
	rows = cur.fetchall()
	for row in rows:
		print(row)

def main():
	database = "C:\\sqlite\dataloggertest.db"

	conn = connect_to_db(database)
	with conn:
		#create new entry for db
		datetime_object = datetime.datetime.now()
		print("datetime object = ")
		print (datetime_object)
		weight = 23.3
		type_date = 'Beer'
		log = (datetime_object, weight, type_date)
		print("log looks like this ")
		print(log)
		loggerid = create_entry(conn, log)
		print("logger id is ")
		print(loggerid)
		select_all_logs(conn)














	#string to define table for storing logged scale data
	#sql_create_scale_logger_table = """ CREATE TABLE IF NOT EXISTS logger (id integer PRIMARY KEY,time_data datetime,weight_data decimal,type_date text); """

    #create database connection
	#conn = connect_to_db(database)
	#if conn is not None:
    #	#create scale_logger_table
	#	create_table(conn, sql_create_scale_logger_table)
	#	print("Table created")
	#	disconnect_from_db(conn)
	#	print("Disconnected from db")
	#else:
	#	print("Error:  Could not create connection to database")



if __name__ == '__main__':
	#create_connection("C:\\sqlite\dataloggertest.db")    
	main()