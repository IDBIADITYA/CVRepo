import cx_Oracle


class Oracle:
	def __init__(self, db_creds, batch_size=50):
		self.username = db_creds.get('username')
		self.password = db_creds.get('password')
		self.host = db_creds.get('host')
		self.conn = None
		self.port = db_creds.get('port')
		self.database = db_creds.get('database')
		self.batch_size = batch_size

	def connect(self):
		creds = '{}/{}@{}:{}/{}'.format(self.username, self.password, self.host, self.host, self.database)
		try:
			self.conn = cx_Oracle.connect(creds)
			return self.conn
		except:
			return self.conn

	def cursor(self):
		return self.conn.cursor()

	def close(self):
		self.conn.close()
		return True

	def run_query(self, sql):
		try:
			records = []
			creds = '{}/{}@{}:{}/{}'.format(self.username, self.password, self.host, self.port, self.database)
			with cx_Oracle.connect(creds)as connection:
				print("Connected!")
				with connection.cursor() as cursor:
					print("Cursor Created!")
					# execute the SQL statement
					cursor.execute(sql)
					while True:
						# fetch rows
						rows = cursor.fetchmany(self.batch_size)
						print(rows)
						if not rows:
							print("No Data found!")
							break
						else:
							print("No rows")
						for value in rows:
							records.append({"applicant_id": value[0], "recruitment_id": value[1]})

			return records
		except cx_Oracle.Error as error:
			print("Inside Exception: Something went wrong.")
			print(error)

		return []
