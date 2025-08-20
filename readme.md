

A conversational chatbot with multiple personalities built with Streamlit and OpenAI's GPT model.

## Features

- Multiple AI personalities (Friendly, Professional, Sarcastic)
- Pattern-based responses for common queries
- OpenAI GPT integration for complex conversations
- Streamlit web interface

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your OpenAI API key: `OPENAI_API_KEY=your_key_here`
4. Run the app: `streamlit run chatbot.py`

## Deployment

1. Create a GitHub repository with all files
2. Sign up for Streamlit Community Cloud
3. Connect your GitHub repository
4. Set the OPENAI_API_KEY as a secret in Streamlit Cloud settings
5. Deploy your app

## File Structure

- `chatbot.py` - Main application code
- `personalities.json` - Personality definitions and pattern responses
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not included in git)
