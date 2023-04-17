import streamlit as st
import numpy as np
import re
import pandas as pd
import nltk
nltk.download('all')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load data
news_df = pd.read_csv('train.csv')
news_df = news_df.fillna(' ')
news_df['content'] = news_df['author'] + ' ' + news_df['title']
X = news_df.drop('label', axis=1)
y = news_df['label']

# Define stemming function
ps = PorterStemmer()


def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [ps.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content


# Apply stemming function to content column
news_df['content'] = news_df['content'].apply(stemming)

# Vectorize data
X = news_df['content'].values
y = news_df['label'].values
vector = TfidfVectorizer()
vector.fit(X)
X = vector.transform(X)

# Split data into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

# Fit logistic regression model
model = LogisticRegression()
model.fit(X_train, Y_train)

import streamlit as st
from streamlit_option_menu import option_menu

# horizontal menu
selected = option_menu(
    menu_title=None,  # required
    options=["Home", "Fake News Detection", "Information"],  # required
    icons=["house", "caret-down-square-fill", "book"],  # optional
    menu_icon=" cast ",  # optional
    default_index=1,  # optional
    orientation="horizontal",
    styles={
        "container": {"padding": "1!important", "background-color"
                                                "icon": {"color": "orange", "font-size": "25px"},

                      "nav-link": {
                          "font-size": "25px",
                          "text-align": "left",
                          "margin": "0px",
                          "==hover-color": "#eee",
                      },
                      "nav-link-selected": {"background-color": "green"},

                      },
    }

)


st.subheader("OUR BATTLE AGAINST FAKE NEWS")
st.write(
    "The aim of the fake news project is to help news readers to identify bias and misinformation in news articles in "
    "a quick and reliable fashion."
    "We have collected news articles with veracity labels from fact-checking websites and used them to train text "
    "classification systems to detect fake from real news."
    "You can paste a piece of text and examine its similarity to our collection of true vs. false news articles. "
    "Enjoy Testing! ")

st.markdown("<h1 style='text-align: center; color: black;'>FAKE NEWS DETECTOR</h1>", unsafe_allow_html=True)
input_text = st.text_input('Enter news Article')


def prediction(input_text):
    input_data = vector.transform([input_text])
    prediction = model.predict(input_data)
    return prediction[0]


if input_text:
    pred = prediction(input_text)
    if pred == 1:
        st.write('The News is Fake')
    else:
        st.write('The News Is Real')
