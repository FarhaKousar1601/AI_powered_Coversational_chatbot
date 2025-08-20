from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("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"))

# Test the API
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Write a haiku about AI"}],
        max_tokens=50
    )
    print("API Connection Successful!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print(f"API Connection Failed: {e}")
