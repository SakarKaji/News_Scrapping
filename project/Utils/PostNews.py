import json
import requests
from .Utils import *
import pandas as pd
import logging
import os
from news.id_mapping import id_for

# content_url = 'http://3.16.15.203/api/v1/bot/content'


# def postnews(content: json = None, error: str = None):
#     source_name = content['source_name']

#     if content is None:
#         status = "Error"
#         log = f"Error received in {source_name} while scrapping beacause of {error}."

#     else:
#         header = content['title']
#         content_description = content['content_description']
#         published_date = content['published_date']
#         category = content['category_name']

#         print(header, content_description, published_date, category)

#         if (content_description is None or published_date is None):
#             logging.error(f"invalid data {content} for {source_name}")
#             status = 'Error'
#             log = f"invalid data {content}"
#             return False

#         print(f"URL :: {content_url}, Content :: {content}")

#         res = requests.post(content_url, json=content)
#         print(f"Response :: {res}")

#         return_text = res.json().get('detail', '')

#         if return_text == "Duplicate object":
#             logging.error(f"duplicate {header} for {source_name}")
#             status = "Duplicate"
#             log = f"duplicate {header}"

#         elif res.status_code == 200:
#             logging.info(
#                 f"news post success for {source_name} with title {header}")
#             status = "Success"
#             log = f"news post success for title {header}"

#         elif res.status_code == 400:
#             logging.info(
#                 f"news post failure for {source_name} with title {header}")
#             status = "Faliure"
#             log = f"news post faliure for title {header}"

#         else:
#             logging.info(
#                 f"news post  for {source_name} with title {header}")
#             status = "Unknown"
#             log = f"news post unknown for title {header}"

#     log_data = {
#         'source': [source_name] or [None],
#         'category': [category] or [None],
#         'status': [status] or [None],
#         'log': [log] or [None]
#     }
#     df = pd.DataFrame(log_data)

#     file_path = get_report_file_path()

#     if not file_path:
#         return

#     if not os.path.isfile(file_path):
#         df.to_csv(file_path, mode='w', index=False, header=True)

#     else:
#         df.to_csv(file_path, mode='a', index=False, header=False)


content_url = os.environ.get("BACKEND_URL")
# bearer_token = os.environ.get("ACCESS_TOKEN")


def postnews(content: json = None):
    headers = {
        # 'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    # res = requests.post(content_url,json=content,headers=headers)

    # logging.info(f"Response :: {res}")


    if content["source"] in ["ictsamachar"]:
        news = {
                'title': content["title"],
                'content_description': content["content_description"],
                'published_date': content["published_date"],
                'image_url': content["image_url"],
                'url': content["url"],
                'category_name': content["category"],
                'is_recent': content["is_recent"],
                'source_id': id_for[content["source"]],
                'is_trending': True
                }
        logging.info(f"Production news :: {news}")
        if news["content_description"]:
            res = requests.post(url="http://3.13.147.29/api/v1/bot/content",
                json=news,
                headers=headers)
            logging.info(f"Response :: {res}")
    return

def postnews_server(content: json = None):
    headers = {
        # 'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    res = requests.post("http://3.13.147.29/api/v1/bot/content",
                        json=content,
                        headers=headers)
    logging.info(f"Response :: {res}")
    return
