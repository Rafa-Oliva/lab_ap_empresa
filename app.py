from flask import Flask, render_template, request, escape, redirect, url_for
from search4web import search4letters, log_request
from sqlite_db import*

app = Flask(__name__)


# @app.route("/")
# def hello() -> '302':
#     return redirect("/entry")


# @app.route("/<name>")
# def hello(name):
#    return f"Hello, {escape(name)}!"

# @app.route("/index")
# def index():
#    return f"Index Page"



#C:\Users\rafao\Documents\2_Master\Laboratorio_Aplicaciones_Empresariales\myproject>py -m flask run

#delete_user_database()
start_user_database()

@app.route("/search", methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results: '
    result = str(search4letters(phrase, letters))
    log_request(request, result)
    return str(search4letters(phrase, letters))

@app.route("/login", methods=['POST'])
def login_page():
    if request.form.get('login') == 'LOGIN':
        username = request.form['username']
        password = request.form['password']
        if login_authentication(username,password):
            return redirect(url_for('entry_page', username=username))
        else:
            return render_template('display_error.html', the_error='Incorrect username and/or password')
    elif request.form.get('register') == 'REGISTER':
        redirect(url_for('register_page'))
        return render_template('register.html')
    elif request.form.get('incognito_mode') == 'INCOGNITO_MODE':
        login_anonymous()
        return redirect(url_for('entry_page', username='Anonymous'))

@app.route("/register", methods=['POST'])
def register_page():
    if request.form.get('register') == 'REGISTER':
        username = request.form['username']
        password = request.form['password']
        if register_new_user(username,password):
            return redirect(url_for('entry_page', username=username))
        else:
            return render_template('display_error.html', the_error='The username selected already exists')


@app.route('/')
#@app.route("/index")
def main_page():
    return render_template('login.html')

@app.route("/<username>/entry")
def entry_page(username):
    return render_template('entry.html')

@app.route("/error")
def error_page(error):
    return render_template('display_error.html', the_error=error)


@app.route("/result", methods=['POST'])
def results_page():
    phrase = request.form['phrase']
    letters = request.form['letters']
    result: str = str(search4letters(phrase, letters))
    return render_template('results.html',
                           the_title='Here are your results:',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=result)

@app.route('/viewlog')
def view_the_log() -> str:
    with open('search.log', 'r') as log:
        contents = log.read()
    return escape(contents)

