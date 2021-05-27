import os
import sys
import re
from utils import *

class transliterate():
    def __init__(self, lp):
        self.path = (os.path.dirname(__file__) or ".") + "/data/"
        self.dict = dict()
        self.lm = dict()
        self.lp = lp
        self.window_size = 2

        tr = dict()
        if lp == "cntw":
            dicts = ("st.mono", "st.multi", "cntw.sem", "cntw.phon", "cntw.typo")
        if lp == "twcn":
            dicts = ("ts.mono", "ts.multi", "twcn.sem", "twcn.phon", "twcn.typo")
        if lp[:4] == "zhpy":
            dicts = ("zhpy.mono", "zhpy.multi", "zypy")
            if lp in ("zhpyko", "zhpyzy"):
                fo = open(self.path + lp[2:] + ".tsv")
                for line in fo:
                    a, b = line.strip().split("\t")
                    tr[a] = b
                fo.close()
        for x in dicts:
            self.load_dict(x, tr)

        if lp == "cntw":
            self.load_lm("st.prob")

        self.maxlen = max(map(len, self.dict))

    def load_dict(self, filename, tr):
        fo = open(self.path + filename + ".tsv")
        for line in fo:
            a, *b = line.strip().split("\t")
            b = list(map(remove_zh_tone_marks, b))
            b = [" ".join(tr[w] if w in tr else w for w in w.split(" ")) for w in b]
            self.dict[a] = b
        fo.close()

    def load_lm(self, filename):
        fo = open(self.path + filename + ".tsv")
        for line in fo:
            p, f, w = line.strip().split("\t")
            self.lm[w] = (float(p), int(f))
        fo.close()

    def convert(self, line, capitalize = True, spacing = True, ignore_space = True):
        sp = " " * ignore_space
        pos = [i > 0 and line[i - 1] == sp for i, w in enumerate(line) if w != sp]
        seq = list(line.replace(sp, ""))
        pos, seq = self.model1(pos, seq)
        seq = self.model2(seq)
        out = ""
        for i, w in enumerate(seq):
            sp = " " * pos[i]
            if i > 0 and self.lp[:4] == "zhpy":
                if type(seq[i]) == type(seq[i - 1]) == list:
                    sp = " " * spacing
                elif list in (type(seq[i]), type(seq[i - 1])):
                    sp = " "
            if type(w) == list:
                w = w[0]
            w = (w.capitalize() if capitalize else w for w in w.split(" "))
            out += sp + (" " * spacing).join(w)
        return out

    def model1(self, pos, seq): # rule based
        i = 0
        while i < len(seq):
            for j in range(min(self.maxlen, len(seq) - i), 0, -1):
                x = "".join(seq[i:i + j])
                if x in self.dict:
                    break
            else:
                i += 1
                continue
            y = self.dict[x]
            y = [y] if len(y) > 1 or self.lp[:4] == "zhpy" else y[0]
            pos[i:i + len(x)] = [pos[i], *[False for _ in range(len(y) - 1)]]
            seq[i:i + len(x)] = y
            i += 1 if self.lp[:4] == "zhpy" else len(y)
        return pos, seq

    def model2(self, seq): # statistical
        for i in range(len(seq)):
            if type(seq[i]) == str:
                continue
            p1 = max(0, i - self.window_size)
            p2 = min(len(seq), i + self.window_size + 1)
            p = i - p1
            ys, _ys = [], [""]
            for j in range(p1, p2):
                _ys = [y + w for w in seq[j] for y in _ys]
            for y in _ys:
                for j in range(self.window_size, 0, -1):
                    if p >= j:
                        w = y[p - j:p + 1]
                        if w in self.lm:
                            ys.append((y[p], w, *self.lm[w]))
                    if p + j <= len(y):
                        w = y[p:p + j]
                        if w in self.lm:
                            ys.append((y[p], w, *self.lm[w]))
                    if p >= j and p + j <= len(y):
                        w = y[p - j:p + j]
                        if w in self.lm:
                            ys.append((y[p], w, *self.lm[w]))
                    if len(ys):
                        break
            ys.sort(key = lambda x: (-len(x[1]), -x[2]))
            seq[i] = [(ys[0] if ys else seq[i])[0]]
        return seq

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: %s cntw|twcn|zhpy|zhpyko text" % sys.argv[0])
    tr = transliterate(sys.argv[1])
    fo = open(sys.argv[2])
    for line in fo:
        line = line.strip()
        output = tr.convert(line, capitalize = False, spacing = True)
        print(output)
    fo.close()
