import streamlit as st
import openai
import json
import os
import random
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load personality data
def load_personalities():
    with open('personalities.json', 'r') as f:
        return json.load(f)

# Initialize the app
def initialize_app():
    st.set_page_config(
        page_title="Multi-Personality AI Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Load personality data
    data = load_personalities()
    personalities = data["personalities"]
    patterns = data["patterns"]
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "personality" not in st.session_state:
        st.session_state.personality = "friendly"
    
    if "personalities" not in st.session_state:
        st.session_state.personalities = personalities
    
    if "patterns" not in st.session_state:
        st.session_state.patterns = patterns

# Check if a message matches any pattern
def match_pattern(message: str, patterns: List[Dict]) -> str:
    message_lower = message.lower()
    for pattern in patterns:
        for p in pattern["patterns"]:
            if p.lower() in message_lower:
                return pattern["tag"]
    return None

# Get a response from the pattern-based system
def get_pattern_response(tag: str, personality: Dict) -> str:
    if tag in personality["responses"]:
        return random.choice(personality["responses"][tag])
    return None

# Get response from OpenAI
def get_ai_response(messages: List[Dict], personality: Dict) -> str:
    try:
        # Prepare the message history with the system prompt
        chat_messages = [
            {"role": "system", "content": personality["system_prompt"]}
        ]
        
        # Add conversation history
        for msg in messages:
            chat_messages.append(msg)
        
        # Create a completion using the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Main app function
def main():
    initialize_app()
    
    st.title("🤖 Multi-Personality AI Chatbot")
    st.markdown("Chat with different AI personalities!")
    
    # Sidebar for personality selection
    with st.sidebar:
        st.header("Personality Settings")
        
        # Personality selector
        personality_options = {
            key: st.session_state.personalities[key]["name"] 
            for key in st.session_state.personalities.keys()
        }
        
        selected_personality = st.selectbox(
            "Choose a personality:",
            options=list(personality_options.keys()),
            format_func=lambda x: personality_options[x]
        )
        
        # Update personality if changed
        if selected_personality != st.session_state.personality:
            st.session_state.personality = selected_personality
            st.session_state.messages = []
            st.rerun()
        
        # Display current personality info
        st.subheader("Current Personality")
        personality = st.session_state.personalities[st.session_state.personality]
        st.write(f"**Name:** {personality['name']}")
        st.write(f"**Description:** {personality['system_prompt']}")
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This chatbot can respond with different personalities using both pattern matching and OpenAI's GPT model.")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Display personality greeting if no messages yet
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            st.markdown(personality["greeting"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get current personality
        personality = st.session_state.personalities[st.session_state.personality]
        
        # Check if message matches any pattern
        pattern_tag = match_pattern(prompt, st.session_state.patterns)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # First try to use pattern-based response
                if pattern_tag:
                    pattern_response = get_pattern_response(pattern_tag, personality)
                    if pattern_response:
                        st.markdown(pattern_response)
                        st.session_state.messages.append({"role": "assistant", "content": pattern_response})
                    else:
                        # Fall back to AI if no pattern response available
                        ai_response = get_ai_response(st.session_state.messages, personality)
                        st.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    # Use AI for non-pattern messages
                    ai_response = get_ai_response(st.session_state.messages, personality)
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    main()
