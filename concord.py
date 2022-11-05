#!/usr/bin/python3
import fileinput


def lower_str_arr(arr):
    """
    Input: arr str[]
    Output: the same array but with everything lowered
    """
    temp_arr = []
    for word in arr:
        temp_arr.append(word.lower())

    return temp_arr
def get_exceptions(words_list):
    """
    Input: words_list - str[], the list of all words taken from stdin
    Output: exception_words_list, a list of exception words contained between ''' and \""\" in the stdin
    """
    exception_words_list = []
    is_exception_being_read = False
    for word in words_list: #start recordeing when ' and stop when "
        if '\'' in word:
            is_exception_being_read = True
        elif '\"' in  word:
            is_exception_being_read = False
        elif is_exception_being_read:
            exception_words_list.append(word.strip('\n'))
    
    exception_words_list = lower_str_arr(exception_words_list)
    exception_words_list = [*set(exception_words_list)]
    return exception_words_list

def get_rid_of_exceptions(current_words, exception_words):
    """
    Input: current_words - str [] and exception_words - str[]
    Output: current_words - str[] with all words listed in exception_words removed
    """
    current_words.pop(0) #get rid of the random int at the start
    current_words_placeholder = lower_str_arr(current_words) # copy into the placeholder, or else the x's and y's will get messed up
    current_words_original = current_words.copy()
    for x in range(0, len(exception_words)):
        for y in range(0, len(current_words_placeholder)):

            if (current_words_placeholder[y] == exception_words[x]):
                current_words.remove(current_words_original[y])

            elif ('\'' in current_words_placeholder[y] and current_words.count('\'\'\'\'') > 0) or ( '\"' in current_words_placeholder[y] and current_words.count('\"\"\"\"') > 0):
                #make sure the elements exist in the actual array 
               current_words.remove(current_words_placeholder[y])

    #remove the duplicates
    current_words = lower_str_arr(current_words)
    current_words = [*set(current_words)]
    return current_words

def sort_sentances(current_words, sent):
    """
    Input : curent_words - string [] , sent - string []
    Output : final_sent - string [], the concorded array of all sentances, with the main word capitalized
    """
    final_sent = [] 
    temp_current_words = []
    lower_sent = lower_str_arr(sent) #lower everything
    for x in range(0 , len(current_words)):
        for y in range(0, len(sent)):
            sentance_lowered= lower_sent[y].split(' ') #turn the sent into an array
            sentance_normal = sent[y].split(' ')
            word = current_words[x]
            for z in range(0, len(sentance_lowered)):
                if sentance_lowered[z] == word:
                    placeholder_sent = sentance_normal.copy()
                    placeholder_sent[z] = sentance_normal[z].upper()
                    final_sent.append((' ').join(placeholder_sent))
                    temp_current_words.append(word)
    temp_current_words.sort()
    return [final_sent, temp_current_words]

def format_sentance(sent, word):
    """
    Input: string sent, the sentance ; string word, the word we are formating this around; char [] base, the base sentance we will be filling
    Output: a formated sentance as specified in fluff() 
    """
    final_sent = ""
    leftmost_pos = 10
    rightmost_pos = 60
    center_pos = 30
    word = word.upper()
    position = sent.find(word)
    while position > (center_pos - leftmost_pos): #while things do not fit on the left
        sent = sent.split(' ', 1)[1]
        position = sent.find(word) #remove a word from the left until it fits into 20 chars

    while (len(sent) - position - len(word)) > (rightmost_pos - center_pos - len(word) + 1) : #while they do not fit on the right of the word
        sent_arr =sent.split(' ')
        sent_arr.pop(-1)
        sent = (" ").join(sent_arr)
        position = sent.find(word)

    #add the nice spaces
    position = sent.find(word)
    final_sent = sent
    while(position != center_pos):
        if position < center_pos:
            final_sent = " " + final_sent
        elif position > center_pos:
            final_sent = final_sent.split(' ', 1)[1]
        position = final_sent.find(word) + 1
    return final_sent
def fluff(arr, sorted_words):
    """
    Input : str[] arr, holds all the lines which will be output
    Output: str[] fluffed_arr, will be an array which follows the formatting requirements
            indexed words are at 30th column
            words to the left of the index, appear only if they do not go further left than col 10
            words to the right of the index, appear only if they go no further than col 60
    """
    fluffed_arr = []
    for i in range(0, len(arr)): #each sentance
        fluffed_arr.append(format_sentance(arr[i], sorted_words[i]))
    return fluffed_arr

def main():
    is_Exception = True
    exception_list = []
    current_words = []
    sentances = []
    final_arr = []
    for line in fileinput.input():
        current_word = line.strip().strip('\n').split() #removes unneccesary whitespaces, and new lines then splits it by spaces into words
        current_words.extend(current_word) #current_words will become a list holding every single word in stdin
        if not is_Exception:
            sentances.append(line.strip())
        if '\"' in line:
            is_Exception = False
        #sentances will hold a list of all the sentances

    exception_list = get_exceptions(current_words) # get the exception list 
    current_words = get_rid_of_exceptions(current_words, exception_list) # get just the words that will be sorted into current_words
    current_words.sort()
    final_arr_list = sort_sentances(current_words , sentances)
    final_arr = final_arr_list[0]
    current_words = final_arr_list[1]
    fluffed_arr = fluff(final_arr, current_words)
    for sent in fluffed_arr:
        print(sent)

if __name__ == "__main__":
    main()
    
