import sqlite3 as sql3
from contextlib import contextmanager


class Employee:
    def __init__(self, name:str = "", site:str = "", salary:float = 0.0, empstatus:str = "",empdept:str = ""):
        self._empstatus = empstatus # Employee Status
        self._name = name
        self._salary = salary
        self._site  =  site
        self._empdept = empdept
        
    @contextmanager
    def get_db_connection(self):
        conn = None
        try:
            conn = sql3.connect('employee.db')
            yield conn
        finally:
            if conn:
                conn.close()
                
    def validate_salary(self,salary):
         if salary < 0:
             raise ValueError('Error! Negative Salary') 
         return salary  
             
    def validate_status(self,status):
        valid_status = ['Active','Inactive','On-Leave','Vacation']
        status_cap = status.strip().title()
        if status not in valid_status:
            raise ValueError('Invalid Status')
        return status.capitalize()
    
    def validate_empid_exists(self,empid):
        with self.get_db_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM employee WHERE empid = ?',(empid,))
            count = c.fetchone()[0]
            if count == 0:
                raise ValueError(f'{empid} does not exists')
               
        
    @property
    def empdept(self):
        return self._empdept
    @empdept.setter
    def empdept(self,value):
        self._empdept = value
        
    @property
    def name(self):
         return self._name    
    @name.setter
    def name(self,value):
        self._name = value

    @property
    def site(self):
        return self._site
    @site.setter
    def site(self,value):
        self._site = value
                    
    @property
    def salary(self):
        return self._salary
    @salary.setter
    def salary(self,value):
        self._salary = self.validate_salary(value)    
        
    @property
    def empstatus(self):
        return self._empstatus
    @empstatus.setter
    def empstatus(self,value):
        self._empstatus = self.validate_status(value)
        
    def creating_emp(self):
        try:
            name = input("Enter Employee Name: ").strip()
            if not name:
                raise ValueError('Name cannot be empty')
                
            site = input("Enter Site: ").strip()
            if not site:
                raise ValueError('Site cannot be empty')
            try:
                    
                salary = float(input("Enter Salary: "))
                salary = self.validate_salary(salary)
            except Exception as e:
                if 'could not convert' in str(e):
                    raise ValueError('Please enter a valid salary')
                raise e
                
            status = input('Enter Status :').strip()
            status = self.validate_status(status)
            
            empdept = input("Enter Employee Department: ").strip()
            if not empdept:
                raise ValueError('Provide Department')
    
            # Database operations
            with self.get_db_connection() as conn:
                c = conn.cursor()
            
                c.execute('''
                    CREATE TABLE IF NOT EXISTS employee(
                       empid INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            site TEXT NOT NULL,
                            salary REAL NOT NULL,
                            empstatus TEXT NOT NULL,
                            empdept TEXT NOT NULL
                    )                  
                    ''')
                c.execute("""
                    INSERT INTO employee (name,site,salary,empstatus,empdept)
                    VALUES (?,?,?,?,?)
                    """,(name,site,salary,status,empdept))
                conn.commit()
                emp_id = c.lastrowid                #auto-generated empid
                print(f"Employee details has been saved with ID {emp_id}!")
            
        except ValueError as e:
            raise ValueError(f"Error: Missing Parameter : {e}!")
        except sql3.Error as e:
            print(f'Error {e}') 
        except Exception as e:
                print(f"Unexpected Error")
                
    def delete_emp(self,empid:int):
        try:
            self.validate_empid_exists(empid)
            
            with self.get_db_connection() as conn:
                c = conn.cursor()
                
                # Get employee name before deletion for confirmation
                c.execute("SELECT name FROM employee WHERE empid = ?", (empid,))
                name = c.fetchone()[0]

                c.execute("DELETE FROM employee WHERE empid = ?", (empid,))
                conn.commit()
                
            print(f"Employee '{name}' (ID: {empid}) has been deleted successfully!")
            
        except ValueError as e:
            print(f"Error: {e}")
        except sql3.Error as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
 
    def update_emp(self,empid):
        try:
            self.validate_empid_exists(empid)
            
            with self.get_db_connection() as conn:
                c = conn.cursor()
                
                # Display current employee info
                c.execute("SELECT name, site, salary, empstatus, empdept FROM employee WHERE empid = ?", (empid,))
                current_data = c.fetchone()
                name, site, salary, status, dept = current_data
                
                print(f"\nCurrent employee information:")
                print(f"Name: {name}")
                print(f"Site: {site}")
                print(f"Salary: {salary}")
                print(f"Status: {status}")
                print(f"Department: {dept}")
                
                print("\nWhat would you like to update?")
                print("1. Name")
                print("2. Site")
                print("3. Salary")
                print("4. Status")
                print("5. Department")
                
                choice = input("Enter choice (1-5): ").strip()
                
                if choice == '1':
                    new_value = input("Enter new Name: ").strip()
                    if not new_value:
                        raise ValueError("Name cannot be empty")
                    c.execute("UPDATE employee SET name = ? WHERE empid = ?", (new_value, empid))
                    
                elif choice == '2':
                    new_value = input("Enter new Site: ").strip()
                    if not new_value:
                        raise ValueError("Site cannot be empty")
                    c.execute("UPDATE employee SET site = ? WHERE empid = ?", (new_value, empid))
                    
                elif choice == '3':
                    try:
                        new_value = float(input("Enter new Salary: "))
                        new_value = self.validate_salary(new_value)
                        c.execute("UPDATE employee SET salary = ? WHERE empid = ?", (new_value, empid))
                    except ValueError as e:
                        if "could not convert" in str(e):
                            raise ValueError("Please enter a valid number for salary")
                        raise e
                        
                elif choice == '4':
                    new_value = input("Enter new Status (Active/Inactive): ").strip()
                    new_value = self.validate_status(new_value)
                    c.execute("UPDATE employee SET empstatus = ? WHERE empid = ?", (new_value, empid))
                    
                elif choice == "5":
                    new_value = input("Enter new Department: ").strip()
                    if not new_value:
                        raise ValueError("Department cannot be empty")
                    c.execute("UPDATE employee SET empdept = ? WHERE empid = ?", (new_value, empid))
                    
                else:
                    print("Invalid choice. Update cancelled.")
                    return
                
                conn.commit()
                
            print(f"Employee with ID {empid} has been updated successfully!")
            
        except ValueError as e:
            print(f"Error: {e}")
        except sql3.Error as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        
    def view_all(self):
        try:
            with self.get_db_connection() as conn:
                c = conn.cursor()
                c.execute("SELECT empid, name, site, salary, empstatus, empdept FROM employee ORDER BY empid")
                rows = c.fetchall()
                
                if rows:
                    print("\n" + "="*95)
                    print(f"{'ID':<5} {'Name':<25} {'Site':<15} {'Salary':<12} {'Status':<12} {'Department':<20}")
                    print("="*95)
                    
                    for row in rows:
                        empid, name, site, salary, status, dept = row
                        print(f"{empid:<5} {name:<25} {site:<15} ${salary:<11.2f} {status:<12} {dept:<20}")
                    
                    print("="*95)
                    print(f"Total employees: {len(rows)}")
                else:
                    print("No employees found in the database.")
        
        except sql3.Error as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        
if __name__ == "__main__":
    emp = Employee()
    
    while True:
        print("\n--- Employee Management CLI ---")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. View All Employees")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            emp.creating_emp()
        elif choice == '2':
            empid = int(input("Enter Employee ID to update: "))
            emp.update_emp(empid)
        elif choice == '3':
            empid = int(input("Enter Employee ID to delete: "))
            emp.delete_emp(empid)
        elif choice == '4':
            emp.view_all()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")        