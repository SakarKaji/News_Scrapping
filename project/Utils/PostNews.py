import json
import requests
from .Utils import *
import pandas as pd
import logging
import os

content_url = 'http://3.144.127.185/api/v1/bot/content'

def postnews(content:json=None, error:str = None):
    source_name = content['source_name']

    if content is None :
        status = "Error"
        log = f"Error received in {source_name} while scrapping beacause of {error}."

    header = content['title']
    content_description = content['content_description']
    published_date = content['published_date']
    category = content['category_name']

    if (content_description is None) or (validate_date(published_date) is None):
        logging.error(f"invalid data {content} for {source_name}")
        status = 'Error'
        log = f"invalid data {content}"
        return False
    

    res = requests.post(content_url, json=content)
    return_text = res.json().get('detail', '')
    if return_text == "Duplicate object":
        logging.error(f"duplicate {header} for {source_name}")
        status = "Duplicate"
        log = f"duplicate {header}"

    if res.status_code == 200:
        logging.info(f"news post success for {source_name} with title {header}")
        status = "Success"
        log = f"news post success for title {header}"

    log_data = {
            'source': [source_name], 
            'category': [category], 
            'status':[status] ,
            'log': [log]
            }
    df = pd.DataFrame(log_data)

    file_path = get_report_file_path()
    print(file_path)

    if not os.path.isfile(file_path):
        df.to_csv(file_path, mode='w', index=False, header=True)
    else:
        df.to_csv(file_path, mode='a', index=False, header=False)





