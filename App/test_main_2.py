import sqlite3 as sql
from datetime import datetime, timedelta
from DataFrame.SqliteHelper import SQL


def test_addHabitStreak_daily(habitName="test1"):
    sql_object = SQL()
    streak_days_1 = None
    streak_days_2 = None
    d = datetime.today() - timedelta(days=1)
    d2 = str(d)
    d3 = d2[0:10]
    conn = sql.connect("HabitTracker.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE habits SET last_updated='{d3}' WHERE habit='{habitName}'")
    cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
    for last in cursor:
        streak_days_1 = str(last[0])
    conn.commit()

    sql_object.addHabitStreak(habitName="test1")

    cursor.execute(f"SELECT streak_days FROM habits WHERE habit='{habitName}'")
    for last in cursor:
        streak_days_2 = str(last[0])
    conn.commit()
    conn.close()

    print("")
    print("TESTING REPORT FOR TEST1 DAILY HABIT")
    assert int(streak_days_2) - int(streak_days_1) == 1
    print("Difference of daily habit is increased by 1.")