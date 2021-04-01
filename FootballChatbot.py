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








if __name__ == '__main__':
    # Main code here