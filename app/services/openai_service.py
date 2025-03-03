# app/openai_service.py

from openai import ChatCompletion
from app.config import Config

# openai.api_key = Config.OPENAI_API_KEY


def generate_openai_response(prompt):
    

    completion = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Customer supoport assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    return completion.choices[0].message.content






