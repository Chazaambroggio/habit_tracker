import sqlite3, csv


connection = sqlite3.connect("habit_database.db")
cursor = connection.cursor()

# Check for preexisting predefine data.
check_predefine_data = cursor.execute("SELECT * FROM habit_details WHERE username = ?",('root',)).fetchall()

# Only input predefine data when root user doesn't exist.
if len(check_predefine_data) == 0:

	# Read txt with predefine data for habit_details table.
	habit_details_predefine = open("predefine_habit_details.txt")
	habit_details = csv.reader(habit_details_predefine)
	# Upload data into habit_details table.
	cursor.executemany("INSERT INTO habit_details VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", habit_details)

	# Read txt with predefine data for habit_log table.
	habit_log_predefine = open("predefine_habit_log.txt")
	habit_log = csv.reader(habit_log_predefine)
	# Upload data into habit_log table.
	cursor.executemany("INSERT INTO habit_log VALUES (?,?,?,?)", habit_log)

	# Creating default root user.
	cursor.execute("INSERT	INTO login (username, password) VALUES ('root','root')")

	# Commit changes.
	connection.commit()


connection.close()