import json
import requests
import logging
import os

content_url = os.environ.get("BACKEND_URL")
bearer_token = os.environ.get("CONTENT_CREATE_TOKEN")


def postnews(content: json = None):
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    res = requests.post(content_url, json=content, headers=headers)
    logging.info(f"Response :: {res}")
    return
