import requests
import pandas as pd
from io import BytesIO
from .config import base_url, token

def get(url):
    return requests.get(url, headers={'Authorization':token}, verify=False)

def get_all_items():
    return get(f"{base_url}/items").json()

def get_item(item_id):
    return get(f"{base_url}/items/{item_id}").json()

def get_upload(upload_id):
    return get(f"{base_url}/uploads/{upload_id}")


def get_available_data():
    netzsch_items_with_attachments = []
    for item in get_all_items():
        if item['category'] == 'Netzsch':
            print(item['title'])

            if item['has_attachment']:
                netzsch_items_with_attachments.append(item['id'])
    return netzsch_items_with_attachments


def get_data()
netzsch = []
for item_id in netzsch_items_with_attachments:
    details = get_item(item_id)

    for upload in details['uploads']:
        if upload['real_name'].endswith('.xlsx'):
            obj = get_upload(upload['id'])
            df = pd.read_excel(BytesIO(obj.content))
            netzsch.append(df)
            print(df.head())

