import sqlite3
from datetime import datetime


class App:
    def __init__(self):
        self.conn = sqlite3.connect('JournalEntries.db')
        self.c = self.conn.cursor()
        self.c.execute("""
                CREATE TABLE IF NOT EXISTS JournalEntries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                entry TEXT NOT NULL,
                time TEXT NOT NULL
                )
                """)

    def add_entry(self):
        entry = input(f"Journal Entry {datetime.now().strftime("%I:%M %p")}: ").rstrip()
        with self.conn:
            self.c.execute("INSERT INTO JournalEntries (date, entry, time) VALUES (:date, :entry, :time)", 
                    {'date': datetime.now().strftime("%Y-%m-%d"), 'entry': entry, 'time': datetime.now().strftime("%I:%M %p")})

    def display_past_entries(self):
        date = input('what is the date of the entry you would like see?(0000Y-00M-00D) ')
        if date != '':
            self.c.execute("SELECT * FROM JournalEntries WHERE date=:date", {'date': date})
        else:
            self.c.execute("SELECT * FROM JournalEntries")
        
        for i, j in enumerate(self.c.fetchall(), 1):
            print(f"{i}. {j}")
        print('\n')

    def update_entry(self):
        old_date = input('What is the date of the entry? (Y-M-D)  ').rstrip
        new_entry = input('What is the new entry?  ' + '\n').rstrip

        with self.conn:
            self.c.execute("UPDATE JournalEntries SET entry = :entry WHERE date = :date", {'date': old_date, 'entry': new_entry})

    def remove_entry(self):
        old_date = input('What is the date of the entry you would like to remove? (Y-M-D)  ').rstrip
        old_entry = input('What was the entry you would like to remove?  ' + '\n').rstrip
        try:
            with self.conn:
                self.c.execute('DELETE from JournalEntries WHERE date=:date AND entry = :entry', {'date': old_date, 'entry': old_entry})
        except sqlite3.ProgrammingError:
            print("Please enter a valid entry and date")
    def run(self):
        while True:
            options = ['Add entry', 'view entry', 'update entry', 'remove entry']
            for i, j in enumerate(options, 1):
                print(f"{i}. {j}")
            print('press q to quit')
            choice = input("What would you like to do?: ")
            if choice == '1':
                self.add_entry()
            elif choice == '2':
                self.display_past_entries()
            elif choice == '3':
                self.update_entry()
            elif choice == '4':
                self.remove_entry()
            elif choice == 'q' or 'Q':
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == '__main__':
    instance = App()
    instance.run()

