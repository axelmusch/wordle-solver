import random
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pyautogui import press, typewrite

RESULTS_FOLDER = "results/"
RESULTS_FOLDER_TEMP = "results_temp/"
filename = datetime.today().strftime('%d%m%y')+ ".txt"

if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)
if not os.path.exists(RESULTS_FOLDER_TEMP):
    os.makedirs(RESULTS_FOLDER_TEMP)

if not os.path.exists(RESULTS_FOLDER + filename):
    filename = RESULTS_FOLDER + datetime.today().strftime('%d%m%y')+ ".txt"
else:
    filename = RESULTS_FOLDER_TEMP + datetime.today().strftime('%d%m%y')+ ".txt"

options  = Options()
options.add_argument("window-size=1200,1400")
driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
driver.get("https://www.nytimes.com/games/wordle/index.html")


resultFile = open(filename , "w",encoding="utf-8")
resultFile.write("")
resultFile.close()

time.sleep(2)
search_box = driver.find_element(By.XPATH,'//button[@data-testid="Accept all-btn"]').click()
time.sleep(0.25)
search_box = driver.find_element(By.XPATH,'//button[@data-testid="Play"]').click()
time.sleep(0.25)
search_box = driver.find_element(By.XPATH,'//button[@aria-label="Close"]').click()
time.sleep(0.25)

host = driver.find_element(By.ID, 'wordle-app-game')




def print_to_file(text,regular=True):
    print(text)
    logFile = open(filename, "a",encoding="utf-8")
    logFile.write(f"{text}\n")
    logFile.close()

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
    print_to_file('__________________________________')
    print_to_file(f"GUESS {guessCount}")
    typewrite(GUESS1)
    time.sleep(0.5)
    press('enter')
    time.sleep(2)
    row2 = host.find_element(By.XPATH,'//div[@aria-label="Row ' + str(guessCount) + '"]')
    tileElems = row2.find_elements(By.XPATH,'//div[@aria-label="Row ' + str(guessCount) + '"]/div/div[@data-testid="tile"]')
    CORRECT_LETTERS = 0
    boxes = list()
    for idx,tile in enumerate(tileElems,start=0):
        evaluation = tile.get_attribute('data-state')
        letter = tile.get_attribute('innerHTML')

        if evaluation == "correct":
            #print_to_file(letter + ' --> 🟩')
            boxes.append('🟩')
            CORRECT_LETTERS += 1
            if letter not in guess_letters_good:
                guess_letters_good.append(letter)
            guess_letters_place[idx] = letter

        elif evaluation == "present":
            #print_to_file(letter+ ' --> 🟨')
            boxes.append('🟨')
            if letter not in guess_letters_good:
                guess_letters_good.append(letter)
            if letter not in guess_letters_badPlace[idx]:
                guess_letters_badPlace[idx].append(letter)

        elif evaluation == "absent":
            #print_to_file(letter+ ' --> ⬛')
            boxes.append('⬛')
            if letter not in guess_letters_bad and letter not in guess_letters_good:
                guess_letters_bad.append(letter)
        else:
            boxes.append('⬛')
            print('tbd')
    print_to_file("".join(boxes))
    print_to_file(guess_letters_place)
    print_to_file(f"Good letters: {guess_letters_good}")
    print_to_file(f"Good letters but wrong spots : {guess_letters_badPlace}")
    print_to_file(f"Bad  letters : {guess_letters_bad}")

    newlist = list()
    for word in wordlist:
        matchall = list()

        for idx,letter in enumerate(guess_letters_good,start=0):
            if letter not in word:
                matchall.append(False)
        for idx,letter in enumerate(guess_letters_place,start=0):
            if letter != "-":
                if letter == word[idx]:
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
    print_to_file(f"possible words after guess {guessCount}: {GUESS1}, {len(newlist)}")
    print_to_file(str(newlist),False)
    guesses.append(GUESS1)
    commonletters = {}
    #put selector logic
    for word in newlist:
        for index, letter in enumerate(word):
            key = letter
            if key in commonletters:
                commonletters[key] +=1
            else:
                commonletters[key] =1
    print_to_file(f"Common letters: {commonletters}")
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
    print_to_file(f"Best 5 letters({maxMatch} matching): {bestletters}")

    matchCache = [word['word'] for word in matchCache if word['matching'] == maxMatch]
    print_to_file(f"match cache 1 filtered {matchCache}")
    commonlettersSpot = {0:{},1:{},2:{},3:{},4:{}}
    for word in matchCache:
        for index, letter in enumerate(word):
            key = letter
            if key in commonlettersSpot[index]:
                commonlettersSpot[index][key] +=1
            else:
                commonlettersSpot[index][key] =1
    print_to_file(f"Best letters per spot {commonlettersSpot}")
    bestlettersSpot_0 = pick_highest(commonlettersSpot[0],1)
    bestlettersSpot_1 = pick_highest(commonlettersSpot[1],1)
    bestlettersSpot_2 = pick_highest(commonlettersSpot[2],1)
    bestlettersSpot_3 = pick_highest(commonlettersSpot[3],1)
    bestlettersSpot_4 = pick_highest(commonlettersSpot[4],1)
  
    bestlettersSpot = [bestlettersSpot_0,bestlettersSpot_1,bestlettersSpot_2,bestlettersSpot_3,bestlettersSpot_4]
    matchCache2 = list()
    maxMatch2 = 0
    for word in matchCache:
        matchCount = 0
        for index, letter in enumerate(bestlettersSpot):
            if word[index] == list(letter.keys())[0]:
                matchCount += 1
        matchCache2.append({'word':word, 'matching':matchCount})
        if matchCount > maxMatch2:
            maxMatch2 = matchCount
    #----------
    print_to_file(f"Best 5 letters per spot({maxMatch2} matching) {bestlettersSpot}")
    matchCache2 = [word['word'] for word in matchCache2 if word['matching'] == maxMatch2]
    print_to_file(f"match cache 2 filtered {matchCache2}")

    print_to_file(f"Common letters: {str(commonletters)}", False)
    print_to_file(f"matchCache: {str(matchCache)}", False)
 
    newguess = random.choice(matchCache2)
    if CORRECT_LETTERS == 5:
        print_to_file(f"word found after {guessCount} guesses: {newguess}" )
        
        time.sleep(10)
        break
    print_to_file(f"chosen word for guess {guessCount+1}: {newguess}" )
    GUESS1 = newguess
