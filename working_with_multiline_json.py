import pandas as pd
from pandas.io.json import json_normalize
import json
import datetime
import nltk

# Several fields of the original file have nested jsons, so we can't use pandas' built in 'read_json' and instead need to use 'json_normalize'
# As the original file has multiple separate json lines, we need to read them line by line
with open('nlp_exp/datasets/nyt2.json', encoding='utf-8') as data_file:
    data = [json.loads(line) for line in data_file]

books_data = json_normalize(data)

# After inspecting the DataFrame, it turns out the 'price' field was written either as numberDouble or numberInt
# So we need to fill the missing values from one of the columns and then get rid of the extra one
books_data['price.$numberDouble'].fillna(books_data['price.$numberInt'], inplace=True)
books_data.drop(['price.$numberInt'], axis=1, inplace=True)
books_data.columns = ['id', 'amazon_url', 'author', 'bestsellers_date', 'description', 'price', 'published_date', 'publisher', 'rank', 'rank_previous', 'title', 'weeks_on_list']

# Next, both published date and bestsellers date are written as numberLong in original dataset, so  we need to convert that
# Moreover, we don't really need the full date, so we will be extracting just the year
books_data['bestsellers_date'] = books_data['bestsellers_date'].astype('int64')
books_data['bestsellers_date'] = books_data['bestsellers_date'] / 1e3
books_data['bestsellers_date'] = books_data['bestsellers_date'].apply(datetime.datetime.fromtimestamp)
books_data['bestsellers_date'] = books_data['bestsellers_date'].map(lambda x: x.year)

books_data['published_date'] = books_data['published_date'].astype('int64')
books_data['published_date'] = books_data['published_date'] / 1e3
books_data['published_date'] = books_data['published_date'].apply(datetime.datetime.fromtimestamp)
books_data['published_date'] = books_data['published_date'].map(lambda x: x.year)

# After the Data has been successfuly loaded in and preprocessed, we can start analyzing the description
# For that, we shall be using the NLTK library
tokens = nltk.word_tokenize(books_data['description'])

print(tokens)