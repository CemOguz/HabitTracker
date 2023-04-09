"""

This part is just self-explanatory for myself.

import sqlite3
conn = sqlite3.connect("../DataFrame/HabitTracker.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO habits (habit,desc,week_or_daily,date,streak_days,streak_weeks,record,last_updated) VALUES ('Doctor','visit doctor','weekly','2023-01-16','7','1','7','2023-01-16')")
conn.commit()

print("All data deleted from the table.")

conn.close()
"""


