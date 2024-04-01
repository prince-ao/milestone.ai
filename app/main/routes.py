from flask import render_template, make_response, request
from app.main import bp
from ..redis_instance import r, USER_COOKIE_KEY
import uuid
import json
import time


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
                "academic_standing": "",
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
        ...

    return resp


@bp.get('/confirmation')
def confirmation():
    return render_template("confirmation.j2")

@bp.get('/chatbot')
def chatbot():
    return render_template("chatbot.j2")

@bp.post('/ai-response')
def ai_response():
    userInput = request.form['userInput']
    time.sleep(1)
    return "<p class='hidden-response'>There are many different kinds of animals that live in China. Tigers and leopards are animals that live in China's forests in the north. In the jungles, monkeys swing in the trees and elephants walk through the brush.</p>"