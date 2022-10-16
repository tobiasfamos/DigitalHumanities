"""
Access to the French plays
"""


import os
import re
import collections
import lxml.etree
import matplotlib.pyplot as plt
import numpy as np
import nltk
import nltk.tokenize
from scipy import stats


#
# French Theater in XML format
#
# A larger example with XML files
#
PUNCT_RE = re.compile(r'[^\w\s]+$')

def is_punct(string):
    """Check if STRING is a punctuation marker or a sequence of
       punctuation markers.
    """
    return PUNCT_RE.match(string) is not None

def preprocess_text(text, language='French', lowercase=True):
    if lowercase:
        text = text.lower()
    if (language == 'French'):
        text = re.sub("-", " ", text)
        text = re.sub("l'", "le ", text)
        text = re.sub("d'", "de ", text)
        text = re.sub("c'", "ce ", text)
        text = re.sub("j'", "je ", text)
        text = re.sub("m'", "me ", text)
        text = re.sub("qu'", "que ", text)
        text = re.sub("'", " ' ", text)
        text = re.sub("quelqu'", "quelque ", text)
        text = re.sub("aujourd'hui", "aujourdhui", text)
    tokens = nltk.tokenize.word_tokenize(text, language=language)
    tokens = [token for token in tokens if not is_punct(token)]
    return tokens

# Start the job

subgenres = ('Comédie', 'Tragédie', 'Tragi-comédie')

plays, titles, genres = [], [], []
authors, years = [], []


for fn in os.scandir('data/theatre-classique'):
    # Only include XML files
    if not fn.name.endswith('.xml'):
        continue
    tree   = lxml.etree.parse(fn.path)
    genre  = tree.find('//genre')
    title  = tree.find('//title')
    author = tree.find('//author')
    year   = tree.find('//date')
    if genre is not None and genre.text in subgenres:
        lines = []
        for line in tree.xpath('//l|//p'):
            lines.append(' '.join(line.itertext()))
        text = '\n'.join(lines)
        plays.append(text)
        genres.append(genre.text)
        titles.append(title.text)
        if author is not None:
            authors.append(author.text)
        else:
            authors.append('')
        if year is not None:
            years.append(year.text)
        else:
            years.append('')

#
#
#
print (len(plays), len(genres), len(titles), len(authors), len(years))

# %% tokenization takes time
plays_tok = [preprocess_text(play, 'French') for play in plays]


sizeComedie, sizeTragedie, sizeTragiComedie = [], [], []

for anIndex in range(len(plays_tok)):
   aSize = len(plays_tok[anIndex])
   if (genres[anIndex] == 'Comédie'):
      sizeComedie.append(aSize)
   elif (genres[anIndex] == 'Tragédie'):
      sizeTragedie.append(aSize)
   else:
      sizeTragiComedie.append(aSize)

