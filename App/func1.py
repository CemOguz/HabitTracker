import sqlite3 as sql
from datetime import datetime, timedelta

def sevenDaysBefore(habitName):
    global streak_days_1
    d = datetime.today() - timedelta(days=7)
    d2 = str(d)
    d3 = d2[0:10]
    conn = sql.connect("HabitTracker.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE habits SET last_updated='{d3}' WHERE habit='{habitName}'")
    cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
    for last in cursor:
        streak_days_1 = str(last[0])
    conn.commit()
    conn.close()

def addHabitStreak_weekly(habitName):
    global streak_days_2
    weeks = 0
    conn = sql.connect("HabitTracker.db")
    cursor = conn.cursor()

    # ------------------------------------------------
    # adds +1 to week.
    cursor.execute(F"SELECT streak_weeks FROM habits WHERE habit='{habitName}'")
    for row in cursor:
        weeks = int(row[0])
    weeks += 1
    cursor.execute(f"UPDATE habits SET streak_weeks = '{weeks}' WHERE habit = '{habitName}'")
    conn.commit()

    # adds 7 days to streak days since weak is increased by 1.
    cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
    seven_days_added = 7
    for row in cursor:
        seven_days_added += row[0]
    cursor.execute(
        f"UPDATE habits SET streak_days = '{seven_days_added}' WHERE habit = '{habitName}'")
    conn.commit()
    # --------------------------------------------------------

    # Below code works if user passes their previous record.
    cursor.execute(f"SELECT record FROM habits WHERE habit='{habitName}'")
    for row in cursor:
        conn.commit()
        cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
        for i in cursor:
            if int(i[0]) >= row[0]:
                cursor.execute(
                    f"UPDATE habits SET record='{int(i[0])}' WHERE habit='{habitName}'")
                conn.commit()

    cursor.execute(f"UPDATE habits SET last_updated='{str(datetime.today())[0:10]}' WHERE habit='{habitName}'")
    conn.commit()

    # ----------------------------
    cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
    for last in cursor:
        streak_days_2 = str(last[0])
    conn.commit()
    conn.close()

    # -----------------------------

sevenDaysBefore(habitName="test2")
addHabitStreak_weekly(habitName="test2")
