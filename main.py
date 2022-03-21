from flask import Flask, render_template, request

app = Flask('MyApp')


@app.route('/')
def teacher_or_student():
    return render_template('teacher_or_student.html')


@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/student')
def student():
    return render_template('student.html')


app.run(port=8080, host='127.0.0.1', debug=True)
