import database
import default_user
import pandas as pd
import sqlite3
from datetime import datetime, date, time, timedelta
from login import Login
import os
import time

class Habit():	

	def __init__(self):
		''' Initialize connection with database.'''
		
		# Start connection with database.
		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		self.connection = connection
		self.cursor = cursor

		# Adjusting habit periods.
		self.adjust_habits_periods()

		l = Login()
		
		self.username = l.login_menu()

		# Clear console | Using lambda function.
		# If machine is windows use 'cls', for all other machine use 'clear'
		self.clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


	
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

		# Note: habit status are only updated at the end of the period
		# otherwise a habit status would always be 'broken' at the beginning 
		# of the priod while frequency > than frequency count. 
		# That is not proper functioning. 
			
		# Only check for status after period is over.
		if self.today - self.period_start >= timedelta(days = self.period):

		# Check if the habit was performed enough times during the period.
			if self.frequency_count >= self.frequency:	

				# Change status to 'good' and increase habit streak.
				status = 'good'
				self.increase_habit_streak()

			else:

				# Change status to 'broken' and reset habit streak.
				status = 'broken'
				self.reset_habit_streak()
			
			# Update database.
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

		# Update habit streak count in db.
		streak_update =	"UPDATE habit_details SET streak_count = \'" + str(streak_count) + "\', longest_streak = \'" + str(current_longest_streak) + "\' WHERE habit_id = \'" + self.habit_id + "\';"
		self.cursor.execute(streak_update)
		self.connection.commit()

	
	def reset_habit_streak(self):
		''' Function to reset streak.''' 

		# Reset habit streak count to 0.
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

		# Update habit streak count.
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

		print("CHECK-OFF A HABIT")
	
		# Display all habit id and name.
		rows = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?", (self.username,)).fetchall()
		
		# Clean data from tuple format.
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
			print('\nWrong habit_id! Returning to Main Menu...\n')

			# Wait half a second and clear console.
			time.sleep(1.5)
			self.clearConsole()
			
			return

		# Clean data from tuple format.
		for row in rows:

			habit_name = row[0]


		# Get current date
		check_date = datetime.now()

		habit_information = [(self.username,str(self.habit_to_check), habit_name, str(check_date))]

		# Storing habit information. 
		self.cursor.executemany("INSERT INTO habit_log(username, habit_id, habit_name, check_date) VALUES (?,?,?,?)", habit_information)
		# Making change consistent.
		self.connection.commit()

		print(habit_name + ' checked!\n')

		# Increase habit.
		self.increase_frequency_count()
			
		# Wait two and a half seconds and clean console.
		time.sleep(2.5)
		self.clearConsole() 
		

	
	def assign_habit_id(self):
		''' Function to assign a habit_id.'''

		# Searching for last habit_id
		rows = self.cursor.execute("SELECT MAX(habit_id) FROM habit_details WHERE username = ?", (self.username,)).fetchall()

		# Extract from tuple format.
		for row in rows:
			last_habit_id = int(row[0])

		return last_habit_id + 1



	def add_habit(self):
		''' Function to add a new habit in database. '''

		while True:

			# Assigning habit_id
			# try and except is used to assign habit_id 1 when no habit exist.
			try:
				# Get habit_id#
				habit_id = self.assign_habit_id()

			except:
				habit_id = '1'

			# Asking user for habit name
			habit_name = input('\nHabit name: ')

			print('\nPeriod: indicates the timeframe in which you expect to perform a habit X number of times. Ex: yearly, monthly, weekly, daily.')
			print('\nFrequency: indicates the how many time you expect to perform a habit in a given period. Ex: 3 times a week, 1 time a day, etc.')

			# Loop used to ensure acceptable answer.
			while True:

				# Asking user for habit periodicity (integer).
				period = input('\nPlease introuduce the habit period in days format using numbers (Ex: Yearly = 364 ; Monthly = 30 ; Weekly = 7; Daily = 1): ')

				# Checking for a numeric answer.
				if period.isnumeric() == True:
					break

				else: 
					# Wait and clear.
					print('Please enter a number.')
					time.sleep(2)
					self.clearConsole()

			# Loop used to ensure acceptable answer.
			while True:

				# Asking user for habit frequency (integer).
				frequency = input('\nPlease introduce the habit frequency (Ex: 3 times a week = 3; 2 times a day = 2, 1 time a year = 1): ')

				if frequency.isnumeric() == True:
					break 

				else:
					# Wait and clear.
					print('Please enter a number.')
					time.sleep(2)
					self.clearConsole()

					
			correct = input('\nIs the above information correct? y/n or exit: ')

			if correct == 'y':
				
				# Get todays date
				start_date = datetime.now() #.date()

				# increase start period plus 1 period.
				period_end = start_date + timedelta(days=int(period))

				status = 'good'

				habit_information = [(self.username, str(habit_id), habit_name, str(period), str(frequency), str(start_date), str(start_date), str(period_end), '0','0',status, '0')]

				# Storing habit information. 
				self.cursor.executemany("INSERT INTO habit_details(username, habit_id, habit_name, period, frequency, start_date, period_start, period_end, frequency_count ,streak_count, status, longest_streak) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", habit_information)

				# Making change consistent.
				self.connection.commit()

				print('\nHabit succesfully added!\n')

				# Sleep and clear.
				time.sleep(1.5)
				self.clearConsole()

				# Returning to Main Menu
				return False

			elif correct == 'exit':

				# Clean console and return to Main Menu.
				self.clearConsole()
				break

			# Clean console with incorrect info and return to top of loop.
			time.sleep(1.5)
			self.clearConsole()


	def remove_habit(self):
		''' Function to delete a habit. '''

		rows = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		# Display habit id and name	
		for row in rows:

			habit_id = row[0]
			habit_name = row[1]

			print(habit_id, habit_name)

		habit_to_delete = str(input('\nSelect habit to delete: ' ))

		# Preventing user from deleting habit that are not displayed or that belong to another user.
		security_check = self.cursor.execute("SELECT habit_name FROM habit_details WHERE habit_id = ? AND username = ?", (habit_to_delete, self.username)).fetchall()

		# This prevent user from selecting habit id from 
		# other users eventhough the habits are not diplay in the menu
		if len(security_check) == 0:

			print('\nWrong habit_id! Returning to Main Menu...\n')

			# Wait half a second and clear console.
			time.sleep(1.5)
			self.clearConsole()
			
			return

		# If security check is good then
		# Delete habit from database.
		self.cursor.execute("DELETE FROM habit_details WHERE username = ? AND habit_id = ?", (self.username, habit_to_delete,))
		self.connection.commit()

		# Clean console.
		self.clearConsole()



	def current_habit(self):
		''' Function to display current habits.''' 
		
		current_habit_query = self.cursor.execute("SELECT username, habit_id, habit_name, period, frequency, start_date, status FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		# Convert query into dataframe.
		current_habit_df = pd.DataFrame(current_habit_query, columns = ['username', 'habit_id', 'habit_name', 'period', 'frequency', 'start_date', 'status'])
		
		# Check for data existance
		if len(current_habit_df) != 0:
			
			# Display table.
			print ('\n',current_habit_df.to_string(index=False),'\n')

		else:
			print('No data.\n')

		# Exit capability.
		while True:
			if input('\'exit\' to return: ') == 'exit':

				# Clean console.
				self.clearConsole()
				return current_habit_df


	def habits_by_periodicity(self):
		''' Function to display habits filter by periodicity.'''

		period = input("\nSelect period: ")

		habit_query = self.cursor.execute("SELECT username, habit_id, habit_name, period, frequency, start_date, status FROM habit_details WHERE username = ? AND period = ?",(self.username, period)).fetchall()
		
		# Check for data existance.
		if len(habit_query) != 0:

			habit_period_df = pd.DataFrame(habit_query, columns = ['username', 'habit_id', 'habit_name', 'period', 'frequency', 'start_date', 'status'])
			
			# Display table.
			print ('\n',habit_period_df.to_string(index=False),'\n')

			# Exit capability.
			while True:
				if input('\'exit\' to return: ') == 'exit':

					# Clean console.
					self.clearConsole()
					break

			return habit_period_df

		else: 

			print('\nNo habits with that period!\n')

			# Sleep and clean console.
			time.sleep(1.5)
			self.clearConsole()


	def current_habit_streaks(self):
		''' Function to display current habit's streak.'''

		# Get habit id and names from db.
		habit_id_query = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?",(self.username,)).fetchall()

		# Making df.
		habit_id_df = pd.DataFrame(habit_id_query, columns = ['username', 'habit_id'])

		# Check for data existance.
		if len(habit_id_df) != 0:

			# Display table.
			print ('\n',habit_id_df.to_string(index=False), '\n')

		else:

			print('No data.')

			# Sleep, clean and return to Analytics Submenu.
			time.sleep(1.5)
			self.clearConsole()
			return

		habit_id = input('Select habit: ')

		# Get habit streak.
		streak_query = self.cursor.execute("SELECT username, habit_id, habit_name, streak_count, status FROM habit_details WHERE username = ? AND habit_id =?",(self.username,habit_id)).fetchall()
		
		# Security_check.
		if len(streak_query) != 0:

			# Create dataframe 
			current_habit_df = pd.DataFrame(streak_query, columns = ['username', 'habit_id', 'habit_name', 'streak_count', 'status'])

			# Display to user.
			print ('\n',current_habit_df.to_string(index=False), '\n')

			# Exit capability.
			while True:

				if input('\'exit\' to return: ') == 'exit':

					# Clean console.
					self.clearConsole()

					break

			return	current_habit_df

		else: 

			print('\nWrong habit id. Returning to Main Menu...\n')

			# Sleep and clean console.
			time.sleep(1.5)
			self.clearConsole()

	
	def historical_streaks(self):
		''' Function to display historical habits of all habits.'''

		# Getting the historical streak of the user's habits.
		streak_query = self.cursor.execute("SELECT username, habit_id, habit_name, longest_streak FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		# Columns
		historical_streak_df = pd.DataFrame(streak_query, columns = ['username', 'habit_id', 'habit_name', 'longest_historical_streak'])

		# Check for data existance.
		if len(historical_streak_df) !=0:

			# Display table
			print ('\n',historical_streak_df.to_string(index=False), '\n')
		
		else:

			print('No data.\n')

		# Exit capability.
		while True:

			if input('\'exit\' to return: ') == 'exit':

				# Clean console.
				self.clearConsole()
				break

		return historical_streak_df


	def habit_log(self):
		''' Function to display log in habit_log table.'''

		# Display habit id and names.
		habit_id_query = self.cursor.execute("SELECT habit_id, habit_name FROM habit_details WHERE username = ?",(self.username,)).fetchall()
		
		habit_log_df = pd.DataFrame(habit_id_query, columns = ['username', 'habit_id'])

		# Check for data existance.
		if len(habit_log_df) !=0:

			print ('\n',habit_log_df.to_string(index=False), '\n')

		else:

			print('No data.')

			# Sleep and clear console
			time.sleep(1.5)
			self.clearConsole()
			return

		habit_id = input('Select habit: ')

		# Get habit log.
		habit_query = self.cursor.execute("SELECT * FROM habit_log WHERE username = ? AND habit_id =?",(self.username,habit_id)).fetchall()
		
		if len(habit_query) != 0:

			# Create dataframe and display to user.
			current_habit_df = pd.DataFrame(habit_query, columns = ['username', 'habit_id', 'habit_name', 'check_date'])
		
			# Display table.		
			print ('\n',current_habit_df.to_string(index=False), '\n')

			# Exit capability.
			while True:

				if input('\'exit\' to return: ') == 'exit':

					# Clean console.
					self.clearConsole()
					break

			return current_habit_df

		else:
			
			print(self.username + ' has no data to display.')

			# Sleep and clear console.
			time.sleep(2.25)
			self.clearConsole()


	def habit_analytics_submenu(self):
		''' Function to display Habit Analytics menu.'''

		# Print title.
		print('HABIT ANALYTICS')

		# List of submenu to display
		analytics_submenu = ['Current habits', 'Habits by periodicity', 'Streak by habit', 'Historial streaks', 'Check-off Habit log', 'Exit']

		for analytic in analytics_submenu:

			print(analytics_submenu.index(analytic) + 1, analytic)
			
		# User submenu selection.
		analytic_selected = input('\nSelect analytic option: ')

		# Calling submenu according to user selection.
		if analytic_selected == '1':

			# Clear console
			self.clearConsole()

			# Return all currently tracked habits.
			self.current_habit()
			

		elif analytic_selected == '2':

			# Clear console
			self.clearConsole()

			# Return all currently with the same habits.
			self.habits_by_periodicity()
			
		elif analytic_selected == '3':

			# Clear console
			self.clearConsole()

			# Return the longest streak for a given habit.
			self.current_habit_streaks()
			
		elif analytic_selected == '4':
			
			# Clear console
			self.clearConsole()

			# Return the longest run streak habit of all habits.
			self.historical_streaks()

		elif analytic_selected == '5':

			# Clear console
			self.clearConsole()

			# Return the longest run streak habit of all habits.
			self.habit_log()

		elif analytic_selected == '6':

			# Clear console and returns to Main Menu.
			self.clearConsole()
			pass

		else:

			#CLear console
			self.clearConsole()

			#Display Analytics Submenu again.
			self.habit_analytics_submenu()



	def main_menu(self):
		'''Function to display the main menu '''

		while True: 
			
			print('\nMAIN MENU')
			# List of menu options to display	
			menu_options = ['Check-off Habit', 'Add a habit', 'Remove a habit', 'Habit Analytics', 'Log out']
			
			
			for item in menu_options:

				# Displaying menu options to user.
				print(menu_options.index(item) + 1, item)
				
			# User menu selection.
			option_selected = input('\nSelect menu: ')

			# Calling submenu according to user selection.
			if option_selected == '1':

				# Clear console.
				self.clearConsole()

				# Check-off a habit
				self.check_off_habit()
				continue


			elif option_selected == '2':
				
				# Clear console.
				self.clearConsole()

				# Add a habit
				self.add_habit()
				continue

			elif option_selected == '3':

				# Clear console.
				self.clearConsole()

				# Remove a habit
				self.remove_habit()
				continue

			elif option_selected == '4':

				# Clear console.
				self.clearConsole()

				# Habit analytics.
				self.habit_analytics_submenu()
				
				continue

			elif option_selected == '5':

				# Clear console.
				self.clearConsole()

				# Habit analytics.
				self.username = Login().login_menu()
				
				continue

			else:

				print('\nThat menu does not exist. Choose again...\n')
				
				# Sleep for half a second and clean console.
				time.sleep(1.5)
				self.clearConsole()


	

if __name__ == '__main__':


	clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

	clearConsole()

	h = Habit()

	h.main_menu()
	

