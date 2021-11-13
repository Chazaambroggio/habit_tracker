import sqlite3
import pandas as pd
from getpass import getpass


class Login():


	def __init__(self):
		''' Initialize connection with database.'''
		
		# Start connection with database.
		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		self.connection = connection
		self.cursor = cursor


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

				print('\nSuccesful login!')
				
				return False

			else: 

				print('\nLogin failed!')
				break


	def signup(self):
		''' Function to sign up a new user.'''

		while True:

			self.username = input("\nUsername: ")
			self.password = getpass("Password: ")
			

			# Security check.
			existing_user = self.cursor.execute("SELECT username FROM login WHERE username = ?",(self.username,)).fetchall()
				
			if len(existing_user) != 0:

				print('Username already exist.')

			else:
				
				break


		user_credentials = [(self.username, self.password)]

		# Storing user credentials. 
		self.cursor.executemany("INSERT INTO login(username, password) VALUES (?,?)", user_credentials)

		# Making change consistent.
		self.connection.commit()

		print('\nSuccesful signup!')


		
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


		return self.username	