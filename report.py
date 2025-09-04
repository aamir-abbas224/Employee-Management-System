import employee as Emp
import sqlite3 as sql3
from contextlib import contextmanager

class CompanyReports(Emp.Employee):
        
    @contextmanager
    def get_db_connection(self):
        conn = None
        try:
            conn = sql3.connect('employee.db')
            yield conn
        finally:
            if conn:
                conn.close()
                    
    def total_emp(self):
        try:
            with self.get_db_connection() as conn:
                c = conn.cursor()
                c.execute('SELECT COUNT(*) FROM employee')
                count = c.fetchone()[0]
                return count
        except sql3.OperationalError as e:
            raise ValueError('No Record exists') from e
        except Exception as e:
            raise ValueError(f'General Error, cant fecth employees: {e} ') from e
        
    def TotalActiveEmployee(self):
        try:
            with self.get_db_connection() as conn:
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM employee WHERE empstatus = 'Active'")
                count = c.fetchone()[0]
                return count
        except Exception as e:
            raise ValueError(f'Missing/No status found : {e}')                
                
    def TotalInactiveEmployee(self):
        try:
            with self.get_db_connection() as conn:
                c= conn.cursor()
                c.execute("SELECT COUNT(*) FROM employee WHERE empstatus = 'Inactive'")
                count = c.fetchone()[0]
                return count
        except Exception as e:
            raise ValueError(f"Missing/No status Found: {e}")
        
    def TotalLeaveEmployees(self):
        try:
            with self.get_db_connection() as conn:
                c = conn.cursor() 
                c.execute("SELECT COUNT(*) FROM employee WHERE empstatus = 'Leave'")
                count = c.fetchone()[0]
                return count
        except Exception as e:
            raise ValueError(f'Missing/No status found')
        
    def TotalVacationEmployees(self):
        try:
              with self.get_db_connection() as conn:
                c = conn.cursor() 
                c.execute("SELECT COUNT(*) FROM employee WHERE empstatus = 'Vacation'")
                count = c.fetchone()[0]
                return count
        except Exception as e:
            raise ValueError(f'Missing/No status found')
        
    def Summary(self):   
        emp = Emp.Employee()
        return emp.summary()
        
                   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

















if __name__ == "__main__":
    emp = CompanyReports()
    
    while True:
        print("\n--- Employee Management CLI ---")
        print("1.  ")
        print("2.  ")
        print("3.  ")
        print("4.  ")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            
        elif choice == '2':
            
        elif choice == '3':
            
        elif choice == '4':
           
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")                