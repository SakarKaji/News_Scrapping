# import json
# import requests
# import logging
# import os

# content_url = os.environ.get("BACKEND_URL")
# bearer_token = os.environ.get("CONTENT_CREATE_TOKEN")


# def postnews(content: json = None):
#     headers = {
#         'Authorization': f'Bearer {bearer_token}',
#         'Content-Type': 'application/json'
#     }
#     res = requests.post(content_url, json=content, headers=headers)
#     logging.info(f"Response :: {res}")
#     return

import json
import requests
import logging
import os

# content_url = os.environ.get("BACKEND_URL")
# bearer_token = os.environ.get("CONTENT_CREATE_TOKEN")
content_url = "http://18.224.145.213:8080/qs/api/content/create/"


def postnews(content: json = None):
    headers = {
        # 'Authorization': f'Bearer {bearer_token}',
        'Authorization': 'Bearer o0u5Sy0u4LxOpjPE1TgEsFzklR9Cgt',

        'Content-Type': 'application/json'
    }
    res = requests.post("http://18.224.145.213:8080/qs/api/content/create/", json=content, headers=headers)
    logging.info(f"Response :: {res}")
    return
