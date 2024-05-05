from flask import render_template, make_response, request, redirect, session
from app.main import bp
from app.apis.form_handler import DYNAMIC_END_STATE, career_readiness
from ..redis_instance import r, USER_COOKIE_KEY
import uuid
import json


NUMBER_OF_CONFIRMATION_MILESTONES = 5


@bp.get('/')
def index():
    # error = request.headers['Thrown-Error']
    error = session.get('error')

    if error:
        session['error'] = ""

    return render_template("index.j2", error=error)


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
                    "semester_index_start": 0,
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

        if current_state['is_end']:
            resp = redirect('/confirmation')

    return resp


@bp.get('/confirmation')
def confirmation():
    user_uuid = request.cookies.get(USER_COOKIE_KEY)

    if not user_uuid:
        return redirect('/get-to-know-you')

    try:
        response = r.get(f"{user_uuid}:user")
    except Exception:
        return redirect('/get-to-know-you')

    current_state = json.loads(response.decode('utf-8'))

    if not current_state['is_end']:
        return redirect('/get-to-know-you')


    milestones = get_milestones(current_state)

    return render_template("confirmation.j2", milestones=milestones)


def get_milestones(current_state):
    """
    algorithm:
        create a list that stores suggestions (we want at most 5 suggestions)
        go through answers, if answer was no, add that as a suggestion
        add more suggestions from the higher milestones or semesters
    """
    milestones = []
    asked_questions = current_state['career_info']['asked_questions']
    for i, answer in enumerate(current_state['career_info']['answers']):
        if answer == 'no':
            indecies = current_state['career_info']['asked_questions'][i]
            milestones.append(career_readiness[indecies[1][0]][indecies[1][1]])

    if len(milestones) != 5:
        last_question_indecies = asked_questions[-1][1]
        start_semester_index = last_question_indecies[0]
        start_semester_question_index = last_question_indecies[1]

        while len(milestones) < 5:
            start_semester_question_index = start_semester_question_index + 1

            if start_semester_question_index >= len(career_readiness[start_semester_index]):
                start_semester_question_index = 0
                start_semester_index = start_semester_index + 1

            if start_semester_index >= len(career_readiness):
                break

            milestones.append(
                career_readiness[start_semester_index][start_semester_question_index])
    return milestones