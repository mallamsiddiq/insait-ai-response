from openai import OpenAI
from flask import current_app
import random


# Fallback random texts
random_texts = [
    "Randomly generated text 1",
    "Randomly generated text 2",
    "Randomly generated text 3",
    "Randomly generated text 4",
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
