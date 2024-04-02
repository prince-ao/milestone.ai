from flask import render_template, request
from app.chat import chat_bp
import time


@chat_bp.get('/adviser')
def chatbot():
    return render_template("chat.j2")


@chat_bp.post('/ai-response')
def ai_response():
    # userInput = request.form['userInput']

    time.sleep(1)
    return "<p class='hidden-response'>There are many different kinds of animals that live in China. Tigers and leopards are animals that live in China's forests in the north. In the jungles, monkeys swing in the trees and elephants walk through the brush.</p>"
