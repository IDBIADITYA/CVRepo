import cx_Oracle
from dotenv import load_dotenv
from db_utility import *
db_creds = {
				"username": os.getenv("username"),
				"password": os.getenv("password"),
				"database": os.getenv("database"),
				"host": os.getenv("host"),
				"port": os.getenv("port")
			}
db= Oracle(db_creds)
print(db)

curr= Oracle(db_creds)