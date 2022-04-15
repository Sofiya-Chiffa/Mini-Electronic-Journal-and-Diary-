import datetime
from json import loads

from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.classes import Classes
from data.homeworks import Homeworks
from data.users import Users

app = Flask('MyApp')
app.config['SECRET_KEY'] = 'brbrbr'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/school_db.db")
session = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.login == form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(f"/{user.role}")
        return render_template('login_form.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_form.html', form=form)


# @app.route('/teacher', methods=['POST', 'GET'])
# def teacher_enter():
#     if request.method == 'GET':
#         return render_template('teacher_enter.html')
#     elif request.method == 'POST':
#         for teacher in session.query(Teachers).filter(Teachers.login.like(f'%{request.form["login"]}%')):
#             return redirect('/teacher/schedule')
#         else:
#             return redirect('/teacher')

@app.route('/teacher/exit')
def teacher_exit():
    return redirect('/')


@app.route('/teacher/schedule')
def teacher_schedule():
    sch = loads(session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().schedule)
    days = {'Понедельник': [x for x in sch['mon']],
            'Вторник': [x for x in sch['tue']],
            'Среда': [x for x in sch['wed']],
            'Четверг': [x for x in sch['thu']],
            'Пятница': [x for x in sch['fri']]
            }
    rngs = loads(session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().time_schedule)
    times = rngs['day']
    return render_template('teacher_schedule.html', days=days, times=times)


@app.route('/teacher/homework', methods=['POST', 'GET'])
def teacher_homework():
    if request.method == 'GET':
        return render_template('teacher_homework.html')
    elif request.method == 'POST':
        rec_dict = {
            'subject': request.form['subject'],
            'date': request.form['date'],
            'class_num': int(request.form['class_num']),
            'class_name': request.form['class_name'],
            'homework': request.form['homework']
        }

        hm = Homeworks()
        hm.date = datetime.datetime.date(datetime.datetime.strptime(rec_dict['date'], '%d.%m.%Y'))
        hm.subject = rec_dict['subject']
        hm.class_num = rec_dict['class_num']
        hm.class_name = rec_dict['class_name']
        hm.homework = rec_dict['homework']
        session.add(hm)
        session.commit()

        return render_template('teacher_show_homework.html',
                               subject=rec_dict['subject'],
                               date=rec_dict['date'],
                               class_num=rec_dict['class_num'],
                               class_name=rec_dict['class_name'],
                               homework=rec_dict['homework'])


# @app.route('/student', methods=['POST', 'GET'])
# def student_enter():
#     global person_id
#     if request.method == 'GET':
#         return render_template('student_enter.html')
#     elif request.method == 'POST':
#         for user in session.query(Students).filter(Students.name.like(f'%{request.form["login"]}%')):
#             return redirect('/student/diary')
#         else:
#             return redirect('/student')

@app.route('/student/exit')
def student_exit():
    return redirect('/')


@app.route('/student/diary/<n>')
def student_diary(n):
    today = datetime.datetime.today()
    today_weekday = datetime.datetime.today().weekday()
    week_dates = {'Понедельник': str(today - datetime.timedelta(days=(today_weekday - 0 - (int(n) * 7)))),
                  'Вторник': str(today - datetime.timedelta(days=(today_weekday - 1 - (int(n) * 7)))),
                  'Среда': str(today - datetime.timedelta(days=(today_weekday - 2 - (int(n) * 7)))),
                  'Четверг': str(today - datetime.timedelta(days=(today_weekday - 3 - (int(n) * 7)))),
                  'Пятница': str(today - datetime.timedelta(days=(today_weekday - 4 - (int(n) * 7)))),
                  'Суббота': str(today - datetime.timedelta(days=(today_weekday - 5 - (int(n) * 7)))),
                  'Воскресенье': str(today - datetime.timedelta(days=(today_weekday - 6 - (int(n) * 7))))}
    sch = loads(session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().schedule)
    cls_cur = session.query(Classes).filter(Classes.cl_id == current_user.class_id).first()
    print(session.query(Homeworks).filter(
        Homeworks.date == datetime.datetime.strptime(week_dates['Вторник'].split(' ')[0],
                                                     '%Y-%m-%d') and Homeworks.subject == 'Алгебра' and Homeworks.class_num == cls_cur.number and Homeworks.class_name == cls_cur.letter).first().homework)
    homework_data = session.query(Homeworks).filter(Homeworks.class_num == cls_cur.number and Homeworks.class_name == cls_cur.letter).all()
    for d in homework_data:
        print(d.homework)
    days = {'Понедельник': [[x, 1] for x in sch['mon']],
            'Вторник': [[x, 2] for x in sch['tue']],
            'Среда': [[x, 1] for x in sch['wed']],
            'Четверг': [[x, 1] for x in sch['thu']],
            'Пятница': [[x, 1] for x in sch['fri']]
            }
    return render_template('student_diary.html', days=days, week_dates=week_dates, n=int(n), datetime=datetime.datetime)


@app.route('/student/schedule')
def student_schedule():
    sch = loads(session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().schedule)
    days = {'Понедельник': [x for x in sch['mon']],
            'Вторник': [x for x in sch['tue']],
            'Среда': [x for x in sch['wed']],
            'Четверг': [x for x in sch['thu']],
            'Пятница': [x for x in sch['fri']]
            }
    rngs = loads(session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().time_schedule)
    times = rngs['day']
    return render_template('student_schedule.html', days=days, times=times)


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
    data = {'имя': current_user.name, 'фамилия': current_user.surname,
            'отчество': current_user.otchestvo, 'статус': 'ученик',
            'класс': str(
                session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().number) + session.query(
                Classes).filter(Classes.cl_id == current_user.class_id).first().letter
            }
    return render_template('student_profile.html', data=data)


app.run(port=8080, host='127.0.0.1', debug=True)
