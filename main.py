from flask import Flask, render_template, request
from data import db_session

app = Flask('MyApp')


db_session.global_init("db/school_db.db")
session = db_session.create_session()


@app.route('/')
def teacher_or_student():
    return render_template('teacher_or_student.html')


@app.route('/teacher', methods=['POST', 'GET'])
def teacher():
    if request.method == 'GET':
        return render_template('teacher.html')
    elif request.method == 'POST':
        return '1'


@app.route('/student', methods=['POST', 'GET'])
def student():
    if request.method == 'GET':
        return render_template('student.html')
    elif request.method == 'POST':
        return '1'


app.run(port=8080, host='127.0.0.1', debug=True)
