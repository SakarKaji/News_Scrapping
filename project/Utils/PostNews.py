# from core.db.connection import SessionLocal
# from models.content import Content as ModelContent
# from models.source import Category as ModelCategory
# from models.source import Source as ModelSource
# from models.source import Language as ModelLanguage
import html
# from sqlalchemy import func
# from fastapi import (
#     HTTPException,
#     status
# )
import json
# from core.utils.constants import Message
import requests
from Utils import Utils


# db = SessionLocal()

content_url = 'http://3.144.127.185/api/v1/bot/content'

def postnews(content:json=None):
    try:
        res = requests.post(content_url,json=content)
        print(res)
    except Exception as e:
        print(e)


