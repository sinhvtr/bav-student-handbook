import streamlit as st 
from rank_bm25 import BM25Okapi
import json

with open('sotay.json', 'r', encoding='utf8') as fr:
    data = json.load(fr)
corpus = []
for article in data:
    for paragraph in article['article_paragraphs']:
        corpus.append(paragraph['paragraph_text'])

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

st.title("Hệ thống tra cứu quy chế sinh viên Học viện Ngân hàng")
st.text("Dựa trên nội dung phần II cuốn Sổ tay sinh viên năm 2017")

form = st.form(key='my_form')
text_input = form.text_input(label='Viết câu hỏi của bạn')
submit_button = form.form_submit_button(label='Tra cứu')
if submit_button:
    tokenized_query = text_input.split(" ")
    doc_scores = bm25.get_scores(tokenized_query).tolist()
    doc_scores = sorted(doc_scores, reverse=True)
    top_n = bm25.get_top_n(tokenized_query, corpus, n=3)

    st.markdown('**{}**'.format(top_n[0]))
    st.markdown('*Một số kết quả khác:*')
    for result in top_n[1:]:
        st.write(result)
