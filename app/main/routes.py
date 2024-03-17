from flask import render_template, make_response, request
from app.main import bp
from ..redis_instance import r, USER_COOKIE_KEY
import uuid
import json


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/get-to-know-you')
def get_to_know_you():
    resp = make_response(render_template("get-to-know-you.html"))
    user_uuid = request.cookies.get(USER_COOKIE_KEY)

    if not user_uuid:
        user_uuid = str(uuid.uuid4())
        resp.set_cookie(USER_COOKIE_KEY, user_uuid)
        initial_form_state = {
            "state": 0,
            "personal_info": {
                "first_name": "",
                "last_name": ""
            },
            "academic_info": {
                "classes_taken": [],
                "credits_taken": -1,
                "graduation_semester": '',
                "gpa": -1,
                "classification": "",
            },
            "career_info": {}
        }

        json_initial_form_state = json.dumps(initial_form_state)

        try:
            r.set(f"{user_uuid}:user", json_initial_form_state)
        except Exception:
            return {"message": "internal error"}, 500

    else:
        ...

    return resp


@bp.route('/form')
def form():
    return render_template("form.html")

# return json for the next generated question.
# @bp.route('/form_question')
# def formQuestion():
