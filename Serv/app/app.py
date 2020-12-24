from flask import Flask, render_template, request

app = Flask(__name__)
application = app

@app.route('/')
def index():
    return render_template('index.html')
application.run()
