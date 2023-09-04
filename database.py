import psycopg2
import threading
import time
import json


class Database:
    def __init__(self):
        self.spent = None
        self.start_time = None  # Store the start time

    def connect_to_database(self):
        self.start_time = time.time()  # Record the start time
        credentials = self.get_credentials()

        # Create a connection
        self.data_con = psycopg2.connect(
            host=credentials["database_host"],
            port=credentials["port"],
            database=credentials["database_name"],
            user=credentials["database_user"],
            password=credentials["database_password"]
        )

        self.spent = self.data_con.cursor()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - self.start_time
        # Print the elapsed time
        print(f"Database loaded in {elapsed_time:.2f} seconds")

    def get_credentials(self):
        try:
            with open('credentials/database.json', 'r') as config_file:
                config_data = json.load(config_file)
            return config_data
        except FileNotFoundError:
            print("Config file not found.")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON format in config file.")
            return None

    # def create_database(self):
    #     """Create expense table"""
    #     self.spent.execute(
    #         "CREATE TABLE IF NOT EXISTS expense (id SERIAL PRIMARY KEY, money_spent INTEGER NOT NULL, due_date VARCHAR(50), category VARCHAR(20) NOT NULL)")

    #     self.data_con.commit()

    def create_expenses(self, money, date, category):
        """Create an expense"""
        self.spent.execute(
            "INSERT INTO expense (money_spent, due_date, category) VALUES (%s, %s, %s)",
            (money, date, category)
        )
        self.data_con.commit()

        # Obtaining the last item to insert in the list on the application
        self.spent.execute(
            "SELECT * FROM expense WHERE money_spent = %s", (money,))

        select_expense = self.spent.fetchall()

        return select_expense[-1]

    def obtain_expenses(self, date):
        """Get expenses from the current date"""
        self.spent.execute(
            "SELECT id, money_spent, category FROM expense WHERE due_date = %s", (date,))

        day_expenses = self.spent.fetchall()

        return day_expenses

    def delete_expense(self, prim_key):
        """Delete a task"""
        self.spent.execute("DELETE FROM expense WHERE id=%s", (prim_key,))

        self.data_con.commit()

    def all_data(self):

        self.spent.execute(
            "SELECT id, money_spent, category FROM expense")

        expenses_data = self.spent.fetchall()

        return expenses_data

    def expenses_sum(self):
        """Getting the sum of expenses"""

        self.spent.execute(
            "SELECT sum(money_spent) FROM expense")

        spent_sum = self.spent.fetchall()

        expense_sum = sum(res[0] for res in spent_sum)

        return expense_sum

    def asc_expenses(self):
        """Ascending order of dates"""
        self.spent.execute(
            "SELECT * FROM expense ORDER BY strftime('%Y-%m-%d', due_date) DESC")

        asc_expenses = self.spent.fetchall()

        return asc_expenses

    def close_db_connection(self):
        self.data_con.close()
