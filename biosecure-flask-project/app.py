from flask import Flask, render_template
import mysql.connector

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
    cursor.execute("SELECT * FROM mariners")  # Adjust your query as needed
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('home.html', data=data)  # Pass data to your template, if needed

if __name__ == '__main__':
    app.run(debug=True)
