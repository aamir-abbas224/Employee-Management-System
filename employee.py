import sqlite3 as sql3
from contextlib import contextmanager


class Employee:
    def __init__(self, name:str = "", site:str = "", salary:float = 0.0, empstatus:str = "",empdept:str = "",directmanager:str = "",workinghours:float= 0.0,allowance:float=0.0,overtime:float = 0):
        self._empstatus = empstatus # Employee Status
        self._name = name
        self._salary = salary
        self._site  =  site
        self._empdept = empdept
        self._directmanager = directmanager
        self._workinghours = workinghours
        self._allowance = allowance
        self._overtime = overtime
    
    @property
    def workinghours(self):
        return self._workinghours
    @workinghours.setter
    def workinghours(self,value):
        self._workinghours = value
        
    @property
    def allowance(self):
        return self._allowance
    @allowance.setter
    def allowance(self,value):
        self._allowance = value
        
    @property
    def overtime(self):
        return self._overtime
    @overtime.setter
    def overtime(self,value):
        self._overtime = value        

    @property
    def directmanager(self):
        return self._directmanager
    @directmanager.setter
    def directmanager(self,value):
        self._directmanager = value           
        
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
        
        
    @contextmanager
    def get_db_connection(self):
        conn = None
        try:
            conn = sql3.connect('employee.db')
            yield conn
        finally:
            if conn:
                conn.close()
                
                
    def workinghours_validator(self,workhours):
        try:
            if not isinstance(workhours,(int,float)):
                raise ValueError('Invalid Working Hours')
            elif workhours < 0:
                raise ValueError('Working Hours Cannot be in negative')  
            return workhours          
        except Exception as e:
            raise ValueError(f'Unknown Error: {e}')
        
    def overtime_validator(self,ot):
         try:
             if not isinstance(ot,(int,float)):
                 raise ValueError('Invalid input')
             elif ot < 0 :
                 raise ValueError('Overtime Cannot be negative')
             return ot
         except Exception as e:
             raise ValueError(f'Error as {e}')   
        
    def allowance_validator(self,allowance):
        try:
            if not isinstance(allowance,(int,float)):
                raise ValueError('Not a valid input for allowance')
            elif allowance < 0:
                raise ValueError('Allowance cannot be negative')
            return allowance
        except Exception as e:
            raise UnboundLocalError(f"Error : {e}")        
                
    def validate_salary(self,salary):
         if salary < 0:
             raise ValueError('Error! Negative Salary') 
         return salary  
             
    def validate_status(self,status):
        valid_status = ['Active','Inactive','Leave','Vacation','Exit'] #Leave = includes all kinds leave such as Emergency, medical etc except Vacation
        status_cap = status.strip().title()
        if status_cap not in valid_status:
            raise ValueError('Invalid Status')
        return status_cap
        
    def validate_empid_exists(self,empid):
        with self.get_db_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM employee WHERE empid = ?',(empid,))
            count = c.fetchone()[0]
            if count == 0:
                raise ValueError(f'{empid} does not exists')
    
    def validate_manager(self,dirman):
        if dirman == '':
            raise ValueError('No Direct Manager')
        
        with self.get_db_connection() as conn:
            c = conn.cursor()
            #check if table exists
            c.execute("""SELECT name FROM sqlite_master
                      WHERE type = 'table' AND name = 'employee' """)
            table_exists = c.fetchone()
            if not table_exists:
                return dirman
            c.execute('SELECT COUNT(*) FROM employee WHERE name = ?',(dirman,))
            count = c.fetchone()[0]
            
            if count == 0:
                raise ValueError('No Direct Manager / has no manager: None')
            return dirman           
         
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
            
            dirman = input('Enter the name of direct manager of the employee: ')
            dirman = self.validate_manager(dirman) 
            
            allowance = float(input("Enter the allowance if any : "))
            allowance = self.allowance_validator(allowance)
            
            overtime = float(input("Enter Overtime if any: "))
            overtime = self.overtime_validator(overtime)
            
            workinghours = float(input("Enter basic working hours : "))
            workinghours = self.workinghours_validator(workinghours)
    
            # Database operations
            with self.get_db_connection() as conn:
                c = conn.cursor()
            
                c.execute('''
                    CREATE TABLE IF NOT EXISTS employee(
                       empid INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            site TEXT NOT NULL,
                            salary REAL NOT NULL,
                            workinghours REAL NOT NULL,
                            allowance REAL NOT NULL,
                            overtime REAL NOT NULL,
                            empstatus TEXT NOT NULL,
                            empdept TEXT NOT NULL,
                            directmanager TEXT
                    )                  
                    ''')
                c.execute("""
                    INSERT INTO employee (name,site,salary,allowance,workinghours,overtime,empstatus,empdept,directmanager)
                    VALUES (?,?,?,?,?,?,?,?,?)
                    """,(name,site,salary,allowance,workinghours,overtime,status,empdept,dirman))
                conn.commit()
                emp_id = c.lastrowid                #auto-generated empid
                print(f"Employee details has been saved with ID {emp_id}!")
            
        except ValueError as e:
            print(f"Error: {e}")
            raise ValueError(f"Error: {e}!")
        except sql3.Error as e:
            print(f'DataBase Error: {e}') 
        except Exception as e:
                print(f"Unexpected Error: {e}")
                
    def delete_emp(self,empid:int):
        try:
            self.validate_empid_exists(empid)
            
            with self.get_db_connection() as conn:
                c = conn.cursor()
                
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
                c.execute("SELECT name, site, salary,allowance,workinghours,overtime,empstatus, empdept , directmanager FROM employee WHERE empid = ?", (empid,))
                current_data = c.fetchone()
                name, site, salary, allowance, workinghours, overtime, status, dept , dirman = current_data
                
                print(f"\nCurrent employee information:")
                print(f"Name: {name}")
                print(f"Site: {site}")
                print(f"Salary: {salary}")
                print(f" Allowance : {allowance}")
                print(f" Working Hourse : {workinghours}")
                print(f" Overtime: {overtime}")
                print(f"Status: {status}")
                print(f"Department: {dept}")
                print(f"Direct Manager: {dirman}")
                
                
                print("\nWhat would you like to update?")
                print("1. Name")
                print("2. Site")
                print("3. Salary")
                print("4. Allowance")
                print("5. Working Hours")
                print("6. Overtime")
                print("7. Status")
                print("8. Department")
                print("9. Direct Manager")
                
                choice = input("Enter choice (1-9): ").strip()
                
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
                
                elif choice == '6':
                    new_value = input('Please Provide New Manager: ').strip()
                    new_value = self.validate_manager(new_value)
                    c.execute('UPDATE employee SET directmanager = ? WHERE empid = ? ',(new_value,empid))
                    if not new_value:
                        raise ValueError('Please enter again!  : ')
                    
                elif choice == '7':
                    new_value = float(input('Please Provide Allownace if any : '))
                    new_value = self.allowance_validator(new_value)
                    c.execute('UPDATE employee SET allowance = ? WHERE empid = ? ',(new_value,empid))
                    if not new_value:
                        raise ValueError('Please enter again!  : ')
                
                elif choice == '8':
                    new_value = input('Please Provide Working Hours : ')
                    new_value = self.workinghours_validator(new_value)
                    c.execute('UPDATE employee SET workinghours = ? WHERE empid = ? ',(new_value,empid))
                    if not new_value:
                        raise ValueError('Please enter again!  : ')
                    
                elif choice == '9':
                    new_value = input('Please Provide Overtime if any : ')
                    new_value = self.overtime_validator(new_value)
                    c.execute('UPDATE employee SET overtime = ? WHERE empid = ? ',(new_value,empid))
                    if not new_value:
                        raise ValueError('Please enter again!  : ')        
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
                c.execute("SELECT empid, name, site, salary,allowance,workinghours,overtime,empstatus, empdept, directmanager FROM employee ORDER BY empid")
                rows = c.fetchall()
                
                if rows:
                    print("\n" + "="*140)
                    print(f"{'ID':<4} {'Name':<15} {'Site':<10} {'Salary':<8} {'Allowance':<8} {'Working Hours':<10} {'Overtime':<8}{'Status':<10} {'Department':<12} {'Direct Manger':<12}")
                    print("="*140)
                    
                    for row in rows:
                        empid, name, site, salary,allowance,workinghours,overtime, status, dept, dirman = row
                        print(f"{empid:<4} {name:<15} {site:<10} {salary:<8f} {allowance:<8.0}{workinghours:<10.1f} {overtime:8.1f} {status:<10} {dept:<12} {dirman:<12}")
                    
                    print("="*140)
                else:
                    print("No employees found in the database.")
        
        except sql3.Error as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
            
    def summary(self):
            with self.get_db_connection() as conn:
                c = conn.cursor()
                c.execute("SELECT empid, name, site, salary,allowance,workinghours,overtime,empstatus, empdept, directmanager FROM employee ORDER BY empid")
                rows = c.fetchall()
                
                print(f"Total employees: {len(rows)}")
                regular_hours = sum(row[5] for row in rows) #total r
                total_overtime = sum(row[6] for row in rows) #total ov
                print(f"Company total - Regular Hours : {regular_hours:.2f}, Overtime : {total_overtime:2f}")

if __name__ == "__main__":
    emp = Employee()
    
    while True:
        print("\n--- Employee Management CLI ---")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. View All Employees")
        print("5. Summary")
        print("6. Exit")
        
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
            print("Summary....")
            emp.summary()
        elif choice == '6':
            print('Exited')    
            break
        else:
            print("Invalid choice. Try again.")        