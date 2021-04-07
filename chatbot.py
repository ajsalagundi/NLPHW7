# Kirtana Kalavagunta
# Ananth Salagundi
# CS 4395.0W1
# Due: 4/3/2021

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import nltk, pickle, random, string, spacy, os

user_model = {
    'name': "",
    'personal questions asked': [],
    'personal information': [],
    'likes': [],
    'dislikes': []
}


def parse_response(user_response):
    stop_words = stopwords.words("english") + ['Green', "Bay", 'Packers']
    user_words = word_tokenize(user_response)
    updated = [word for word in user_words if word not in stop_words and word not in punctuation]
    wnl = WordNetLemmatizer()
    words = []

    for word in updated:
        word = wnl.lemmatize(word)
        if word in ['draft', 'scout', 'college', 'prospect', 'pick']:
            words.append(word)
        elif word in ['free', 'agency', 'agent', 'signing']:
            words.append(word)
        elif word in ['contract', 'negotiation']:
            words.append(word)

    return words

# ------------------------------- NER FACTS ---------------------------------------------
def ner_fact_generation(article):
    return article

# ------------------------------ PERSONAL QUESTIONS ---------------------------------------------
def personal_questions(user):
    questions = {
        1: 'How long have you been a fan of the Packers?',
        2: 'Why are you a fan of the Packers?',
        3: "What team do you hate the most?",
        4: "Who's your favorite player on the Packers?",
        5: "Who's your least favorite player on the Packers?",
        6: "Do you come from a family of Packer fans, or are you a lone ranger?"
    }

    while True:
        num = random.randint(1, 6)
        answered = user['personal questions asked']
        if num not in answered:
            user['personal questions asked'].append(num)
            return questions[num]


if __name__ == "__main__":
    knowledge_base = pickle.load(open("kb.p", "rb"))  # get the knowledge base from the web crawler
    current_user = {}
    stop, ask = False, False

    if os.path.isfile("./users.pickle"):
        users = pickle.load(open("users.pickle", "rb"))  # get the previous user models
    else:
        users = {}

    # ------------------------- GREETINGS AND USER PROFILE --------------------------------------------

    print("Howdy! This is the Green Bay Bot, the guy with the latest Packer news!")
    print("You can ask me about Green Bay's free agency moves, their contract negotiations, and the draft.")
    # Ask and store the user's name
    name = input("What's your name so I can get to know you better?")
    name = name.strip()
    if name in users.keys():
        current_user = users[name]
        print("Welcome back, fellow Cheesehead!")
        print(personal_questions(current_user))
        current_user['personal information'].append(input(name + ": "))
    else:
        user_model['name'] = name
        current_user = user_model
        users[name] = user_model

    # ------------------------- PERSONALIZATION --------------------------------------------

    # Ask if the user is a fan of GBP for personalization
    fan = input("Are you a fan of the Green Bay Packers? Type yes / no")
    if fan == "yes":
        current_user['likes'].append('fan')
    else:
        current_user['dislikes'].append('not a fan')

    # ------------------------- MAIN QUESTIONS --------------------------------------------

    while not stop:
        print("What would you like to know about the off season for the Green Bay Packers?")
        user_resp = input(name + ": ")
        parsed = parse_response(user_resp)
        articles = [knowledge_base[word] for word in parsed if word in knowledge_base.keys()]

        # Check for a valid search
        if len(articles) > 0:
            # If it's valid, then show the response and ask them if they want to more about the question they asked.
            print(articles[0])  # Need to format this response
            # Ask the user if they want to know more facts about the previous question
            print("Do you want to know more about this?")
            user_resp = input(name + ": ")
            if user_resp.lower() in ['yes', 'yeah', 'yep']:
                # If they want to know more, then print a fun fact about the previous question's topic
                print()
        else:
            print("Unfortunately, I am not aware of this.")
            user_resp = input(name + ": ")

        print("Would you like to know something else? Type yes/no")
        user_resp = input(name + ": ")

        if user_resp == 'yes':
            continue
        else:
            print("If you would like to end this conversation, please respond with 'bye'.")
            user_resp = input(name + ": ")
            if user_resp == 'bye':
                stop = True
                print("Aw, I'm sorry to see you go! Did you like the information I gave you?")
                user_resp = input(name + ": ")

                if user_resp.lower() in ['yes', 'yeah', 'yep']:
                    users[name]['likes'].append("liked the bot's information")
                else:
                    users[name]['dislikes'].append("didn't like the bot's information")

                print("Before you leave, could you answer this question for me?")
                print(personal_questions(current_user))
                current_user['personal information'].append(input(name + ": "))
                print("Thank you so much! Go Pack Go!")

                pickle.dump(users, open("users.pickle", "wb"))
                exit(0)
