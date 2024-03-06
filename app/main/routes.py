from flask import render_template
from app.main import bp


@bp.route('/')
def index():
    return render_template("index.html")

@bp.route('/navbar')
def navbar():
    return render_template("navbar.html")

@bp.route('/form')
def form():
    return render_template("form.html")

# return json for the next generated question.
# @bp.route('/form_question')
# def formQuestion():


