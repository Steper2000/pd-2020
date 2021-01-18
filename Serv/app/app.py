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

@app.route('/')
def index():
    pass
    return render_template('index.html', users=users, headers=headers)

@app.route('/pd')
def pd():
    mask=''
    return render_template('pd.html', users=users, headers=headers, mask=mask)

@app.route('/pd', methods=['POST'])
def pdsearch():
    mask=''
    # Подбор маски
    if request.method == 'POST':
        select = request.form.get('datatype')
        if select=="pasport":
            mask=r'^\d\d\d\d\d\d\d\d\d\d$'
        elif select=="account":
            mask=r'^\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d$'
        elif select=="new":
            mask=request.form.get('selfmask')
    # Её приминение
    pdlist=[]
    pdkeys=[]
    for user in users:
        for key in user:
            res=re.match(mask, user[key])
            if res!=None:
                print(key, user[key], mask, res)
                pdkeys.append(key)
                print(pdkeys)
        print(pdkeys)
        pdlist.append(pdkeys.copy()) # Оказывается если не написать копи, то в pdlist будут меняться внутренности, когда меняется pdkeys
        print(pdlist)
        pdkeys.clear()
    print(pdlist)
    return render_template('pd.html', users=users, headers=headers, mask=mask, pdlist=pdlist)

@app.route('/process_data/', methods=['POST'])
def search():
    userssearched= []
    #userssearched.append(users[0])
    if request.method == 'POST':
        select = request.form.get('searchoose')
        information = request.form.get('information') 
        print(information)
        # print(next(item for item in users if item['code'] == '000000003'))
        for item in users:
            if item[select].find(information)!=-1:
                userssearched.append(item)
        #userssearched.append(next(item for item in users if item[select].find(information)!=-1))
    return render_template('index.html', users=userssearched, headers=headers)

application.run()
