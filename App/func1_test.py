import App.func1 as f1

def test_func1():
    print("")
    print("TESTING REPORT FOR TEST2 WEEKLY HABIT")
    f1.sevenDaysBefore(habitName='test2')
    print("Streak days value initially is : " + str(f1.streak_days_1))
    f1.addHabitStreak_weekly(habitName='test2')
    print("Streak days value is now increased to : " + str(f1.streak_days_2))
    assert int(f1.streak_days_2) - int(f1.streak_days_1) == 7