import random

currentWord = "sight"

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

guess1 = "night"

count = 1
guess_letters_good = list()
guess_letters_bad = list()
guess_letters_place = ["-","-","-","-","-"]


for i in guess1:
    if i in currentWord:
        guess_letters_good.append(i)
        if i == currentWord[count-1]:
            #print(i, " correct letter at place " ,count)
            guess_letters_place[count-1] = i
        else:
           print(i, " correct letter wrong place ")
    else:
        guess_letters_bad.append(i)
    count = count +1

print(guess_letters_place)
print("good letters",guess_letters_good)
print("bad letters",guess_letters_bad)

newlist = list()

for word in wordlist:
    matchall = list()
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
        
        for badletter in guess_letters_bad:
            if badletter not in word:
                print(word)
                print("---")
    
