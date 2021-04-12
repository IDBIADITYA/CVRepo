import cx_Oracle

sql = """
	select * from ps_hrs_app_profile where hrs_person_id = '243936'  and hrs_profile_seq='1';
"""
batch_size = 20

try:
	with cx_Oracle.connect()as connection:
		with connection.cursor() as cursor:
			# execute the SQL statement
			cursor.execute(sql)
			while True:
				# fetch rows
				rows = cursor.fetchmany(batch_size)
				if not rows:
					print("No Data found!")
					break
				# display rows
				for row in rows:
					print(row)
except cx_Oracle.Error as error:
	print(error)

