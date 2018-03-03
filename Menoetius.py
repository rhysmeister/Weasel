"""
Menoetius is the Greek God of Rudeness - http://www.godchecker.com/pantheon/greek-mythology.php?deity=MENOETIUS

This Python class is an attempt to implement some of the ideas found in the following paper;

"Automated Hate Speech Detection and the Problem of Offensive Language"

https://arxiv.org/pdf/1703.04009.pdf

Stemming - https://pypi.python.org/pypi/stemming/1.0
Categorizing and Tagging Words - http://www.nltk.org/book/ch05.html
Text stats - https://pypi.python.org/pypi/textstat

 pip install stemming textstat nltk pysentiment

"""

import copy, nltk, pysentiment
from textstat.textstat import textstat

class UnsupportedStemmingException(Exception):
    pass

class Menoetius:

    original_text = None
    lowercase_text = None
    stems = None
    pos_tags = None
    sentiment_scores = None
    text_stats = None

    def __init__(self, text):
        assert isinstance(text, str)
        self.original_text = copy.deepcopy(text)
        self.lowercase_text = self.do_lowercase(text)
        self.stems = self.do_stemming(self.do_split(self.lowercase_text, " "))
        self.pos_tags = self.do_pos(self.lowercase_text)
        self.sentiment_scores = self.do_sentiment_scores(self.lowercase_text)
        self.text_stats = self.do_text_stats(self.lowercase_text)

    def do_lowercase(self, text):
        return text.lower()

    def do_split(self, text, split_by=" "):
        return text.split(split_by)

    def do_stemming(self, text_array, stemmer="porter2"):
        assert isinstance(text_array, list)
        if stemmer == "porter2":
            from stemming.porter2 import stem
        elif stemmer == "lovins":
            from stemming.lovins import stem
        elif stemmer == "paicehusk":
            from stemming.paicehusk import stem
        elif stemmer == "porter":
            from stemming.porter import stem
        else:
            raise UnsupportedStemmingException("We don't support the stemmer {0}".format(stemmer))
        stems = []
        for word in text_array:
            stems.append(stem(word))
        return stems

    def do_pos(self, text):
        return nltk.pos_tag(text)

    def do_sentiment_scores(self, text):
        hiv4 = pysentiment.HIV4()
        tokens = hiv4.tokenize(text)
        score = hiv4.get_score(tokens)
        return (tokens, score)

    def do_text_stats(self, text):
        ### Syllable Count
        syllable_count = textstat.syllable_count(text)
        ### Lexicon Count
        lexicon_count = textstat.lexicon_count(text, True)
        ### Sentence Count
        sentence_count = textstat.sentence_count(text)
        ### The Flesch Reading Ease formula
        try:
            flesch_reading_ease = textstat.flesch_reading_ease(text)
        except TypeError as e:
            flesch_reading_ease = None
        #* 90-100 : Very Easy
        #* 80-89 : Easy
        #* 70-79 : Fairly Easy
        #* 60-69 : Standard
        #* 50-59 : Fairly Difficult
        #* 30-49 : Difficult
        #* 0-29 : Very Confusing
        ### The The Flesch-Kincaid Grade Level
        try:
            flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        except TypeError as e:
            flesch_kincaid_grade = None
        ## The Fog Scale (Gunning FOG Formula)
        gunning_fog = textstat.gunning_fog(text)
        ### The SMOG Index
        smog_index = textstat.smog_index(text)
        ### Automated Readability Index
        automated_readability_index = textstat.automated_readability_index(text)
        ### The Coleman-Liau Index
        try:
            coleman_liau_index = textstat.coleman_liau_index(text)
        except TypeError as e:
            coleman_liau_index = None
        ### Linsear Write Formula
        linsear_write_formula = textstat.linsear_write_formula(text)
        ### Dale-Chall Readability Score
        dale_chall_readability_score = textstat.dale_chall_readability_score(text)
        ### Readability Consensus based upon all the above tests
        try:
            text_standard = textstat.text_standard(text)
        except TypeError as e:
            text_standard = None
        return (syllable_count,
                lexicon_count,
                sentence_count,
                flesch_reading_ease,
                flesch_kincaid_grade,
                gunning_fog,
                smog_index,
                automated_readability_index,
                coleman_liau_index,
                linsear_write_formula,
                dale_chall_readability_score,
                text_standard)
