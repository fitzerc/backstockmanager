import sqlite3

class dbClass():
	bsdb = sqlite3.connect('backstockdb')
	#Create Tote Table
	cursor = bsdb.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS tote\
			  (\
			   toteColor  STR NOT NULL,\
			   toteNumber STR NOT NULL,\
			   toteSize   STR NOT NULL,\
			   date       STR,\
			   sex        STR,\
			   cat        STR,\
			   subcat     STR,\
			   season     STR,\
			   hung       INT,\
			   sensor     INT,\
			   off        INT,\
			   offLoc     STR,\
			   PRIMARY KEY (toteColor, toteNumber, toteSize)\
			  )''')

	#Create Req Table
	cursor = bsdb.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS req\
			  (\
			   sex    INT DEFAULT 0,\
			   season INT DEFAULT 0,\
			   hung   INT DEFAULT 0,\
			   sensor INT DEFAULT 0,\
			   off    INT DEFAULT 0,\
			   offLoc INT DEFAULT 0\
			  )''')

	#Create Pass Table
	cursor = bsdb.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS pass\
			  (\
			   pass       STR          ,\
			   settings   INT DEFAULT 0,\
			   toteManage INT DEFAULT 0,\
			   fillTote   INT DEFAULT 0,\
			   editTote   INT DEFAULT 0\
			  )''')

	#Create miscFields
	cursor = bsdb.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS miscFields\
			  (\
			   param STR,\
			   value STR\
			  )''')
	bsdb.commit()

	#Create password
	cursor = bsdb.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS passwd\
			  (\
			   name STR NOT NULL,\
			   password STR NOT NULL,\
			   security INT DEFAULT 5\
			  )''')
	bsdb.commit()
        cursor = bsdb.cursor()
        sql = "SELECT * FROM passwd WHERE name = 'admin'" 
        cursor.execute(sql)
        test = cursor.fetchone()
        if not test:
            sql = "INSERT INTO passwd(name,password,security)VALUES(?,?,?)"
            cursor.execute(sql,('admin','pass1234',5))
            bsdb.commit()
	bsdb.close()



