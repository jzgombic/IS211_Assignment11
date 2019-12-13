from flask import Flask
from flask import redirect as rd
from flask import render_template as template
from flask import request as req
import re
import os.path
from os import path


app = Flask(__name__)

TODO = []


@app.route("/")
def home():

    TODO.clear()

    if not path.exists('TODO.txt'):
        open("TODO.txt", "w+")

    with open("TODO.txt", 'r') as t:
        for task in t:
            TODO.append(tuple(task.split(',')))        

    return template('index.html',todo=TODO)


@app.route("/submit", methods=['POST'])
def submit():

    TODO.clear()

    task = req.form['task']
    email = req.form['email']
    priority = req.form['priority']
    
    if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
        return rd("/")
    elif not task:
        return rd("/")
    elif priority == "Select Priority":
        return rd("/")
    
    (open("TODO.txt", "a+")).write(task +','+ email + ','+ priority+ '\n')
    (open("TODO.txt", "a+")).close()

    TODO.append((task,email,priority))

    print(TODO)

    return rd('/')


@app.route("/delete", methods=['POST'])
def delete():

    TODO.clear()

    with open("TODO.txt", 'r') as t:
        for task in t:
            TODO.append(tuple(task.split(',')))

    f = open('TODO.txt', 'r+')
    f.truncate(0)

    id = req.form['deleteId']
    del TODO[int(id)-1]
    
    for item in TODO:
        (open("TODO.txt", "a+")).write(item[0]+', '+item[1]+', '+ item[2])
        (open("TODO.txt", "a+")).close()

    return rd('/')


@app.route("/clear", methods=['POST'])
def clear():

    (open('TODO.txt', 'r+')).truncate(0)

    return rd("/")
    

if __name__=='__main__':
    app.run(debug=True)
