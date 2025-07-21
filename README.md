# AI Dating Adventure Game

An interactive dating simulation game powered by AI that generates story content in real-time based on player choices.

## Features

- **Dynamic Story Generation**: Uses OpenAI GPT to create unique story paths
- **Multiple Romantic Paths**: Different characters and endings based on choices
- **Session Management**: Remembers player choices and story context
- **Fallback System**: Uses static story content if AI is unavailable

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key (it starts with `sk-`)

### 3. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 4. Run the Game

```bash
python app.py
```

### 5. Play the Game

Open your browser and go to: `http://127.0.0.1:5000`

## How It Works

1. **Static Story**: The game starts with predefined story nodes
2. **AI Generation**: When you reach a new story branch, the AI generates content
3. **Context Tracking**: The game remembers your choices to maintain story continuity
4. **Fallback**: If AI fails, it falls back to static content

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Typical game session**: ~$0.01-0.05
- **Monthly cost**: ~$1-5 for regular play

## Alternative LLM Options

### Local Options (Free)

1. **Ollama**:
   ```bash
   # Install Ollama
   # Download from https://ollama.ai/
   
   # Run a model
   ollama run llama2
   ```

2. **LM Studio**:
   - Download from https://lmstudio.ai/
   - GUI interface for local models

### Other API Options

1. **Anthropic Claude**: More expensive but excellent for creative writing
2. **Google Gemini**: Good performance, competitive pricing
3. **Hugging Face**: Many model options, some free tiers

## Customization

### Modify System Prompt

Edit the `system_prompt` in `app.py` to change the AI's behavior:

```python
system_prompt = """Your custom instructions here..."""
```

### Add More Static Content

Edit `story.py` to add more predefined story nodes.

### Change Game Theme

Modify the prompts and story context to create different types of games (mystery, fantasy, etc.).

## Troubleshooting

### "Import openai could not be resolved"
- Make sure you installed requirements: `pip install -r requirements.txt`

### "OpenAI API key not found"
- Set the environment variable correctly
- Restart your terminal after setting the variable

### "API rate limit exceeded"
- Wait a few minutes before trying again
- Consider upgrading your OpenAI plan

### Game not generating new content
- Check your internet connection
- Verify your API key is valid
- Check the console for error messages

## License

This project is for educational purposes. Please respect OpenAI's terms of service. 