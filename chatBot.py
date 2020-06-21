#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import re
import os
import playsound
from gtts import gTTS 
import os 
import pygame

reflections = {
    'am': 'are',
    'was': 'were', 
    'i': 'you',
    "i'd": 'you would',
    "i've": 'you have',
    "i'll": 'you will',
    'my': 'your',
    'are': 'am',
    "you've": 'I have',
    "you'll": 'I will',
    'your': 'my',
    'yours': 'mine',
    'you': 'me',
    'me': 'you',
    }
listOfChoices = [
    'family',
    'friends',
    'life',
    'work',
    'job',
    'happiness',
    'goals',
    'dreams',
    ]
psychobabble = [
    [r'I am Old',
        ['You seem to be younger than me :p']
    ],
    [r'Coronavirus',
        ['Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. \nMost people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness. The best way to prevent and slow down transmission is be well informed about the COVID-19 virus, the disease it causes and how it spreads. Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow). \nAt this time, there are no specific vaccines or treatments for COVID-19. However, there are many ongoing clinical trials evaluating potential treatments. WHO will continue to provide updated information as soon as clinical findings become available.']
    ], 
    [r'help',
        ['Do you want me to call your loved ones and inform them about your condition right now?']
    ],
    [r'yes', 
        ["Sure!, will do that. It's always fun to talk to you"]
    ],
    [r'Who are you?',
        ["I am codevid. Your personal assistant. ;)"]
    ],
    [r'Are you human?',
        ["I am more humane than many humans out there. I'm built with love by humans err engineers. :p"]
    ],
    [r'SOS',
        ["Please  don't panic!. I am monitoring your actions. Do you want me to make emergency calls?"]
    ],
    [r'(.*) news (.*)', 
        ["Ok seems like you're interested more in the world rather than me. \nNow taking you to our in house news site\nLoading...."]

    ],
    [r'I need (.*)', 
        ['Would it really help you to get {0}?',
        'Are you sure you need {0}?']
    ],
    [r'thank you',
        ['So kind of you! Glad to help you']
    ],
    [r'welcome',
        ['So kind of you! Glad to help you']
    ],
    [r'Why don\'?t you ([^\?]*)\??', 
        ["Do you really think I don't {0}?"
        , 'Perhaps eventually I will {0}.', 'Do you really want me to {0}?'
     ]
    ],
    [r'Why can\'?t I ([^\?]*)\??',
        ['Do you think you should be able to {0}?',
        'If you could {0}, what would you do?',
        "I don't know -- why can't you {0}?", 'Have you really tried?']
    ],
    [r'I can\'?t (.*)',
        ["How do you know you can't {0}?",
        'Perhaps you could {0} if you tried.',
        'What would it take for you to {0}?']
    ],
    [r'I am (.*)',
        ['Did you come to me because you are {0}?',
        'How long have you been {0}?', 'How do you feel about being {0}?']
    ],
    [r'I\'?m (.*)', 
        ['How does being {0} make you feel?',
        'Do you enjoy being {0}?', "Why do you tell me you're {0}?",
        "Why do you think you're {0}?"]
    ],
    [r'Are you ([^\?]*)\??',
        ['Why does it matter whether I am {0}?',
        'Would you prefer it if I were not {0}?',
        'Perhaps you believe I am {0}.',
        'I may be {0} -- what do you think?']
    ],
    [r'What (.*)', 
        ['Why do you ask?',
        'How would an answer to that help you?', 'What do you think?']
    ],
    [r'How (.*)',
        ['How do you suppose?',
        'Perhaps you can answer your own question.',
        "What is it you're really asking?"]
    ],
    [r'Because (.*)',
        ['Is that the real reason?',
        'What other reasons come to mind?',
        'Does that reason apply to anything else?',
        'If {0}, what else must be true?']
    ],
    [r'(.*) sorry (.*)',
        ['There are many times when no apology is needed.',
        'What feelings do you have when you apologize?']
    ],
    [r'Hello(.*)', 
        ["Hello... I'm glad you could drop by today.",
        'Hi there... how are you today?',
        'Hello, how are you feeling today?']
    ],
    [r'I think (.*)', 
        ['Do you doubt {0}?', 'Do you really think so?',
        "But you're not sure {0}?"]
    ],
    [r'(.*) friend (.*)', 
        ['Tell me more about your friends.',
        'When you think of a friend, what comes to mind?',
        "Why don't you tell me about a childhood friend?"]
    ],
    [r'Yes',
        ['You seem quite sure.',
        'OK, but can you elaborate a bit?']
    ],
    [r'(.*) computer(.*)', 
        ['Are you really talking about me?',
        'Does it seem strange to talk to a computer?',
        'How do computers make you feel?',
        'Do you feel threatened by computers?']
    ],
    [r'Is it (.*)', 
        ['Do you think it is {0}?',
        "Perhaps it's {0} -- what do you think?",
        'If it were {0}, what would you do?', 'It could well be that {0}.']
        
    ],
    [r'It is (.*)', 
        ['You seem very certain.',
        "If I told you that it probably isn't {0}, what would you feel?"]
    ],
    [r'Can you ([^\?]*)\??', 
        ["What makes you think I can't {0}?",
        'If I could {0}, then what?',
        'Why do you ask if I can {0}?']
    ],
    [r'Can I ([^\?]*)\??', 
        ["Perhaps you don't want to {0}.",
        'Do you want to be able to {0}?',
        'If you could {0}, would you?']
    ],
    [r'You are (.*)', 
        ['Why do you think I am {0}?',
        "Does it please you to think that I'm {0}?",
        'Perhaps you would like me to be {0}.',
        "Perhaps you're really talking about yourself?"]
    ],
    [r'You\'?re (.*)', 
        ['Why do you say I am {0}?',
        'Why do you think I am {0}?',
        'Are we talking about you, or me?']
    ],
    [r'I don\'?t (.*)', 
        ["Don't you really {0}?", "Why don't you {0}?",
        'Do you want to {0}?']
    ],
    [r'I feel (.*)', 
        ['Good, tell me more about these feelings.',
        'Do you often feel {0}?', 
        'When do you usually feel {0}?',
        'When you feel {0}, what do you do?']
    ],
    [r'I have (.*)', 
        ["Why do you tell me that you've {0}?",
        'Have you really {0}?',
        'Now that you have {0}, what will you do next?']
    ],
    [r'I would (.*)', 
        ['Could you explain why you would {0}?',
        'Why would you {0}?', 
        'Who else knows that you would {0}?']
    ],
    [r'Is there (.*)', 
        ['Do you think there is {0}?',
        "It's likely that there is {0}.",
        'Would you like there to be {0}?']
    ],
    [r'My (.*)', 
        ['I see, your {0}.', 'Why do you say that your {0}?',
        'When your {0}, how do you feel?']
    ],
    [r'You (.*)', 
        ['We should be discussing you, not me.',
        'Why do you say that about me?', 
        'Why do you care whether I {0}?']
    ],
    [r'Why (.*)', 
        ["Why don't you tell me the reason why {0}?",
        'Why do you think {0}?']
    ],
    [r'I want (.*)', 
        ['What would it mean to you if you got {0}?',
        'Why do you want {0}?', 'What would you do if you got {0}?',
        'If you got {0}, then what would you do?']
    ],
    [r'(.*) mother(.*)', 
        ['Tell me more about your mother.',
        'What was your relationship with your mother like?',
        'How do you feel about your mother?',
        'How does this relate to your feelings today?',
        'Good family relations are important.']
    ],
    [r'(.*) father(.*)', 
        ['Tell me more about your father.',
        'How did your father make you feel?',
        'How do you feel about your father?',
        'Does your relationship with your father relate to your feelings today?',
        'Do you have trouble showing affection with your family?']
    ],
    [r'(.*) child(.*)', 
        ['Did you have close friends as a child?',
        'What is your favorite childhood memory?',
        'Do you remember any dreams or nightmares from childhood?',
        'Did the other children sometimes tease you?',
        'How do you think your childhood experiences relate to your feelings today?']
    ],
    [r'(.*)\?', 
        ['Why do you ask that?',
        'Please consider whether you can answer your own question.',
        'Perhaps the answer lies within yourself?',
        "Why don't you tell me?"]
    ],
    [r'quit', 
        [" Sad to see you go! \n Hope to see you soon. \n I'll be there for you, even when you're offline.. ;)"]
    ],
    [r'Good (.*)', 
        ['Hey there hope you are enjoying! This is a typo.'
        ]
    ],
    [r'I am feeling lucky',
        ['Glad to hear that, Hope I keep you entertained!']
    ],
    [r'Coronavirus',
        ['Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. \nMost people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness. The best way to prevent and slow down transmission is be well informed about the COVID-19 virus, the disease it causes and how it spreads. Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow). \nAt this time, there are no specific vaccines or treatments for COVID-19. However, there are many ongoing clinical trials evaluating potential treatments. WHO will continue to provide updated information as soon as clinical findings become available.']
    ], 
    [r'(.*)', 
        ['Please tell me more.',
        "I don't seem to get you! Can you please try again?",
        "What exactly do you want me to do?",
        "You can try my other functionalities",
        "Seems like you have a problem",
        "I don't like our connections"
        ]
    ]

]


def reflect(fragment):
    tokens = fragment.lower().split()
    for (i, token) in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement, randomNumber):
    for (pattern, responses) in psychobabble:
        match = re.match(pattern, statement.rstrip('.!'))
        if match:
            response = random.choice(responses)
            if response == 'plannedQuestion':
                response = "Let's change focus a bit... Tell me about your {}.".format(listOfChoices[randomNumber])
                return response.format(*[reflect(g) for g in match.groups()])
            else:
                return response.format(*[reflect(g) for g in match.groups()])

def scrapeNews(topic):
    pass 
def main():
    print('Hello. What is on your mind today?')

    while True:
        randomNumber = random.randint(0,len(listOfChoices))
        statement = input('> ')
        if statement == '':
            statement = input("> ")
        if statement.lower() == 'news':
            topic = input("What do you want the news about? ")
            scrapeNews(topic)
            continue

        print(analyze(statement, randomNumber))
        # mytext = analyze(statement, randomNumber)
        # language = 'en'
        # myobj = gTTS(text=mytext, lang=language, slow=False) 
        # myobj.save("response.mp3") 
        # playsound.playsound('response.mp3', True)
        


        if statement == r'quit':
            mytext = analyze(statement, randomNumber)
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False) 
            myobj.save("response.mp3") 
            playsound.playsound('response.mp3', True)
            playsound.playsound('exit.mp3', True)
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Thanks. Stopped because of KeyboardInterrupt")
    except ValueError:
        print("Oops!, you look confused, Shall we start again?")

			