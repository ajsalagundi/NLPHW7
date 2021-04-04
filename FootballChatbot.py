# Kirtana Kalavagunta
# Ananth Salagundi 
# CS 4395.0W1
# Due: 3/4/2021

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pickle
import random
import string
import spacy 

users = {}

bot_questions ={
        '0': 'Are you a fan of the Green Bay Packers?',
        '1': 'Would you like to hear about the latest scouting reports ?', # Insert Player's Name
        '2': 'Have you heard about the latest free agency signings by the Green Bay Packers?',
 }

possible_user_patterns ={  # possible user responses to the questions, the keys correspond to the bot questions keys
    '0': ['Yes', 'Yep ', 'Yup ', 'Yes I am a fan ', 'Yes I am a huge fan ', 'Yeah I like them ', 'Yeah I love them ', 'Yes I like them ' , 'Yes I love them ', 'No I hate them ', 'No I do not like them', 'No ', 'No I don\’t like them '],
    '1': ['Yes I would ', 'Yes ', 'Sure ', 'No ', 'No thank you ', 'Yes please ', 'Nah not really interested ', 'Yeah, I’ve heard we’ve targeted placeholder. Is this true? ' , 'No, but I’m interested in learning more '],
    '2': ['Yes I have', 'Yeah! I’ve heard we are signing placeholder. Is this true? ' , 'No, but I\’m interested in learning more ', 'Yep ', 'Yup ', 'Nope ']
 }

possible_bot_responses ={  # possible bot responses to the user patterns, the keys correspond to the user pattern keys and the order is the same as user order
    '0': ['That\'s great! ', 'Me too!', 'They are my favorite team too! ', 'But they are such a good team! ', 
    'Aw, they are such a good team though :(', 'That is great!  Would you like to hear about the latest scouting reports ?'],
    '1': ['Cool! Well, according to the latest news, the Packers are targeting {Player Y} because he’s touted for {description of scout from news article}.', 'That\'s too bad. :(',],
    '2': ['That\'s amazing! What have you heard? ',  'That\'s cool, I did not know that! ', 'That\'s awesome! Well, you should be excited since you were right! According to the latest news reports, the Packers are signing placeholder for placeholder', 
    'Cool! Well, according to the latest reports, the Packers are interested in signing placeholder. '],  
}

bot_conversation ={  # possible bot continuation responses for keeping the conversation going after originally asking the question
    '0': ['Why do you like the team?', 'Why don\'t you like the team?', 'Why do you not like them?', 'Why don\'t you like them?', 'Why do you hate them?'],
    '1': ['Would you like to know anything else about the Green Bay Packers? '],
    '2': ['Would you like to know anything else about the Green Bay Packers? '],

}

bot_convo_responses ={  # list of responses a bot can come up with during conversation with a user. The keys are the user responses, values are possible bot resposnes
    'i like them because': ['So you like them because placeholder.', 'You like it because placeholder.'],
    'i love them because': ['So you love them because placeholder.', 'You love them because placeholder.'],
    'i do not like them because': ['So you do not like them because placeholder.', 'You do not like them because placeholder.'],
    'i don\'t like them because': ['So you don\'t like them because placeholder.', 'You don\'t like them because placeholder.'],
    'they are': ['They are placeholder.'],
    'i think': ['You think placeholder.'], 
    'are my favorite because': ['So they are your favorite because placeholder', 'They are your favorite because placeholder.'],
    'i hate them because': ['You hate them because placeholder.'],
}

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad you are talking to me!"]

# get_user_name function. This function takes in the original user response and parses it with Spacy NER to get the user's name
def get_user_name(user_input):

    if len(user_input) == 0:  # the user did not provide any input
        return ''  # return an empty string, the user did not provide a name

    name = ''
    nlp = spacy.load("en_core_web_sm")  # use the small version of the english web core
    words = nlp(user_input)  # use spacy NER to get the user input tagged

    for ent in words.ents:  # for every part of the input that was tagged
        if ent.label_ == "PERSON":  # find the name
            name = ent.text  # set name to the name of the user

    if name == '':  # spacy did not catch the name
        if len(user_input) == 1:  # user only provided their name
            name = user_input
        else:  # user provided more information than just a name
            stop_words = stopwords.words('english')  # get stop words
            stop_words += ['name', 'usually', 'called', 'go', 'by', '.', '!', '?']
            tokens = word_tokenize(user_input.lower())
            name = [n for n in tokens if n not in stop_words]
            name = ' '.join(name)
            return name.capitalize()  # return the name

    return name  # return the name

# getUsername function. This function takes in the original user response and parses it with Spacy NER to get the user's name
def getUsername (userInput):

    if len(userInput) == 0:  
        return ''  

    name = ''

    # use spacy NER to get the user input tagged
    nlp = spacy.load("en_core_web_sm")  
    words = nlp(userInput)  

    # set name to the name of the user
    for ent in words.ents:  
        if ent.label_ == "PERSON":  
            name = ent.text  

    if name == '':  # spacy did not catch the name
        if len(userInput) == 1:  # user only provided their name
            name = userInput
        else:  # user provided more information than just a name
            stopWords = stopwords.words('english')  # get stop words
            stopWords += ['name', 'usually', 'called', 'go', 'by', '.', '!', '?']
            tokens = word_tokenize(userInput.lower())
            name = [n for n in tokens if n not in stopWords]
            name = ' '.join(name)
            return name.capitalize()  # return the name

    return name  # return the name

###############################################

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


###############################################

def wants_topic(userResponse):
    tokens = word_tokenize(userResponse)  # tokenize the userResponse

    for token in tokens:
        if token == 'topic' or token == 'topics' or token == 'sentence' or token == 'sentences':  # user wants a list of the topics
            return True
    return False

###############################################


def funFacts(topics, name): # GBB stands for Green bay bot. 
    print("GBB: Which of my topics do you want to know about?")  # prompt user for one of the topics
    chooseTopic = []  # variable for the user's response
    while chooseTopic == []:  # while the user hasn't entered a valid topic
        response = input(name + ": ")  # get the user's response
        tokens = word_tokenize(response.lower())  # get the tokens
        chooseTopic = [t for t in tokens if t in topics.keys()]  # get the topic
        if chooseTopic == []:  # user did not give a valid response
            print("GBB: I\'m sorry, I don't know about that topic. Please try again! ")

    chooseTopic = chooseTopic[0]  # get just the string of the topic from the list
    print("GBB: I found an article on the web about " + chooseTopic.capitalize() + ":")
    print("GBB: " + random.choice(topics.get(chooseTopic)) + "\n")  # give the user a fact about the topic

    def ask_question():
        choice = random.choice(list(bot_questions.keys()))  # get a random choice
        return choice, bot_questions[choice]  # return the question number and the question

########################################################

def response(knowledge, userResponse):
    botResponse = ''
    topic = ''
    tokens = word_tokenize(userResponse)
    for token in tokens:
        if token in knowledge.keys():
            topic = token
            break

    if topic in knowledge.keys():  # the user had one of the topics in their sentence
        botResponse = "GBB: I found an article on the web about " + topic.capitalize() + ": \n"
        botResponse = botResponse + "GBB: " + random.choice(knowledge.get(topic)) + "\n"  # give the user a fact about the topic

    return topic, botResponse

    ##################################################

# parseUserResponse function. This function parses the given user response to try and find important details to
# to use in a more customized bot response
def parseUserResponse(userResponse, possUser, botResponse, user, numQuestion, idx):
    finalResp = ''
    stopWords = stopwords.words('english')
    stopWords += ['really', 'like', 'n\'t', 'play', 'Green Bay Packers', 'prefer', '\'m', 'want', 'able', '\'s', '.', '!', '?', ':']
    stopWords += ['my', 'player', 'football', 'fun', 'fact', 'offseason', 'super bowl', 'cheesehead']
    tokens = word_tokenize(userResponse)  # turn the user response into tokens
    botTokens = word_tokenize(botResponse)
    tokenNotInStopword = [token for token in tokens if token not in stopWords]  # remove any stop words
    noBotStopwords = [token for token in botTokens if token not in stopWords]  # remove any stop words
    removeBot = [token for token in tokenNotInStopword if token not in noBotStopwords]

    removeBot = ' '.join(removeBot)

    if botResponse[0] == ' ':  # going to add customized part to the beginning of the bot response
        finalResp = removeBot.capitalize() + botResponse  # add the botResponse part
    elif botResponse[-1] == ' ':  # going to add customized part to the end of the bot response
        finalResp = botResponse + removeBot  # add the botResponse part
    elif 'placeholder' in botResponse:  # placed a placeholder to replace with the bot part
        if 'placeholder' in botResponse and botResponse.index('placeholder') == 0:  # placeholder is the first thing
            removeBot = removeBot.capitalize()  # capitalize the removeBot
        finalResp = botResponse.replace('placeholder', removeBot)  # replace the placeholder
    else:  # response is a statement in itself
        finalResp = botResponse  # set the final response to just the bot response

    if numQuestion == '0' and idx < 2:  # user response was a happy response for question 0
        if 'Green Bay Packers' not in user['likes']:  # did not already add to the list of user likes
            user['likes'].append('Green Bay Packers')  # user likes the team, add it to their likes
        else:  # already know the user likes the team
            finalResp = 'Oops, I knew that! '  # set the final response accordingly

    elif numQuestion == '0' and idx >= 2:  # user response was a negative response for question 0
        if 'Green Bay Packers' not in user['dislikes'] and 'Green Bay Packers' in user['likes']:
            user['likes'].remove('Green Bay Packers')  # remove from the likes
            user['dislikes'].append('Green Bay Packers')  # add to the dislikes
            finalResp = 'I thought you liked the team! Oh well, guess you are not a Cheesehead. '  # set the finalResp
        elif 'Green Bay Packers' not in user['dislikes']:  # did not already add to the list of user dislikes
            user['dislikes'].append('Green Bay Packers')  # user does not like the team, add it to their dislikes
        else:  # already know the user doesn't like the team
            finalResp = 'I hoped you changed your mind. '  # set the final response accordingly

    elif numQuestion == '1' and idx < 3:  # user response was a happy response for question 1
        if removeBot.capitalize() not in user['likes']:  # has not already been added before
            user['likes'].append(removeBot.capitalize())  # add the superhero to their likes
        else:  # user has mentioned this before
            finalResp = 'You told me this before!'  # set the final response accordingly

    elif numQuestion == '1' and idx >= 3:  # user response was a negative response for question 1
        if 'Superheroes' not in user['dislikes']:  # superheroes have not already been added to the user dislikes
            user['dislikes'].append('Superheroes')  # add superheroes to their dislikes
        else:  # already added before
            finalResp = 'I know you do not like the team :( I wish I could change your mind! '  # set the final response accordingly

    elif numQuestion == '2':  # user gave a fun fact
        if 'play' in userResponse:  # user plays a game 
            removeBot = 'play ' + removeBot  # add play to the personal info fun fact
        if 'like' in userResponse or 'love' in userResponse and 'not like' not in userResponse and removeBot not in user['likes']:  # user said they like or love something
            user['likes'].append(removeBot)  # add their fun fact to their likes
        if 'dislike' in userResponse or 'do not like' in userResponse or 'hate' in userResponse and removeBot not in user['dislikes']: # user said something they do not like
            user['dislikes'].append(removeBot)  # add their fun fact to their dislikes
        if removeBot not in user['personalInfo']:  # user has not mentioned it before
            user['personalInfo'].append(removeBot)  # add the fun fact to their personalInfo
        else:  # user has mentioned this before
            finalResp = 'Oops, you told me this already!'  # set the final response accordingly

    elif numQuestion == '3':  # user was asked a part they didn't like about the team
        phrase = 'The ' + removeBot + ' from Green Bay Packers'
        if phrase not in user['dislikes']:  # the part has not been mentioned before
            user['dislikes'].append(phrase)  # add the part they didn't like to their dislikes
            if phrase in user['likes']:  # user said they liked this part before
                user['likes'].remove(phrase)  # remove from the likes
                finalResp = 'I thought you liked that part! I guess you changed your mind....'  # set finalResp
        else:  # user has mentioned this before
            finalResp = 'You already told me you didn\'t like that part!'  # set the final response accordingly

    elif numQuestion == '4' and idx < 4:  # user was asked their favorite part of the team and gave positive response
        phrase = 'The ' + removeBot + ' from Green Bay Packers'
        if phrase not in user['likes']:  # the part has not been mentioned before
            user['likes'].append(phrase)  # add their favorite part to their likes
            if phrase in user['dislikes']:  # user previously said they did not like this part
                user['dislikes'].remove(phrase)  # remove from the dislikes
                finalResp = 'You told me you didn\'t like this part! I\'m so happy you changed your mind.'  # set finalResp
        else:
            finalResp = 'You already told me this was your favorite part! I was hoping you had another.'  # set the final response accordingly

    elif numQuestion == '4' and idx >= 4:  # user was asked their favorite part of the team and gave negative response
        if 'Green Bay Packers' not in user['dislikes'] and 'Green Bay Packers' in user['likes']:  # user said they liked it before
            user['likes'].remove('Green Bay Packers')  # remove from the likes
            user['dislikes'].append('Green Bay Packers')  # add to the dislikes
            finalResp = 'I thought you liked the team! Oh well, I guess you changed your mind.'  # set the finalResp
        elif 'Green Bay Packers' not in user['dislikes']:  # have not already added the team to the user's dislikes
            user['dislikes'].append('Green Bay Packers')  # add the team to their dislikes
        else:  # user has already mentioned this before
            finalResp = 'You already told me you did not like the team. I was hoping you changed your mind. :('  # set the final response accordingly

    elif numQuestion == '5' and idx < 3:  # user was asked their favorite character and gave positive response
        if removeBot not in user['likes']:  # character has not been added to their likes yet
            user['likes'].append(removeBot)  # add the character to their likes

    elif numQuestion == '5' and idx >= 3:  # user was asked their favorite character and gave a negative response
        phrase = 'The players in the Green Bay Packers'  # phrase to add to the user's dislikes
        if phrase not in user['dislikes']:  # has not been added to their dislikes yet
            user['dislikes'].append(phrase)  # add to their dislikes
        else:  # phrase was already in their dislikes
            finalResp = 'Aw man! I thought I could change your mind. '  # set finalResp

    return finalResp

# LemTokens function. This function lemmatizes the tokens
def LemTokens(tokens):
    lemmer = WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]

# LemNormalize function. This function removes punctuation before tokenizing the lowered text and calling LemTokens
def LemNormalize(text):
    remPunctDict = dict((ord(punct), None) for punct in string.punctuation)
    return LemTokens(nltk.word_tokenize(text.lower().translate(remPunctDict)))

# conversation function. This function takes the current question and user and continues the conversation of that question
def conversation(userResp, question_num, user):
    response = ''
    sentences = possible_user_patterns.get(question_num)
    responses = possible_bot_responses.get(question_num)

    req_tfidf = 0  # variable for req_tfidf
    while req_tfidf == 0:
        sentences = [sentence.lower() for sentence in sentences]  # lower all the sentences
        sentences.append(userResp)  # add the user response to the sentences
        # see if can find a similar possible user response in responses we have rules for using tfidf and cosine similarity
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
        tfidf = TfidfVec.fit_transform(sentences)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if 'i have' in userResp:  # I have is in the response, tfidf has trouble getting this
            parsed_response = parse_userResp(userResp, sentences[2], responses[2], user, question_num, 2)
            response = parsed_response
            idx = 2
        elif 'no' in userResp and question_num == '0':  # no is the response but this might get removed in stop words
            parsed_response = parse_userResp(userResp, sentences[4], responses[4], user, question_num, 4)
            response = parsed_response
            idx = 4
        elif req_tfidf == 0:  # user response did not match a previously defined pattern
            sentences.remove(userResp)  # remove the original userResp
            print('GBB: I am sorry, I don\'t understand what you mean.')
            userResp = input(user['name'] + ': ')  # get the user's input again
        else:  # user response matched a previously defined pattern
            parsed_response = parse_userResp(userResp, sentences[idx], responses[idx], user, question_num, idx)
            response = parsed_response  # get the corresponding bot response

    return response, idx, userResp

# continue_conversation function. This function is for keeping the conversation going on a little longer after getting
# a user response to a question
def continue_conversation(org_response, question_num, user, idx, knowledge):
    bot_ques = bot_conversation[question_num]  # get the possible bot questions
    bot_rep = bot_ques[idx]  # get the corresponding bot response

    stop_words = stopwords.words('english')
    stop_words += ['really', 'like', 'n\'t', 'play', 'endgame', 'prefer', '\'m', 'want', 'able', 'since', 'I', 'favorite', '.', '!', '?', ':']
    stop_words += ['movie', 'love', 'part', 'Marvel', 'marvel', '\'s', 'character', 'superhero', 'dc', 'superpower', 'superpowers']
    stop_words += ['learned', 'power', 'would', 'avengers']
    stop_words.remove('is')
    stop_words.remove('are')
    stop_words.remove('me')
    stop_words.remove('more')
    stop_words.remove('the')
    stop_words.remove('you')
    stop_words.remove('it')
    tokens = word_tokenize(org_response)  # turn the user response into tokens
    bot_tokens = word_tokenize(bot_rep)
    no_stop_words_user = [token for token in tokens if token not in stop_words]  # remove any stop words
    no_stop_words_bot = [token for token in bot_tokens if token not in stop_words]  # remove any stop words
    remove_bot_part = [token for token in no_stop_words_user if token not in no_stop_words_bot]

    remove_bot_part = ' '.join(remove_bot_part)

    if 'placeholder' in bot_rep:  # have a placeholder to fit in the question
        bot_rep = bot_rep.replace('placeholder', remove_bot_part)

    print("GBB: " + bot_rep)  # ask the new question
    userResp = input(user['name'] + ': ')  # get the user's response
    userResp = userResp.lower()  # lower the response

    topic, topic_response = response(knowledge, userResp)  # if user mentioned topic give a fact about it
    if topic != '':  # user mentioned a topic
        print("GBB: I see you mentioned " + topic.capitalize())  # print that the user mentioned the topic
        print("GBB: ", end="")
        print(topic_response)


    req_tfidf = 0

    user_rep = bot_convo_responses.keys()  # get the possible user responses
    while req_tfidf == 0:
        tokens = word_tokenize(userResp)  # tokenize the response
        no_stop_words = [token for token in tokens if token not in stop_words]  # get the important words
        important_words = ' '.join(no_stop_words)  # create the important part
        first = important_words.find('is')
        if first != -1:  # if the word is in the string
            again = important_words.find('is', first + 1)
            if again != -1:  # is in the string twice
                important_words = important_words.replace('is', '', 1)  # replace the first occurrence

        sentences = [sentence.lower() for sentence in user_rep]  # lower all the sentences
        sentences.append(userResp)  # add the user response to the sentences
        # see if can find a similar possible user response in responses we have rules for using tfidf and cosine similarity
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
        tfidf = TfidfVec.fit_transform(sentences)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if req_tfidf == 0:  # did not find a corresponding user pattern
            print('GBB: I\'m sorry, I did not understand what you said.')
            sentences.remove(userResp)
        else:  # found a match
            key = sentences[idx].strip()  # get the corresponding key
            bot_responses = bot_convo_responses.get(key)  # get the possible bot responses
            if len(bot_responses) == 0:  # thought it found a match but it did not
                print('GBB: I\'m sorry, I did not understand what you said.')
                sentences.remove(userResp)
                continue  # keep the loop going
            rep = random.choice(bot_responses)  # choose a random bot response

            if rep[0] == ' ':  # placeholder to add the important things at the beginning
                rep = important_words.capitalize() + rep  # create the response
            elif rep[-1] == ' ':  # placeholder to add the important things at the end
                rep = rep + important_words  # create the response
            elif 'placeholder' in rep:  # have placeholder in the response to add important data there
                rep = rep.replace('placeholder', important_words)

            print('GBB: ' + rep)  # print out the bot's response
            continue

        userResp = input(user['name'] + ': ')  # get the user's response
        userResp = userResp.lower()  # lower case the response

        topic, topic_response = response(knowledge, userResp)  # if user mentioned topic give a fact about it
        if topic != '':  # user mentioned a topic
            print("GBB: I see you mentioned " + topic.capitalize())  # print that the user mentioned the topic
            print("GBB: ", end="")
            print(topic_response)

    return  #return to main


if __name__ == '__main__':
    # Main code here
    knowledge_base = pickle.load(open("kb.p", "rb")) # get the knowledge base from the web crawler

    # users = pickle.load(open("users.pickle", "rb"))  # get the previous user models
    currentUser = ''  # variable for the current user
    name = ''  # variable for the user's name
    flag = True  # flag for the loop

    # introduce the bot
    print("GBB: Go Pack Go! I'm GBB! ")
    print("GBB: Please enter \"bye\", \"thanks\", or \"thank you\" to exit when done.")
    print("GBB: When talking to me, please use full sentences to have an error-free experience!")

    # get the user's name
    print("GBB: What is your name?")  # get the user's name
    user_name = input("User: ")  # read in the user's name
    remPunctDict = dict((ord(punct), None) for punct in string.punctuation)
    user_name = user_name.translate(remPunctDict)
    user_name = user_name
    name = get_user_name(user_name)  # get the user's name after parsing the input

    while name == '':  # if the user doesn't actually enter a name
        print("GBB: Please tell me your name. ")
        user_name = input("User: ")  # read in the user's name
        user_name = user_name.translate(remPunctDict)
        name = get_user_name(user_name).capitalize()  # get the user's name after parsing the input
    name = name.capitalize()

    for user in users:  # check if the user already has a model
        if user['name'] == name:  # the user already has a user model
            currentUser = user  # get that user
            break  # end the loop, found the user looking for

    if currentUser == '':  # new user
        print("GBB: Hello " + name + "!")  # greet the user with their name
        users.append(base_user_model)  # add a new user to the list of users
        users[-1]['name'] = name  # set  the new user's name to the name given
        currentUser = users[-1]  # get the current user
    else:  # user is a returning user
        print("GBB: Hello " + name + "! Welcome back!")  # welcome the user back
        if currentUser.get('likes'):  # the user likes are not empty
            print("GBB: I remember you like " + random.choice(currentUser.get('likes')))  # print out a random thing the user likes
        else:  # user likes are empty
            print("GBB: I do not currently know much about what you like " + name + ".")  # tell user do not know much about their likes
        if currentUser.get('dislikes'):  # the user dislikes are not empty
            print("GBB: I remember you dislike " + random.choice(currentUser.get('dislikes')))  # print out a random thing the user dislikes
        else:  # user dislikes are empty
            print("GBB: I do not currently know much about what you don\'t like " + name + ".")  # tell the user do not know much about their dislikes
        if currentUser.get('personal_info'):  # have something personal about the user saved
            print("GBB: I remember you told me something about: " + random.choice(currentUser.get('personal_info')))  # print out a random thing in personal_info
        else:  # user personal_info is empty
            print("GBB: I do not currently know much about you " + name + ".")  # tell user do not know much about them

    while flag:  # while the user still wants to talk
        print("GBB: Would you like me to ask you a question or do you want to hear a sentence from one of my outside knowledge topics? ")  # ask user what they want
        userResp = input(name + ": ")  # prompt the user for a response
        userResp = userResp.lower()  # lower case the user's response
        remPunctDict = dict((ord(punct), None) for punct in string.punctuation)
        userResp = userResp.translate(remPunctDict)
        if userResp != 'bye':  # the user still wants to talk
            if userResp == 'thanks' or userResp == 'thank you':  # the user is saying thank you
                flag = False
                print("GBB: You are welcome. Have a nice day!")
            else:
                if greeting(userResp):  # user said a greeting
                    print("GBB: " + greeting(userResp))

                elif wants_topic(userResp):  # if the user wants a list of the topics
                    print("GBB: Here are the topics I have sentences from the web about: ")
                    [print(top.capitalize()) for top in knowledge_base.keys()]  # print the topics
                    ask_about_topics(knowledge_base, name)  # move conversation forward about a topic

                elif 'question' in userResp:  # user did not say a greeting or a thanks and does not want a topic to ask about
                    question_num, question = ask_question()  # get the number of the question and the question
                    print('GBB: ' + question)  # ask the user a question
                    userResp = input(name + ": ")  # get the user's response for the question
                    userResp = userResp.lower()  # lower case the user's response
                    topic, topic_response = response(knowledge_base, userResp)  # if user mentioned topic give a fact about it
                    if topic != '':  # user mentioned a topic
                        print("GBB: I see you mentioned " + topic.capitalize())  # print that the user mentioned the topic
                        print("GBB: ", end="")
                        print(topic_response)
                    GBB_response, idx, userResp = conversation(userResp, question_num, currentUser)  # get the response
                    print('GBB: ' + GBB_response)  # keep the conversation going
                    continue_conversation(userResp, question_num, currentUser, idx, knowledge_base)  # conversation part 2

                else:  # user gave bad input
                    print("GBB: Please say whether you want a question or a topic.")

        else:  # user is done talking
            flag = False
            print("GBB: Bye! take care...")

    users = users  # dump the new collection of users to the file
