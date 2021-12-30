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