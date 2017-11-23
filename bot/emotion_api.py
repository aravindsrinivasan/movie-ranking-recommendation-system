
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