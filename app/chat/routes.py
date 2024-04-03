from flask import render_template, request, redirect, session
from app.chat import chat_bp
import time


@chat_bp.get('/adviser')
def chatbot():
    print(str(request.referrer).split('/')[-1])
    if str(request.referrer).split('/')[-1] != 'confirmation':
        resp = redirect('/')

        session['error'] = "try clicking get started"

        return resp
    return render_template("chat.j2")


@chat_bp.post('/ai-response')
def ai_response():
    userInput = request.form['userInput']

    time.sleep(1)
    return "There are many different kinds of animals that live in China. Tigers and leopards are animals that live in China's forests in the north. In the jungles, monkeys swing in the trees and elephants walk through the brush."
