from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash 
from .script import Graph

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def homepage():
    graph = request.args.get('graph', default="GEN", type = str)
    obj = Graph(graph)
    script, div = obj.get_graph()
    return render_template("homepage.html", script=script, div=div) 

@app.errorhandler(Exception)
def unhandled_exception(e):
    flash( "OOPS! Something is wrong!", category="danger")
    return redirect(url_for('homepage'))


if __name__== '__main__':
    app.run(port=5000, debug=True)