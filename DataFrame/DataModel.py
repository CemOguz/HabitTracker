import sqlite3
import pandas as pd
from tabulate import tabulate
from DataFrame.SqliteHelper import SQL


class Data:
    """
    This class is to display, list and sort the data we add or delete in the DB.
    showData() function is to display the data in a proper table by using tabulate module.
    """

    def __init__(self):
        self.sql = SQL()
        self.conn = sqlite3.connect("HabitTracker.db") # database connection is established here

        # column names and data are added in a dictionary in the format of key and value .
        self.data = {'Description': [], 'Daily/Weekly': [],
                     'Date Started': [], 'Streak (Days)': [],
                     'Streak (Weeks)': [], 'Record': [],'Last Updated':[]}

        self.df = pd.read_sql_query("SELECT * FROM habits", self.conn, index_col="habit") #this is where i choose habit as index.
        # now setting the sql table column names same with self. data column names.
        self.df = self.df.rename(
            columns={'desc': 'Description', 'week_or_daily': 'Daily/Weekly', 'date': 'Date Started',
                     'streak_days': 'Streak (Days)',
                     'streak_weeks': 'Streak (Weeks)', 'record': 'Record','last_updated':'Last Updated'})

        #writing the selected data from db to the columns.
        self.data['Description'] = self.df['Description'].tolist()
        self.data['Daily/Weekly'] = self.df['Daily/Weekly'].tolist()
        self.data['Date Started'] = self.df['Date Started'].tolist()
        self.data['Streak (Days)'] = self.df['Streak (Days)'].tolist()
        self.data['Streak (Weeks)'] = self.df['Streak (Weeks)'].tolist()
        self.data['Record'] = self.df['Record'].tolist()
        self.data['Last Updated']=self.df['Last Updated'].tolist()

    #defining the outer shape of the table
    def showData(self):
        print(tabulate(self.df, tablefmt="rounded_grid", headers="keys"))