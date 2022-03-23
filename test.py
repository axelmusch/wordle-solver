"""  for i in guess1:
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
        count = count +1 """