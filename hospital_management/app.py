from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database Initialization
def init_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            disease TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']

        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)", (name, age, disease))
        conn.commit()
        conn.close()
        return redirect('/patients')

    return render_template('add_patient.html')

@app.route('/patients')
def view_patients():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('view_patients.html', patients=patients)

@app.route('/delete/<int:patient_id>')
def delete_patient(patient_id):
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
    return redirect('/patients')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
