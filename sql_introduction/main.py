import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "meggyecske",
    password = "kelkáposzta",
    database="logiscool"
)

cursor = db.cursor()

def create_database(dbname):
    cursor.execute(f"CREATE DATABASE {dbname}")
    
def show_databases():
    cursor.execute("SHOW DATABASES")
    
def print_results():
    for result in cursor:
        print(result)
    
#create_database("logiscool")
#show_databases()