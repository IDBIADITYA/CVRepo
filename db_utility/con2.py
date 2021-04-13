import cx_Oracle
#ip = '10.160.33.11'
#port = 1521
#SID = 'sysadm.PS_HRS_APP_RES'
#dsn_tns = cx_Oracle.makedsn(ip, port, SID)

# You might get these via environment variable to make thing secure
username = 'staqo'
password = 'STAQO123'

conn = cx_Oracle.connect(username, password, "10.160.33.11:1521/sysadm")

print(conn.version)
conn.close()