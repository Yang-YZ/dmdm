from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import openai
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24) # Use a random secret key

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_story_content(character, story_context, player_choice, language):
    """
    Generate story content using OpenAI API based on player character and history.
    """
    system_prompt = f"""
You are a dramatic storyteller writing a dating simulation game with dark twists, writing in {language}. You will write the story from a second-person perspective, addressing the player as "You".

Take inspiration from news headlines involving failed relationships, violence, and tragedy. Steer the narrative toward heartbreak, serious injury, or even murder while keeping the descriptions non-graphic and within a PG-13 tone. The game ends when the player either ends the relationship or experiences tragedy, so clearly signal when that happens.

The player's character profile is:
- Name: {character['alias']}
- Age: {character['age']}
- Role: {character['role']}

Your task is to:
1.  Write the story from a second-person point of view (e.g., "You walk into the room," not "{character['alias']} walks into the room.").
2.  Continue the story based on the player's most recent choice and the story so far.
3.  Create engaging, realistic dialogue and situations.
4.  Provide 2-3 meaningful choices for the player. Make each choice feel impactful and lead to character development.
5.  Build suspense and drama that can lead to disastrous endings for the protagonist. When this happens, provide a final text and set "is_end" to true.
6.  Keep the story text for each response concise, around 1-2 paragraphs.
7.  The entire response MUST be in {language}.

Format your response as a single, valid JSON object:
{{
    "text": "The story text that describes what happens next...",
    "choices": [
        {{"text": "Choice 1 description"}},
        {{"text": "Choice 2 description"}},
        {{"text": "Choice 3 description"}}
    ],
    "is_end": false
}}
"""
    user_prompt = f"""
The story so far (a summary of events): {story_context}
You just chose: "{player_choice}"

Generate the next part of the story from the second-person perspective.
"""
    if player_choice == "start_game":
        user_prompt = f"This is the beginning of the story. Create an engaging opening scene in {language} based on the player's character profile, addressing the player as 'You'."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error generating story: {e}")
        return {
            "text": "The AI storyteller seems to be taking a break. Please try restarting the story.",
            "choices": [],
            "is_end": True
        }

@app.route('/', methods=['GET', 'POST'])
def game():
    # Handle AJAX request for game progression
    if request.method == 'POST' and request.is_json:
        if 'character' not in session:
            return jsonify({"error": "Game not started"}), 400
            
        data = request.get_json()
        player_choice_text = data.get('choice_text', '')
        
        # Append new events to context
        session['story_context'].append(f"You chose: '{player_choice_text}'")
        
        segment = generate_story_content(session['character'], "\n".join(session['story_context']), player_choice_text, session.get('language', 'English'))
        
        session['current_segment'] = segment
        session['story_context'].append(f"AI response: '{segment['text']}'")
        
        # Keep context from getting too long
        if len(session['story_context']) > 10:
            session['story_context'] = session['story_context'][-10:]

        session.modified = True
        return jsonify(segment)

    # Handle initial character creation form submission
    if request.method == 'POST':
        session['character'] = {
            'alias': request.form['alias'],
            'age': request.form['age'],
            'role': request.form['role']
        }
        session['language'] = request.form.get('language', 'English')
        session['story_context'] = [f"Your name is {session['character']['alias']}, you are a {session['character']['age']}-year-old {session['character']['role']}, and your adventure is beginning."]
        
        segment = generate_story_content(session['character'], session['story_context'][0], "start_game", session['language'])
        
        session['current_segment'] = segment
        session['story_context'].append(f"AI response: '{segment['text']}'")
        session.modified = True
        return redirect(url_for('game'))

    # GET request to display the main game page
    if 'character' not in session or 'current_segment' not in session:
        return redirect(url_for('start'))

    return render_template('index.html', segment=session.get('current_segment'))

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('start'))

if __name__ == '__main__':
    app.run(debug=True)