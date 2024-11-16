from flask import Blueprint, render_template, request, session, redirect
from openai import OpenAI
from app.utils import format_response
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []  # Initialize conversation history

    if request.method == 'POST':
        # Initial form submission with age, gender, etc.
        if request.form.get('age'):
            age = request.form.get('age')
            gender = request.form.get('gender')
            occasion = request.form.get('occasion')
            budget = request.form.get('budget')
            interests = request.form.get('interests')

            # Create the initial prompt for ChatGPT
            # prompt = f"Suggest a gift for a {age} year old {gender} for {occasion}. The budget is {budget}."
            prompt = f" {age} yaşındaki bir {gender} için {occasion} hediyesi öner. Bütçe {budget}TL. Cevabı 5 madde ve türkçe olarak ilet"
            
            if interests:
                #prompt += f" They are interested in {interests}."
                prompt += f" İlgi alanları: {interests}."

            # Add user input to history
            session['history'].append({"role": "user", "content": prompt})

        # Handle subsequent user inputs
        elif request.form.get('user_input'):
            user_input = request.form.get('user_input')
            session['history'].append({"role": "user", "content": user_input})

        if len(session['history']) > 10:
            session['history'] = session['history'][-10:]

        # Call ChatGPT API with the updated history
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=session['history']
        )

        assistant_response = response.choices[0].message.content
        formatted_response = format_response(assistant_response)
        # Add the assistant's response to the history
        session['history'].append({"role": "assistant", "content": formatted_response})

        if len(session['history']) > 10:
            session['history'] = session['history'][-10:]
    shown_history=session.get('history', [])
    if len(shown_history) > 1:
        shown_history= shown_history[1:]

    return render_template('index.html', history=shown_history)

@main.route('/clear', methods=['GET'])
def clear_history():
    session.pop('history', None)
    return redirect('/')
