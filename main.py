from flask import Flask, render_template, request

from data import db_session

app = Flask('MyApp')

db_session.global_init("db/school_db.db")
session = db_session.create_session()


@app.route('/')
def teacher_or_student():
    return render_template('teacher_or_student.html')


@app.route('/teacher', methods=['POST', 'GET'])
def teacher_enter():
    if request.method == 'GET':
        return render_template('teacher_enter.html')
    elif request.method == 'POST':
        return '1'


@app.route('/student', methods=['POST', 'GET'])
def student_enter():
    if request.method == 'GET':
        return render_template('student_enter.html')
    elif request.method == 'POST':
        return '1'


@app.route('/student/diary')
def student_diary():
    days = {'Понедельник': [['Математика', '...'], ['Русский язык', '..'], ['Окружающий мир', ''], ['Литература', ''],
                            ['', '']],
            'Вторник': [['ИЗО', '.'], ['Математика', '...'], ['Русский язык', ''], ['Физ-ра', ''],
                        ['Английский язык', '.']],
            'Среда': [['История', '.'], ['Информатика', ''], ['Русский язык', '.'], ['Технология', '..'], ['', '']],
            'Четверг': [['География', '..'], ['Физ-ра', '.'], ['Математика', ''], ['Русский язык', '.'], ['', '']],
            'Пятница': [['Окружающий мир', '..'], ['Математика', '....'], ['Музыка', '..'], ['Литература', '..'],
                        ['', '']]
            }
    return render_template('student_diary.html', days=days)


@app.route('/student/schedule')
def student_schedule():
    days = {'Понедельник': ['Математика', 'Русский язык', 'Окружающий мир', 'Литература', ''],
            'Вторник': ['ИЗО', 'Математика', 'Русский язык', 'Физ-ра', 'Английский язык'],
            'Среда': ['История', 'Информатика', 'Русский язык', 'Технология', ''],
            'Четверг': ['География', 'Физ-ра', 'Математика', 'Русский язык', ''],
            'Пятница': ['Окружающий мир', 'Математика', 'Музыка', 'Литература', '']
            }
    return render_template('student_schedule.html', days=days)


@app.route('/student/grade')
def student_grade():
    return render_template('student_grade.html')


app.run(port=8080, host='127.0.0.1', debug=True)
