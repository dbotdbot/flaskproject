import datetime
import sqlite3
class dbUtil(object):

	def __init__(self):
		#self.conn = connect_to_db(db_file)
		print("dbUtil class initialized")

	def connect_to_db(self, db_file):
		#returns Connection object of db_file
		try:
			conn = sqlite3.connect(db_file)
			print("Connected to db")
			return conn
		except Error as e:
			print(e)

		return None

	def checkData(self, date_time, weight, type):
		return True

	def select_all_logs(self, conn):
		cur = conn.cursor()
		cur.execute("SELECT * FROM logger")
		rows = cur.fetchall()
		for row in rows:
			print(row)

	def create_entry(self, conn, data_to_log):
		print("got into create_entry")
		sql = ''' INSERT INTO logger(time_data,weight_data,type_date) VALUES(?,?,?) '''
		cur = conn.cursor()
		print("got cursor")
		try:
			cur.execute(sql, data_to_log)
			print("seemed to execute create entry")
			return cur.lastrowid
		except:
			print("some sort of error occured")
			return -1
