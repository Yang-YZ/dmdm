from flask import Flask, render_template, request, session, redirect
from story import story
import openai
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random string

# Initialize OpenAI client
# Set your OpenAI API key here
openai.api_key = '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'

def generate_story_content(current_node, player_choice, story_context):
    """
    Generate story content using OpenAI API
    """
    try:
        system_prompt = """You are a creative storyteller writing a dating simulation game. The player is Sarah, a 22-year-old college student. 

Your task is to:
1. Continue the story based on the player's choice
2. Create engaging, realistic dialogue and situations
3. Provide 2-3 meaningful choices that lead to different outcomes
4. Keep the tone light, romantic, and appropriate for a dating game
5. Make each choice feel impactful and lead to character development

Format your response as JSON:
{
    "text": "The story text that describes what happens next...",
    "choices": [
        {"text": "Choice 1 description", "next_node": "unique_node_name_1"},
        {"text": "Choice 2 description", "next_node": "unique_node_name_2"},
        {"text": "Choice 3 description", "next_node": "unique_node_name_3"}
    ]
}"""

        user_prompt = f"""
Current story context: {story_context}
Current situation: {current_node}
Player's choice: {player_choice}

Continue the story from here, considering the player's choice and the overall context.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "text": content,
                "choices": [
                    {"text": "Continue", "next_node": "continue"},
                    {"text": "Go back", "next_node": "start"}
                ]
            }
            
    except Exception as e:
        print(f"Error generating story: {e}")
        # Fallback to static story
        return story.get(current_node, story['start'])

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize session if needed
    if 'story_context' not in session:
        session['story_context'] = "Sarah is a 22-year-old college student going to a party."
    
    current_node = 'start'
    if request.method == 'POST':
        current_node = request.form.get('next_node', 'start')
        player_choice = request.form.get('choice_text', '')
        
        # Update story context
        session['story_context'] += f" Sarah chose: {player_choice}. "
        
        # Check if we have a static story node
        if current_node in story:
            segment = story[current_node]
        else:
            # Generate dynamic content
            segment = generate_story_content(current_node, player_choice, session['story_context'])
            # Store generated content in session for consistency
            session['generated_nodes'] = session.get('generated_nodes', {})
            session['generated_nodes'][current_node] = segment
    else:
        # GET request - start fresh
        session['story_context'] = "Sarah is a 22-year-old college student going to a party."
        session['generated_nodes'] = {}
        segment = story[current_node]
    
    return render_template('index.html', segment=segment, current_node=current_node)

@app.route('/restart', methods=['POST'])
def restart():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True) 