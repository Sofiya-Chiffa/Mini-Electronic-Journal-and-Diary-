from flask import Flask, render_template, request

app = Flask('MyApp')


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
    days = [[['Математика', '...'], ['Русский язык', '..'], ['Окружающий мир', ''], ['Литература', ''], ['', '']],
            [['ИЗО', '.'], ['Математика', '...'], ['Русский язык', ''], ['Физ-ра', ''], ['Английский язык', '.']],
            [['История', '.'], ['Информатика', ''], ['Русский язык', '.'], ['Технология', '..'], ['', '']],
            [['География', '..'], ['Физ-ра', '.'], ['Математика', ''], ['Русский язык', '.'], ['', '']],
            [['Окружающий мир', '..'], ['Математика', '....'], ['Музыка', '..'], ['Литература', '..'], ['', '']]]
    return render_template('student_diary.html', days=days)


@app.route('/student/schedule')
def student_schedule():
    days = [['Математика', 'Русский язык', 'Окружающий мир', 'Литература', ''],
            ['ИЗО', 'Математика', 'Русский язык', 'Физ-ра', 'Английский язык'],
            ['История', 'Информатика', 'Русский язык', 'Технология', ''],
            ['География', 'Физ-ра', 'Математика', 'Русский язык', ''],
            ['Окружающий мир', 'Математика', 'Музыка', 'Литература', '']]
    return render_template('student_schedule.html', days=days)


@app.route('/student/grade')
def student_grade():
    return render_template('student_grade.html')


app.run(port=8080, host='127.0.0.1', debug=True)
