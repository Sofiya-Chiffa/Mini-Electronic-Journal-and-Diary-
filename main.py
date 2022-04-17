import datetime
import json
from json import loads
from flask_restful import reqparse, abort, Api, Resource
from data.grades import Grade
from flask import Flask, render_template, request, redirect, jsonify
from flask_login import LoginManager, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.classes import Classes
from data.homeworks import Homeworks
from data.users import Users

app = Flask('MyApp')
api = Api(app)
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


@app.route('/teacher/grade/<obj_name>', methods=['POST', 'GET'])
def teacher_grade(obj_name):
    if request.method == 'POST':
        gr = Grade()
        gr.date = datetime.datetime.date(datetime.datetime.strptime(request.form['date'], '%d.%m.%Y'))
        gr.subject = obj_name
        gr.name = session.query(Users).filter(Users.surname == request.form['name'],
                                              Users.class_id == current_user.class_id).first().name
        gr.surname = request.form['name']
        gr.grade = request.form['grade']
        session.add(gr)
        session.commit()
    lst_obj = ['Русский', 'Английский', 'Алгебра', 'Литература', 'Информатика', 'ИЗО',
               'Физ-ра', 'Музыка']
    std_all_inf = session.query(Users).filter(Users.class_id == current_user.class_id,
                                              Users.role == 'student/diary/0').all()
    grades_list = dict()
    for std in std_all_inf:
        grades_list[f'{std.surname} {std.name} {std.otchestvo}'] = session.query(Grade).filter(Grade.name == std.name,
                                                                                               Grade.surname == std.surname,
                                                                                               Grade.subject == obj_name).all()
        if grades_list[f'{std.surname} {std.name} {std.otchestvo}'] is None:
            grades_list[f'{std.surname} {std.name} {std.otchestvo}'] = list()
        else:
            grades_std = list()
            for d in grades_list[f'{std.surname} {std.name} {std.otchestvo}']:
                grades_std.append(d.grade)
            grades_list[f'{std.surname} {std.name} {std.otchestvo}'] = grades_std
    students = list()
    for k in grades_list.keys():
        if len(grades_list[k]) != 0:
            students.append([k, grades_list[k], round(sum(grades_list[k]) / len(grades_list[k]), 2)])
        else:
            students.append([k, '', 0.0])
    return render_template('teacher_grade.html', students=students, obj=obj_name, lst_obj=lst_obj)


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
    days = {'Понедельник': [[x, session.query(Homeworks).filter(
        Homeworks.date == datetime.datetime.strptime(week_dates['Понедельник'].split(' ')[0], '%Y-%m-%d'),
        Homeworks.subject == x, Homeworks.class_num == cls_cur.number, Homeworks.class_name == cls_cur.letter).first()]
                            for x in sch['mon']],
            'Вторник': [[x, session.query(Homeworks).filter(
                Homeworks.date == datetime.datetime.strptime(week_dates['Вторник'].split(' ')[0], '%Y-%m-%d'),
                Homeworks.subject == x, Homeworks.class_num == cls_cur.number,
                Homeworks.class_name == cls_cur.letter).first()] for x in sch['tue']],
            'Среда': [[x, session.query(Homeworks).filter(
                Homeworks.date == datetime.datetime.strptime(week_dates['Среда'].split(' ')[0], '%Y-%m-%d'),
                Homeworks.subject == x, Homeworks.class_num == cls_cur.number,
                Homeworks.class_name == cls_cur.letter).first()] for x in sch['wed']],
            'Четверг': [[x, session.query(Homeworks).filter(
                Homeworks.date == datetime.datetime.strptime(week_dates['Четверг'].split(' ')[0], '%Y-%m-%d'),
                Homeworks.subject == x, Homeworks.class_num == cls_cur.number,
                Homeworks.class_name == cls_cur.letter).first()] for x in sch['thu']],
            'Пятница': [[x, session.query(Homeworks).filter(
                Homeworks.date == datetime.datetime.strptime(week_dates['Пятница'].split(' ')[0], '%Y-%m-%d'),
                Homeworks.subject == x, Homeworks.class_num == cls_cur.number,
                Homeworks.class_name == cls_cur.letter).first()] for x in sch['fri']]
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


class AllInf(Resource):
    def get(self, cls_nl):
        if len(cls_nl) < 2:
            return jsonify({'Класс отсутствует': None})
        cls = session.query(Classes.cl_id).filter(Classes.number == int(cls_nl[:-1]),
                                                  Classes.letter == cls_nl[-1]).first()
        if cls is None:
            return jsonify({'Класс отсутствует': None})
        students = session.query(Users).filter(Users.class_id == cls[0], Users.role == 'student').all()
        cls_dict = dict()
        teacher = session.query(Users).filter(Users.class_id == cls[0], Users.role == 'teacher').first()
        if teacher is not None:
            cls_dict['teachers'] = [{'surname': teacher.surname, 'name': teacher.name, 'otchestvo': teacher.otchestvo}]
        else:
            cls_dict['teachers'] = None
        if students is not None:
            cls_dict['students'] = list()
            for std in students:
                cls_dict['students'].append({'surname': std.surname, 'name': std.name, 'otchestvo': std.otchestvo})
        else:
            cls_dict['students'] = None
        sch = loads(session.query(Classes).filter(Classes.cl_id == cls[0]).first().schedule)
        cls_dict['schedule'] = {'Понедельник': [x for x in sch['mon']],
                                'Вторник': [x for x in sch['tue']],
                                'Среда': [x for x in sch['wed']],
                                'Четверг': [x for x in sch['thu']],
                                'Пятница': [x for x in sch['fri']]
                                }

        return jsonify(cls_dict)


api.add_resource(AllInf, '/api/<cls_nl>')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
