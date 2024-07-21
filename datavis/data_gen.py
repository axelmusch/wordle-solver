import json 
import math

def generate_scores():
    print('scores')

def shannon_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:  # Avoid log(0) which is undefined
            entropy += p * math.log2(1 / p)
    return entropy

def safe_log2(x):
    return math.log2(x) if x > 0 else 0

def result_to_json(dict, filename="sample2"):

    with open("datavis/" + filename + ".json", "w") as outfile: 
        json.dump(dict, outfile)
    outfile.close()


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

WORDLE_WORDS = load_words('././words.txt')
ALL_WORDS = load_words('././allwords.txt')
WORDLE_WORDS_COUNT = len(WORDLE_WORDS)
ALL_WORDS_COUNT = len(ALL_WORDS)

f = open('./datavis/scores.json')
WORDS_SCORES = json.load(f)
f.close()


def get_words_that_match_pattern(word_to_check, pattern):
    words_to_return = []
    for word in ALL_WORDS:
        can_add_word = True
        for index,p in enumerate(pattern):
            if p == '2':
                if not word_to_check[index] == word[index]:
                    can_add_word = False
            elif p == '1':
                if not (word_to_check[index] in word and word_to_check[index] != word[index]):
                    can_add_word = False
            elif p == '0':
                if word_to_check[index] in word:
                    can_add_word = False
        if can_add_word == True:
            words_to_return.append(word)
    return words_to_return
    
def generate_data(words=ALL_WORDS):
    to_return = dict()
    for word in words:
        to_return[word] = dict()
        results_scores = dict()
        for checkingword in WORDLE_WORDS:
            word_result = ""
            for index,letter in enumerate(word):
                if letter == checkingword[index]:
                    word_result += "2"
                elif letter in checkingword:
                    word_result += "1"
                else:
                    word_result += "0"

            if word_result in results_scores :
                results_scores[word_result]["total"] += 1
            else:
                results_scores[word_result] = {"total":1}

        sorted_keys = dict(sorted(results_scores.items(), key=lambda item: item[1]["total"],reverse=True))
        
        probs = []
        for key in sorted_keys:
            t = sorted_keys[key]["total"] / WORDLE_WORDS_COUNT
            probs.append(t)
            sorted_keys[key]["percentage"] = t*100
        avg = shannon_entropy(probs)

        to_return[word]["score"] = avg
        to_return[word]["patterns"] = sorted_keys
        
        for pattern in to_return[word]["patterns"]:
            next_guesses = get_words_that_match_pattern(word,pattern)
            print(f"word: {word} guesses for pattern({pattern}): {len(next_guesses)}")
            #loo-p over all words to checj wuth next guesses
            results_scores_2 = dict()
            for word_2 in ALL_WORDS:
                results_scores_2[word_2] = {}
                for checkingword in next_guesses:
                    word_result = ""
                    for index,letter in enumerate(word_2):
                        if letter == checkingword[index]:
                            word_result += "2"
                        elif letter in checkingword:
                            word_result += "1"
                        else:
                            word_result += "0"

                    if word_result in results_scores_2[word_2] :
                        results_scores_2[word_2][word_result]["total"] += 1
                    else:
                        results_scores_2[word_2][word_result] = {"total":1}

                sorted_keys_2 = dict(sorted(results_scores_2[word_2].items(), key=lambda item: item[1]["total"],reverse=True))


                probs = []
                for key in sorted_keys_2:
                    t = sorted_keys_2[key]["total"] / len(next_guesses)
                    probs.append(t)
                avg = shannon_entropy(probs)
                #sorted_keys_2[word_2]["score"] = avg
                results_scores_2[word_2] = avg
            results_scores_2 = dict(sorted(results_scores_2.items(), key=lambda item: item[1],reverse=True))
            results_scores_2 = {k: results_scores_2[k] for k in list(results_scores_2)}
            to_return[word]["patterns"][pattern]["next_guesses"] = results_scores_2

    return to_return


temp_words = ['soare']
results = generate_data(temp_words)


sorted_results = dict(sorted(results.items(),key=lambda x: (x[1]['score']),reverse=True))
#sorted_scores = dict(sorted(results_all.items(),key=lambda x: x[1],reverse=True))
results = sorted_results
#print(results)
result_to_json(results)


""" #results_all = dict()
#loop over all words
#for word in temp_words:
for word in ALL_WORDS:
    results[word] = dict()
    results_scores = dict()
    print(f"Analyzing {word}...")
    for checkingword in WORDLE_WORDS:
        word_result = ""
        word_result_visual = ""
        for index,letter in enumerate(word):
            if letter == checkingword[index]:
                word_result += "2"
                word_result_visual += "🟩"
            elif letter in checkingword:
                word_result += "1"
                word_result_visual += "🟨"
            else:
                word_result += "0"
                word_result_visual += "⬛"
        #print(f"Result for {word} with {checkingword}: {word_result}")
        if word_result in results_scores :
            results_scores[word_result]["total"] += 1
            results_scores[word_result]["next_guesses"].append(checkingword)
        else:
            
            results_scores[word_result] = {"total":1, "next_guesses":[checkingword]}

    sorted_keys = dict(sorted(results_scores.items(), key=lambda item: item[1]["total"],reverse=True))
    

    probs = []
    for key in sorted_keys:
        t = sorted_keys[key]["total"] / WORDLE_WORDS_COUNT
        probs.append(t)

        
    avg = shannon_entropy(probs)
   # print(probs)
    #print(f"shannon thing: {avg}")
    results[word]["score"] = avg
    #results_all[word] = avg

    results[word]["patterns"] = sorted_keys

#result_to_json(sorted_scores,"scores") """