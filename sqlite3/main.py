# -*- coding: utf-8 -*-

import sqlite3

def dropTable():
	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		DROP_SQL = "DROP TABLE SAMPLE_TABLE"
		cur.execute(DROP_SQL)
	finally:
		cur.close()
		conn.close()
	###
###

def createTable():
	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		CREATE_SQL = \
			"CREATE TABLE IF NOT EXISTS SAMPLE_TABLE ( " \
			+ " COL1 TEXT  PRIMARY KEY " \
			+ ",COL2 TEXT " \
			+ ",COL3 REAL " \
			+ " ) "
		cur.execute(CREATE_SQL)
	finally:
		cur.close()
		conn.close()
	###
###

def insertRecord(pk_val):
	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		INSERT_SQL = \
			"INSERT INTO SAMPLE_TABLE ( " \
			+ " COL1 " \
			+ ",COL2 " \
			+ ",COL3 " \
			+ ") VALUES ( " \
			+ f"'{pk_val}'" \
			+ ",'てきすと2' " \
			+ ",12345 " \
			+ ") " 
		cur.execute(INSERT_SQL)
		conn.commit()
	finally:
		cur.close()
		conn.close()
	###
###

def insertRecordBind(pk_val, col2_val, col3_val):
# 参考
# 	https://eerfstartup.hatenablog.jp/entry/2017/06/17/233941

	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		INSERT_SQL = \
			"INSERT INTO SAMPLE_TABLE ( " \
			+ " COL1 " \
			+ ",COL2 " \
			+ ",COL3 " \
			+ ") VALUES ( " \
			+ "?,?,? " \
			+ ") " 
		cur.execute(INSERT_SQL, [pk_val, col2_val, col3_val])
		conn.commit()
	finally:
		cur.close()
		conn.close()
	###
###

def insertRecordBind2(pk_val, col2_val, col3_val):
# 参考
# 	https://eerfstartup.hatenablog.jp/entry/2017/06/17/233941

	list = []
	list.append(pk_val)
	list.append(col2_val)
	list.append(col3_val)

	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		INSERT_SQL = \
			"INSERT INTO SAMPLE_TABLE ( " \
			+ " COL1 " \
			+ ",COL2 " \
			+ ",COL3 " \
			+ ") VALUES ( " \
			+ "?,?,? " \
			+ ") " 
		cur.execute(INSERT_SQL, list)
		conn.commit()
	finally:
		cur.close()
		conn.close()
	###
###

def deleteRecord():
	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		DELETE_SQL = "DELETE FROM SAMPLE_TABLE "
			
		cur.execute(DELETE_SQL)
		conn.commit()
	finally:
		cur.close()
		conn.close()
	###
###

def selectRecordFetchone():
	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		SELECT_SQL = "SELECT * FROM SAMPLE_TABLE "
			
		cur.execute(SELECT_SQL)
		
		list = cur.fetchone()
		print(list)
		print(list[0])
		print(list[1])
		print(list[2])
	finally:
		cur.close()
		conn.close()
	###
###

def selectRecordFetchall():
	dbname = "SAMPLE_DB.db"
	conn = sqlite3.connect(dbname)
	try:
		cur = conn.cursor()
		SELECT_SQL = "SELECT * FROM SAMPLE_TABLE "
			
		cur.execute(SELECT_SQL)
		
		list = cur.fetchall()
		for row in list:
			print(row)
			print(row[0])
			print(row[1])
			print(row[2])
		###
	finally:
		cur.close()
		conn.close()
	###
###

def testSqlite3():
# 	dropTable()
	createTable()
	deleteRecord()
	insertRecord("ぴーけー1")
	insertRecord("ぴーけー2")
	insertRecord("ぴーけー3")
	insertRecordBind("ぴーけーばいんど", "てきすと", 98765.4321)
	insertRecordBind2("ぴーけーばいんど2", "てきすと", 98765.4321)
	selectRecordFetchone()
	selectRecordFetchall()
###

####################################################
def run():
	testSqlite3()
####################################################
run()