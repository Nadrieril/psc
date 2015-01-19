import nltk
import nltk.data


class analyser:
    """
    A class to parse natural language
    """
    tagger = None
    chunker = None

    def __init__(self, tagger=None, chunker=None):
        self.openTagger(tagger)
        self.openChunker(chunker)

    def openTagger(self, tagger):
        self.tagger = nltk.data.load(tagger)

    def openChunker(self, chunker):
        self.chunker = nltk.data.load(chunker)

    def parseSentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tagged_tokens = self.tagger.tag(tokens)
        tree = self.chunker.parse(tagged_tokens)
        return tree

alyser = analyser("taggers/treebank_aubt.pickle",
                  "chunkers/treebank_chunk_ub.pickle")
alyser.parseSentence("This is a sentence i'd like to parse. It doesn't meen"
                     "that much, but it only is a dummy example").draw()
