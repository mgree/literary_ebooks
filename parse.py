import sys, os, glob, codecs
import nltk

try:
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
except:
    tokenizer = None
    
def tokenize(text, train = True):
    global tokenizer
    
    if train or tokenizer is None:
        trainer = nltk.tokenize.punkt.PunktTrainer()
        trainer.train(text)
        tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(trainer.get_params())

    return tokenizer.tokenize(text)

def parse(text):
    for raw in tokenize(text):
        yield raw.replace("\r\n\r\n","\n").replace("\r\n"," ")

def golf(ss,length = 140):
    poss = []
    
    for s in ss:
        if len(s) == length:
            yield s
            
        if len(s) < length:
            poss = map(lambda p: p + " " + s, poss) + [s]

            for k in filter(lambda p: len(p) == length,poss):
                yield k
            poss = filter(lambda p: len(p) < length, poss)
        
if __name__ == '__main__':
    args = dict(enumerate(sys.argv))
    src = args.get(1,"-")
    
    if src == '-':
        f = sys.stdin
    else:
        f = codecs.open(src,"r","utf8")

    sentences = parse(f.read())
    for s in golf(sentences):
        print s
