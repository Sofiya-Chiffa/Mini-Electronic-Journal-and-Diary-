from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from json import loads
from data.homeworks import Homeworks
from data.classes import Classes
from data import db_session
from data.users import Users
import datetime as dt

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


@app.route('/teacher/exit')
def teacher_exit():
    return redirect('/')


@app.route('/teacher/schedule')
def teacher_schedule():
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


@app.route('/student/exit')
def student_exit():
    return redirect('/')


@app.route('/student/diary')
def student_diary():
    today = dt.datetime.date(dt.datetime.today())
    today_weekday = dt.datetime.today().weekday()
    week_dates = {'Понедельник': str(today - dt.timedelta(days=(today_weekday - 0))),
                  'Вторник': str(today - dt.timedelta(days=(today_weekday - 1))),
                  'Среда': str(today - dt.timedelta(days=(today_weekday - 2))),
                  'Четверг': str(today - dt.timedelta(days=(today_weekday - 3))),
                  'Пятница': str(today - dt.timedelta(days=(today_weekday - 4))),
                  'Суббота': str(today - dt.timedelta(days=(today_weekday - 5))),
                  'Воскресенье': str(today - dt.timedelta(days=(today_weekday - 6)))}
    sch = loads(session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().schedule)
    # лол, что?
    print(session.query(Homeworks).filter(str(Homeworks.date).split()[0] == week_dates['Вторник'] and
                                          Homeworks.subject == 'Алгебра').first())
    print(str(session.query(Homeworks).filter(Homeworks.subject == 'Алгебра').first().date).split()[0] ==
          week_dates['Вторник'])
    days = {'Понедельник': [[x, 1] for x in sch['mon']],
            'Вторник': [[x, 1] for x in sch['tue']],
            'Среда': [[x, 1] for x in sch['wed']],
            'Четверг': [[x, 1] for x in sch['thu']],
            'Пятница': [[x, 1] for x in sch['fri']]
            }
    return render_template('student_diary.html', days=days, week_dates=week_dates)


@app.route('/student/schedule')
def student_schedule():
    sch = loads(session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().schedule)
    days = {'Понедельник': [x for x in sch['mon']],
            'Вторник': [x for x in sch['tue']],
            'Среда': [x for x in sch['wed']],
            'Четверг': [x for x in sch['thu']],
            'Пятница': [x for x in sch['fri']]
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
    data = {'имя': current_user.name, 'фамилия': current_user.surname,
            'отчество': current_user.otchestvo, 'статус': 'ученик',
            'класс': str(
                session.query(Classes).filter(Classes.cl_id == current_user.class_id).first().number) + session.query(
                Classes).filter(Classes.cl_id == current_user.class_id).first().letter
            }
    return render_template('student_profile.html', data=data)


app.run(port=8080, host='127.0.0.1', debug=True)
