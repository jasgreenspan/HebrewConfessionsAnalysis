import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import datetime as dt
from PIL import Image, ImageFont
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
from bidi.algorithm import get_display

# Define the stopwords
stopwords_file = open('heb_stopwords.txt', encoding="utf-8")
stopwords = [get_display(line[:-1]) for line in stopwords_file]

# Adjust the stopwords for common words in this specific corpus
stopwords.remove('ביבא')
stopwords += ['שכ', 'ייה'] 

# Read in the posts (after segmentation process)
with open('posts_segmented.txt', 'r', encoding="utf-8") as file:
    data = file.read().replace('\n', ' ')

# Create and generate a word cloud image:
mask = np.array(Image.open('heart_mask.jpg'))
wordcloud = WordCloud(colormap='prism',  
                      max_words=40,
                      stopwords=stopwords,
                      collocations=True,
                      mask=mask,
                      font_path="TsMatka-Bold.otf")
wordcloud.generate_from_text(get_display(data))
# freq = wordcloud.process_text(get_display(data))
# print(dict(Counter(freq).most_common(5)))

# Save the generated image:
fig = plt.figure(figsize=(10,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
fig.savefig('wordcloud.png')