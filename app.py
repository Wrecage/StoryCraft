from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

#Groq API key
api_key = ''
client = Groq(api_key=api_key)

def generate_story(characters, setting, plot_twist):
    prompt = (
        f"Create a short story with the following elements:\n"
        f"Characters: {characters}\n"
        f"Setting: {setting}\n"
        f"Plot Twist: {plot_twist}\n"
    )
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192"
        )
        story = response.choices[0].message.content.strip()
        return story
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    characters = data.get('characters')
    setting = data.get('setting')
    plot_twist = data.get('plot_twist')
    
    story = generate_story(characters, setting, plot_twist)
    return jsonify({'story': story})

if __name__ == '__main__':
    app.run(debug=True)
