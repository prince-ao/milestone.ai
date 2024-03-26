from flask import request, make_response, render_template
from flask_restx import Resource, Namespace
from ..redis_instance import r, USER_COOKIE_KEY
import json
import datetime

form_ns = Namespace('form', description="Operations related to form handling")

DYNAMIC_STATE_START = 8
DYNAMIC_END_STATE = 13

upgrade_courses = ['CSC211', 'CSC326', 'CSC330',
                   'CSC346', 'CSC382', 'CSC446', 'CSC490']  # upgrade courses upgrade the user's question set to the respective index

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
        "Have you utilized Career & Professional Development events to enhance job search skills?",
        "Have you met with a career advisor to review your resume, portfolio, and cover letter?",
        "Did you inform your network about your job search?",
        "Are you actively applying for jobs and tracking your applications?",
        "Are you considering graduate school?"
    ],
    [
        "Did you apply for internship prep programs like CUNY Tech Prep?",
        "Have you initiated a side project, like a web or mobile app?",
        "Are you contributing to open source projects?",
        "Have you been involved in local hackathons or coding events?",
        "Are you a member of any student professional organizations?"
    ],
]


@form_ns.route('/state')
class State(Resource):

    def _get_state_question(self, current_state, end):
        current_state_number = current_state['state']
        if current_state_number >= DYNAMIC_STATE_START:
            if current_state_number == DYNAMIC_STATE_START:
                question = render_template("questions/dynamic/d-state-0.j2")
            else:
                try:
                    current_index = current_state['career_info']['meta_data']['current_question'] - 1
                    answer = current_state['career_info']['answers'][current_index]
                    if answer == 'yes':
                        question = render_template(
                            "questions/dynamic/d-state-1.j2",
                            question=current_state['career_info']['asked_questions'][current_index],  # noqa
                            is_end=end,
                            yes_checked="checked"
                        )
                    else:
                        question = render_template(
                            "questions/dynamic/d-state-1.j2",
                            question=current_state['career_info']['asked_questions'][current_index],  # noqa
                            is_end=end,
                            no_checked="checked"
                        )
                except Exception:
                    question = render_template(
                        "questions/dynamic/d-state-1.j2",
                        question=current_state['career_info']['asked_questions'][current_index],  # noqa
                        is_end=end,
                    )

        elif current_state_number == 1:
            question = render_template(
                "questions/state-1.j2",
                first_name=current_state['personal_info']['first_name'],
                last_name=current_state['personal_info']['last_name']
            )
        elif current_state_number == 3:
            question = render_template(
                "questions/state-3.j2",
                classes_taken=current_state['academic_info']['classes_taken']
            )
        elif current_state_number == 4:
            current_year = datetime.datetime.now().year
            semester_range = []
            for year in range(current_year, current_year + 7):
                semester_range.append(f"spring {year}")
                semester_range.append(f"fall {year}")
            question = render_template(
                "questions/state-4.j2",
                semester_range=semester_range,
                graduation_semester=current_state['academic_info']['graduation_semester']
            )
        elif current_state_number == 5:
            question = render_template(
                "questions/state-5.j2",
                current_gpa=float(current_state['academic_info']['gpa'])
            )
        else:
            question = render_template(
                f"questions/state-{current_state_number}.j2"
            )

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
        Next Features:
            - fix the initial semester start
            - implement confirmation page
            - handle route authorization
            - style stuff
                - fix form
    """

    def _update_state(self, current_state, data, user_uuid):
        current_state_number = current_state['state']
        current_state_type = data['type']

        if current_state_type == 'next':
            if current_state_number == 1:
                if data['first_name'] and data['last_name']:
                    current_state['personal_info']['first_name'] = data['first_name']
                    current_state['personal_info']['last_name'] = data['last_name']
                else:
                    raise ValueError("missing first_name or last_name.")
            elif current_state_number == 3:
                if not isinstance(data['classes_taken'], list):
                    data['classes_taken'] = [data['classes_taken']]

                current_state['academic_info']['classes_taken'] = data['classes_taken']

                for i, upgrade_course in enumerate(upgrade_courses):
                    if upgrade_course in data['classes_taken']:
                        current_state['career_info']['meta_data']['semester_index'] = i + 1
                        break
            elif current_state_number == 4:
                current_state['academic_info']['graduation_semester'] = data['graduation_semester']
            elif current_state_number == 5:
                current_state['academic_info']['gpa'] = data['gpa']
            elif current_state_number >= DYNAMIC_STATE_START:
                current_state['career_info']['meta_data']['semester_question_index'] = current_state['career_info']['meta_data']['semester_question_index'] + 1  # noqa

                # get all required info
                current_question = current_state['career_info']['meta_data']['current_question']
                semester_index = current_state['career_info']['meta_data']['semester_index']
                semester_question_index = current_state['career_info']['meta_data']['semester_question_index']
                asked_questions = current_state['career_info']['asked_questions']
                answers = current_state['career_info']["answers"]

                if current_question > 0:
                    if len(asked_questions) <= current_question:
                        answers.append(data['selection'])
                    else:
                        answers[current_question - 1] = data['selection']
                    current_state['career_info']["answers"] = answers

                current_state['career_info']['meta_data']['current_question'] = current_question + 1

                # if the we need a new question
                if len(asked_questions) <= current_question:
                    if semester_index == len(questions) - 1 and semester_question_index == len(questions[semester_index]):
                        current_state['is_end'] = True
                    if len(questions[semester_index]) == semester_question_index - 1:
                        current_state['career_info']['meta_data']['semester_index'] = semester_index + 1
                        current_state['career_info']['meta_data']['semester_question_index'] = 0

                    # print(current_state)
                    semester_index = current_state['career_info']['meta_data']['semester_index']
                    semester_question_index = current_state['career_info']['meta_data']['semester_question_index']
                    asked_questions.append(
                        questions[semester_index][semester_question_index - 1])
                    current_state['career_info']['asked_questions'] = asked_questions

            current_state['state'] = current_state_number + 1
        elif current_state_type == 'previous' and current_state['state'] > 0:
            if current_state['career_info']['meta_data']['current_question'] > 0:
                current_state['career_info']['meta_data']['current_question'] = current_state['career_info']['meta_data']['current_question'] - 1
            current_state['state'] = current_state_number - 1
        elif current_state_type == 'done':
            current_question = current_state['career_info']['meta_data']['current_question']
            answers = current_state['career_info']["answers"]
            if current_question > len(answers):
                answers.append(data['selection'])
            else:
                answers[current_question - 1] = data['selection']
            current_state['career_info']["answers"] = answers
            print(current_state)

        r.set(f"{user_uuid}:user", json.dumps(current_state))

    def _is_end_state(self, current_state):

        if current_state['state'] >= DYNAMIC_END_STATE:
            return True
        else:
            return current_state['is_end']

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

        # print(end)

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

        if data['type'] == 'done':
            resp = make_response({}, 200)
            resp.headers['HX-Redirect'] = '/confirmation'
            return resp

        return self._get_state_question_or_error(current_state, end)
