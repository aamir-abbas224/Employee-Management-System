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
                c.execute("SELECt  , SUM(overtime)")
                    
    def Salary_Summary(self):
        pass
    
    def Allowance_Summary(self):
        pass
    
    def Total_Payable(self):            #monthly
        pass
    