import random
import sys
currentWord = "start"
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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pyautogui import press, typewrite, hotkey
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.nytimes.com/games/wordle/index.html")
search_box = driver.find_element_by_id('pz-gdpr-btn-accept').click()

host = driver.find_element(By.TAG_NAME, 'game-app')
shadowRoot = driver.execute_script("return arguments[0].shadowRoot", host)

modelHost = shadowRoot.find_element(By.TAG_NAME, 'game-modal')
modalRoot = driver.execute_script("return arguments[0].shadowRoot", modelHost)

modalRoot.find_element(By.CLASS_NAME, 'close-icon').click()


typewrite('rates')
driver.implicitly_wait(0.5)
press('enter')
time.sleep(3)

board = shadowRoot.find_element(By.ID, 'board')

rowHost = board.find_element(By.TAG_NAME, 'game-row')
rowRoot = driver.execute_script("return arguments[0].shadowRoot", rowHost)

row = rowRoot.find_element(By.CLASS_NAME, 'row')

tileHost = row.find_element(By.TAG_NAME, 'game-tile')
tileRoot = driver.execute_script("return arguments[0].shadowRoot", tileHost)

tile = rowRoot.find_element(By.CLASS_NAME, 'row')

rowHTML = tile.get_attribute('innerHTML')
evalu = rowHTML.split("</game-tile>") 
print('tile--> ',evalu)
#print('tile--> ',tile.value_of_css_property('color'))



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

#driver.quit()

guess_letters_good = list()
guess_letters_badPlace = [list(),list(),list(),list(),list()]
guess_letters_bad = list()
guess_letters_place = ["-","-","-","-","-"]
square_array = list()

for guessCount in range(1, 1):
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
    
