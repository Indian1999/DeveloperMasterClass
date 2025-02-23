import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "meggyecske",
    password = "kelkáposzta"
)

cursor = db.cursor()

def create_database(dbname):
    cursor.execute(f"CREATE DATABASE {dbname}")
    
create_database("logiscool")