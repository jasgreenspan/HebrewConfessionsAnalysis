import os
import time
import pandas as pd
import datetime as dt
from bidi.algorithm import get_display
from dotenv import load_dotenv
import requests
		
def get_segmented_text_yap(text, timeout_time):
    """
    Taken from https://www.langndata.com/heb_parser/api_reference
    """
    load_dotenv()
    token = os.environ.get("api-token")

    # Escape double quotes in JSON.
    text = text.replace(r'"', r'\"')
    url = 'https://www.langndata.com/api/heb_parser?token=%s' % token
    _json ='{"data":"'+text+'"}'    	 
    headers = {'content-type': 'application/json'}
    r = requests.post(url,  data=_json.encode('utf-8'), headers={'Content-type': 'application/json; charset=utf-8'}, timeout=timeout_time)
    
    if 'segmented_text' in r.json():
        return r.json()['segmented_text']
    elif 'msg' in r.json() and r.json()['msg'] == "There is no hebrew characters in your text":
        return 'NO HEBREW'
    else:
        return ''

def segment_text(text):
    # Clean the text from Hebrew prefixes
    # YAP queries are max 250 words
    n = 150
    text = text.split()
    text_chunks = [' '.join(text[i:i + n]) for  i in range(0, len(text), n)]
    segmented_text = ''
    prev_chunk = ''
    for chunk in text_chunks:
        timeout_time = 5
        segmented_chunk = get_segmented_text_yap(get_display(chunk), timeout_time)
        while segmented_chunk == '' or segmented_chunk == prev_chunk:
            print("Timeout time: " + str(timeout_time))
            time.sleep(timeout_time) # Wait for the timeout time
            timeout_time += 1
            segmented_chunk = get_segmented_text_yap(get_display(chunk), timeout_time)
        
        if segmented_chunk == "NO HEBREW": # For posts writen not in Hebrew
            continue

        print(get_display(segmented_chunk))
        prev_chunk = segmented_chunk
        
        segmented_text += segmented_chunk + " "
    
    # Correct the Hebrew words that are processed incorrectly
    segmented_text.replace(get_display('להט ב'), get_display('להטב'))
    segmented_text.replace(get_display('ל היות'), get_display('להיות'))

    return segmented_text


if __name__ == "__main__":
    # Load in the dataframe
    df = pd.read_csv(os.getcwd() + '\confessions_data.csv')

    # Filter empty posts
    df['Text'] = df['Text'].fillna("")

    # TODO: remove punctuation characters (creates spacing issue with YAP)
    
    # Go over all of the posts and parse them using YAP
    for index, row in df.iterrows():
        post = row['Text']
        segmented_post = segment_text(post)
        df.at[index, 'Text'] = segmented_post

    df.to_csv(os.getcwd() + '/posts_segmented.csv')