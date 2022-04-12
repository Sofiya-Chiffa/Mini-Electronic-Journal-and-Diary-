from json import dumps
from data import db_session
import datetime as dt
from data.classes import Classes
from data.homeworks import Homeworks
from data.users import Users

db_session.global_init('db/school_db.db')
session = db_session.create_session()

clas = Classes()
clas.number = 5
clas.letter = 'A'
clas.schedule = dumps({"mon": ["Алгебра", "Литература", "Информатика", "Английский"],
                       "tue": ["Физ-ра", "География", "Литература", "Физика", "История"],
                       "wed": ["Русский", "Геометрия", "География", "Химия", "Биология"],
                       "thu": ["Литература", "Физ-ра", "Информатика", "Английский"],
                       "fri": ["Биология", "Русский", "Музыка", "ИЗО"]})
clas.time_schedule = dumps({"day": ["8:00", "8:50", "9:40", "10:40", "11:30"]})

session.add(clas)

hm = Homeworks()
hm.date = dt.datetime.date(dt.datetime.today())  # получается из формы бррр
hm.subject = 'Алгебра'
hm.class_num = 5
hm.class_name = 'А'
hm.homework = 'Номер 1, 2 и 3 стр. 115'

session.add(hm)

st1 = Users()
st1.name = 'Вася'
st1.surname = 'Пупкин'
st1.otchestvo = 'Владимирович'
st1.role = 'student/diary'
st1.login = 'Вася'
st1.password = 'Пупкин'
st1.class_id = 1
session.add(st1)
st2 = Users()
st2.name = 'Пупка'
st2.surname = 'Васькин'
st2.otchestvo = 'Мировладович'
st2.role = 'student/diary'
st2.login = 'Пупка'
st2.password = 'Васькин'
st2.class_id = 1
session.add(st2)
th = Users()
th.name = 'Марья'
th.surname = 'Щербакова'
th.otchestvo = 'Ивановна'
th.role = 'teacher/schedule'
th.login = 'maria'
th.password = 'teacher-1'
th.class_id = 1

session.add(th)
session.commit()
