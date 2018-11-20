# -*- coding: utf-8 -*-
import nltk
import regex as regex


def remove_stopwords(text):
    chars = ['.', '/', '\'', '"', '$', '%', '^', '&', '*', '(', ')', '-', '_',
             '+', '=', '@', ':', ';', '~', '`', '´', '\\', ',', '<', '>', '|',
             '[', ']', '{', '}', 'º', 'ª', '#', '1', '2', '3', '4', '5', '6',
             '7', '8', '9', '0']
    newText = [t for t in text if t not in chars]
    stopwords = nltk.corpus.stopwords.words('portuguese')

    wordsArray = []

    newText = ''.join(newText)
    words = newText.split()

    for w in words:
        newWord = regex.sub(u'', t)
        if not newWord == u'':
            wordsArray.append(newWord)

    content = [w for w in wordsArray if w.lower().strip() not in stopwords]

    return content

#nltk.download()

print(remove_stopwords("teste. para ver # se $ está, removendo. Tudo!"))
#print(nltk.corpus.stopwords.words('portuguese'))