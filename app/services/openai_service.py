from openai import OpenAI
from flask import current_app
import random


# Fallback random texts
random_texts = [
    "I'm here to help! What can I do for you today?",
    "It looks like I can't reach OpenAI right now, but I'm still here to assist!",
    "Let's keep things rolling! What would you like to ask?",
    "Something seems off, but I’m still ready to chat!",
    "I may not have AI superpowers right now, but I can still try my best!",
    "Having a bit of trouble reaching OpenAI—how else can I assist?",
    "Technical hiccups happen, but I'm still here for you!",
    "Looks like my brain isn't fully online—ask me anyway!",
]


def generate_openai_response(prompt):
    openai_api_key = current_app.config.get('OPENAI_API_KEY')

    if openai_api_key:
        client = OpenAI(api_key=openai_api_key)

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Customer support assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        return completion.choices[0].message.content

    return random.choice(random_texts)
