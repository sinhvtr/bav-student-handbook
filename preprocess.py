import json

with open('sotaysvhvnh_rutgon.txt', 'r') as fr:
    text = fr.read()

text = text.replace('\n\n', '\t')
text = text.replace('\n', ' ')

lines = text.split('\t')
lines = [line.strip() for line in lines]
lines = [line.replace('  ', ' ') for line in lines]

data = []
last_article_id = 1
article_paragraphs = []
for line in lines:
    if line.startswith('Điều '):        
        
        last_paragraph_id = 1
        if last_article_id == 1:
            article = {
                "article_id": last_article_id,
                "article_text": line,
                "article_paragraphs": []
            }
        else:
            
            article["article_paragraphs"] = article_paragraphs
            data.append(article)
            article_paragraphs = []
            article = {
                "article_id": last_article_id,
                "article_text": line,
                "article_paragraphs": []
            }
        last_article_id = last_article_id + 1
    else:
        paragraph = {
            "paragraph_id": last_paragraph_id,
            "paragraph_text": line
        }
        article_paragraphs.append(paragraph)
        last_paragraph_id = last_paragraph_id + 1

with open('sotay.json', 'w', encoding='utf8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)
