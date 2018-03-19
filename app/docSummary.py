import functools
import re
import nltk.data
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer


def clean(string):
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\\\(", " \( ", string)
    string = re.sub(r"\\\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\]\]", "", string)
    string = re.sub(r"\n", "", string)
    string = string.rstrip()
    string = remove_text_inside_brackets(string, "(){}[]")
    return string.strip()


def remove_text_inside_brackets(text, brackets):
    count = [0] * (len(brackets) // 2)  # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b:  # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1) ** is_close  # `+1`: open, `-1`: close
                if count[kind] < 0:  # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else:  # character is not a [balanced] bracket
            if not any(count):  # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)


def reorder_sentences(output_sentences, input):
    def custom_sort(s1, s2):
        return input.find(s1) - input.find(s2)

    output_sentences.sort(key=functools.cmp_to_key(custom_sort))
    return output_sentences


def get_summarized(input, num_sentences):
    input = clean(input)
    tokenizer = RegexpTokenizer('\w+')
    base_words = [word.lower() for word in tokenizer.tokenize(input)]
    words = [word for word in base_words if word not in stopwords.words()]
    word_frequencies = FreqDist(words)
    most_frequent_words = [pair[0] for pair in word_frequencies.most_common(100)]

    input = remove_text_inside_brackets(input, "====")

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    actual_sentences_pre = sent_detector.tokenize(input)
    actual_sentences = []
    for sentence in actual_sentences_pre:
        if len(sentence.split()) <= 6:
            continue
        else:
            actual_sentences.append(sentence)
    working_sentences = [sentence.lower() for sentence in actual_sentences]
    output_sentences = []

    for word in most_frequent_words:
        for i in range(0, len(working_sentences)):
            if word in working_sentences[i] and actual_sentences[i] not in output_sentences:
                output_sentences.append(actual_sentences[i])
                break
            if len(output_sentences) >= num_sentences:
                break

            if len(output_sentences) >= num_sentences:
                break
    for sentence in output_sentences:
        sentence.capitalize()
    return reorder_sentences(output_sentences, input)


def summarize(input, num_sentences):
    return " ".join(get_summarized(input, num_sentences))
