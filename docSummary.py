import sklearn
import numpy
import scipy
import nltk.data
import re

def clean(string):

    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    # string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = remove_text_inside_brackets(string)
    # string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    return string.strip()

def remove_text_inside_brackets(text, brackets="[]"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)

def main():
    input = 'The English Wikipedia reached 4,000,000 registered user accounts on 1 April 2007,[15] ' \
            'just a little over a year since it had crossed a threshold of 1,000,000 registered user accounts in late ' \
            'February 2006.[16] Over 800,000 editors have edited Wikipedia more than 10 times.[17] 300,000 editors edit ' \
            'Wikipedia every month[citation needed]; of these, over 30,000 perform more than 5 edits per month, and a little' \
            ' over 3,000 perform more than 100 edits per month.[18] By 24 November 2011, a total of 500 million edits ' \
            'had been performed on the English Wikipedia.[citation needed] As the largest Wikipedia edition, and because ' \
            'English is such a widely used language, the English Wikipedia draws many users and editors whose native ' \
            'language is not English. Such users may seek information from the English Wikipedia rather than the Wikipedia ' \
            'of their native language because the English Wikipedia tends to contain more information about general ' \
            'subjects. Successful collaborations have been developed between non-native English speakers who successfully ' \
            'add content to the English Wikipedia and native English speakers who act as copyeditors for them.'

    result = clean(input)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    print('\n'.join(tokenizer.tokenize(result)))
    

main()



