#path = '//Hydromassage1/aqtsdb/DB/CustomerDatabase.txt'
dpath = 'C:/Users/POS/Desktop/CustomerDatabase.txt'
path = 'C:/Users/POS/Downloads/_.csv'

class Customer:
    first_name = ''
    last_name = ''
    phone_number = ''

    def __init__(self, first_name, last_name, phone_number):
        self.first_name = self.clean_name(first_name)
        self.last_name = self.clean_name(last_name)
        self.phone_number = self.clean_number(phone_number)

    def clean_name(self,n):
        n = n.replace('"','')
        n = n.strip()
        return n

    def clean_number(self, p):
        p = p.strip()
        p = p.replace('"','')
        p = p.replace('(','')
        p = p.replace(')','')
        p = p.replace(' ','')
        p = p.replace('-','')
        p = p[3:]
        return p

    def __repr__(self):
        return "'%s,%s,%s'" % (self.first_name, self.last_name, self.phone_number)

db = open(dpath,'r+')
customer_database = open(path,'r')
dblines = db.readlines()
lines = customer_database.readlines()
customers_to_add = []
for i in range(1,len(lines)):
    values = lines[-i].split(',')
    #print("Member Name:",values[9],values[10],'\n' + "Phone Number:",values[0][0:3]+'-'+values[0][3:]+'\n')
    customers_to_add.append(Customer(values[5],values[4],values[8]))

for customer in customers_to_add:
    if (customer.phone_number != '' and len(customer.phone_number) == 7):
        print("Adding:", customer)
    else:
        print("Could not add:", customer, "please add a phone number to the customer and try again.")

input()
