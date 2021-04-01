from urllib import request
from bs4 import BeautifulSoup
import os, nltk, math, xml, re, pickle

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def grab_urls():
    url = "https://packerswire.usatoday.com/category/latest-packers-news/"
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    list_urls = []
    counter = 0
    for link in soup.find_all('a'):
        if counter == 15:
            break
        href = str(link.get('href'))
        if href.startswith('http'):
            if href not in list_urls:
                if re.search('/[\d]{4}/[\d]{2}/[\d]{2}/', href):
                    list_urls.append(link.get('href'))
                    counter += 1
    return list_urls


def grab_text(urls):
    i, files = 1, []
    for url in urls:
        html = request.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        with open(os.path.join(os.getcwd(), f"url{i}.text"), 'w+') as file:
            file.write(soup.get_text())
            file.close()
            files.append(f"url{i}.text")
            i += 1
    return files


def clean_text(filenames):
    i = 1
    for filename in filenames:
        file = open(filename, 'r')
        raw_text = file.read()
        raw_text = raw_text.replace("\n", "").replace("\t", "")
        sents = sent_tokenize(raw_text)
        with open(os.path.join(os.getcwd(), f"url{i}.out"), 'w+') as file:
            for sent in sents:
                file.write(sent)
                file.write('\n')
            file.close()
            i += 1
    return i


def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc)
    st = stopwords.words('english')
    tokens = [w for w in tokens if w.isalpha() and w not in st]

    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t]/len(tokens)

    return tf_dict


def calc_idf(vocab, vocab_list):
    idf_dict = {}

    for term in vocab:
        temp = ['x' for voc in vocab_list if term in voc]
        idf_dict[term] = math.log((1 + num_docs)/(1 + len(temp)))

    return idf_dict


def create_tfidf(tf, idf):
    tf_idf = {}

    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    return tf_idf


def extract_important(tf_idfs):
    important, weights = [], {}
    for t in tf_idfs:
        for item, value in sorted(t.items(), key=lambda x: x[1], reverse=True):
            if value not in weights.values():
                weights[item] = value
    s = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    important.append(s[26:102])
    return important


def build_sentence_bank(files):
    dbank = []
    for f in files:
        with open(f, 'r') as file:
            raw_text = file.read()
            raw_text = raw_text.replace("\n", "").replace("\t", "")
            sents = sent_tokenize(raw_text)
            for sent in sents:
                dbank.append(sent)

    return dbank


def build_kb(terms, files):
    kb = {}
    data_bank = build_sentence_bank(files)

    for term in terms:
        kb[term] = [sent for sent in data_bank if term in sent]

    return kb


if __name__ == "__main__":
    urls = grab_urls()
    fs = grab_text(urls)
    num_docs = clean_text(fs)
    vocab = set()

    docs = []
    for f in fs:
        with open(f, 'r') as file:
            docs.append(file.read().lower().replace('\n', ' '))

    tfs = []
    for doc in docs:
        tfs.append(create_tf_dict(doc))

    for tf in tfs:
        vocab = vocab.union(set(tf.keys()))

    idf = calc_idf(vocab, tfs)
    tf_idfs = []
    for tf in tfs:
        tf_idfs.append(create_tfidf(tf, idf))

    important_words = extract_important(tf_idfs)
    print(important_words)
    # knowledge_base = build_kb(future_words, fs)
    # pickle.dump(knowledge_base, open('kb.p', 'wb'))
