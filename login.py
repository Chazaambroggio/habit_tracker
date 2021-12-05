import sqlite3
import pandas as pd
from getpass import getpass
import os
import time
from datetime import datetime, timedelta

class Login():


	def __init__(self):
		''' Initialize connection with database.'''
		
		# Start connection with database.
		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		self.connection = connection
		self.cursor = cursor

		# Clear console | Using lambda function.
		# If machine is windows use 'cls', for all other machine use 'clear'
		self.clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


	def login(self):
		''' Function to login an existing user.'''

		while True:

			self.username = input("\nUsername: ")

			# getpass hides the password.
			self.password = getpass("Password: ")

			# Check for credential in db.
			login_query = self.cursor.execute("SELECT username, password FROM login WHERE username = ? AND password = ?",(self.username, self.password)).fetchall()

			# if correct credential were found, then login succesful.
			if len(login_query) != 0:

				self.clearConsole()
				#print('\nSuccesful login!')
				
				return False

			else: 

				print('\nLogin failed!')

				time.sleep(1.5)
				# Clear console 
				self.clearConsole()

				break


	def signup(self):
		''' Function to sign up a new user.'''

		while True:

			self.username = input("\nUsername: ")
			self.password = getpass("Password: ")
			

			# Security check for existing user.
			existing_user = self.cursor.execute("SELECT username FROM login WHERE username = ?",(self.username,)).fetchall()
				
			if len(existing_user) != 0:

				print('Username already exist.')

				# Sleep half a second and clear console.
				time.sleep(1.5)
				self.clearConsole()
				break

			else:

				user_credentials = [(self.username, self.password)]

				# Storing user credentials in db. 
				self.cursor.executemany("INSERT INTO login(username, password) VALUES (?,?)", user_credentials)

				# Making change consistent.
				self.connection.commit()

				# Ask for predefined habits.
				if input('\nAdd predefined habits? y/n: ') == 'y':

					self.predefined_habits()

				print('\nSuccesful signup!')

				# Sleep half a second and clear console.
				time.sleep(1.5)
				self.clearConsole()

				break



	def predefined_habits(self):
		''' Function to add predefined habits into new users. '''

		# Predefined habit's names.
		predefined_habits = ['Coding', 'Read', 'Hike', 'Investing', 'Visiting Family']

		# Predefined habit's periods.
		predefined_periods =  [7, 1, 30, 7, 30]

		# Predefined habit's frequency.
		predefined_frequencies = [5, 1, 2, 1, 1]		

		habit_id = 1

		position = 0

		today = datetime.now()

		# Loop to add habits.
		for habit_name in predefined_habits:

			# Calculating period_end.
			period_end = today + timedelta(days = predefined_periods[position])

			# habit_details information for each predefined habit.
			predefined_habit_details = [(self.username, str(habit_id), habit_name, str(predefined_periods[position]), str(predefined_frequencies[position]), str(today), str(today), str(period_end), '0', '0', 'good', '0')]
			
			# Update db.
			self.cursor.executemany("INSERT INTO habit_details VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", predefined_habit_details)

			# increase id and position.
			habit_id +=1
			position +=1

		self.connection.commit()

		
	def login_menu(self):
		''' Funtion to display login menu'''
		
		print('\n \n Welcome to "Habit Tracker"!\n \n')


		while True:

			#Login menu
			print('\n1) Login \n2) Signup')

			user_selection = input('\nSelect an option: ')

			if user_selection == '1':

				# Only exit loop when login is succesful.
				if self.login() == False:

					break

			elif user_selection == '2':

				self.signup()

			# Clean screen when enter a non-existing option.
			else: 

				# Clear console 
				self.clearConsole()

		# return username to habit_tracker.py
		return self.username	