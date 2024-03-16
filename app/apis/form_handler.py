from flask import request, make_response, render_template
from flask_restx import Resource, Namespace
from ..redis_instance import r, USER_COOKIE_KEY
import json

form_ns = Namespace('form', description="Operations related to form handling")


@form_ns.route('/state')
class State(Resource):
    def _get_state_question(self, current_state, end):
        question = render_template(
            f"questions/state-{current_state['state']}.html",
            html_button=self._get_html_button(current_state, end),
            end=end
        )

        return question

    def _get_html_button(self, current_state, end):
        button = ''
        if current_state['state'] != 0:
            button += '<button id="previous" type="submit">previous</button>'
        if end:
            button += '<a href="/confirmation"><button type="button">done</button></a>'
        else:
            button += '<button id="next" type="submit">next</button>'
        return button

    def _get_state_question_or_error(self, state, end):
        try:
            resp = make_response(self._get_state_question(state, end))
            resp.headers['content-type'] = 'text/html'
            return resp
        except IndexError:
            return {"message": "index out-of-bound"}, 409

    def _update_state(self, current_state, data, user_uuid):
        if data['type'] == 'next':
            match current_state['state']:
                case 1:
                    if data['first_name'] and data['last_name']:
                        current_state['first_name'] = data['first_name']
                        current_state['last_name'] = data['last_name']
                    else:
                        raise ValueError("missing first_name or last_name.")

            current_state['state'] = current_state['state'] + 1
        elif data['type'] == 'previous' and current_state['state'] > 0:
            current_state['state'] = current_state['state'] - 1
        elif data['type'] == 'done':
            ...

        r.set(f"{user_uuid}:user", json.dumps(current_state))

    def _is_end_state(self, current_state):
        if current_state['state'] == 1:
            return True
        else:
            return False

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
        print(data)

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
