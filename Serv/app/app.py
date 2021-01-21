from flask import Flask, render_template, request
import csv, re

app = Flask(__name__)
application = app

with open('test.csv', encoding='utf-8') as csvfile:
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
    headers=users.pop(0)

cnt = 0
def incr_cnt():
    global cnt
    cnt += 1
    return ''

def get_cnt():
    global cnt
    lcnt = cnt
    # print(lcnt)
    return lcnt

def null_cnt():
    global cnt
    cnt = 0
    return ''

@app.route('/')
def index():
    #print(headers)
    #print(users)
    return render_template('index.html', users=users, headers=headers)

@app.route('/pd')
def pd():
    return render_template('pd.html', users=users, headers=headers, incr_cnt=incr_cnt, get_cnt=get_cnt)

@app.route('/pd', methods=['POST'])
def pdsearch():
    mask=''
    # Подбор маски
    if request.method == 'POST':
        select = request.form.get('datatype')
        print(select)
        if select=="pasport":
            mask=r'^\d{4}\s\d{6}$'
        elif select=="account":
            mask=r'^\d{16}$'
        elif select=="name":
            mask=r'^[А-Яа-я]*\s?[А-Яа-я]+\s[А-Яа-я]+$'
        elif select=="date":
            mask=r'^\d\d?(\.|-|\/)\d\d?(\.|-|\/)\d\d\d?\d?$'
        elif select=="new":
            mask=request.form.get('selfmask')
    # Обработка пустого шаблона
    if mask=='':
        err='Нельзя использовать пустой шаблон. Заполните форму и повторите попытку'
        return render_template('pd.html', users=users, headers=headers, sel=select, mask=mask, err=err, incr_cnt=incr_cnt, get_cnt=get_cnt, null_cnt=null_cnt)
    # Её применение
    pdlist=[]
    pdkeys=[]
    for user in users:
        for key in user:
            res=re.match(mask, user[key])
            if res!=None:
                pdkeys.append(key)
        # Оказывается если не написать .copy, то в pdlist будут меняться внутренности, когда меняется pdkeys
        pdlist.append(pdkeys.copy()) 
        pdkeys.clear()
    return render_template('pd.html', users=users, headers=headers, pdlist=pdlist, sel=select, mask=mask, err='', incr_cnt=incr_cnt, get_cnt=get_cnt, null_cnt=null_cnt)

@app.route('/process_data/', methods=['POST'])
def search():
    userssearched= []
    #userssearched.append(users[0])
    if request.method == 'POST':
        select = request.form.get('searchoose')
        information = request.form.get('information') 
        # print(next(item for item in users if item['code'] == '000000003'))
        for item in users:
            if item[select].find(information)!=-1:
                userssearched.append(item)
        #userssearched.append(next(item for item in users if item[select].find(information)!=-1))
    return render_template('index.html', users=userssearched, headers=headers)

application.run()
