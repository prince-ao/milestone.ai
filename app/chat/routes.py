from flask import render_template, request, redirect, session, make_response
from app.chat import chat_bp
from app.utils.ai import MilestoneAdviser
from app.redis_instance import r, USER_COOKIE_KEY
from app.main.routes import get_milestones
import json

milestoneAdviser = MilestoneAdviser()


@chat_bp.post('/get-messages')
def get_messages():
    cookie = request.cookies.get(USER_COOKIE_KEY)

    history = milestoneAdviser.get_messages(cookie)

    messages = []

    for message in history:
        if message.type == 'human':
            messages.append({"from": "You", "message": message.content, "typing": False})
        else:
            messages.append({"from": "Advisor", "message": message.content, "typing": False})
    
    resp = make_response(messages)
    resp.content_type = "application/json"
    return resp

@chat_bp.get('/adviser')
def chatbot():
    cookie = request.cookies.get(USER_COOKIE_KEY)

    if not cookie:
        resp = redirect('/')

        session['error'] = "try clicking get started"

        return resp

    try:
        response = r.get(f"{cookie}:user")
    except Exception:
        return redirect('/get-to-know-you')

    current_state = json.loads(response.decode('utf-8'))

    if not current_state['is_end']:
        return redirect('/get-to-know-you')

    milestones = get_milestones(current_state)
    name = f"{current_state['personal_info']['first_name']} {current_state['personal_info']['last_name']}"

    return render_template("chat.j2", milestones=milestones, name=name)


@chat_bp.post('/ai-response')
def ai_response():
    userInput = request.form['userInput']
    user_uuid = request.cookies.get(USER_COOKIE_KEY)

    llm_output = milestoneAdviser.query(userInput, user_uuid)

    return llm_output
