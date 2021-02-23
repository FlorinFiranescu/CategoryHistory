import pymysql
from datetime import datetime
def connectToDB(host="localhost", root="root", pswd="", DBName="database"):
    #returns the cursor for the DB
    return pymysql.connect(
        host=host,
        user=root,
        passwd=pswd,
        database= DBName
    )


def checkIfTableExists(cursor, dbName, tableName):
    command="""SELECT * 
    FROM information_schema.tables
    WHERE table_schema = '{}' 
        AND table_name = '{}'
    LIMIT 1;
    """.format(dbName, tableName)
    return cursor.execute(command)


def createTable(cursor, table):
    MYSqlTable = """CREATE TABLE {}(
    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
    DAY CHAR(255) NOT NULL,
    TITLE  CHAR(255) NOT NULL,
    CATEGORY  CHAR(32) NOT NULL,
    BASE_PRICE FLOAT(10) NOT NULL,
    REDUCED_PRICE FLOAT(10) NOT NULL,
    LINK VARCHAR(1000) NOT NULL)""".format(table)

    cursor.execute(MYSqlTable)

def insertValues(cursor, table,day, title, category, base_price, reduced_price, link):
    insertStatement = """INSERT INTO {}(DAY, TITLE, CATEGORY, BASE_PRICE, REDUCED_PRICE, LINK) 
    VALUES('{}', '{}', '{}', '{}', '{}', '{}' );""".format(table,day, title, category, base_price, reduced_price, link)
    return cursor.execute(insertStatement)

def insertProduct(cursor, day, table, product):
    insertStatement = """INSERT INTO {}(DAY, TITLE, CATEGORY, BASE_PRICE, REDUCED_PRICE, LINK) 
    VALUES('{}', '{}', '{}', '{}', '{}', '{}' );""".format(table, day, product.title, product.category, product.base_price, product.reduced_price, product.link)
    return cursor.execute(insertStatement)

def checkDayInDB(cursor,table, day):
    selectStatement = "SELECT id FROM {} WHERE DAY='{}'".format(table, day)
    return cursor.execute(selectStatement)



