import sys, os, glob, codecs
import nltk

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def parse(f):
    for raw in tokenizer.tokenize(f):
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
