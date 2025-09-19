import mysql.connector

con = mysql.connector.connect(host = "localhost", user = "root",passwd = "2020Bca01")
cursor = con.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS mca_minor_project")
cursor.execute("SHOW DATABASES")
for db in cursor:
    print(db)
cursor.close()
con.close()
print("---------Database created successfully!------------")

con1 = mysql.connector.connect(host = "localhost", user = "root",passwd = "2020Bca01",database = "mca_minor_project")
cursor1 = con1.cursor()

student = "CREATE TABLE Student (uid INT PRIMARY KEY,name VARCHAR(255) NOT NULL,course ENUM('BCA', 'MCA', 'BTech', 'MTech', 'BBT', 'MBA') NOT NULL, section VARCHAR(25),    semester ENUM('1', '2', '3', '4', '5', '6', '7', '8') NOT NULL);"
# attendance = "CREATE TABLE Attendance (uid INT,name VARCHAR(255),day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday') NOT NULL, date DATE NOT NULL,period ENUM('1', '2', '3', '4', '5', '6', '7') NOT NULL,status ENUM('Present', 'Absent') NOT NULL, FOREIGN KEY (uid) REFERENCES student(uid));"
attendance = "CREATE TABLE Attendance (uid INT,name VARCHAR(255),day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday') NOT NULL, date DATE NOT NULL,period ENUM('1', '2', '3', '4', '5', '6', '7') NOT NULL,status ENUM('Present', 'Absent') NOT NULL, primary key(uid, date, period));"

cursor1.execute(student)
cursor1.execute(attendance)

for tb in cursor1:
    print(tb)
    
con1.commit()
cursor1.close()
con1.close()

print("----------All the table Executed successfully!------------")