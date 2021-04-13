from dotenv import load_dotenv, find_dotenv
import os
from db_utility.connect import *


def cred():
    find_dotenv()
    load_dotenv()
    db_credentials = {"username": os.getenv("username"),
                      "password": os.getenv("password"),
                      "database": os.getenv("database"),
                      "host": os.getenv("host"),
                      "port": os.getenv("port")
                      }

    return db_credentials


def database_est():
    creds = cred()
    Oracle(creds)
    curr = Oracle.cursor
    return curr


def get_resume():
    curr = database_est()



get_resume()
