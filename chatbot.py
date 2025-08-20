import streamlit as st
import json
import random
import datetime
from typing import Dict, List, Any

# Load personality data
def load_personalities():
    with open('personalities.json', 'r') as f:
        return json.load(f)

# Initialize the app
def initialize_app():
    st.set_page_config(
        page_title="Rule-Based Chatbot",
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

# Get a contextual response based on message content
def get_contextual_response(message: str, personality: Dict) -> str:
    message_lower = message.lower()
    
    # Check for specific contextual patterns
    if any(word in message_lower for word in ["weather", "rain", "sun", "temperature"]):
        if personality["name"] == "Sarcastic Assistant":
            return "Oh, you want a weather report? Sorry, I left my meteorology degree in my other server."
        elif personality["name"] == "Professional Assistant":
            return "I do not have access to real-time weather data. You might consult a dedicated weather service."
        else:
            return "I'm not connected to weather services, but I hope it's nice where you are!"
    
    elif any(word in message_lower for word in ["time", "date", "day", "year"]):
        now = datetime.datetime.now()
        if personality["name"] == "Sarcastic Assistant":
            return f"It's {now.strftime('%H:%M')}. Do you have somewhere better to be?"
        elif personality["name"] == "Professional Assistant":
            return f"The current time is {now.strftime('%H:%M on %A, %B %d, %Y')}."
        else:
            return f"It's currently {now.strftime('%H:%M')} on this lovely day!"
    
    elif any(word in message_lower for word in ["joke", "funny", "laugh"]):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why couldn't the bicycle stand up by itself? It was two tired!",
            "What do you call a bear with no teeth? A gummy bear!"
        ]
        return random.choice(jokes)
    
    # Default response based on personality
    return personality["responses"]["default"][0]

# Main app function
def main():
    initialize_app()
    
    st.title("🤖 Rule-Based Chatbot")
    st.markdown("Chat with different AI personalities - no API required!")
    
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
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This is a rule-based chatbot that doesn't require any API. It uses pattern matching and predefined responses.")
        st.markdown("**Available Personalities:**")
        for key, value in st.session_state.personalities.items():
            st.markdown(f"- {value['name']}")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Display personality greeting if no messages yet
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            personality = st.session_state.personalities[st.session_state.personality]
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
                        # Fall back to contextual response if no pattern response available
                        contextual_response = get_contextual_response(prompt, personality)
                        st.markdown(contextual_response)
                        st.session_state.messages.append({"role": "assistant", "content": contextual_response})
                else:
                    # Use contextual response for non-pattern messages
                    contextual_response = get_contextual_response(prompt, personality)
                    st.markdown(contextual_response)
                    st.session_state.messages.append({"role": "assistant", "content": contextual_response})

if __name__ == "__main__":
    main()
