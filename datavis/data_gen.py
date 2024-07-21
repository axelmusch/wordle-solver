import json 
import math

def shannon_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:  # Avoid log(0) which is undefined
            entropy += p * math.log2(1 / p)
    return entropy

def safe_log2(x):
    return math.log2(x) if x > 0 else 0

def result_to_json(dict):
    with open("datavis/sample2.json", "w") as outfile: 
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

words = load_words('././words.txt')
all_words = load_words('././allwords.txt')

words_count = len(words)
results = dict()
temp_words = ['slate','crane','soare']
#loop over all words
for word in temp_words:
#for word in all_words:
    #TODO: check every word with the other words for 'fitness' of current word
    results[word] = dict()
    results_scores = dict()
    results_points = 0
    print(f"Analyzing {word}...")
    for checkingword in words:
        word_result = ""
        word_result_visual = ""
        for index,letter in enumerate(word):
            if letter == checkingword[index]:
                word_result += "2"
                results_points += 2
                word_result_visual += "🟩"
            elif letter in checkingword:
                word_result += "1"
                results_points += 1
                word_result_visual += "🟨"
            else:
                word_result += "0"
                results_points += 0
                word_result_visual += "⬛"
        #print(f"Result for {word} with {checkingword}: {word_result}")
        if word_result in results_scores :
            results_scores[word_result] += 1
        else:
            results_scores[word_result] = 1
    sorted_keys = dict(sorted(results_scores.items(), key=lambda item: item[1],reverse=True))
    total_infomation = 0
    
  
    probs = []
    for key in sorted_keys:
        t = sorted_keys[key] / words_count
        probs.append(t)

        
    avg = shannon_entropy(probs)
   # print(probs)
    print(f"shannon thing: {avg}")
    results[word]["points"] = results_points
    results[word]["avg"] = avg
    results[word]["scores"] = sorted_keys
sorted_results = dict(sorted(results.items(),key=lambda x: (x[1]['avg']),reverse=True))
results = sorted_results
#print(results)
result_to_json(results)