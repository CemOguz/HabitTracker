from DataFrame.DataModel import Data
from DataFrame.SqliteHelper import SQL


class App:
    """first class in main.py.
    Needs to be run for the application to start."""

    def __init__(self):
        self.sql = SQL()

    def mainMenu(self):
        '''calls and displays the main menu after a task is completed by user.'''
        #the reason this is not under the init function is that we have to refresh the table each time we get back to the menu.
        #if it was under the init, since the class was called for once, it would not refresh the table after a new update.
        Data().showData()
        print(" / WELCOME TO HABIT TRACKER \ ".center(90))
        print("  | Please Select an Option  |  ".center(90))
        print("   (1) Check Off Habit    ".center(90))
        print("   (2) Manage Habits    ".center(90))
        print("   (3) Analyze Habits   ".center(90))
        print("   (4) Exit    ".center(90))
        choice = input("\nYour Choice: ")

        if choice == "1":
            self.checkOff()
        if choice == "2":
            self.manageHabits()
        if choice == "3":
            print("(1) What's my longest habit?\n(2) What's the list of my current daily habits?\n"
                  "(3) What's the number of habits\n(4) What's my longest habit streak?\n"
                  "(5) What's the sum of all days in my tracker\n(6) What's the sum of all weeks in my tracker\n")
            analyzeChoice = input("Please select a choice: ")
            # this if block returns the answer of selected options from above questions.
            if analyzeChoice == "1":
                print(self.sql.findLongestHabit())
                self.mainMenu()
            if analyzeChoice == "2":
                print("Your daily habits are: ")
                print(self.sql.findAllDailyHabits())
                self.mainMenu()
            if analyzeChoice == "3":
                print(f"You have {self.sql.findNumberOfHabits()} habits")
                self.mainMenu()
            if analyzeChoice == "4":
                print("Your longest habit streak is: ", self.sql.longestHabitStreak())
                self.mainMenu()
            if analyzeChoice == "5":
                print("Sum of all days is: ", self.sql.sumOfAllDays())
                self.mainMenu()
            if analyzeChoice == "6":
                print("Sum of all weeks is: ", self.sql.sumOfAllWeeks())
                self.mainMenu()
            #--------------------------------------------------------------
    def checkOff(self):
        '''this function is called to check off a habit.'''
        habitName = input("Please enter a habit name so it will be added to your Habit Streak (0 for main menu): ")
        if habitName == 0:
            self.mainMenu()
        else:
            self.sql.addHabitStreak(f"{habitName}")
            self.mainMenu()

    def manageHabits(self):
        '''add or delete an habit'''
        print("What do you want to do on habit tracker? ".center(90))
        print("(1) Add a New Habit".center(90))
        print("(2) Delete a Habit".center(90))
        print("(3) Back to main menu".center(90))
        choiceHabits = input("\nYour Choice: ")
        if choiceHabits == "1":
            backChoice = input("Add Habits (you can go back by pressing 1 to continue, press any button to keep going): ")
            if backChoice == "1":
                self.mainMenu()
            else:
                #asks all the attributes of an habit, and inserts into table on the database.
                habitName = input("Your habit name: ")
                habitDesc = input("Enter a description for the habit: ")
                dayOrWeek = input("Is the habit daily or weekly?: ").lower()
                startDay = input("Start Date YYYY-MM-DD: ")

                self.sql.addTable(habitName, habitDesc, dayOrWeek, startDay)
                print(f"{habitName} Has Been Successfully Added to your habits".upper())
                self.mainMenu() # let's go back to main menu
                #----------------------------------------------------------------------
        if choiceHabits == "2":
            choice = input("Which habit would you like to delete? (1 for main menu): ")
            if choice == "1":
                self.mainMenu()
            else:
                # we call this function to delete an entire habit row.
                self.sql.deleteFromTable(f"{choice}")
                print(f"Successfully Deleted {choice} from your habit table".upper())
                self.mainMenu()
                #-------------------------------------------------
        if choiceHabits == "3":
            self.mainMenu()

if __name__ == "__main__":
    App().mainMenu()  # Application starts running here.