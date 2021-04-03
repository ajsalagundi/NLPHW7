from urllib import request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os, re, pickle, io, spacy

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from collections import Counter
from string import punctuation

nlp = spacy.load('en_core_web_lg')


def grab_urls():
    targets = ["https://packerswire.usatoday.com/category/latest-packers-news/", "https://www.packers.com/news/", "https://www.espn.com/blog/green-bay-packers", "https://www.acmepackingcompany.com/#stories"]
    list_urls = []

    for url in targets:
        parse_url = urlparse(url)
        html = request.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = str(link.get('href'))
            if href.startswith('http'):
                if href not in list_urls:
                    if re.search('/[\d]{4}/[\d]{2}/[\d]{2}/', href):
                        list_urls.append(link.get('href'))
                    if re.search('/news/', href):
                        list_urls.append(link.get('href'))
            if href.startswith('/news/'):
                list_urls.append(parse_url.scheme + "://" + parse_url.netloc + link.get('href'))
            if href.startswith('/blog/green-bay-packers/post/'):
                list_urls.append(parse_url.scheme + "://" + parse_url.netloc + link.get('href'))
    return list(set(list_urls))


def grab_text(urls):
    with io.open(os.path.join(os.getcwd(), f"url_out.text"), 'w+', encoding='utf-8') as f:
        for url in urls:
            html = request.urlopen(url).read().decode('utf8')
            soup = BeautifulSoup(html, 'html.parser')
            paras = soup.find_all('p')
            for paragraph in paras:
                paragraph = paragraph.get_text().replace("\n", "").replace("\t", "")
                sents = sent_tokenize(paragraph)
                for sent in sents:
                    f.write(sent)
                    f.write('\n')
    f.close()


def extract_important(text):
    """
    THIS CODE IS INSPIRED BY Ng Wai Foong. HERE'S THE LINK: https://betterprogramming.pub/extractive-text-summarization-using-spacy-in-python-88ab96d1fd97
    :param text:
    :return:
    """
    important_words = []
    doc = nlp(text)

    # Generating the most important words based on pos tagging
    for token in doc:
        if (token.text not in stopwords.words('english') and token.text not in punctuation) and token.pos_ in ['NOUN', 'PROPN', 'VERB']:
            important_words.append(token.text)

    # Normalizing the words based on the frequency of the most common word
    freq_words = Counter(important_words)
    most_freq_word = freq_words.most_common(1)[0][1]
    for word in freq_words:
        freq_words[word] = freq_words[word]/most_freq_word

    return freq_words.most_common(1000)


def build_sentence_bank(data_file):
    dbank = []
    for line in data_file:
        raw_text = line.replace("\n", "").replace("\t", "")
        for sent in sent_tokenize(raw_text):
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
    print("------------------------------------- GOT URLS ----------------------------------")
    grab_text(urls)
    print("---------------------------------- CLEANED TEXT ---------------------------------")

    f = io.open('url_out.text', 'r', encoding='utf-8')
    important_words = extract_important(f.read())
    print("---------------------------- GOT IMPORTANT WORDS --------------------------------")

    for word in ['draft', 'NFL', 'Green Bay Packers', 'offseason', 'preseason', 'free agency', 'snaps', 'touches', 'deals', 'weapons', 'scouts',
                'talented', 'super bowl', 'regular season', 'college recruits', 'draft day', 'scout tape', 'Lambeau Field', 'Wisconsin',
                'cheesehead', 'football', 'lombardi trophy', 'championships', 'super bowl rings', 'draft pick']:
        # These are some reserve words commonly used in the domain of the application's knowledge base.
        important_words.append(word)
    knowledge_base = build_kb(list(set(important_words)), f)
    pickle.dump(knowledge_base, open('kb.p', 'wb'))
    print("------------------------- FINISHED BUILDING KB ----------------------------------")
