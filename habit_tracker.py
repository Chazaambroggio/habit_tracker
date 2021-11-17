import database
import predefine_habits
import pandas as pd
import sqlite3
from datetime import datetime, date, time, timedelta
from login import Login

class Habit():	

	def __init__(self):
		''' Initialize connection with database.'''
		
		# Start connection with database.
		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		self.connection = connection
		self.cursor = cursor

		# Habit status control and 
		# habits streak count should be trigger here.

		# Adjust status before adjusting habit periods.

		self.adjust_habits_periods()

		l = Login()
		
		self.username = l.login_menu()

	
	def adjust_habits_periods(self):
		''' Function to adjust habit periods.'''

		habit_dates = self.cursor.execute("SELECT habit_id, period, frequency, period_start, frequency_count FROM habit_details").fetchall()

		# Obtain detail of each habit.
		for row in habit_dates:
				
			self.habit_id = row[0]
				
			self.period = row[1]
				
			self.frequency = row[2]
				
			self.period_start = row[3]
				
			self.frequency_count = row[4]

			# converting str into datetime.datetime
			self.period_start = datetime.strptime(self.period_start,'%Y-%m-%d %H:%M:%S.%f')

			self.today = datetime.now()
		
			# Rescheduling period_start and period_end 
			# to be able to check for frequency accordinly.
			# While loop to reschedule as many times as needed.
			while (self.today - self.period_start) > timedelta(days = self.period):

				self.period_start = self.period_start + timedelta(days = self.period)

				self.period_end = self.period_start + timedelta(days = self.period)

				# Check for habit status.
				self.check_habit_status()

				# Reset frequency_count for new period.
				self.frequency_count = 0

				period_update =	"UPDATE habit_details SET period_start = \'" + str(self.period_start) + "\', period_end = \'" + str(self.period_end) + "\', frequency_count = \'" + str(self.frequency_count) + "\'  WHERE habit_id = \'" + self.habit_id + "\';"

				self.cursor.execute(period_update)
				self.connection.commit()


	def check_habit_status(self):
		''' Function to adjust habit status'''
		
		# Only check for status after period is over.
		if self.today - self.period_start >= timedelta(days = self.period):

		# Check if the habit was performed enough times.
		# during the period.
			if self.frequency_count >= self.frequency:	

				status = 'good'
				self.increase_habit_streak()

			else:

				status = 'broken'
				self.reset_habit_streak()
			

			period_update =	"UPDATE habit_details SET status = \'" + status + "\' WHERE habit_id = \'" + self.habit_id + "\';"

			self.cursor.execute(period_update)
			self.connection.commit()



	def increase_habit_streak(self):
		''' Function to increase habit streak.''' 

		# Streak count is how many periods a habit has been completed in a row.
		# Streak will only increase when a habit has been succesfully performe with the correct frequency over 
		# the specified period of time.

		# Retrive habit streak count.
		rows = self.cursor.execute("SELECT streak_count, longest_streak FROM habit_details WHERE habit_id = ?", self.habit_id).fetchall()

		for row in rows:
			last_streak_count = int(row[0])
			current_longest_streak = int(row[1])

		# Current streak
		streak_count = last_streak_count + 1 

		# If the current habit streak is greater than
		# the longest streak update longest streak.
		if streak_count > current_longest_streak:

			current_longest_streak = streak_count

		# Update habit streak count
		streak_update =	"UPDATE habit_details SET streak_count = \'" + str(streak_count) + "\', longest_streak = \'" + str(current_longest_streak) + "\' WHERE habit_id = \'" + self.habit_id + "\';"

		self.cursor.execute(streak_update)
		self.connection.commit()

	
	def reset_habit_streak(self):
		''' Function to reset streak.''' 

		# reset habit streak count to 0.
		streak_update =	"UPDATE habit_details SET streak_count = '0' WHERE habit_id = \'" + self.habit_id + "\';"

		self.cursor.execute(streak_update)
		self.connection.commit()


	def increase_frequency_count(self):
		''' Function to increase frequency count.''' 

		# Retrive habit streak count.
		rows = self.cursor.execute("SELECT frequency, frequency_count FROM habit_details WHERE habit_id = ?", self.habit_to_check).fetchall()
		
		for row in rows:
			frequency = int(row[0])
			last_frequency_count = int(row[1])

		frequency_count = last_frequency_count + 1 

		# Update habit streak count
		frequency_count_update =	"UPDATE habit_details SET frequency_count = \'" + str(frequency_count) + "\' WHERE habit_id = \'" + self.habit_to_check + "\';"

		self.cursor.execute(frequency_count_update)
		self.connection.commit()

		# Period goal achieved.
		if frequency_count == frequency:
			self.habit_id = self.habit_to_check
			self.increase_habit_streak()

			print('\nYou achived your period goal, great job!\n')

		# Period goal not achieved yet.
		elif frequency_count < frequency:

			print(str(frequency - frequency_count) +  ' more times to reach your period goal. You are almost there!\n')
		
		# Period goal overachieved.
		elif frequency_count > frequency:

			print("\nWow! You just over performed your habit goal for this period. Amazing job!\n")
			
	

	def check_off_habit(self):
		''' Function to check-off a habit.'''

		# maybe make this a function.	
		# Display all habit id and name.
		rows = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?", (self.username,)).fetchall()
			
		for row in rows:
			habit_id = row[0]
			habit_name = row[1]

			print(habit_id, habit_name)

		self.habit_to_check = str(input('\nSelect habit to Check-off: ' ))

		# Getting name of habit selected.
		rows = self.cursor.execute("SELECT habit_name FROM habit_details WHERE habit_id = ? AND username = ?", (self.habit_to_check, self.username)).fetchall()

		# This prevent user from selecting habit id from 
		# other users eventhough the habits are not diplay in the menu
		if len(rows) == 0:
			print('\nWrong habit_id! Returning to Main Menu.\n')
			return

		for row in rows:

			habit_name = row[0]

		# Get current time.
		#check_time = datetime.now().strftime('%H:%M:%S')

		# Get current date
		check_date = datetime.now()

		habit_information = [(self.username,str(self.habit_to_check), habit_name, str(check_date))]

		# Storing habit information. 
		self.cursor.executemany("INSERT INTO habit_log(username, habit_id, habit_name, check_date) VALUES (?,?,?,?)", habit_information)
		# Making change consistent.
		self.connection.commit()

		# Increase habit.
		self.increase_frequency_count()
		
		# Check status?? To tell the user what is left to complete the period.
		####
		print(habit_name + ' checked!\n')

	
	def assign_habit_id(self):
		''' Function to assign a habit_id.'''

		# Searching for last habit_id
		rows = self.cursor.execute("SELECT MAX(habit_id) FROM habit_details").fetchall()
		
		# 
		for row in rows:
			last_habit_id = int(row[0])

		return last_habit_id + 1



	def add_habit(self):
		''' Function to add a new habit in database. '''

		while True:

			# Assigning habit_id
			# try and except is used to assign habit_id 1 when no habit exist.
			try:
				habit_id = self.assign_habit_id()

			except:
				habit_id = '1'

			# Asking user for habit name
			habit_name = input('\nHabit name: ')

			print('\nPeriod: indicates the timeframe in which you expect to perform a habit X number of times. Ex: yearly, monthly, weekly, daily.')
			print('\nFrequency: indicates the how many time you expect to perform a habit in a given period. Ex: 3 times a week, 1 time a day, etc.')

			# Asking user for habit periodicity (integer).
			period = int(input('\nPlease introuduce the habit period in days format (Ex: Yearly = 364 ; Monthly = 30 ; Weekly = 7; Daily = 1): '))

			# Asking user for habit frequency (integer).
			frequency = int(input('\nPlease introduce the habit frequency (Ex: 3 times a week = 3; 2 times a day = 2, 1 time a year = 1): '))


			if input('\nIs the above information correct? y/n: ') == 'y':
				
				# Get todays date
				start_date = datetime.now() #.date()

				# increase start period plus 1 period.
				period_end = start_date + timedelta(days=period)

				status = 'good'

				habit_information = [(self.username, str(habit_id), habit_name, str(period), str(frequency), str(start_date), str(start_date), str(period_end), '0','0',status, '0')]

				# Storing habit information. 
				self.cursor.executemany("INSERT INTO habit_details(username, habit_id, habit_name, period, frequency, start_date, period_start, period_end, frequency_count ,streak_count, status, longest_streak) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", habit_information)

				# Making change consistent.
				self.connection.commit()

				print('\nHabit succesfully added!\n')

				# Returning to Main Menu
				return False


	def remove_habit(self):
		''' Function to delete a habit. '''

		rows = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		# Display habit id and name	
		for row in rows:
			habit_id = row[0]
			habit_name = row[1]

			print(habit_id, habit_name)

		habit_to_delete = str(input('\nSelect habit to delete: ' ))

		# Delete habit from database.
		self.cursor.execute("DELETE FROM habit_details WHERE username = ? AND habit_id = ?", (self.username, habit_to_delete,))
		self.connection.commit()
	

	def current_habit(self):
		''' Function to display current habits.''' 
		
		current_habit_query = self.cursor.execute("SELECT username, habit_id, habit_name, period, frequency, start_date, status FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		# Convert query into dataframe.
		current_habit_df = pd.DataFrame(current_habit_query, columns = ['username', 'habit_id', 'habit_name', 'period', 'frequency', 'start_date', 'status'])
		
		print ('\n',current_habit_df.to_string(index=False),'\n')

		return	current_habit_df


	def habits_by_periodicity(self):
		''' Function to display habits filter by periodicity.'''

		period = input("\nSelect period: ")

		habit_query = self.cursor.execute("SELECT username, habit_id, habit_name, period, frequency, start_date, status FROM habit_details WHERE username = ? AND period = ?",(self.username, period)).fetchall()
		
		if len(habit_query) != 0:

			habit_period_df = pd.DataFrame(habit_query, columns = ['username', 'habit_id', 'habit_name', 'period', 'frequency', 'start_date', 'status'])
			
			print ('\n',habit_period_df.to_string(index=False),'\n')

			return habit_period_df

		else: 

			print('\nNo habits with that period\n')



	def current_habit_streaks(self):
		''' Function to display current habit's streak.'''

		# Display habit id and names.
		habit_id_query = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		habit_id_df = pd.DataFrame(habit_id_query, columns = ['username', 'habit_id'])
		print ('\n',habit_id_df.to_string(index=False), '\n')


		habit_id = input('Select habit: ')


		# Get habit streak.
		streak_query = self.cursor.execute("SELECT username, habit_id, habit_name, streak_count, status FROM habit_details WHERE username = ? AND habit_id =?",(self.username,habit_id)).fetchall()
		
		# Create dataframe and display to user.
		current_habit_df = pd.DataFrame(streak_query, columns = ['username', 'habit_id', 'habit_name', 'streak_count', 'status'])
		print ('\n',current_habit_df.to_string(index=False), '\n')

		return	current_habit_df

	
	def historical_streaks(self):
		''' Function to display historical habits of all habits.'''

		streak_query = self.cursor.execute("SELECT username, habit_id, habit_name, longest_streak FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		historical_streak_df = pd.DataFrame(streak_query, columns = ['username', 'habit_id', 'habit_name', 'longest_historical_streak'])
		print ('\n',historical_streak_df.to_string(index=False), '\n')

		return historical_streak_df


	def habit_log(self):
		''' Function to display log in habit_log table.'''

		# Display habit id and names.
		habit_id_query = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		habit_id_df = pd.DataFrame(habit_id_query, columns = ['username', 'habit_id'])
		print ('\n',habit_id_df.to_string(index=False), '\n')

		habit_id = input('Select habit: ')

		# Get habit streak.
		streak_query = self.cursor.execute("SELECT * FROM habit_log WHERE username = ? AND habit_id =?",(self.username,habit_id)).fetchall()
		
		# Create dataframe and display to user.
		current_habit_df = pd.DataFrame(streak_query, columns = ['username', 'habit_id', 'habit_name', 'check_date'])
		print ('\n',current_habit_df.to_string(index=False), '\n')




	def habit_analytics_submenu(self):
		''' Function to display Habit Analytics menu.'''

		#List of submenu to display
		analytics_submenu = ['Current habits', 'Habits by periodicity', 'Streak by habit', 'Historial streaks', 'Check-off Habit log']

		for analytic in analytics_submenu:

			print(analytics_submenu.index(analytic) + 1, analytic)
			
		# User submenu selection.
		analytic_selected = input('\nSelect analytic option: ')

		# Calling submenu according to user selection.
		if analytic_selected == '1':

		# Return all currently tracked habits.
			self.current_habit()

		elif analytic_selected == '2':

			# Return all currently with the same habits.
			self.habits_by_periodicity()
			
		elif analytic_selected == '3':

			# Return the longest streak for a given habit.
			self.current_habit_streaks()
			
		elif analytic_selected == '4':

			# Return the longest run streak habit of all habits.
			self.historical_streaks()

		elif analytic_selected == '5':

			# Return the longest run streak habit of all habits.
			self.habit_log()



	def main_menu(self):
		'''Function to display the main menu '''

		while True: 
			
			print('\nMAIN MENU')
			# List of menu options to display	
			menu_options = ['Check-off Habit', 'Add a habit', 'Remove a habit', 'Habit Analytics']
			
			
			for item in menu_options:

				# Displaying menu options to user.
				print(menu_options.index(item) + 1, item)
				
			# User menu selection.
			option_selected = input('\nSelect menu: ')

			# Calling submenu according to user selection.
			if option_selected == '1':

				# Check-off a habit
				self.check_off_habit()
				continue


			elif option_selected == '2':

				# Add a habit
				self.add_habit()
				continue

			elif option_selected == '3':

				# Remove a habit
				self.remove_habit()
				continue

			elif option_selected == '4':
				self.habit_analytics_submenu()
				
				continue

			else:

				print('\nThat menu does not exist. Choose again...\n')


	

if __name__ == '__main__':

	#file_drawing = open('bad_habits.txt', 'r')
	#print(file_drawing.read())
	#file_drawing.close()

	h = Habit()

	h.main_menu()


	## Exit capabilities. 