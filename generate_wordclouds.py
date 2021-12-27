import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from bidi.algorithm import get_display

# Define stopwords as conjuctions, prepositions, negations
# word_list = pd.read_excel(os.getcwd() + '\stopwords.xlsx')
# word_list = word_list["Undotted"][(word_list["POS"] == 'conjunction')
#                                  | (word_list["POS"] == 'preposition')
#                                  | (word_list["Reps"] > 1000)]
# stopwords = [get_display(word, upper_is_rtl=True) for word in word_list]
stopwords_file = open('heb_stopwords.txt', encoding="utf-8")
stopwords = [get_display(line[:-1], upper_is_rtl=True) for line in stopwords_file]
print(stopwords)

# Load in the dataframe
df = pd.read_csv(os.getcwd() + '\confessions_data.csv')

# Combine the text of all the posts
text = " ".join(post for post in df.Text)

# Create and generate a word cloud image:

wordcloud = WordCloud(stopwords=stopwords, font_path='C:\WINDOWS\FONTS\AHRONBD.TTF').generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()