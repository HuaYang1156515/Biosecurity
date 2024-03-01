import mysql.connector
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='biosecurity'
    )
    return connection

@app.route('/')
def home():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM some_table")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)
