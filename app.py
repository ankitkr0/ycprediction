from flask import Flask, request, render_template, flash
import groq  # Ensure this import is correct based on how you've installed the Groq client library
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

app = Flask(__name__)

def get_prediction(name, company_name, company_intro):
    client = groq.Groq()  # Assuming Groq() is the correct way to instantiate your client
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Predict whether this company will be accepted in the next Y Combinator batch or not. Roast them while you predict though. Keep it to less than 150 words. Never ask any questions."},
            {"role": "user", "content": name},
            {"role": "user", "content": company_name},
            {"role": "user", "content": company_intro}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None
    )
    prediction = ""
    for chunk in completion:
        prediction += chunk.choices[0].delta.content or ""
    return prediction

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        company_name = request.form.get('company_name')
        company_intro = request.form.get('company_intro')
        if not (name and company_name and company_intro):
            flash("All fields are required.")
            return render_template('form.html')
        
        prediction = get_prediction(name, company_name, company_intro)
        return render_template('result.html', prediction=prediction)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)