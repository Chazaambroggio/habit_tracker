import sqlite3, csv

connection = sqlite3.connect("habit_database.db")
cursor = connection.cursor()

# Check for existance of root user data. 
check_predefine_user = cursor.execute("SELECT * FROM habit_details WHERE username = ?",('root',)).fetchall()

# Check for 'root' existance..
if len(check_predefine_user) == 0:

	# Read txt with predefine data for habit_details table.
	habit_details_predefine = open("root_predefine_habit_details.txt")
	habit_details = csv.reader(habit_details_predefine)
	# Upload data into habit_details table.
	cursor.executemany("INSERT INTO habit_details VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", habit_details)

	# Read txt with predefine data for habit_log table.
	habit_log_predefine = open("root_predefine_habit_log.txt")
	habit_log = csv.reader(habit_log_predefine)
	# Upload data into habit_log table.
	cursor.executemany("INSERT INTO habit_log VALUES (?,?,?,?)", habit_log)

	# Creating default root user.
	cursor.execute("INSERT	INTO login (username, password) VALUES ('root','root')")

	# Commit changes.
	connection.commit()

connection.close()