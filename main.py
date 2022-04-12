from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
from data import db_session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data.students import Students
from data.teachers import Teachers

app = Flask('MyApp')
app.config['SECRET_KEY'] = 'brbrbr'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/school_db.db")
session = db_session.create_session()


@login_manager.user_loader
def load_student(s_id):
    db_sess = db_session.create_session()
    return db_sess.query(Students).get(s_id)


@login_manager.user_loader
def load_teacher(t_id):
    db_sess = db_session.create_session()
    return db_sess.query(Teachers).get(t_id)


class LoginForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/')
def teacher_or_student():
    return render_template('teacher_or_student.html')


@app.route('/teacher', methods=['POST', 'GET'])
def teacher_enter():
    if request.method == 'GET':
        return render_template('teacher_enter.html')
    elif request.method == 'POST':
        for teacher in session.query(Teachers).filter(Teachers.login.like(f'%{request.form["login"]}%')):
            return redirect('/teacher/schedule')
        else:
            return redirect('/teacher')


@app.route('/teacher/schedule')
def teacher_schedule():
    # for teacher in session.query(Teachers).filter(Teachers.name.like('%Марья%')):
    #    d_us = teacher. ...
    #    print(loads(d_us))
    days = {'Понедельник': ['Математика', 'Русский язык', 'Окружающий мир', 'Литература', '-'],
            'Вторник': ['ИЗО', 'Математика', 'Русский язык', 'Физ-ра', 'Английский язык'],
            'Среда': ['История', 'Информатика', 'Русский язык', 'Технология', '-'],
            'Четверг': ['География', 'Физ-ра', 'Математика', 'Русский язык', '-'],
            'Пятница': ['Окружающий мир', 'Математика', 'Музыка', 'Литература', '-']
            }
    return render_template('teacher_schedule.html', days=days)


@app.route('/teacher/homework', methods=['POST', 'GET'])
def teacher_homework():
    if request.method == 'GET':
        return render_template('teacher_homework.html')
    elif request.method == 'POST':
        rec_dict = {
            'subject': request.form['subject'],
            'date': request.form['date'],
            'homework': request.form['homework'],
        }
        return render_template('teacher_show_homework.html',
                               subject=rec_dict['subject'],
                               date=rec_dict['date'],
                               homework=rec_dict['homework'])


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
