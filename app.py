from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = 'aspro1111'

# Load student data
STUDENT_CSV = 'students.csv'
data = pd.read_csv(STUDENT_CSV)

@app.route('/')
def home():
    return render_template('login2.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email'].strip().lower()
    phone = request.form['phone'].strip()

    user = data[(data['Email'].str.lower() == email) & (data['Phone'].astype(str) == phone)]

    if not user.empty:
        session['email'] = email
        session['name'] = user.iloc[0]['Name']
        session['drive_link'] = user.iloc[0]['DriveLink']
        return redirect(url_for('dashboard'))
    else:
        return render_template('login2.html', error="Invalid email or phone number")

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect('/')
    return render_template('dash.html', name=session['name'], drive_link=session['drive_link'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
