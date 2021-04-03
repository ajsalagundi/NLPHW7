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

bot_questions ={
        '0': 'Are you a fan of the Green Bay Packers?',
        '1': 'Would you like to hear about the latest scouting reports ?', # Insert Player's Name
        '2': 'Have you heard about the latest free agency signings by the Green Bay Packers?',
 }

possible_user_patterns = {  # possible user responses to the questions, the keys correspond to the bot questions keys
    '0': ['Yes', 'Yep ', 'Yup ', 'Yes I am a fan ', 'Yes I am a huge fan ', 'Yeah I like them ', 'Yeah I love them ', 'Yes I like them ' , 'Yes I love them ', 'No I hate them ', 'No I do not like them', 'No ', 'No I don\’t like them '],
    '1': ['Yes I would ', 'Yes ', 'Sure ', 'No ', 'No thank you ', 'Yes please ', 'Nah not really interested ', 'Yeah, I’ve heard we’ve targeted placeholder. Is this true? ' , 'No, but I’m interested in learning more '],
    '2': ['Yes I have', 'Yeah! I’ve heard we are signing placeholder. Is this true? ' , 'No, but I\’m interested in learning more ', 'Yep ', 'Yup ', 'Nope ']
 }

ppossible_bot_responses = {  # possible bot responses to the user patterns, the keys correspond to the user pattern keys and the order is the same as user order
    '0': ['That\'s great! ', 'Me too!', 'They are my favorite team too! ', 'But they are such a good team! ', 
    'Aw, they are such a good team though :(', 'That is great!  Would you like to hear about the latest scouting reports ?'],
    '1': ['Cool! Well, according to the latest news, the Packers are targeting {Player Y} because he’s touted for {description of scout from news article}.', 'That\'s too bad. :(',],
    '2': ['That\'s amazing! What have you heard? ',  'That\'s cool, I did not know that! ', 'That\'s awesome! Well, you should be excited since you were right! According to the latest news reports, the Packers are signing placeholder for placeholder', 
    'Cool! Well, according to the latest reports, the Packers are interested in signing placeholder. '],  
}

bot_conversation = {  # possible bot continuation responses for keeping the conversation going after originally asking the question
    '0': ['Why do you like the team?', 'Why don\'t you like the team?', 'Why do you not like them?', 'Why don\'t you like them?', 'Why do you hate them?'],
    '1': ['Would you like to know anything else about the Green Bay Packers? '],
    '2': ['Would you like to know anything else about the Green Bay Packers? '],

}

bot_convo_responses = {  # list of responses a bot can come up with during conversation with a user. The keys are the user responses, values are possible bot resposnes
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








if __name__ == '__main__':
    # Main code here