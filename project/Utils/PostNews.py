import json
import requests
from Utils import Utils

content_url = 'http://3.144.127.185/api/v1/bot/content'

def postnews(content:json=None):
    try:
        print(content)
        res = requests.post(content_url,json=content)
       
    except Exception as e:
        print(e)


