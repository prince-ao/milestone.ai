from flask import request, make_response, render_template, redirect
from flask_restx import Resource, Namespace
from ..redis_instance import r, USER_COOKIE_KEY
import json
import datetime

form_ns = Namespace('form', description="Operations related to form handling")

DYNAMIC_STATE_START = 8
DYNAMIC_END_STATE = 12

upgrade_courses = ['CSC211', 'CSC326', 'CSC330',
                   'CSC346', 'CSC382', 'CSC446', 'CSC490']  # upgrade courses upgrade the user's question set to the respective index

career_readiness = [
    [
        "Create a Handshake Account with Career Services.",
        "Create a Draft Resume.",
        "Review Major Required Courses.",
        "Join a Student Club."
    ],
    [
        "Create a LinkedIn Account.",
        "Explore Career Options for Computer Science Majors.",
        "Attend a Hackathon.",
        "Create a GitHub Account.",
        "Attend Professional Development Workshops and seminars."
    ],
    [
        "Develop a Network of Contact Through LinkedIn.",
        "Update Your Resume.",
        "Identify a Mentor with Whom You Can Check-in Periodically.",
        "Post to Your GitHub Account.",
        "Attend Professional Development Workshops."
    ],
    [
        "Contribute to open source projects.",
        "Apply for internship prep programs (CUNY Tech Prep, TTP, ...).",
        "Launch a side project (web app or mobile).",
        "Participate in local hackathons or coding events to collaborate on code and meet other students.",
        "Join student professional organizations."
    ],
    [
        "Create an effective resume.",
        "Utilize LinkedIn to build your professional network: Start marketing yourself and building relationships on LinkedIn.",
        "Work in at least one software internship position by summer of Junior year",
        "Consider self-guided learning outside the classroom",
        "Attend career fairs, local meetings, conferences and seminars."
    ],
    [
        "Acquire technical internship interview readiness (Practice, practice, practice)",
        "Acquire confidence developing in one industry tech stack beyond whats taught in the classroom",
        "Work in at least one software internship position by summer of Junior year",
        "Consider self-guided learning outside the classroom",
        "Participate in a virtual work experience program"
    ],
    [
        "Take advantage of events offered by Career & Professional Development to perfect your job search, interviewing and employability skills",
        "Schedule an appointment with the career advisor to go over your final resume, portfolio, cover letter, etc",
        "Alert contacts in your network to remind them you are in the process of searching for a job",
        "Apply, apply and apply for more jobs. Record your progress and remember to follow-up on your applications"
    ],
    [
        "Apply, apply and apply for more jobs. Record your progress and remember to follow-up on your applications",
        "Arrange for references. These can be professors, connections, internship positions or others who know your interests, abilities, skills and work habits",
        "If appropriate, complete the process of applying to graduate school",
        "Take the mandatory Senior Exit Survey"
    ]
]

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
    ],
    [
        "Are you actively applying for jobs and tracking your applications?",
        "Did you arrange references?",
        "If appropriate, have you complete the process of applying to graduate school?",
        "Have you taken the Senior Exit Survey?"
    ],
]

@form_ns.route('/reset')
class Reset(Resource):
    def get(self):
        resp = redirect('/get-to-know-you')
        resp.delete_cookie(USER_COOKIE_KEY)

        return resp


@form_ns.route('/state')
class State(Resource):

    def _get_state_question(self, current_state, end):
        current_state_number = current_state['state']
        if current_state_number >= DYNAMIC_STATE_START:
            if current_state_number == DYNAMIC_STATE_START:
                question = render_template("questions/dynamic/d-state-0.j2")
            else:
                current_index = current_state['career_info']['meta_data']['current_question'] - 1
                _question = current_state['career_info']['asked_questions'][current_index][0]
                try:
                    answer = current_state['career_info']['answers'][current_index]
                    if answer == 'yes':
                        question = render_template(
                            "questions/dynamic/d-state-1.j2",
                            question=_question,
                            is_end=end,
                            yes_checked="checked"
                        )
                    else:
                        question = render_template(
                            "questions/dynamic/d-state-1.j2",
                            question=_question,
                            is_end=end,
                            no_checked="checked"
                        )
                except Exception:
                    question = render_template(
                        "questions/dynamic/d-state-1.j2",
                        question=_question,
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
        elif current_state_number == 6:
            question = render_template(
                "questions/state-6.j2",
                credits_taken=int(
                    current_state['academic_info']['credits_taken'])
            )
        elif current_state_number == 7:
            current_year = datetime.datetime.now().year
            standings = [
                'lower freshman',
                'upper freshman',
                'lower sophomore',
                'upper sophomore',
                'lower junior',
                'upper junior',
                'lower senior',
                'upper senior',
            ]
            question = render_template(
                "questions/state-7.j2",
                standings=standings,
                academic_standing=current_state['academic_info']['academic_standing']
            )

        else:
            question = render_template(
                f"questions/state-{current_state_number}.j2"
            )
        # print(current_state)
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
                try:
                    if not isinstance(data['classes_taken'], list):
                        data['classes_taken'] = [data['classes_taken']]

                    current_state['academic_info']['classes_taken'] = data['classes_taken']
                except Exception:
                    current_state['academic_info']['classes_taken'] = []

                for i, upgrade_course in enumerate(reversed(upgrade_courses)):
                    if upgrade_course in current_state['academic_info']['classes_taken']:
                        current_state['career_info']['meta_data']['semester_index'] = len(
                            upgrade_courses) - i
                        current_state['career_info']['meta_data']['semester_index_start'] = len(
                            upgrade_courses) - i
                        break
            elif current_state_number == 4:
                current_state['academic_info']['graduation_semester'] = data['graduation_semester']
            elif current_state_number == 5:
                current_state['academic_info']['gpa'] = data['gpa']
            elif current_state_number == 6:
                current_state['academic_info']['credits_taken'] = data['credits_taken']
            elif current_state_number == 7:
                current_state['academic_info']['academic_standing'] = data['academic_standing']
            elif current_state_number >= DYNAMIC_STATE_START:
                current_state['career_info']['meta_data']['semester_question_index'] = current_state['career_info']['meta_data']['semester_question_index'] + 1  # noqa

                # get all required info
                current_question = current_state['career_info']['meta_data']['current_question']
                semester_index = current_state['career_info']['meta_data']['semester_index']
                semester_question_index = current_state['career_info']['meta_data']['semester_question_index']
                asked_questions = current_state['career_info']['asked_questions']
                answers = current_state['career_info']["answers"]

                if current_question > 0:
                    # if its a new question (user didn't go back to a question they already answered)
                    if len(asked_questions) <= current_question:
                        answers.append(data['selection'])
                    # if we went back and forth we may not need to append since that
                    # question was already in the state.
                    else:
                        # add the answer.
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
                    asked_questions.append((
                        questions[semester_index][semester_question_index - 1],
                        (semester_index, semester_question_index - 1))
                    )
                    current_state['career_info']['asked_questions'] = asked_questions

            current_state['state'] = current_state_number + 1
        elif current_state_type == 'previous' and current_state['state'] > 0:
            if current_state['career_info']['meta_data']['current_question'] > 0:
                current_state['career_info']['meta_data']['current_question'] = current_state['career_info']['meta_data']['current_question'] - 1
            if current_state['state'] == DYNAMIC_STATE_START:
                current_state['career_info']['asked_questions'] = []
                current_state['career_info']['answers'] = []
                current_state['career_info']['meta_data']['semester_index'] = 0
                current_state['career_info']['meta_data']['semester_question_index'] = 0
                current_state['career_info']['meta_data']['current_question'] = 0
                current_state['career_info']['meta_data']['semester_index_start'] = 0
                current_state['is_end'] = False
            current_state['state'] = current_state_number - 1
        elif current_state_type == 'done':
            current_question = current_state['career_info']['meta_data']['current_question']
            answers = current_state['career_info']["answers"]
            if current_question > len(answers):
                answers.append(data['selection'])
            else:
                answers[current_question - 1] = data['selection']
            current_state['career_info']["answers"] = answers
            current_state['is_end'] = True

        r.set(f"{user_uuid}:user", json.dumps(current_state))

    def _is_end_state(self, current_state):
        if current_state['state'] >= DYNAMIC_END_STATE:
            current_state['is_end'] = True

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
        print(current_state)

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
