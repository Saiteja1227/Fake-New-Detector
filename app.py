import streamlit as st
import requests
from newspaper import Article
import textwrap
from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

model = load_model()

st.title("🕵️‍♂️ Fake News Detector for WhatsApp & YouTube")

url = st.text_input("Paste a news article URL or YouTube link")

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title + "\n" + article.text
    except Exception as e:
        return None

def preprocess_text(text, max_words=512):
    words = text.split()
    return " ".join(words[:max_words])

if url:
    if "youtube.com" in url or "youtu.be" in url:
        st.warning("YouTube link detected. Text extraction from YouTube is not supported in this demo.")
    else:
        st.info("Extracting content...")
        content = extract_text_from_url(url)
        if content:
            st.success("Content extracted. Analyzing...")
            with st.expander("Extracted Text"):
                st.write(textwrap.shorten(content, width=700, placeholder="..."))
            processed_content = preprocess_text(content)
            result = model(processed_content)[0]
            label = result['label']
            score = round(result['score'] * 100, 2)
            st.subheader(f"Result: **{label}**")
            st.write(f"Confidence Score: {score}%")
        else:
            st.error("Could not extract text. Please check the link.")
