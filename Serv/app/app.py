from flask import Flask, render_template, request
import csv

app = Flask(__name__)
application = app

@app.route('/')
def aaa():
    with open('C:\\1C_project\\pd-2020\\Serv\\app\\test.csv', encoding='utf-8') as csvfile:
        users = []
        reader = csv.reader(csvfile)
        for row in reader:
            user = {}
            user["code"] = row[0]
            user["name"] = row[1]
            user["birth"] = row[2]
            user["who"] = row[3]
            user["pasport"] = row[4]
            user["account"] = row[5]
            users.append(user)
    return render_template('index.html', users=users)
application.run()
