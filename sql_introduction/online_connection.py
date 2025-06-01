import mysql.connector

try:
    db = mysql.connector.connect(
        host = "szombat-14-45.ct8uayiqoj9l.eu-north-1.rds.amazonaws.com",
        user = "admin",
        password = "kelkaposzta",
        database = "test_db"
    )
    print("Connection succesfull!")
    cursor = db.cursor()

    # Step 1: Create a test table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            age INT
        )
    """)
    print("✅ Table 'users' created successfully!")

    # Step 2: Insert test data
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Alice", "alice@example.com", 25))
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Bob", "bob@example.com", 30))
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Charlie", "charlie@example.com", 22))

    db.commit()
    print("✅ Test data inserted successfully!")

    # Step 3: Fetch and print the data
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    print("\n📌 Users Table Data:")
    for row in rows:
        print(row)

    # Close connection
    cursor.close()
    db.close()
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
