from mysql import connector 

Pass=input('Enter mysql password:')
conn = connector.connect(host = 'localhost',user='root',password=Pass)
Cursor = conn.cursor()
Cursor.execute('CREATE DATABASE Bank_Data')
Cursor.execute('USE Bank_Data')
Cursor.execute("""CREATE TABLE User_data
	(Username VARCHAR(25) PRIMARY KEY NOT NULL,
	Password CHAR(4) NOT NULL,
	Account_no CHAR(11),
	Name VARCHAR(25),
	DOB DATE,
	Phone_no VARCHAR(10),
	Balance INTEGER)
	""")
Cursor.execute("""CREATE TABLE Log_file
	(
		Sl_No Integer Auto_Increment primary key,
		Date_and_Time Varchar(25),
		Username VARCHAR(25),
		Account_no VARCHAR(11),
		Description VARCHAR(100)
	)
	""")
print('Table Created Sucessfully!!')
