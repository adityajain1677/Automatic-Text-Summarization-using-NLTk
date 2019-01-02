import bs4 as bs
import urllib.request
import re
import nltk

scrapped_data = urllib.request.urlopen('https://cloud.google.com/blog/products/gcp/problem-solving-with-ml-automatic-document-classification')
article = scrapped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')


paragraphs = parsed_article.find_all('p')

article_text = "";

for p in paragraphs:
    article_text +=p.text 


article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
formatted_article_text= re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(article_text)


stopwords = nltk.corpus.stopwords.words('english')

word_frequency = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequency.keys():
             word_frequency[word] = 1
        else:
            word_frequency[word] += 1


maximum_frequency = max(word_frequency.values())
for word in word_frequency.keys():
    word_frequency[word] = (word_frequency[word]/maximum_frequency)

sentence_scores = {}  
for sent in sentence_list:  
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequency.keys():
            if len(sent.split(' ')) < 30:    
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequency[word]
                else:
                    sentence_scores[sent] += word_frequency[word]


import heapq  
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)  
print(summary) 




