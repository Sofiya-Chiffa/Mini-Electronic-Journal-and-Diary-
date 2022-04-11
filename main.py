from flask import Flask, render_template, request, redirect
from data import db_session
from json import loads, dumps
import datetime as dt
from data.classes import Classes
from data.homeworks import Homeworks
from data.students import Students
from data.teachers import Teachers

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
    global person_id
    if request.method == 'GET':
        return render_template('student_enter.html')
    elif request.method == 'POST':
        for user in session.query(Students).filter(Students.name.like(f'%{request.form["login"]}%')):
            return redirect('/student/diary')
        else:
            return redirect('/student')


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
    # for user in session.query(Students).filter(Students.name.like('%Вася%')):
    #    d_us = user.class_id.schedule
    #    print(loads(d_us))
    days = {'Понедельник': ['Математика', 'Русский язык', 'Окружающий мир', 'Литература', '-'],
            'Вторник': ['ИЗО', 'Математика', 'Русский язык', 'Физ-ра', 'Английский язык'],
            'Среда': ['История', 'Информатика', 'Русский язык', 'Технология', '-'],
            'Четверг': ['География', 'Физ-ра', 'Математика', 'Русский язык', '-'],
            'Пятница': ['Окружающий мир', 'Математика', 'Музыка', 'Литература', '-']
            }
    return render_template('student_schedule.html', days=days)


@app.route('/student/grade')
def student_grade():
    grades = {'subg1': [5, 4, 3, 5], 'subg2': [5, 4, 5, 5, 5, 5],
              'subg3': [5, 4, 4, 4, 5]
              }
    grd_sum = {'subg1': round(sum(grades['subg1']) / len(grades['subg1']), 2),
               'subg2': round(sum(grades['subg2']) / len(grades['subg2']), 2),
               'subg3': round(sum(grades['subg3']) / len(grades['subg3']), 2)}
    return render_template('student_grade.html', grades=grades, grd_sum=grd_sum)


@app.route('/student/profile')
def student_profile():
    return render_template('student_profile.html')


app.run(port=8080, host='127.0.0.1', debug=True)
