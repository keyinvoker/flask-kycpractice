import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
)

mycursor = mydb.cursor()

mycursor.execute('CREATE DATABASE kycapp')

mycursor.execute('SHOW DATABASES')
for db in mycursor:
    print(db)