try: # use these if Python 2
    unicode_chr, range = unichr, xrange
except NameError: # Python 3
    unicode_chr = chr

def makeString(charMax):
    s = []
    for i in range(1,charMax):
        try:
            char = unicode_chr(i)
        except ValueError:
            continue # can't map to unicode, try next x
        s.append(char)
    return s

n=60
l=makeString(1024)
ll = [l[i:i + n] for i in range(0, len(l), n)]
with open("unicode-test.dat",'w',encoding='utf-8') as ofh:
    for t in ll:
        ofh.write(''.join(t))


