#imports
import json
import logging
import re
import random
import pyphen

from collections import OrderedDict

class Translation:
    #initializes class
    def __init__(self, real_language_influences_list, more_of_list, less_of_list, none_of_list):
        #sets translation instance equal to provided parameters
        self.real_language_influences_list = real_language_influences_list
        self.more_of_list = more_of_list
        self.less_of_list = less_of_list
        self.none_of_list = none_of_list

    #intakes a single word and outputs a list of syllables
    def syllabize(self, word):
        #convert word to lower case
        word = word.lower()

        #remove apostrophes by splitting the word into sub-words
        syllable = word.split('\'')

        #assuming input language is English, hyphenate and then split the word on the hyphenations
        syllable = [s for w in syllable for s in pyphen.Pyphen(lang='en').inserted(w).strip().split('-')]

        #keep syllables in order during return
        syllables = list(OrderedDict.fromkeys(syllable))

        return syllables

    #changes supplied text from English to specified fantasy language  
    def translate(self, text_in):
        #load the real languages json file for later
        f = open('translator_app/real_languages.json')
        real_languages = json.load(f)
        real_languages = real_languages['real_languages']
        
        #list of characters/syllables that will become the translated phrase
        translated_list = []

        #splits text_in into distinct words but maintains punctuation and non-letter characters
        words = re.split(r'(@?\w+)(\s+|\W)', text_in)
        print(words)
        #break down words into syllables using syllabize
        for word in words:
            #check if word is proper noun, indicated by surrounding address (@) symbols. If so, preserve it and remove symbol.
            if re.match(r'@\w+', word):
                translated_word = word.strip('@')
            #check if word is, indeed, a word. If it is, break it down into syllables
            elif re.match(r'\w+', word):
                syllables = self.syllabize(word)
                #translates or replaces each syllable with a syllable from real_languages.json, randomly chosen based on user's language selections, and combines them into translated_word
                translated_word = ''
                for syllable in syllables:
                    randomLanguage = random.choice(self.real_language_influences_list)
                    translated_syllable = random.choice(real_languages[randomLanguage]['syllables'])
                    #moderate letter frequency based on user inputs - this feels like it's bad; should review alternatives in the future
                    if any(item not in translated_syllable for item in self.more_of_list):
                        translated_syllable = random.choice(real_languages[randomLanguage]['syllables'])
                    if any(item in translated_syllable for item in self.less_of_list):
                        translated_syllable = random.choice(real_languages[randomLanguage]['syllables'])
                    counter = 0
                    while any(item in translated_syllable for item in self.none_of_list):
                        translated_syllable = random.choice(real_languages[randomLanguage]['syllables'])
                        counter +=1
                        if counter > 100:
                            translated_syllable = 'no words match criteria :('
                            break
                    logging.debug(translated_syllable)
                    translated_word = ''.join((translated_word, translated_syllable))
                #if original word was capitalized, then capitalize translated word
                if word[0].isupper():
                    if word.isupper() and len(word) >= 2:
                        translated_word = translated_word.upper()
                    else:
                        translated_word = translated_word.capitalize()
            else:
                translated_word = word

            translated_list.append(translated_word)
            
        #combine everything into one string
        translated_phrase = ''.join(translated_list)

        #remove instances of multiple spaces due to input or unmapped syllables
        translated_phrase = re.sub(' +', ' ', translated_phrase)

        return translated_phrase