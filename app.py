from flask import Flask, render_template, request, escape
from search4web import search4letters, log_request

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

@app.route("/search", methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results: '
    result = str(search4letters(phrase, letters))
    log_request(request, result)
    return str(search4letters(phrase, letters))


@app.route('/')
@app.route("/entry")
def entry_page():
    return render_template('entry.html',
                           the_title='Welcome to search  letters on the web!')


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

