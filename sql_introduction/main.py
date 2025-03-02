import mysql.connector
import pandas as pd # pip install pandas (terminálba)

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
    
def insert_john_snow():
    cursor.execute("INSERT INTO customers (name, address, country, postal_code, age, email, telephone) VALUES ('John Snow', 'Hammer street 8.', 'USA', 5427, 35, 'john.snow@gmail.com', 564583257)")
    db.commit()
    cursor.execute("SELECT * FROM customers")
    print_results()
    
def clear_table(table_name):
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")

def upload_data_to(data, table_name):
    for row in data.iterrows():
        cursor.execute(f"INSERT INTO {table_name} (name, address, country, postal_code, age, email, telephone) VALUES ('{row[1]['name']}', '{row[1]['address']}', '{row[1]['country']}', '{row[1]['postal_code']}', '{row[1]['age']}', '{row[1]['email']}', '{row[1]['telephone']}')")
    db.commit()
    
table_name = "customers"
field_names = ["name", "address", "country", "postal_code", "age", "email", "telephone"]
field_types = ["VARCHAR(255)","VARCHAR(255)","VARCHAR(255)", "INT(255)", "INT(255)","VARCHAR(255)","VARCHAR(255)"]

#clear_table("customers")

#data = pd.read_csv("sql_introduction\generated_data.csv", delimiter = ";")

#upload_data_to(data, "customers")

def select_bulgarians():
    cursor.execute("SELECT name, email, country FROM customers WHERE country = 'Bulgaria'")
    results = cursor.fetchall()
    bulgarians = {}
    for row in results:
        bulgarians[row[0]] = row[1]
    print(bulgarians)

def select_country_starts_with(start):
    cursor.execute(f"SELECT name, email, country FROM customers WHERE country LIKE '{start}%'")
    results = cursor.fetchall() # Egy lista, ami tuple-ket tartalmaz
    for item in results:
        print(item)
    
select_country_starts_with("m")

# Kérdezzük le azokat a sorokat, ahol a névben benne van egy 'a' betű és country nevében is van 'a'
# name, country, postal_code, és ezt tároljuk el egy erre alkalmas adatszerkezetben
    


