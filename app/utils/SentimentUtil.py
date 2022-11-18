import regex as re

# Turns the positive or negative words in the txt file to the array containing each word.
def setupWordsFromTxt(filename):
    file = open(filename,'r')
    
    words = []

    for line in file.readlines():
        words.append(line.strip())
    
    return words

# Removes the stopwords from the list of words.
def removeStopWords(words, stop_words):
    processed_words = []

    for word in words:
        if(word not in stop_words):
            processed_words.append(word)

    return processed_words

# Get the number of words from the text.
def getNumberOfWordsFromText(text):
    lower_case = text.lower()
    url_removed_text =  " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", lower_case).split())

    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    
    emoji_removed_text = emoji_pattern.sub(r'', url_removed_text)
    words = emoji_removed_text.split(' ')

    return len(words)



# Gives the word count for a given sentiment.
def getSentimentWordCount(text, filename):
    comparing_words = setupWordsFromTxt(filename)
    stop_words = setupWordsFromTxt('stoplist.txt')

    lower_case = text.lower()
    url_removed_text =  " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", lower_case).split())

    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    
    emoji_removed_text = emoji_pattern.sub(r'', url_removed_text)
    words = emoji_removed_text.split(' ')
    
    processed_words = removeStopWords(words, stop_words)

    count = 0

    for word in processed_words:
        if word in comparing_words:
            count+=1

    return count

# Gives us the sentiment score
def getSentimentScore(text):
    positive_word_count = getSentimentWordCount(text, 'positive.txt')
    negative_word_count = getSentimentWordCount(text, 'negative.txt')

    if (positive_word_count == 0 and negative_word_count == 0):
        return 0
    return round((positive_word_count - negative_word_count)/(positive_word_count + negative_word_count),3)

