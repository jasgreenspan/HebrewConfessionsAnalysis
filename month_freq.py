import os
import time
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from bidi.algorithm import get_display

month_names = {
    	1:'January',
		2:'February',
		3:'March',
		4:'April',
		5:'May',
		6:'June',
		7:'July',
		8:'August',
		9:'September',
		10:'October',
		11:'November',
		12:'December'		}

# Lines for writing data to file
file_lines = []

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

# Start wordcloud plot
months = list(range(1, 13))
plt.figure()

# Go over each month in the current year to get the top words
df['Date'] = pd.to_datetime(df['Date'])
current_year = 2021

for month in months:

    print("Processing Month: " + str(month))
    month_text = ' '.join(post for post in df.Text[(df['Date'].dt.year == current_year) & (df['Date'].dt.month == month)])

    file_lines += ["Month: " + str(month) + "\n"]
    wordcloud = WordCloud(colormap='tab10',  
                      max_words=15, 
                      stopwords=stopwords,
                      collocations=True,
                      background_color='white',
                      font_path="TsMatka-Bold.otf").generate_from_text(get_display(month_text))
    freq = wordcloud.words_
    file_lines += [get_display(str(a)) + "\n" for a in Counter(freq).most_common(20)]

    plt.subplot(3, 4, month).set_title(month_names[month])
    plt.plot()
    plt.imshow(wordcloud)
    plt.axis("off")


plt.show()
plt.savefig('month_wordclouds.png', bbox_inches='tight')

f = open("freq_by_month.txt", "w", encoding="utf-8")
f.writelines(file_lines)
f.close()
