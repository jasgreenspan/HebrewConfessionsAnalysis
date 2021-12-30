import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import datetime as dt
from PIL import Image, ImageFont
from wordcloud import WordCloud, ImageColorGenerator
from bidi.algorithm import get_display

# Define the stopwords
stopwords_file = open('heb_stopwords.txt', encoding="utf-8")
stopwords = [get_display(line[:-1]) for line in stopwords_file]

# Adjust the stopwords for common words in this specific corpus
stopwords.remove('ביבא')
stopwords += ['שכ', 'ייה'] 

# Load in the dataframe
df = pd.read_csv(os.getcwd() + '\posts_segmented.csv')

# Filter empty posts
df['Text'] = df['Text'].fillna("")

# Combine the text of all the posts from the current year
df['Date'] = pd.to_datetime(df['Date'])
current_year = 2021
text = " ".join([post for post in df['Text'][df['Date'].dt.year == current_year]])

# Create and generate a word cloud image:
mask = np.array(Image.open('pride_flag.jpg'))
image_colors = ImageColorGenerator(mask)
wordcloud = WordCloud(color_func=image_colors,  
                      max_words=50, 
                      stopwords=stopwords,
                      collocations=True,
                      background_color='white',
                      mask=mask,
                      font_path="TsMatka-Bold.otf")
wordcloud.generate_from_text(get_display(text))

# Save the generated image:
wordcloud.to_file('wordcloud.png')