path = '//Hydromassage1/aqtsdb/DB/CustomerDatabase.txt'
customer_database = open(path,'r')

lines = customer_database.readlines()

for i in range(1,11):
    values = lines[-i].split(',')
    print("Member Name:",values[9],values[10],'\n' + "Phone Number:",values[0][0:3]+'-'+values[0][3:]+'\n')
    #print(lines[-i])
customer_database.close()
input()
