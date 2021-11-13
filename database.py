import sqlite3
import pandas as pd

# Create/connect to database.
connection = sqlite3.connect("habit_database.db")
cursor = connection.cursor()

# Create habit_details table
cursor.execute(''' 
		CREATE TABLE IF NOT EXISTS habit_details
		(username TEXT, habit_id TEXT, habit_name TEXT, period INTEGER, frequency INTEGER,
		start_date DATE, period_start DATE, period_end DATE, frequency_count INTEGER, streak_count INTEGER, status TEXT, 
		longest_streak INTEGER)
		''')

# Create habit_log table
cursor.execute(''' 
		CREATE TABLE IF NOT EXISTS habit_log
		(username TEXT, habit_id INTEGER, habit_name TEXT, check_date DATE)
		''')

# Create login table
cursor.execute(''' 
		CREATE TABLE IF NOT EXISTS login
		(username TEXT, password TEXT)
		''')

