def has_zhuyin(x):
    for c in x:
        if "\u3105" <= c <= "\u312F":
            return True
    return False

def remove_diacritics(x):
    y = ""
    for c in x:
        if c in "āáǎà": c = "a"
        if c in "ēéěèêê̄ếê̌ề": c = "e"
        if c in "īíǐì": c = "i"
        if c in "ōóǒò": c = "o"
        if c in "ūúǔù": c = "u"
        if c in "üǖǘǚǜ": c = "ü"
        if c in "m̄ḿm̀": c = "m"
        if c in "ńňǹ": c = "n"
        y += c
    return y

_KSI = "g kk n d tt r m b pp s ss 0 j jj ch k t p h".split(" ")
_KSM = "a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i".split(" ")
_KSF = "k k k n n n t l k m l l l l l m p p t t ng t t k t p t".split(" ")

def romanize_ko(x):
    o = ""
    for c in x:
        u = ord(c)
        if u < 0xAC00 or u > 0xD7A3:
            o += c
            continue
        u -= 0xAC00
        f = u % 28
        m = u // 28 % 21
        i = u // 28 // 21
        if i != 11:
            o += _KSI[i]
        o += _KSM[m]
        if f > 0:
            o += _KSF[f - 1]
    return o
