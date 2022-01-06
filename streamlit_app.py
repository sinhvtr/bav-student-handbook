import streamlit as st 
from rank_bm25 import BM25Okapi
import json
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

NUM_DOCS = 5

with open('sotay.json', 'r', encoding='utf8') as fr:
    data = json.load(fr)
corpus = []
meta = [(0, 0)]
count = 0
for article in data:
    corpus.append(article['article_text'])
    count = count + 1
    for paragraph in article['article_paragraphs']:
        corpus.append(paragraph['paragraph_text'])
        count = count + 1
    meta.append((article['article_id'], count))
tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)
tfidf_vectorizer = TfidfVectorizer()
tfidf_corpus = tfidf_vectorizer.fit_transform(corpus)

st.title("Hệ thống tra cứu quy chế sinh viên Học viện Ngân hàng")
st.text("Dựa trên nội dung cuốn Sổ tay sinh viên năm 2017")

form = st.form(key='my-form')
text_input = form.text_input(label='Viết câu hỏi của bạn')
search_type = form.radio('Kiểu tìm kiếm', ('TFIDF', 'BM25'))
submit = form.form_submit_button('Tìm kiếm')
if submit:
    if search_type == 'BM25':
        tokenized_query = text_input.split(" ")
        doc_scores = bm25.get_scores(tokenized_query).tolist()
        indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:NUM_DOCS]
        doc_scores = sorted(doc_scores, reverse=True)
        top_n = bm25.get_top_n(tokenized_query, corpus, n=NUM_DOCS)
        # print(top_n)
    else:
        query_vector = tfidf_vectorizer.transform([text_input])
        cosine_sims = [cosine_similarity(query_vector, paragraph) for paragraph in tfidf_corpus]
        indices = sorted(range(len(cosine_sims)), key=lambda i: cosine_sims[i], reverse=True)[:NUM_DOCS]
        sorted_pairs = sorted(zip(cosine_sims, corpus), key=lambda tup:tup[0], reverse=True)
        top_n = [paragraph[1] for paragraph in sorted_pairs]
        top_n = top_n[:5]
        print(cosine_sims[:5])
    for i in range(len(meta)-1):
        if indices[0] >= meta[i][1] and indices[0] < meta[i+1][1]:
            start_index = meta[i][1]
            end_index = meta[i+1][1]
    st.subheader('Kết quả trùng khớp nhất')
    st.markdown('**{}**'.format(top_n[0]))
    # full_article = st.checkbox('Tài liệu đầy đủ')
    # if full_article:
    st.subheader('Tài liệu đầy đủ')
    for i in range(start_index, end_index):
        if i == indices[0]:
            st.markdown('*{}*'.format(corpus[i]))
        else:
            st.markdown('{}'.format(corpus[i]))
    st.write('****************************')
    st.subheader('*Một số kết quả khác:*')
    for result in top_n[1:]:
        st.write(result)
