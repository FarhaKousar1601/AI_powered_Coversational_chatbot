# Rule-Based Chatbot

A personality-based chatbot that doesn't require any external API. It uses pattern matching and predefined responses.

## Features

- Multiple AI personalities (Friendly, Professional, Sarcastic)
- Pattern-based responses for common queries
- Contextual responses for weather, time, and jokes
- No API required - completely self-contained
- Streamlit web interface

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run chatbot.py`

## Deployment

1. Create a GitHub repository with all files
2. Sign up for Streamlit Community Cloud
3. Connect your GitHub repository
4. Deploy your app (no API keys needed!)

## How It Works

This chatbot uses a rule-based system with:
1. Pattern matching for common phrases
2. Personality-specific responses
3. Contextual responses for certain topics
4. Random selection from multiple response options

## File Structure

- `chatbot.py` - Main application code
- `personalities.json` - Personality definitions and pattern responses
- `requirements.txt` - Python dependencies
