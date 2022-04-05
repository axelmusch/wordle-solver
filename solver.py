"""A dummy docstring."""
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pyautogui import press, typewrite

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.nytimes.com/games/wordle/index.html")
time.sleep(0.25)

search_box = driver.find_element_by_id('pz-gdpr-btn-accept').click()

host = driver.find_element(By.TAG_NAME, 'game-app')
shadowRoot = driver.execute_script("return arguments[0].shadowRoot", host)

modelHost = shadowRoot.find_element(By.TAG_NAME, 'game-modal')
modalRoot = driver.execute_script("return arguments[0].shadowRoot", modelHost)
time.sleep(0.25)
modalRoot.find_element(By.CLASS_NAME, 'close-icon').click()
time.sleep(0.25)

def load_words(WORDLIST_FILENAME):
    """load words"""
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


wordlist = load_words('./words.txt')
guesses = list()
guess1 = "sloan"

#driver.quit()

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

    typewrite(guess1)
    time.sleep(0.5)
    press('enter')
    time.sleep(2)

    board = shadowRoot.find_element(By.ID, 'board')
    rowElems = board.find_elements(By.TAG_NAME,"game-row")
    rowRoot = driver.execute_script("return arguments[0].shadowRoot", rowElems[guessCount-1])
    row2 = rowRoot.find_element(By.CLASS_NAME, 'row')
    tileElems = row2.find_elements(By.TAG_NAME,"game-tile")
    correctLetters = 0
    for idx,tile in enumerate(tileElems,start=0):
        evaluation = tile.get_attribute('evaluation')
        letter = tile.get_attribute('letter')

        if evaluation == "correct":
            print(letter, ' --> correct')
            correctLetters += 1
            if letter not in guess_letters_good:
                guess_letters_good.append(letter)
            guess_letters_place[idx] = letter

        elif evaluation == "present":
            print(letter, ' --> present')
            if letter not in guess_letters_good:
                guess_letters_good.append(letter)
            if letter not in guess_letters_badPlace[idx]:
                guess_letters_badPlace[idx].append(letter)

        elif evaluation == "absent":
            print(letter, ' --> absent')
            if letter not in guess_letters_bad and letter not in guess_letters_good:
                guess_letters_bad.append(letter)
        else:
            print('tbd')

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
            if val is False:
                checkAll = False

        if checkAll is True:
            checkBadLetter = True
            for badletter in guess_letters_bad:
                if badletter in word:
                    checkBadLetter = False
            if checkBadLetter is True:
                canAddWord = True
                for idx,position in enumerate(guess_letters_badPlace,start=0):
                    for letter in position:
                        if letter == word[idx]:
                            print(letter, "cant be in spot ", idx+1)
                            print(word, "not valid")
                            canAddWord = False
                if canAddWord is True and word not in guesses:
                    newlist.append(word)

    print('possible words after guess %d :' % (guessCount), guess1)    
    print(newlist)

    if correctLetters == 5:
        print("word found after %d guesses: " % (guessCount+1), newguess)
        break
    guesses.append(guess1)
    newguess = random.choice(newlist)
    print("chosen word for guess %d: " % (guessCount+1), newguess)
    guess1 = newguess
