import unittest
from habit_tracker import Habit
import pandas as pd
import sqlite3
from pandas.util.testing import assert_frame_equal

class TestHabit(unittest.TestCase):
	global habit_tracker
	habit_tracker = Habit()

	def test_current_habit(self):
		''' Function to test Analytucs module - Current habits.'''


		# Expected dataframe when filter by habit periodicity.
		test_list = [
		['root','1', 'Coding', int('7'), int('5'), '2021-10-01 00:00:00.1', 'broken'],
		['root','2', 'Read', int('1'), int('1'), '2021-10-01 00:00:00.1', 'broken'],
		['root','3', 'Hike', int('30'), int('2'), '2021-10-07 00:00:00.1', 'good'], 
		['root','4','Investing', int('7'), int('1'),'2021-10-07 00:00:00.1','broken'],
		['root','5', 'Visiting Family', int('30'), int('1'), '2021-10-15 00:00:00.1', 'good']
		]
		
		expected_df = pd.DataFrame(test_list, columns=['username', 'habit_id', 'habit_name', 'period', 'frequency', 'start_date', 'status'])

		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		# Storing df to test.
	
		test_df = habit_tracker.current_habit()
		
		# Comparing both dataframes.
		pd.testing.assert_frame_equal(test_df, expected_df)



	def test_habit_by_period(self):
		''' Function to test Analytucs module - Habit by periodicity.'''

		# Expected dataframe when filter by habit periodicity.
		test_list = [
		['root','1', 'Coding', int('7'), int('5'), '2021-10-01 00:00:00.1', 'broken'], 
		['root','4','Investing', int('7'), int('1'),'2021-10-07 00:00:00.1','broken']
		]
		
		expected_df = pd.DataFrame(test_list, columns=['username', 'habit_id', 'habit_name', 'period', 'frequency', 'start_date', 'status'])

		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		# Storing df to test.
		
		test_df = habit_tracker.habits_by_periodicity()
		
		# Comparing both dataframes.
		pd.testing.assert_frame_equal(test_df, expected_df)

	
	def test_current_habit_streaks(self):
		''' Function to test Analytucs module - Streak by habit streak.'''

		# Expected dataframe when filter by habit periodicity.
		test_list = [
		['root','3', 'Hike', int('1'), 'good'], 
		]
		
		expected_df = pd.DataFrame(test_list, columns=['username', 'habit_id', 'habit_name', 'streak_count', 'status'])

		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		# Storing df to test.
		
		test_df = habit_tracker.current_habit_streaks()
		
		# Comparing both dataframes.
		pd.testing.assert_frame_equal(test_df, expected_df)



	def test_historical_streaks(self):
		''' Function to test Analytucs module - Historical streaks.'''

		# Expected dataframe when filter by historical streaks.
		test_list = [
		['root','1', 'Coding', int('3')],
		['root','2', 'Read', int('22')],
		['root','3', 'Hike', int('1')],
		['root','4', 'Investing', int('5')],
		['root','5', 'Visiting Family', int('0')], 
		]
		
		expected_df = pd.DataFrame(test_list, columns=['username', 'habit_id', 'habit_name', 'longest_historical_streak'])

		connection = sqlite3.connect("habit_database.db")
		cursor = connection.cursor()

		# Storing df to test.
		
		test_df = habit_tracker.historical_streaks()
		
		# Comparing both dataframes.
		pd.testing.assert_frame_equal(test_df, expected_df)




if __name__ == '__main__':

	unittest.main()