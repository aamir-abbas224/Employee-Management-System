import sqlite3 as sql3
from contextlib import contextmanager
import employee as Emp
import report as rep

class FinanceManagement(rep.CompanyReports):
    
    @contextmanager
    def get_db_connection(self):
        conn = None
        try:
            conn = sql3.connect('employee.db')
            yield conn
        finally:
            if conn:
                conn.close()
    
    def Overtime_Summary(self):
        try:
            with self.get_db_connection() as conn:
                c = conn.cursor()
                # Example: assume table 'employees' has columns 'emp_id', 'name', and 'overtime'
                c.execute("""
                    SELECT emp_id, name, SUM(overtime) AS total_overtime
                    FROM employees
                    GROUP BY emp_id, name
                """)
                results = c.fetchall()
                print("Overtime Summary:")
                for row in results:
                    print(f"ID: {row[0]}, Name: {row[1]}, Total Overtime: {row[2]}")
        except sql3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def Salary_Summary(self):
        # Placeholder: implement later
        pass
    
    def Allowance_Summary(self):
        # Placeholder: implement later
        pass
    
    def Total_Payable(self):  # monthly
        # Placeholder: implement later
        pass
