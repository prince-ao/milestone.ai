from flask import render_template, make_response, request, redirect
from app.main import bp
from app.apis.form_handler import DYNAMIC_END_STATE
from ..redis_instance import r, USER_COOKIE_KEY
import uuid
import json


@bp.get('/')
def index():
    return render_template("index.j2")


@bp.get('/get-to-know-you')
def get_to_know_you():
    resp = make_response(render_template("get-to-know-you.j2"))
    user_uuid = request.cookies.get(USER_COOKIE_KEY)

    if not user_uuid:
        user_uuid = str(uuid.uuid4())
        resp.set_cookie(USER_COOKIE_KEY, user_uuid)
        initial_form_state = {
            "state": 0,
            "is_end": False,
            "personal_info": {
                "first_name": "",
                "last_name": ""
            },
            "academic_info": {
                "classes_taken": [],
                "credits_taken": 0,
                "graduation_semester": '',
                "gpa": 0,
                "classification": "",
            },
            "career_info": {
                "meta_data": {
                    # index within possible questions (x)
                    "semester_index": 0,
                    # index within possible questions (y)
                    "semester_question_index": 0,
                    # current question within asked_questions
                    "current_question": 0,
                },
                "asked_questions": [],
                "answers": []
            }
        }

        json_initial_form_state = json.dumps(initial_form_state)

        try:
            r.set(f"{user_uuid}:user", json_initial_form_state)
        except Exception:
            return {"message": "internal error"}, 500

    else:
        try:
            response = r.get(f"{user_uuid}:user")
        except Exception:
            return {"message": "internal error"}, 500

        current_state = json.loads(response.decode('utf-8'))

        if current_state['state'] >= DYNAMIC_END_STATE:
            resp = redirect('/confirmation')

    return resp


@bp.get('/confirmation')
def confirmation():
    return render_template("confirmation.j2")
