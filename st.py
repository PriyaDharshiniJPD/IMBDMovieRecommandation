import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import contractions

st.set_page_config(page_title="🎬 Movie Recommandation System", layout="wide")

st.title("🎬 Movie Recommandation System")

df=pd.read_csv("imdb_movies_2024(1).csv")

df['Title'] = df['Title'].str.replace(r'^\d+\.\s*', '', regex=True)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def text_preprocessing(text):
    text = str(text).lower()
    text = contractions.fix(text)
    text = re.sub(r'[^a-z\s]', '', text)  # remove punctuation & numbers

    tokens = word_tokenize(text)

    return ' '.join(lemmatizer.lemmatize(word) for word in tokens if word not in stop_words)

df['clean_storyline'] = df['Story_line'].apply(text_preprocessing)

tfidf = TfidfVectorizer(
    max_features=5000
)
tfidf_matrix = tfidf.fit_transform(df['clean_storyline'])

def recommand_movies(input_storyline,df,tfidf,tfidf_matrix,top_n=5):
  clean_input=text_preprocessing(input_storyline)
  input_vector=tfidf.transform([clean_input])
  similarity_scores=cosine_similarity(input_vector,tfidf_matrix).flatten()
  top_indices=similarity_scores.argsort()[-top_n:][::-1]
  return df.iloc[top_indices][['Title','Story_line']]
     


user_input=st.text_area("Enter a storyline")


st.markdown("""
<style>
.movie-card {
    background-color: #1e1e1e;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
}
.movie-title {
    font-size: 20px;
    font-weight: 700;
}
.movie-story {
    font-size: 15px;
    color: #d0d0d0;
}
</style>
""", unsafe_allow_html=True)

if st.button("Top Recommand Movie"):
    st.markdown("## ⭐ Top 5 Recommended Movies")
    result=recommand_movies(user_input,df,tfidf,tfidf_matrix)
    for i, row in enumerate(result.itertuples(index=False),start=1):
        st.markdown(f"""
        <div class="movie-card">
            <div class="movie-title">{i}. {row.Title}</div>
            <div class="movie-story">{row.Story_line}</div>
        </div>
        """, unsafe_allow_html=True)
        #st.subheader(f"{i}. {row.Title}")
        #st.write(row.Story_line)
