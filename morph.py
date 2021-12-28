import os
import time
import pandas as pd
import datetime as dt
from bidi.algorithm import get_display
import requests
		
def get_segmented_text_yap(text):
    """
    Taken from https://www.langndata.com/heb_parser/api_reference
    """
    # Escape double quotes in JSON.
    text = text.replace(r'"', r'\"')
    url = 'https://www.langndata.com/api/heb_parser?token=%s' % api-token
    _json ='{"data":"'+text+'"}'    	 
    headers = {'content-type': 'application/json'}
    r = requests.post(url,  data=_json.encode('utf-8'), headers={'Content-type': 'application/json; charset=utf-8'}, timeout=5)
    
    return r.json()['segmented_text']


if __name__ == "__main__":
    # Load in the dataframe
    df = pd.read_csv(os.getcwd() + '\confessions_data.csv')

    # Combine the text of all the posts from the current year
    df['Date'] = pd.to_datetime(df['Date'])
    current_year = 2021
    text = ' '.join(get_display(post) for post in df.Text[df['Date'].dt.year == current_year])
    text = text.split()

    # Clean the text from Hebrew prefixes
    # YAP queries are max 250 words
    n = 100
    text_chunks = [' '.join(text[i:i + n]) for i in range(0, len(text), n)]
    segmented_text = ''
    for chunk in text_chunks:
        segmented_chunk = get_segmented_text_yap(chunk)
        time.sleep(3)
        segmented_text += segmented_chunk
    
    # Correct the Hebrew word for LGBT that was separated
    segmented_text.replace(get_display('להט ב'), get_display('להטב'))

    text_file = open("posts_segmented.txt", "w", encoding='utf8')
    text_file.write(segmented_text)
    text_file.close()