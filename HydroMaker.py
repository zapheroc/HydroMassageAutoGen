from datetime import datetime as dt
import os
from shutil import copyfile


class Customer:
    first_name = ''
    last_name = ''
    phone_number = ''

    def __init__(self, first_name, last_name, phone_number):
        self.first_name = self._clean_name(first_name)
        self.last_name = self._clean_name(last_name)
        self.phone_number = self._clean_number(phone_number)

    def _clean_name(self, n):
        n = n.replace('"', '')
        n = n.strip()
        return n

    def _clean_number(self, p):
        if p == '\n':
            raise ValueError('The customer requires a phone number.')
        p = p.strip()
        p = p.replace('"', '')
        p = p.replace('(', '')
        p = p.replace(')', '')
        p = p.replace(' ', '')
        p = p.replace('-', '')
        if (len(p) > 7):
            p = p[3:]
        if len(p) != 7:
            raise ValueError('The customer has an invalid phone number.')
        # Check if the number casts to an integer. If it doesn't this will raise an exception.
        int(p)
        return p

    def __repr__(self):
        return "'%s, %s, %s'" % (self.first_name, self.last_name, self.phone_number)


class FileManager:
    db_path = ''
    new_entry_path = ''
    customer_dictionary = {}
    customers_to_add = []
    hydro_massage_db = None
    new_entries_db = None
    
    '''
    On init, pass in the paths of the files to manipulate. Since there are only two files, two
    arguments are required.
    '''
    def __init__(self, db_path, new_entry_path):
        self.db_path = db_path
        self.new_entry_path = new_entry_path

    '''
    Read the hydromassage database, and also the datatrack CSV, and store the hydromassage entries in a CSV.
    During this process, check for malformed or absent phone numbers and catch errors from these number, displaying them
    to the user. For valid new entries which can be added, add them to the list of customers to add.
    '''
    def read_databases(self):
        self.hydro_massage_db = open(self.db_path, 'r+', encoding='latin-1')
        self.new_entries_db = open(self.new_entry_path, 'r')
        
        dblines = self.hydro_massage_db.readlines()
        dbnew = self.new_entries_db.readlines()
        for line in dblines:
            values = line.split(',')
            # print(values[0], values[9], values[10])
            try:
                #print('hi')
                self.customer_dictionary[values[0]] = Customer(values[10], values[9], values[0])
            except ValueError as e:
                continue
                # print("In the database, there is an aberrant phone number for", values[10],values[9], "the number is:", values[0])
            
        for i in range(1, len(dbnew)):
            values = dbnew[-i].split(',')
            try:
                #print('hi')
                self.customers_to_add.append(Customer(values[5], values[4], values[8]))
            except ValueError as e:
                print("Could not add", values[5].replace('"', ''), values[4].replace('"', ''), "agreement number", '#' + values[1].replace('"', '') + '.', e)
        
    ''' 
    Checks if a customer exists in the current hydromassage database. If they don't
    then add them. If they do, print a message saying that they were already added.
    This function will automatically backup the hydromassage log to <hydromassage_database_name>.bac, 
    just in case there is an error with this program.
    '''

    def write_new_customers(self):
        # To ensure no data is lost, always backup the database before writing to it.
        copyfile(self.db_path, self.db_path + '.bac')
        # Only try to write if there are customers to add.
        if len(self.customers_to_add) > 0:
            for customer in self.customers_to_add:
                # Depending on if the customer's number is in the database, inform the user.
                if (customer.phone_number in self.customer_dictionary):
                    print("The number for", customer, "is already added to the HydroMassage as", self.customer_dictionary[customer.phone_number])
                else:
                    # This gets the correct date to write to the database.
                    date = dt.now().strftime('%m/%d/%Y')
                    self.hydro_massage_db.write("%s,10,,Enabled,Recurring,no,no,%s,,%s,%s,,NONE,NONE,NONE,10,%s,No Usage,No Usage,No Usage,No Usage,yes,NONE,NONE,0,10,0,0,\n" % (customer.phone_number, date, customer.last_name, customer.first_name, date))
                    print("Adding: ", customer)
    
    ''' 
    Close up the open databases.
    '''

    def close_files(self):
        self.hydro_massage_db.close()
        self.new_entries_db.close();

    ''' 
    Delete the CSV from datatrack, since it's not needed. 
    '''  

    def delete_new_entries_CSV(self):
        os.remove(self.new_entry_path)
        

class InputManager:
    
    database_path = '//Hydromassage1/aqtsdb/DB/CustomerDatabase.txt'
    #database_path = 'CustomerDatabase.txt'
    new_entry_path = '_.csv'
    
    def __init__(self):
        print(''' Usage: Export the datatrack hydromassage log as a CSV to the same location as this file (probably the desktop).
        Then, run this file! The hydromassage should automatically be populated with entries!\n''')
        
        print("Now reading the HydroMassage database from %s, and the new entry HydroMassage Log from %s\n" % (self.database_path, self.new_entry_path))
        file_manager = FileManager(self.database_path, self.new_entry_path)
        # Read the database, catching in fileIO errors.
        try:
            file_manager.read_databases()
        except BaseException as e:
            print("Error:", e)
            return
        # Write the database, catching in IOErrors, or errors backing up the file.
        try:    
            file_manager.write_new_customers()
        except BaseException as e:
            print(e)
            
        file_manager.close_files();
        
        # The CSV file isn't needed any longer, so let the user delete it right from here.
        print("Do you want to delete the CSV file %s? (y/n)" % (self.new_entry_path))
        response = input().lower();
        if (response == 'y'):
            file_manager.delete_new_entries_CSV()
            print("File Deleted.")
        else:
            print("File not Deleted.")
            
        print("Press any key to exit.")
        input()
        
inputmanager = InputManager();
