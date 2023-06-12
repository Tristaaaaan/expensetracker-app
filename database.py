import sqlite3


class Database:
    def __init__(self):
        self.data_con = sqlite3.connect('expense.db')
        self.spent = self.data_con.cursor()
        self.create_database()

    def create_database(self):
        """Create expense table"""
        self.spent.execute(
            "CREATE TABLE IF NOT EXISTS expense(id integer PRIMARY KEY AUTOINCREMENT, money_spent integer NOT NULL, due_date varchar(50), category varchar(20) NOT NULL)")
        self.data_con.commit()

    def create_expenses(self, money, date, category):
        """Create an expense"""
        self.spent.execute(
            "INSERT INTO expense(money_spent, due_date, category) VALUES(?, ?, ?)", (money, date, category,))
        self.data_con.commit()

        # Obtaining the last item to insert in the list on the application
        select_expense = self.spent.execute(
            "SELECT * FROM expense WHERE money_spent = ?", (money,)).fetchall()

        return select_expense[-1]

    def obtain_expenses(self, date):
        """Get expenses from the current date"""
        day_expenses = self.spent.execute(
            "SELECT * FROM expense WHERE due_date = ?", (date,)).fetchall()

        return day_expenses

    def delete_expense(self, prim_key):
        """Delete a task"""
        self.spent.execute("DELETE FROM expense WHERE id=?", (prim_key,))

        self.data_con.commit()

    def all_data(self):
        expenses_data = self.spent.execute("SELECT * FROM expense").fetchall()

        return expenses_data

    def expenses_sum(self):
        """Getting the sum of expenses"""
        spent_sum = self.spent.execute(
            "SELECT sum(money_spent) FROM expense").fetchall()

        expense_sum = sum(res[0] for res in spent_sum)

        return expense_sum

    def asc_expenses(self):
        """Ascending order of dates"""
        asc_expenses = self.spent.execute(
            "SELECT * FROM expense ORDER BY strftime('%Y-%m-%d', due_date) DESC").fetchall()

        return asc_expenses

    def close_db_connection(self):
        self.data_con.close()
