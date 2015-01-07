from nltk import word_tokenize, sent_tokenize, pos_tag

"""
Tokenizers.
"""


def tokenize(text):
    """
    Split a text into tokens (words, morphemes, names and punctuation).
    """
    return custom_word_tokenize(refactor(text))

def refactor(text):
    res=text
    for c in ALWAYS_REMOVE:
        res=res.replace(c," ")
    return res


MAJ=("ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÙŒ")
PUNKT=(";.,?!:_()'/’\u2019()[]=")

ALWAYS_REMOVE="()[]="

      


def tokenize_and_tag(text):
    """
    Yields a list of sentences.
    Each sentence is a list of words, without punctuation.
    We add spaces before Uppercase letters, to make sure names are separated
    (which is not always the case in our raw data)
    All words are kept, including : remaining punctuation, digits, small words or letters.
    """
    for sent in custom_sent_tokenize(text):
        words=[]
        sent2=sent
        for i in MAJ:
            sent2=sent2.replace(i," "+i)
        for i in PUNKT:
            sent2=sent2.replace(i," ")
        split=word_tokenize(sent2)
        yield (pos_tag(split))




def concepts_tokenize(text):
    words=[]
    for sent in custom_sent_tokenize(text):
        sent2=sent
        for i in MAJ:
            sent2=sent2.replace(i," "+i)
        for i in PUNKT:
            sent2=sent2.replace(i," ")
        split=word_tokenize(sent2)
        tokens=pos_tag(split)
        for key,val in tokens:
            if val in USEFUL_TAGS and not contains_digits(key) and key not in DISMISS:#suppress NNP !!
                words.append([key,val])
    return words       


BOUNDARIES=["!",".","?","\n","'"]

def custom_sent_tokenize(text):
    temp=[]
    sents=[]
    car2=' '
    for car in text:
        if (car in MAJ and car2 != ' '):
            sents.append(''.join(temp))
            temp=[]
            temp.append(car)
        elif car not in BOUNDARIES:
            temp.append(car)
        else:
            sents.append(''.join(temp))
            temp=[]
        car2=car
    return sents

def custom_word_tokenize(text):
    """
    Tokenizer which recognizes named_entities, and keeps the order of the words.
    """
    words=[]
    for sent in custom_sent_tokenize(text):
        split = word_tokenize(sent)
        tokens = pos_tag(split)
        temp = []
        for key,val in tokens:
            if val=='NNP':
                temp.append(key)
            else:
                if temp:
                    words.append(' '.join(temp))
                    temp=[]
                words.append(key)
        if temp:
            words.append(' '.join(temp))
            temp=[]
    return words



if __name__=="__main__":
    text="""Peyton Manning will have a new left tackle protecting his blindside after the Denver Broncos placed Ryan Clady on season-ending injured reserve Wednesday.

Clady hurt his left foot Sunday when New York Giants defensive lineman Cullen Jenkins rolled up on him while the Broncos were trying to run out the clock in their 41-23 win. Clady will soon undergo surgery for what's being called a Lisfranc tear, which involves a separation of ligaments and joints in the foot.

Chris Clark, a fifth-year journeyman, will take the place of Clady - the undisputed leader on the line - and make his first career start at left tackle Monday night when the Broncos (2-0) host the Oakland Raiders (1-1).

''Stepping up into a role like this, it's not going to be hard for me to adjust,'' said Clark, who received a two-year contract extension on Monday. ''It's not about filling a guy's shoes for me. It's about me creating my legacy, just helping the team the best way I can and doing my job.''

Still, those are some big cleats for Clark to fill.
"""

    for w in (tokenize_and_tag(text)):
        print(w)
