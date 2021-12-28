import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from bidi.algorithm import get_display
from morph import get_segmented_text_yap

# def prefix_separator(data):
#     valid_prefixes = 'כשמלוהב'
#     words = list(data.split(" "))
#     edited_words = words

#     for i, word1 in enumerate(words):
#         # Look at words that begin with a prefix
#         prefix1 = word1[-1]
#         if prefix1 in valid_prefixes:
#             # Split word from prefix if another word exists without it in the list
#             for word2 in words:
#                 prefix2 = word2[-1]
#                 if word2 == word1[:-1]:
#                     edited_words[i] = prefix1 + ' ' + word2
#                 elif prefix1 != prefix2 and prefix2 in valid_prefixes and word2[:-1] == word1[:-1]:
#                     edited_words[i] = prefix1 + ' ' + word2[:-1]

#     return edited_words

# Define the stopwords
stopwords_file = open('heb_stopwords.txt', encoding="utf-8")
stopwords = [get_display(line[:-1]) for line in stopwords_file]

# Load in the dataframe
df = pd.read_csv(os.getcwd() + '\confessions_data.csv')

# Combine the text of all the posts
text = ' '.join(get_display(post) for post in df.Text)
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

# Create and generate a word cloud image:
wordcloud = WordCloud(stopwords=stopwords, font_path='C:\WINDOWS\FONTS\AHRONBD.TTF').generate(get_display(segmented_text))

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()