# https://scontent.xx.fbcdn.net/v/t35.0-12/23897059_1592951714095199_1230073467_o.jpg?_nc_ad=z-m&_nc_cid=0&oh=c0b4b2c0545111278ffb4f4b6f689135&oe=5A19EA20

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
body = "{ 'url': 'https://scontent.xx.fbcdn.net/v/t35.0-12/23897059_1592951714095199_1230073467_o.jpg?_nc_ad=z-m&_nc_cid=0&oh=c0b4b2c0545111278ffb4f4b6f689135&oe=5A19EA20'}"

try:
    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
    #   URL below with "westcentralus".
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)

    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    print(e)
