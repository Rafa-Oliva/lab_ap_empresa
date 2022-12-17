import flask
from flask import Flask, render_template, request, escape, redirect, url_for
from search4web import search4letters, log_request
from sqlite_db import *

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

# C:\Users\rafao\Documents\2_Master\Laboratorio_Aplicaciones_Empresariales\myproject>py -m flask run

start_user_database()


@app.route('/')
@app.route("/index")
def main_page():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login_page():
    if request.form.get('login') == 'LOGIN':
        username = request.form['username']
        password = request.form['password']
        if login_authentication(username, password):
            return redirect(url_for('entry_page', username=username))
        else:
            return render_template('display_error.html', the_error='Incorrect username and/or password')
    elif request.form.get('register') == 'REGISTER':
        redirect(url_for('register_page'))
        return render_template('register.html')
    elif request.form.get('incognito_mode') == 'INCOGNITO MODE':
        login_anonymous()
        return redirect(url_for('entry_page', username='Anonymous'))
    elif request.form.get('visit_counter') == 'VISIT COUNTER':
        return redirect(url_for('visit_counter_page'))
    elif request.form.get('view_log') == 'VIEW LOG':
        return redirect(url_for('view_log_page'))


@app.route("/register", methods=['POST'])
def register_page():
    if request.form.get('register') == 'REGISTER':
        username = request.form['username']
        password = request.form['password']
        if register_new_user(username, password):
            return redirect(url_for('entry_page', username=username))
        else:
            return render_template('display_error.html', the_error='The username selected already exists')


@app.route("/<username>/entry")
def entry_page(username):
    return render_template('entry.html', the_username=username)


@app.route("/<username>/result", methods=['POST'])
def results_page(username):
    phrase = request.form['phrase']
    letters = request.form['letters']
    result: str = str(search4letters(phrase, letters))
    log_entry = 'Search PHRASE=' + phrase + ' | LETTERS=' + letters + ' | RESULT=' + result
    new_entry_log(username, log_entry)
    return render_template('results.html', the_username=username, the_phrase=phrase, the_letters=letters, the_results=result)


@app.route('/visit_counter')
def visit_counter_page():
    contents = get_visit_counter()
    header = ['USERNAME', 'VISIT COUNT']  # Create the table's column headers
    return render_template('view_table.html', the_title='visit counter',the_contents=flask.Markup(create_html_table(header, sorted(contents,reverse=True))))

@app.route('/viewlog')
def view_log_page():
    contents = get_log()
    header = ['TIME', 'USERNAME', 'ACTION']  # Create the table's column headers
    return render_template('view_table.html', the_title='log', the_contents=flask.Markup(create_html_table(header, sorted(contents))))


def create_html_table(header, contents):
    table = "<table>\n"
    table += "  <tr>\n"
    for column in header:
        table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </tr>\n"

    # Create the table's row data
    for line in contents[0:]:
        if len(header) == 2:
            number_visits, username = line
            row = [username, number_visits]
            print(row)
            #row = [number_visits, username]
        elif len(header) == 3:
            time, username, action = line
            row = [time, username, action]
        table += "  <tr>\n"
        for column in row:
            table += "    <td>{0}</td>\n".format(str(column).strip())
        table += "  </tr>\n"

    table += "</table>"
    return table
