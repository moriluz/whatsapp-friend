import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
        # model="text-davinci-003",
        # prompt=prompt,
        # temperature=0.7,
        # max_tokens=256,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0
    )
    print(response)
    return response.choices[0].message['content']


def generate_dalle_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=2,
        size="1024x1024",
    )
    return response['data'][0]['url']

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").lower()
    chatgpt_response = generate_chatgpt_response(incoming_msg)

    resp = MessagingResponse()
    if "art" in incoming_msg:
        image_url = generate_dalle_image(chatgpt_response)
        resp.message("").media(image_url)
    else:
        resp.message(chatgpt_response)

    print("res ", resp)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
