from flask import render_template, request, redirect, session, make_response
from app.chat import chat_bp
from app.utils.ai import MilestoneAdviser
from app.redis_instance import USER_COOKIE_KEY

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

    return render_template("chat.j2")


@chat_bp.post('/ai-response')
def ai_response():
    userInput = request.form['userInput']
    user_uuid = request.cookies.get(USER_COOKIE_KEY)

    llm_output = milestoneAdviser.query(userInput, user_uuid)

    return llm_output
