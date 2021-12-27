import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from bidi.algorithm import get_display

# Define the stopwords
stopwords_file = open('heb_stopwords.txt', encoding="utf-8")
stopwords = [get_display(line[:-1]) for line in stopwords_file]

# Load in the dataframe
df = pd.read_csv(os.getcwd() + '\confessions_data.csv')

# Combine the text of all the posts
text = " ".join(post for post in df.Text)

# Clean the text from Hebrew prefixes


# Create and generate a word cloud image:
wordcloud = WordCloud(stopwords=stopwords, font_path='C:\WINDOWS\FONTS\AHRONBD.TTF').generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()