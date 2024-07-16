import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pyautogui import press, typewrite

options  = Options()
options.add_argument("window-size=1200,1400")
driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
driver.get("https://www.nytimes.com/games/wordle/index.html")

time.sleep(2)
search_box = driver.find_element(By.XPATH,'//button[@data-testid="Accept all-btn"]').click()
time.sleep(0.25)
search_box = driver.find_element(By.XPATH,'//button[@data-testid="Play"]').click()
time.sleep(0.25)
search_box = driver.find_element(By.XPATH,'//button[@aria-label="Close"]').click()
time.sleep(0.25)

host = driver.find_element(By.ID, 'wordle-app-game')

def load_words(wordlist_filename):
    """load words"""
    print ("Loading word list from file...")
    temp_wordlist = list()
    # 'with' can automate finish 'open' and 'close' file
    with open(wordlist_filename,encoding="utf-8") as f:
        # fetch one line each time, include '\n'
        for line in f:
            # strip '\n', then append it to wordlist
            temp_wordlist.append(line.rstrip('\n'))
    print (" ", len(temp_wordlist), "words loaded.")
    #print ('\n'.join(wordlist))
    return temp_wordlist

def pick_highest(obj, num=1):
    """Returns 5 most used letters"""
    if num > len(obj):
        return False
    sorted_keys = sorted(obj, key=obj.get, reverse=True)
    required_obj = {key: obj[key] for key, ind in zip(sorted_keys, range(num))}
    return required_obj

wordlist = load_words('./words.txt')
guesses = list()
LETTERS = "abcdefghijklmnopqrstuvwxyz".split()
print(LETTERS)
GUESS1 = "suave"

#driver.quit()

guess_letters_good = list()
guess_letters_badPlace = [list(),list(),list(),list(),list()]
guess_letters_bad = list()
guess_letters_place = ["-","-","-","-","-"]
square_array = list()

for guessCount in range(1, 7):
    print('__________________________________')
    print(f"GUESS {guessCount}")
    typewrite(GUESS1)
    time.sleep(0.5)
    press('enter')
    time.sleep(2)
    row2 = host.find_element(By.XPATH,'//div[@aria-label="Row ' + str(guessCount) + '"]')
    tileElems = row2.find_elements(By.XPATH,'//div[@aria-label="Row ' + str(guessCount) + '"]/div/div[@data-testid="tile"]')
    CORRECTED_LETTERS = 0
    for idx,tile in enumerate(tileElems,start=0):
        evaluation = tile.get_attribute('data-state')
        letter = tile.get_attribute('innerHTML')

        if evaluation == "correct":
            print(letter, ' --> correct')
            CORRECTED_LETTERS += 1
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

        CHECK_ALL = True
        for val in matchall:
            if val is False:
                CHECK_ALL = False

        if CHECK_ALL is True:
            CHECK_BAD_LETTER = True
            for badletter in guess_letters_bad:
                if badletter in word:
                    CHECK_BAD_LETTER = False
            if CHECK_BAD_LETTER is True:
                CAN_ADD_WORD = True
                for idx,position in enumerate(guess_letters_badPlace,start=0):
                    for letter in position:
                        if letter == word[idx]:
                            #print(letter, "cant be in spot ", idx + 1)
                            #print(word, "not valid")
                            CAN_ADD_WORD = False
                if CAN_ADD_WORD is True and word not in guesses:
                    newlist.append(word)
    print(f"possible words after guess {guessCount} : ", GUESS1)
    #print(newlist)
    guesses.append(GUESS1)
    commonletters = {}
    #put selector logic
    for word in newlist:
        for letter in word:
            if letter in commonletters:
                commonletters[letter] +=1
            else:
                commonletters[letter] =1
    bestletters = pick_highest(commonletters,5)

    matchCache = list()
    maxMatch = 0
    for word in newlist:
        matchCount = 0
        for letter in bestletters:
            if letter in word:
                matchCount += 1
        matchCache.append({'word':word, 'matching':matchCount})
        if matchCount > maxMatch:
            maxMatch = matchCount

    matchCache = [word['word'] for word in matchCache if word['matching'] == maxMatch]

    #----------
    print(commonletters)
    print(matchCache)
    newguess = random.choice(matchCache)
    if CORRECTED_LETTERS == 5:
        print(f"word found after {guessCount} guesses: ", newguess)
        time.sleep(10)
        break
    print(f"chosen word for guess {guessCount+1}: ", newguess)
    GUESS1 = newguess
