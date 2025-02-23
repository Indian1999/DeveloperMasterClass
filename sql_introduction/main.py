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
        
def create_table(table_name:str, field_names:list, field_types:list) -> None:
    # CREATE TABLE table_name (name VARCHAR(255), address VARCHAR(255))
    fields = ""
    for i in range(len(field_names)):
        fields += field_names[i] + " " + field_types[i] + ", "
    fields = fields[:-2]
    cursor.execute(f"CREATE TABLE {table_name} ({fields})")
    
table_name = "customers"
field_names = ["name", "address", "country", "postal_code", "age", "email", "telephone"]
field_types = ["VARCHAR(255)","VARCHAR(255)","VARCHAR(255)", "INT(255)", "INT(255)","VARCHAR(255)","VARCHAR(255)"]
create_table(table_name, field_names, field_types)