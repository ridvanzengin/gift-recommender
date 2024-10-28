from flask import Blueprint, render_template, request
from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    suggestion = ''
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        occasion = request.form.get('occasion')
        budget = request.form.get('budget')
        interests = request.form.get('interests')
        # Create prompt for ChatGPT
        prompt = f"Suggest a gift for a {age} year old {gender} for {occasion}. The budget is {budget}"
        if interests:
            prompt += f" who likes {interests}"
        print(prompt)
        # Call ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        suggestion = response.choices[0].message.content

    return render_template('index.html', suggestion=suggestion)

