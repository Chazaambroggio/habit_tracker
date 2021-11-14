# Habit Tracker

Habit Tracker allow its users to create, remove and keep track of habits. A habit is any activity that is perform with a certain frequency within a given period of time. Habit Tracker also has analytics capabilities, allowing users to examine their habits in more details. 


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