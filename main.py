from flask import Flask

app = Flask('MyApp')

app.run(port=8080, host='127.0.0.1', debug=True)
