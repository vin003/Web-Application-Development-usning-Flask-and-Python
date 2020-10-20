import mysql
try :
    conn=mysql.connector.connect(host="localhost",port=3306, password="", user="root", database="codingthunder")
    print("Successs")
except Exception as e:
    print("Error ",e)
cur=conn.cursor()
cur.execute("SELECT * FROM contacts") 
records =cus.fetchAll()
print("No of records in the tables ",cur.rowcount)

for row in records:
    print("doc id" , row[0])
    print("doc name",row[1])
    print("email details ",row[3])
    print("contact details ",row[4])
    print("contact date",row[5])