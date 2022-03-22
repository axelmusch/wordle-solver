import random
import sys
currentWord = "slosh"
#https://www.nytimes.com/games/wordle/index.html

import requests
from bs4 import BeautifulSoup

from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi


URL = "https://www.nytimes.com/games/wordle/index.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
#print(soup)

results = soup.find_all('body')

#print ('results',results)
#for child in results[0].children:
    #print(child)

from selenium import webdriver
driver = webdriver.Chrome('./chromedriver')

    #self.open("https://www.nytimes.com/games/wordle/index.html")
    #self.click("game-app::shadow game-modal::shadow game-icon")


def load_words(WORDLIST_FILENAME):
       print ("Loading word list from file...")
       wordlist = list()
       # 'with' can automate finish 'open' and 'close' file
       with open(WORDLIST_FILENAME) as f:
            # fetch one line each time, include '\n'
            for line in f:
                # strip '\n', then append it to wordlist
                wordlist.append(line.rstrip('\n'))
       print (" ", len(wordlist), "words loaded.")
       #print ('\n'.join(wordlist))
       return wordlist

def choose_word (wordlist):
       return random.choice (wordlist)

wordlist = load_words('words.txt')

guess1 = "sloan"


guess_letters_good = list()
guess_letters_badPlace = [list(),list(),list(),list(),list()]
guess_letters_bad = list()
guess_letters_place = ["-","-","-","-","-"]
square_array = list()

for guessCount in range(1, 7):
    squareString = "-"
    print('__________________________________')
    print("start guess %d" % (guessCount))
    count = 1
    for i in guess1:
        if i in currentWord:
           
            if i not in guess_letters_good:
                guess_letters_good.append(i)
            if i == currentWord[count-1]:
                #print(i, " correct letter at place " ,count)
                guess_letters_place[count-1] = i
                squareString += 'green'
            else:
                #print(i, " correct letter wrong place ")
                squareString += 'yellow'
                if i not in guess_letters_badPlace[count-1]:
                    guess_letters_badPlace[count-1].append(i)
        else:
            squareString += 'black'
            if i not in guess_letters_bad:
                guess_letters_bad.append(i)
        count = count +1

    print(squareString)
    print(guess_letters_place)
    print("good letters",guess_letters_good)
    print("goodbad letters",guess_letters_badPlace)
    print("bad letters",guess_letters_bad)

    newlist = list()

    for word in wordlist:
        matchall = list()

        for idx,letter in enumerate(guess_letters_good,start=0):
            if letter not in word:
                matchall.append(False)
        for idx,letter in enumerate(guess_letters_place,start=0):
            #print(idx, letter)
            
            if letter != "-":
                if letter == word[idx]:
                    #print("start with correct letter", word)
                    matchall.append(True)
                else:
                    matchall.append(False)

        checkAll = True
        for val in matchall:
            if val == False:
                checkAll = False

        if checkAll == True:
            checkBadLetter = True
            for badletter in guess_letters_bad:
                if badletter in word:
                    checkBadLetter = False
            if checkBadLetter == True:
                newlist.append(word)

    print('possible words after guess %d :' % (guessCount), guess1)    
    print(newlist)
    newguess = random.choice(newlist)
   
    print("chosen word for guess %d: " % (guessCount+1), newguess)
    guess1 = newguess
    if newguess == currentWord:
        print("word found after %d guesses: " % (guessCount+1), newguess)
        break
    
