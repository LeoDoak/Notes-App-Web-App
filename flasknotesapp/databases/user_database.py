#https://www.ionos.com/digitalguide/websites/web-development/sqlite3-python/

'''
Run this file to create the database, checks the database to make sure that it already has admin access in it and has the names, 
nobody should have to run this since the database should be created and stored within the user databse folder
'''

import sqlite3

def create_database(connection): 
	#check to see if database is created 
	print(connection.total_changes)
	cursor =  connection.cursor()
	#check for admin access 
	cursor.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER, username TEXT, password TEXT,email TEXT)")
	cursor.execute("SELECT username, password FROM user where user_id = 0 and email = 'admin@uncw.edu'")
	row = cursor.fetchall()
	#if no admin access found then it'll add one
	if (len(row) == 0 ):
		cursor.execute("INSERT INTO user VALUES(0, 'admin','1234','admin@uncw.edu')") #create admin access
		print("Admin access has been added to the database")
	else:
		print("Admin access already in system")
	connection.commit()
	cursor.execute("SELECT * FROM user")
	rows = cursor.fetchall()
	print(rows)

# checklogin only a test function, the function call is 
def checklogin(connection): 
	cursor =  connection.cursor()
	usname = 'admin'
	pswd = '1234'
	cursor.execute("SELECT username, password FROM user where user_id = user_id")
	row = cursor.fetchall()
	print(row)
	if row[0][0] == usname and row[0][1] == pswd: 
		return True
	else: 
		return False 

def main(): 
	connection = sqlite3.connect("user.db")
	create_database(connection)
	#print(checklogin(connection))
	connection.close() 
		
if __name__ == "__main__":
    main()
