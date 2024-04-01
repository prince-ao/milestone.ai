from flask import render_template
from app.chat import chat_bp


@chat_bp.get('/chat')
def confirmation():
    return render_template("chat.j2")
