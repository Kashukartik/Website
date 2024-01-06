from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask import render_template
app = Flask(__name__)

# Initialize the database
conn = sqlite3.connect('qna.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    );
''')
conn.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    );
''')
conn.close()

@app.route('/')
def index():
    # Fetch all questions from the database
    conn = sqlite3.connect('qna.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions ORDER BY id DESC')
    questions = cursor.fetchall()
    conn.close()
    return render_template('index.html', questions=questions)

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # Insert the question into the database
        conn = sqlite3.connect('qna.db')
        conn.execute('INSERT INTO questions (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('ask.html')

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    conn = sqlite3.connect('qna.db')
    cursor = conn.cursor()

    # Fetch the question details
    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    question = cursor.fetchone()

    if request.method == 'POST':
        answer_content = request.form['answer']
        # Insert the answer into the database
        cursor.execute('INSERT INTO answers (question_id, content) VALUES (?, ?)', (question_id, answer_content))
        conn.commit()

    # Fetch all answers for the question
    cursor.execute('SELECT * FROM answers WHERE question_id = ? ORDER BY id DESC', (question_id,))
    answers = cursor.fetchall()

    conn.close()
    return render_template('question.html', question=question, answers=answers)

@app.route('/home')
def home():
    # Add logic for the home page if needed
    return render_template('home.html')

@app.route('/login')
def login():
    # Add logic for the login page if needed
    return render_template('login.html')

@app.route('/signup')
def signup():
    # Add logic for the signup page if needed
    return render_template('signup.html')




if __name__ == '__main__':
    app.run(debug=True)


