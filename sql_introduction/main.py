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
    fields = ""
    for i in range(len(field_names)):
        fields += field_names[i] + " " + field_types[i] + ", "
    fields = fields[:-2]
    cursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {fields})")
    
table_name = "customers"
field_names = ["name", "address", "country", "postal_code", "age", "email", "telephone"]
field_types = ["VARCHAR(255)","VARCHAR(255)","VARCHAR(255)", "INT(255)", "INT(255)","VARCHAR(255)","VARCHAR(255)"]


cursor.execute("INSERT INTO customers (name, address, country, postal_code, age, email, telephone) VALUES ('John Snow', 'Hammer street 8.', 'USA', 5427, 35, 'john.snow@gmail.com', 564583257)")
db.commit()
cursor.execute("SELECT * FROM customers")
print_results()
