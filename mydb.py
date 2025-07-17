# create a connection to ysql server using mysql connector

import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd ='password',
)

#create cursorObject
cursorObject = dataBase.cursor()

#create a db
cursorObject.execute("CREATE DATABASE CRM")

print("all done")