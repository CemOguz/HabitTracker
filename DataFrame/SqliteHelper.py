import sqlite3 as sql
'''importing SQLite module'''


class SQL:
    """
    The main class for adding and deleting habits to habit table."""

    def __init__(self):
        self.conn = sql.connect("HabitTracker.db")
        self.cursor = self.conn.cursor()
        # We first create the table along with data types.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS habits (habit TEXT,desc TEXT,
        week_or_daily TEXT,date TEXT,streak_days INTEGER,streak_weeks INTEGER,record INTEGER,last_updated TEXT)""")
        self.conn.commit()

    def addTable(self, habitName, habitDesc, weekOrDaily, date, streak=0, streak_weeks=0, record=0):
        '''this function is to add habit including its parameters of name, description and weekly/daily type.'''
        self.cursor.execute(
            f"INSERT INTO habits (habit,desc,week_or_daily,date,streak_days,streak_weeks,record,last_updated) VALUES {habitName, habitDesc, weekOrDaily, date, streak, streak_weeks, record, date}")
        self.conn.commit()

    def deleteFromTable(self, habitName):
        '''deletes a habit from the table.'''
        self.cursor.execute(f"DELETE FROM habits WHERE habit='{habitName}'")
        self.conn.commit()

    def addHabitStreak(self, habitName):
        '''Adds an habit streak to the habit's count according to their type and attributes. Does necessary checks with if statements where necessary'''
        from datetime import datetime
        from App.main import App

        #Calculate the difference of Last updated date and now, and returns an integer.
        days = 0
        weeks = 0
        format = "%Y-%m-%d"
        currentTime = str(datetime.now().date())
        lastUpdated = None
        self.cursor.execute(f"SELECT last_updated FROM habits WHERE habit='{habitName}'")
        for last in self.cursor:
            lastUpdated = str(last[0])
        self.conn.commit()
        lastFormatted = datetime.strptime(lastUpdated, format)
        nowFormatted = datetime.strptime(currentTime, format)
        delta = nowFormatted - lastFormatted # subtraction happens here.
        #print("delta days:  ", delta.days)
        #This was just a check to see the result, so I commented it.---------------

        self.cursor = self.conn.execute(f"SELECT week_or_daily from habits WHERE habit='{habitName}'")
        for row in self.cursor:
            if row[0] == "daily":  # checks if it's a daily habit.

                if delta.days == 0:
                    print("It has not been 24 hours since you last checked off.")
                elif delta.days == 1:  # this part works if user checks off just to daily habit in 1 day.

                    # Adds +1 to streak days count.
                    self.cursor = self.conn.execute(f"SELECT week_or_daily from habits WHERE habit='{habitName}'")
                    for row in self.cursor:
                        if row[0] == "daily":
                            self.cursor = self.conn.execute(
                                f"SELECT streak_days FROM habits WHERE habit = '{habitName}'")
                            for row in self.cursor:
                                days = int(row[0])
                            days += 1
                            # ---------------------------------------------------------------------------------------
                            # # This block checks if streak is larger than the record.
                            self.cursor = self.conn.execute(f"SELECT record FROM habits WHERE habit = '{habitName}'")
                            for row in self.cursor:
                                if days > int(row[0]):
                                    self.cursor.execute(
                                        f"UPDATE habits SET record = '{days}' WHERE habit = '{habitName}'")
                                    self.conn.commit()
                            self.cursor.execute(f"UPDATE habits SET streak_days = '{days}' WHERE habit = '{habitName}'")
                            self.conn.commit()
                            # -----------------------------------------------------------------------

                            #  As the last task, updates the last_updated field with current time.
                            self.cursor = self.conn.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
                            for row in self.cursor:
                                if int(row[0]) % 7 == 0:
                                    self.cursor = self.conn.execute(
                                        f"SELECT streak_weeks FROM habits WHERE habit='{habitName}'")
                                    for i in self.cursor:
                                        weeks = int(i[0])
                                    weeks += 1
                                    self.cursor.execute(
                                        f"UPDATE habits SET streak_weeks = '{weeks}' WHERE habit = '{habitName}'")
                            self.cursor.execute(
                                f"UPDATE habits SET last_updated='{currentTime}' WHERE habit='{habitName}'")
                            self.conn.commit()
                            # ------------------------------------------------------------------
                else:  # If user doesn't check off a daily habit on daily, below code runs.
                    print("You have broken your habit your daily streak and week has been reset to 0 ")
                    self.cursor.execute(
                        f"UPDATE habits SET streak_days='{0}', streak_weeks='{0}',last_updated='{nowFormatted.now().date()}' WHERE habit='{habitName}'")
                    self.conn.commit()
            if row[0] == "weekly":  # checks if it's a weekly habit.

                if delta.days >= 8:  # if user doesn't check off weekly, below code block runs.
                    print("You have broken your habit your daily streak and week has been reset to 0 ")
                    # equals streak days and weeks to zero, and updates last_updated to current time.
                    self.cursor.execute(
                        f"UPDATE habits SET streak_days='{0}', streak_weeks='{0}',last_updated='{currentTime}' WHERE habit='{habitName}'")
                    self.conn.commit()
                if delta.days < 7:  # prints out that user still has days to check off for a weekly habit.
                    print(f"You have {delta.days} days past since last check-off")
                    App().mainMenu()  # returns to main menu
                if delta.days == 7:  # if user checks off on 7 days, below code works.
                    days = 0
                    weeks = 0

                    # adds +1 to week.
                    self.cursor.execute(F"SELECT streak_weeks FROM habits WHERE habit='{habitName}'")
                    for row in self.cursor:
                        weeks = int(row[0])
                    weeks += 1
                    self.cursor.execute(f"UPDATE habits SET streak_weeks = '{weeks}' WHERE habit = '{habitName}'")
                    self.conn.commit()
                    # ------------------------------------------------

                    # adds 7 days to streak days since weak is increased by 1.
                    self.cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
                    seven_days_added = 7
                    for row in self.cursor:
                        seven_days_added += row[0]
                    self.cursor.execute(
                        f"UPDATE habits SET streak_days = '{seven_days_added}' WHERE habit = '{habitName}'")
                    self.conn.commit()
                    # --------------------------------------------------------

                    # updates last updated to current time.
                    self.cursor.execute(f"UPDATE habits SET last_updated='{currentTime}' WHERE habit='{habitName}'")
                    self.conn.commit()
                    # -----------------------------------------------

                    # Below code works if user passes their previous record.
                    self.cursor.execute(f"SELECT record FROM habits WHERE habit='{habitName}'")
                    for row in self.cursor:
                        self.conn.commit()
                        self.cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
                        for i in self.cursor:
                            if int(i[0]) >= row[0]:
                                self.cursor.execute(
                                    f"UPDATE habits SET record='{int(i[0])}' WHERE habit='{habitName}'")
                                self.conn.commit()
                        else:
                            App().mainMenu()  #returns to main menu
                    # -----------------------------------------------------------


#BELOW FUNCTIONS ARE FOR ANALYZING.
    def findLongestHabit(self):
        '''returns the longest day streak of a habit.'''
        self.cursor.execute("SELECT habit, record FROM habits WHERE record = (SELECT MAX(record) FROM habits)")
        result=self.cursor.fetchone()
        return "Habit:", result[0], "Record:", result[1]

    def findAllDailyHabits(self):
        '''returns the all daily habits'''
        self.cursor.execute("SELECT habit FROM habits WHERE week_or_daily='daily'")
        habits = [row[0] for row in self.cursor.fetchall()] # adding all results to a list
        return habits
    def findNumberOfHabits(self):
        '''returns how many habits you have'''
        self.cursor.execute("SELECT COUNT(habit) FROM habits")
        result=self.cursor.fetchone()
        return result[0]
    def longestHabitStreak(self):
        '''returns longest habit streak by day'''
        self.cursor.execute("SELECT habit, streak_days FROM habits WHERE streak_days = (SELECT MAX(streak_days) FROM habits)")
        result = self.cursor.fetchone()
        return "Habit:", result[0], "Streak:", result[1]
    def sumOfAllDays(self):
        '''returns the sum of all days in column'''
        self.cursor.execute("SELECT SUM(streak_days) FROM habits")
        result=self.cursor.fetchone()
        return result[0]
    def sumOfAllWeeks(self):
        '''returns the sum of all weeks in column'''
        self.cursor.execute("SELECT SUM(streak_weeks) FROM habits")
        result = self.cursor.fetchone()
        return result[0]

    def printTable(self):
        '''prints the table just to test if it works properly'''
        self.cursor.execute("SELECT * FROM habits")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def deleteTable(self):
        '''deletes the table'''
        self.cursor.execute("DELETE FROM habits")
        self.conn.commit()
