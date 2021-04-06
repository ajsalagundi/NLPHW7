# Kirtana Kalavagunta
# Ananth Salagundi
# CS 4395.0W1
# Due: 4/3/2021

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk, pickle, random, string, spacy, os

user_model = {
    'name': "",
    'personal_information': "",
    'likes': [],
    'dislikes': []
}

# bot_questions = {
#     0: 'Are you a fan of the Green Bay Packers?',
#     1: 'What news would you like to know about the Green Bay Packers?'
# }
#
# possible_user_responses = {
#     0: ['yes', 'yep', 'yeah', 'definitely', 'no', 'nope', 'nah'],
#     1: ['I want to hear about who the Packers are scouting for the draft.',
#         "I want to learn about who we're targeting in the offseason.",
#         "I want to know who we're getting in free agency.",
#         "I want to know about any contract negotiations."]
# }


if __name__ == "__main__":
    knowledge_base = pickle.load(open("kb.p", "rb"))  # get the knowledge base from the web crawler
    current_user = {}
    stop = False

    if os.path.isfile("./users.pickle"):
        users = pickle.load(open("users.pickle", "rb"))  # get the previous user models
    else:
        users = {}

    print("Howdy! This is the Green Bay Bot, the guy with the latest Packer news!")

    # Ask and store the user's name
    name = input("What's your name so I can get to know you better?")
    name = name.strip()
    if name in users.keys():
        current_user = users[name]
    else:
        user_model['name'] = name
        current_user = user_model
        users[name] = user_model

    # Ask if the user is a fan of GBP for personalization
    fan = input("Are you a fan of the Green Bay Packers? Type yes / no")
    if fan == "Y":
        current_user['likes'].append('fan')
    else:
        current_user['dislikes'].append('not a fan')

    while stop:
        print("If you would like to end this conversation, please respond with 'bye'.")
        user_resp = input(name + ": ")
        if user_resp == 'bye':
            print("What would you like to know about the off season for the Green Bay Packers?")
