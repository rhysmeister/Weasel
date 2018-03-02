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

import nltk, pysentiment

class UnsupportedStemmingException(Exception):
    pass

class Menoetius:

    original_text = None
    lowercase_text = None
    stems = None
    pos_tags = None
    sentiment_scores = None
    text_stats = None

    def __init__(text):
        assert isinstance(text, str)
        original_text = deepcopy(text)
        lowercase_text = self.to_lowercase(text)
        stems = self.do_stemming(lowercase_text)
        pos_tags = self.do_pos(lowercase_text)
        sentiment_scores = self.do_sentiment_scores(lowercase_text)
        text_stats = self.do_text_stats(lowercase_text)

    def do_lowercase(text):
        return text.lower()

    def do_split(text, split_by=" "):
        return text.split(split_by)

    def do_stemming(text_array, stemmer='porter2'):
        assert isinstance(text_array, list)
        if stemmer = "porter2":
            from stemming.porter2 import stem
        if stemmer = "lovins":
            from stemming.lovins import stem
        if stemmer = "paicehusk":
            from stemming.paicehusk import stem
        if stemmer = "porter":
            from stemming.porter import stem
        else:
            raise UnsupportedStemmingException("We don't support the stemmer {0}".format(stemmer))
        stems = []
        for word in text:
            stems.append(stem(word))
        return stems

    def do_pos(text):
        return nltk.pos_tag(text)

    def do_sentiment_scores(text):
        hiv4 = pysentiment.HIV4()
        tokens = hiv4.tokenize(text)
        score = hiv4.get_score(tokens)
        return (tokens, score)

    def do_text_stats(text):
        ### Syllable Count
        syllable_count = textstat.syllable_count(text)
        ### Lexicon Count
        lexicon_count = textstat.lexicon_count(text, True)
        ### Sentence Count
        sentence_count = textstat.sentence_count(text)
        ### The Flesch Reading Ease formula
        flesch_reading_ease = textstat.flesch_reading_ease(text)
        #* 90-100 : Very Easy
        #* 80-89 : Easy
        #* 70-79 : Fairly Easy
        #* 60-69 : Standard
        #* 50-59 : Fairly Difficult
        #* 30-49 : Difficult
        #* 0-29 : Very Confusing
        ### The The Flesch-Kincaid Grade Level
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        ## The Fog Scale (Gunning FOG Formula)
        gunning_fog = textstat.gunning_fog(text)
        ### The SMOG Index
        smog_index = textstat.smog_index(text)
        ### Automated Readability Index
        automated_readability_index = textstat.automated_readability_index(text)
        ### The Coleman-Liau Index
        coleman_liau_index = textstat.coleman_liau_index(text)
        ### Linsear Write Formula
        linsear_write_formula = textstat.linsear_write_formula(text)
        ### Dale-Chall Readability Score
        dale_chall_readability_score = textstat.dale_chall_readability_score(text)
        ### Readability Consensus based upon all the above tests
        text_standard = textstat.text_standard(text)
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
