def detect_bpmf(x):
    return any("\u3105" <= c <= "\u312F" for c in x)

def remove_zh_tone_marks(x):
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
