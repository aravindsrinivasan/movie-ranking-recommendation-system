import os
import sys
import json
import emotion_api
import simple_recommender as srec
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

                        #send_message(sender_id, "roger that change!")
                        faceEmotions = json.loads(emotion_api.detect_emotion(attachment_link))

                        try:
                            emotion = emotion_api.get_emotion(faceEmotions[0]['scores'])

                            send_message(sender_id,"Based on our predictions, the emotion you are currently feeling is : " + str(emotion))
                            send_message(sender_id,"Let us recommend you some movies based on your current emotion and the movies you have liked on Facebook")
                            title, year, poster, homepage =srec.build_chart(emotion)
                            send_carousel(sender_id, title, year, poster, homepage);
                            return "ok", 200
                        except Exception as e:
                            send_message(sender_id,"Could not detect faces in image, please try again")
                            print(e)
                            return "ok", 200


                    '''
                                        if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]   
                        #query(message_text)
                        send_message(sender_id, "Recommending movies similiar to " + message_text)
                        recommendation = "";
                        recsList = srec.return_bestRec('Romance')
                        for recs in recsList:
                            recommendation += recs
                            recommendation += '\n'
                        send_message(sender_id,recommendation)
                        return "ok", 200'''


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


def send_carousel(recipient,titleList,yearList,imageList,webpageList):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
     params={"access_token": os.environ["PAGE_ACCESS_TOKEN"]},
     data=json.dumps({
      "recipient":{
        "id":recipient
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements":[
               {
                "title": titleList[0],
                "image_url":"https://image.tmdb.org/t/p/w500" + imageList[0],
                "subtitle":yearList[0],
                "default_action": {
                  "type": "web_url",
                  "url": webpageList[0],
                  "webview_height_ratio": "tall",
                },
                "buttons":[
                  {
                    "type":"web_url",
                    "url":webpageList[0],
                    "title":"View Website"
                  }


                ]
              },

                {
                    "title": titleList[1],
                    "image_url": "https://image.tmdb.org/t/p/w500" + imageList[1],
                    "subtitle": yearList[1],
                    "default_action": {
                        "type": "web_url",
                        "url": webpageList[1],
                        "webview_height_ratio": "tall",
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": webpageList[1],
                            "title": "View Website"
                        }

                    ]
                },
                {
                    "title": titleList[2],
                    "image_url": "https://image.tmdb.org/t/p/w500" + imageList[2],
                    "subtitle": yearList[2],
                    "default_action": {
                        "type": "web_url",
                        "url": webpageList[2],
                        "webview_height_ratio": "tall",
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": webpageList[2],
                            "title": "View Website"
                        }

                    ]
                },
                {
                    "title": titleList[3],
                    "image_url": "https://image.tmdb.org/t/p/w500" + imageList[3],
                    "subtitle": yearList[3],
                    "default_action": {
                        "type": "web_url",
                        "url": webpageList[3],
                        "webview_height_ratio": "tall",
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": webpageList[3],
                            "title": "View Website"
                        }

                    ]
                },
                {
                    "title": titleList[4],
                    "image_url": "https://image.tmdb.org/t/p/w500" + imageList[4],
                    "subtitle": yearList[4],
                    "default_action": {
                        "type": "web_url",
                        "url": webpageList[4],
                        "webview_height_ratio": "tall",
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": webpageList[4],
                            "title": "View Website"
                        }

                    ]
                }
            ]
          }
        }
      }
    }),
     headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
      print r.text

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



if __name__ == '__main__':
    app.run(debug=True)
