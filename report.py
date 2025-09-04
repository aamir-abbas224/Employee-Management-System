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
    
    def TotalExitEmployees(self):
        try:
              with self.get_db_connection() as conn:
                c = conn.cursor() 
                c.execute("SELECT COUNT(*) FROM employee WHERE empstatus = 'Exit'")
                count = c.fetchone()[0]
                return count
        except Exception as e:
            raise ValueError(f'Missing/No status found')
    
    def fetch_employee_details(self,empid):
        try:
            with self.get_db_connection() as conn:
                c = conn.cursor() 
                c.execute("SELECT * FROM employee WHERE empid = ?",(empid,))
                result = c.fetchone()[0]
                if not result:
                    raise ValueError(f'No employee with {empid} found!')
                else:
                    return result
        except Exception as e:
            raise ValueError(f'Missing/No employee found')

    
    def Summary(self):   
        emp = Emp.Employee()
        return emp.summary()
        
                   
if __name__ == "__main__":
    emp = CompanyReports()
    
    while True:
        print("\n--- Employee Management CLI ---")
        print("1. Total Employee ")
        print("2. Active Employees ")
        print("3. Inactive Employee ")
        print("4. On-Leave Employees ")
        print("5. Resigned Employees")
        print("6. Fetch Employee Details")
        print("7. Summary")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            emp.total_emp()
        elif choice == '2':
            emp.TotalActiveEmployee()
        elif choice == '3':
            emp.TotalInactiveEmployee()
        elif choice == '4':
            emp.TotalLeaveEmployees()
        elif choice == '5': 
            emp.TotalExitEmployees()
        elif choice == '6':
            empid = int(input("Enter Employee ID : "))
            emp.fetch_employee_details(empid)   
        elif choice == '7':
            emp.summary()   
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")                                 