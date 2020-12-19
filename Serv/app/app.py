from flask import Flask, render_template, request

app = Flask(__name__)
application = app

@app.route('/')
def aaa():
    res = None
    msg = None
    if request.args:
        try:
            n1 = float(request.args.get('n1'))
            op = request.args.get('op')
            n2 = float(request.args.get('n2'))
            if op == '+':
                res = n1 + n2
            elif op == '-':
                res = n1 - n2
            elif op == '*':
                res = n1 * n2
            elif op == '/':
                res = n1 / n2
        except ZeroDivisionError:
            msg = 'You can not devide by zero'
        except ValueError:
            msg = 'Please enter numbers only'
    return render_template('index.html', res = res, msg = msg)
application.run()
