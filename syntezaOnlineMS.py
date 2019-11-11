import os, requests, time
from xml.etree import ElementTree
import winsound

subscription_key = "a9671496f36140c494c21bb77b24b0d4"

class TTS(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)  #Valid for 10 Minutes

    def save_audio(self, textToSay):
        self.tts = textToSay
        base_url = 'https://westeurope.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'interakcja'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'pl-pl')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'pl-PL')
        voice.set('name', 'pl-PL-PaulinaRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)

        if response.status_code == 200:
            with open('sample.wav', 'wb') as audio:
                audio.write(response.content)
                #print("Sample saved")

        else:
            print("\nStatus code: " + str(response.status_code) + "Reason: " + str(response.reason))

def prepare():
    app = TTS(subscription_key)
    app.get_token()
    return app

def synth(token, text):
    token.save_audio(text)
    sample = 'sample.wav'
    winsound.PlaySound(sample, winsound.SND_FILENAME)


if __name__ == "__main__":
    a = prepare()
    synth(a, "1024")
