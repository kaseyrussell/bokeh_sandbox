import requests
import pandas as pd
from io import BytesIO
# from .config import base_url, token
token = 'f0792d99ada3e4328a515b78514b37321b343d048a372d4ce31189b1a309c8dba0e27aad6aa02f96f9c2'
base_url = 'https://localhost/api/v1'

def get(url):
    return requests.get(url, headers={'Authorization':token}, verify=False)

def get_all_items():
    return get(f"{base_url}/items").json()

def get_item(item_id):
    return get(f"{base_url}/items/{item_id}").json()

def get_upload(upload_id):
    return get(f"{base_url}/uploads/{upload_id}")


def get_netzsch_items_with_excel_files():
    """
    Retrieve a list of Netzsch items with attachments
    :return:
    """
    netzsch_items_with_attachments = []
    for item in get_all_items():
        if item['category'] == 'Netzsch':
            print(item['title'])

            if item['has_attachment']:
                details = get_item(item['id'])

                for upload in details['uploads']:
                    if upload['real_name'].endswith('.xlsx'):
                        if 'excel_id' in item:
                            item['excel_ids'].append(upload['id'])
                            item['excel_names'].append(upload['real_name'])
                        else:
                            item['excel_ids'] = [upload['id']]
                            item['excel_names'] = [upload['real_name']]

                netzsch_items_with_attachments.append(item)
    return netzsch_items_with_attachments


def get_dataframes(selected_items):
    """
    For the items selected, retrieve uploads and parse
    :param selected_items:
    :return:
    """
    netzsch = []
    for item in selected_items:
        for upload_id in item['excel_ids']:
            obj = get_upload(upload_id)
            df = pd.read_excel(BytesIO(obj.content))
            netzsch.append(df)
            print(df.head())

    return netzsch




if __name__ == '__main__':
    all_data = get_netzsch_items_with_excel_files()
    netzsch_files = get_dataframes(all_data)

