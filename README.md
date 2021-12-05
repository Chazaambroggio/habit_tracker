# Habit Tracker

Habit Tracker allow its users to create, remove and keep track of habits. A habit is any activity that is perform with a certain frequency within a given period of time. Habit Tracker also has analytics capabilities, allowing users to examine their habits in more details. 

## Technologies

Project created with:

- Python version: 3.9.7

## Requeriments
- Pandas version: 1.3.4

## Installation

To install Habit Tracker you must have [Python 3](https://www.python.org/downloads/) and [GIT](https://git-scm.com/downloads) installed in your pc.

The following instructions only apply to windows machines. 

Download the app's files from the following Github repository.

```bash
git clone https://github.com/Chazaambroggio/habit_tracker.git
````

Navegate to the file habit_tracker that was just cloned into your pc.
```bash
cd habit_tracker
````

Create a virtual environment. 
```bash
py -m venv venv
```

Activate the virtual environment.
```bash
venv\Scripts\activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install app requeriments.
```bash
pip install -r requirements.txt
```

Lunch the app using Python.
```bash
py habit_tracker.py
```

## Usage

The Habit Tracker app comes with a default user (username: 'root', password: 'root'). The account root has 5 predefine habits and 4 weeks of tracked data. This account could be used by a potential new user to explore the app capabilities without the necesity of creating a personal account. 

First, the user will encounter a login menu with a login and sign-up option. New users will have to create an account first, and then login with their credentials.

After a succesful login the user will see a main menu with 4 options:

- Check-off: check-off performed habits.
- Add: Add a new habit.
- Remove: Remove a habit.
- Analytics: Analytics module.

The Analytics module offers a submenu with different analytics capabilities.

- Current habits.
- Habits by periodicity.
- Streak by habit.
- Historical longest streak.
- Check-off habit log.

