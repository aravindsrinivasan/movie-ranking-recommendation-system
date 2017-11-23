import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)

api_key = "dd37c8b977664bf39fccb3f4b7569f78"

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = ""
                    message_image_url = ""
                    attachment_link = "not an image"

                    if messaging_event["message"].get("attachments"):
                        attachment_link = messaging_event["message"]["attachments"][0]["payload"]["url"]
                    print("Image received, boss!")
                    print(attachment_link)

                    send_message(sender_id, "roger that change!")
                    faceEmotions = json.loads(detect_emotion(attachment_link))

                    emotion = get_emotion(faceEmotions[0]['scores'])

                    send_message(sender_id,str(emotion))


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()

def detect_emotion(imgURL):
    ########### Python 2.7 #############
    import httplib, urllib, base64

    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'dd37c8b977664bf39fccb3f4b7569f78',
    }

    params = urllib.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    body = "{ 'url': " + "'" + imgURL + "'" + "}"

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
        #   URL below with "westcentralus".
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def get_emotion(emotions):
    """
    Finds the emotion that has the max score
    :param emotions: dictionary that contains the emotions
    and their scores
    :return maxEmotion: the emotion that has the highest match
    """
    maxScore = 0
    maxEmotion = None
    # Loop through the emotions to find the highest match
    for key in emotions.keys():
        if (maxScore < emotions[key]):
            maxScore = emotions[key]
            maxEmotion = key
    return maxEmotion

if __name__ == '__main__':
    app.run(debug=True)
