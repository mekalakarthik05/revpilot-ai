import os
from openai import OpenAI

client = None

def get_client():
    global client
    if client:
        return client
    try:
        client = OpenAI(api_key=os.getenv("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"))
        return client
    except:
        return None


def ask_llm(prompt):
    client = get_client()
    if not client:
        return None

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return res.choices[0].message.content
    except:
        return None