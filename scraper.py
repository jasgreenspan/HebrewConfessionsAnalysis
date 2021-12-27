import re
import os
import pandas as pd
from facebook_scraper import get_posts
from bidi.algorithm import get_display

# Prepare dataset categories
dates = []
likes = []
comments = []
texts = []
ids = []

for post in get_posts('ReligiousLGBTQconfessions', pages=10):
    post_text = post['text']

    # Take post id number (and only store posts with id)
    id_match = re.match("#[0-9]*", post_text)
    if id_match:
        ids += [id_match.group()]
        post_text = post_text[id_match.end():]

        # Reverse text order from Hebrew
        post_text = get_display(post_text, upper_is_rtl=True)
        texts += [post_text]
        
        # Collect important metadata from post
        dates += [post['time']]
        likes += [post['likes']]
        comments += [post['comments']]

# Save the dataframe    
data = {'Date': dates, 'Likes': likes, 'Comments': comments, 'Text': texts}
df = pd.DataFrame(data, index = ids)
print(df)
df.to_csv(os.getcwd() + '/confessions_data.csv')