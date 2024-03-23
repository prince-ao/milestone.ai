from flask import request, make_response, render_template
from flask_restx import Resource, Namespace
from ..redis_instance import r, USER_COOKIE_KEY
import json

form_ns = Namespace('form', description="Operations related to form handling")

DYNAMIC_STATE_START = 8

questions = [
    [
        "Have you created a Handshake account with Career Services?",
        "Did you draft a resume?",
        "Have you reviewed your major's required courses?",
        "Have you joined any student clubs?"
    ],
    [
        "Have you set up a LinkedIn account?",
        "Did you explore career options for Computer Science majors?",
        "Have you attended a hackathon?",
        "Did you create a GitHub account?",
        "Have you attended any professional development workshops?"
    ],
    [
        "Have you developed a network of contacts on LinkedIn?",
        "Have you recently updated your resume?",
        "Did you find a mentor for periodic check-ins?",
        "Have you been active on your GitHub account?",
        "Did you attend any recent professional development workshops?"
    ],
    [
        "Have you contributed to any open source projects?",
        "Did you apply for any internship prep programs like CUNY Tech Prep?",
        "Have you launched a side project, such as a web or mobile app?",
        "Have you participated in local hackathons or coding events?",
        "Did you join any student professional organizations?"
    ],
    [
        "Have you crafted an effective resume?",
        "Are you using LinkedIn to build your professional network?",
        "Have you applied for internships?",
        "Are you regularly posting to GitHub?",
        "Have you attended any career fairs or professional events?"
    ],
    [
        "Are you prepared for technical internship interviews?",
        "Have you gained confidence in a specific tech stack beyond your classes?",
        "Did you secure a software internship for the summer of your junior year?",
        "Have you engaged in self-guided learning outside of class?",
        "Did you participate in any virtual work experience programs?"
    ],
    [
        "Have you utilized Career & Professional Development events to enhance job search skills?"
        "Have you met with a career advisor to review your resume, portfolio, and cover letter?"
        "Did you inform your network about your job search?"
        "Are you actively applying for jobs and tracking your applications?"
        "Are you considering graduate school?"
    ],
    [
        "Did you apply for internship prep programs like CUNY Tech Prep?"
        "Have you initiated a side project, like a web or mobile app?"
        "Are you contributing to open source projects?"
        "Have you been involved in local hackathons or coding events?"
        "Are you a member of any student professional organizations?"
    ],
]


@form_ns.route('/state')
class State(Resource):
    _is_end = False

    def _get_state_question(self, current_state, end):
        if current_state['state'] >= DYNAMIC_STATE_START:
            if current_state['state'] == DYNAMIC_STATE_START:
                question = render_template("questions/dynamic/d-state-0.j2")
            else:
                print(current_state)
                question = render_template(
                    "questions/dynamic/d-state-1.j2",
                    question=current_state['career_info']['asked_questions'][current_state['career_info']['meta_data']['current_question'] - 1],  # noqa
                    is_end=end

                )
        else:
            question = render_template(
                f"questions/state-{current_state['state']}.j2")

        return question

    def _get_state_question_or_error(self, state, end):
        try:
            resp = make_response(self._get_state_question(state, end))
            resp.headers['content-type'] = 'text/html'
            return resp
        except IndexError:
            return {"message": "index out-of-bound"}, 409

    """
    def _get_html_button(self, current_state, end):
        button = ''
        if current_state['state'] != 0:
            button += '<button id="previous" type="submit">previous</button>'
        if end:
            button += '<a href="/confirmation"><button type="button">done</button></a>'
        else:
            button += '<button id="next" type="submit">next</button>'
        return button
    """

    def _update_state(self, current_state, data, user_uuid):
        if data['type'] == 'next':
            if current_state['state'] == 1:
                if data['first_name'] and data['last_name']:
                    current_state['personal_info']['first_name'] = data['first_name']
                    current_state['personal_info']['last_name'] = data['last_name']
                else:
                    raise ValueError("missing first_name or last_name.")
            elif current_state['state'] >= DYNAMIC_STATE_START:
                print('1')
                print(current_state)
                # update the question index
                current_state['career_info']['meta_data']['semester_question_index'] = current_state['career_info']['meta_data']['semester_question_index'] + 1  # noqa

                # get all required info
                current_question = current_state['career_info']['meta_data']['current_question']
                semester_index = current_state['career_info']['meta_data']['semester_index']
                semester_question_index = current_state['career_info']['meta_data']['semester_question_index']
                asked_questions = current_state['career_info']['asked_questions']

                # if the we need a new question
                if len(asked_questions) <= current_question:
                    current_state['career_info']['meta_data']['current_question'] = current_question + 1
                    print("2")
                    print(current_state)

                    if semester_index == len(questions) - 1 and semester_question_index == len(questions[semester_index]) - 1:
                        self._is_end = True
                    if len(questions[semester_index]) == semester_question_index:
                        current_state['career_info']['meta_data']['semester_index'] = semester_index + 1
                        current_state['career_info']['meta_data']['semester_question_index'] = 0

                    semester_index = current_state['career_info']['meta_data']['semester_index']
                    semester_question_index = current_state['career_info']['meta_data']['semester_question_index']
                    asked_questions.append(
                        questions[semester_index][semester_question_index])
                    current_state['career_info']['asked_questions'] = asked_questions

            current_state['state'] = current_state['state'] + 1
        elif data['type'] == 'previous' and current_state['state'] > 0:
            if current_state['career_info']['meta_data']['current_question'] > 0:
                current_state['career_info']['meta_data']['current_question'] = current_state['career_info']['meta_data']['current_question'] - 1
            current_state['state'] = current_state['state'] - 1
        elif data['type'] == 'done':
            ...

        r.set(f"{user_uuid}:user", json.dumps(current_state))

    def _is_end_state(self, current_state):
        if current_state['state'] >= 13:
            return True
        else:
            return self._is_end

    def get(self):
        user_uuid = request.cookies.get(USER_COOKIE_KEY)

        try:
            response = r.get(f"{user_uuid}:user")
        except Exception:
            return {"message": "user not found"}, 404

        if not user_uuid:
            # handle user does not exist
            ...

        current_state = json.loads(response.decode('utf-8'))

        end = self._is_end_state(current_state)

        return self._get_state_question_or_error(current_state, end)

    def post(self):
        data = request.get_json()

        user_uuid = request.cookies.get(USER_COOKIE_KEY)

        if not user_uuid:
            return {"message": "user not found"}, 401

        try:
            response = r.get(f"{user_uuid}:user")
        except Exception:
            return {"message": "user not found"}, 404

        current_state = json.loads(response.decode('utf-8'))

        try:
            self._update_state(current_state, data, user_uuid)
        except ValueError as err:
            return {"message": err}, 400

        end = self._is_end_state(current_state)

        return self._get_state_question_or_error(current_state, end)
