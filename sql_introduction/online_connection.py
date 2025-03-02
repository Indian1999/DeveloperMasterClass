import mysql.connector

db = mysql.connector.connect(
    host = "us-cdbr-iron-east-03.cleardb.net",
    user = "bd0617aba4eb0d",
    password = "cc31163c",
    database = "heroku_eac377a18b009b8"
)

cursor = db.cursor()

cursor.execute("SHOW TABLES")
