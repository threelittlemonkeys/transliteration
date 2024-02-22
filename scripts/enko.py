import sys
import re
import jamofy

# sonority sequencing principle (SSP)
# sonority hierarchy
# vowels > glides > liquids > nasals > fricatives > affricates > plosives

def normalize(x):

    x = re.sub("\s+", " ", x).strip()

    x = re.sub("[aàáɑɒάαὰ]", "a", x)
    x = re.sub("[eèéɛέὲ]", "e", x)
    x = re.sub("[iìíɪ]", "i", x)
    x = re.sub("[oòóɔɔ̀]", "o", x)
    x = re.sub("[uùúʊ]", "u", x)
    x = re.sub("[gɡ]", "g", x)
    x = re.sub("[lɫ]", "l", x)
    x = re.sub("[rɹ]", "r", x)
    x = re.sub("[æǽӕ]", "æ", x)
    x = re.sub("[əɜʌ]", "ə", x)
    x = re.sub("ɝ", "ər", x)
    x = re.sub("ɪr", "ɪər", x)
    x = re.sub("ʤ", "dʒ", x)
    x = re.sub("ʧ", "tʃ", x)
    x = re.sub("ː", "", x)

    x = re.sub("(?=<[^d]ʒ)j(?=ə)", "", x)
    x = re.sub("(?=<[^t]ʃ)j(?=ə)", "", x)

    x = re.sub("[^abcdefghijklmnopqrstuvwxyzæðŋəʃʒθˈˌ.]", "", x)

    return x

def concat_coda(m):
    return m.group(1) + "_" + m.group(2).replace(' ', '')

def syllabify_ipa(x):

    # onsets
    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bfgkps]l|[bdfgkptθ]r|[dgkst]w|[bdfghklmnpstvzʒθ]j|dʒj|s[kmnpt]"
    C3 = "s[kmpt]j|s[kp][lr]|s[ft]r|skw"

    # vowels
    V1 = "[aeiouæə]" # monophthongs
    V2 = "[aoə][iu]|ei|[eiu]ə" # diphthongs
    V3 = "[aeo]iə|[aoə]uə" # triphthongs

    # phoneme segmentation
    _ipa = normalize(x)
    _ipa = re.sub(f" ?({V2}|{V1})", r" _\1_", _ipa)

    # onset maximalization
    _ipa = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", _ipa)

    # coda concatenation
    _ipa = re.sub("(_[^ ˈˌ.]+)(( [^ _]+)+)(?=[ ˈˌ.])", concat_coda, _ipa)

    # post-processing
    _ipa = re.sub(" ?[ˈˌ] ?", " ", _ipa)
    _ipa = _ipa.strip()
    _ipa = [x.split("_") for x in _ipa.split(" ")]

    return _ipa

def syllabify_en(en, _ipa):

    # onsets
    C1 = "[bcdgkprstw]h|([bdfgjklmnprstxvz])\\2|[bcdfghjklmnpqrstvwxyz]"
    C2 = "[bcfgkps]l|[bcdfgkpt]r|[cdgkpst]w|s[cfkmnpqt]"
    C3 = "s[ckp][lr]|s[ft]r|skw"

    # vowels
    V1 = "[aeiou]|y(?![aeou])"
    V2 = "[aeo]a|[eiou]e|[aeo][ouw]|[aeou][iy]"
    V3 = "(au|e?i)gh|(?<=[st])io(?=n)"

    # phoneme segmentation
    _en = normalize(en)
    _en = re.sub(f" ?({V3}|{V2}|{V1})", r" _\1_", _en)

    # onset maximalization
    _en = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", _en)
    _en = re.sub("^([^ ]+) ", r"\1", _en)

    # coda concatenation
    _en = re.sub("(_[^ ˈˌ]+)(( [^ _]+)+)(?=[ ˈˌ])", concat_coda, _en)

    # post-processing
    _en = _en.strip()
    _en = [x.split("_") for x in _en.split(" ")]

    # silent e
    if len(_en) > len(_ipa) and _en[-1][1] == "e" and _en[-1][2] in "ds":
        s = "".join(_en[-1])
        _en.pop()
        _en[-1][-1] += s

    return _en

def syllabify_enko(_en, _ipa):

    _en = [[x for x in xs] for xs in _en]
    _ipa = [[x for x in xs] for xs in _ipa]

    _en = syllabify_enko_phase1(_en, _ipa)
    _ko = syllabify_enko_phase2(_en, _ipa)
    ko = syllabify_enko_phase3(_en, _ko)

    return ko

def syllabify_enko_phase1(_en, _ipa):

    if len(_ipa) == 1:
        return _en

    if len(_en) != len(_ipa):
        return _en

    for i, (a, b) in enumerate(zip(_en, _ipa)):

        if not i:
            continue

        if len(a) < 2 or len(b) < 2:
            continue

        if b[2] and b[2][0] == "r":
            continue

        if a[1] == "i" and b[1] == "ə": # reduced vowel i
            b[1] = "i"

        elif re.match("[bcdfgkpstz]l", a[0]) and a[1] == "e" \
        and len(b[0]) == 1 and b[1] == "ə" and b[2][0] == "l":
            b[1] = [""]

    return _en

def syllabify_enko_phase2(_en, _ipa):

    # consonants
    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bdfghklmnpstvzʒθ]j|dʒj|[gk]w"
    C3 = "dz|ts|l[mn]|rl"

    _ko = []

    for i, x in enumerate(_ipa):

        try:
            o, n, c = x
        except: # invalid syllable
            return ""

        y = []

        # onset

        o = re.findall(f"{C2}|{C1}", o)

        if not o:
            y.append([""])

        for p in o:

            # syllable-initial /l/
            if p == "l" and (y or _ko):
                s = y[-1] if y else _ko[-1][-1]
                if len(s) != 3:
                    if len(s) == 1:
                        s.append("")
                    s.append("l")

            # syllable-initial /m/, /n/
            if p in ("m", "n") and _ko:
                s = _ko[-1]
                if len(s[-1]) == 3 and s[-1][2] in ("k", "p"):
                    s.append([s[-1].pop()])

            y.append([p])

        # nucleus

        # non-word-final diphong /ou/
        if (c or i < len(_ipa) - 1) and n == "ou":
            n = "o"

        for p in n:
            if len(y[-1]) == 2:
                y.append([""])
            y[-1].append(p)

        # coda

        c = re.findall(f"{C3}|{C2}|{C1}", c)

        for p in c:

            # coda already occupied
            if len(y[-1]) != 2:

                # syllable-final /l/, /m/, /n/
                if p in ("l", "m", "n"):
                    if len(y[-1]) == 1:
                        y[-1].append("")
                    elif y[-1][-1] == "":
                        y[-1].pop()

                else:
                    y.append([])

            # syllable-final /lm/, /ln/
            elif p in ("lm", "ln"):
                y[-1].append("l")
                y.append(["l", "ə"])
                p = p[1]

            # syllable-final /r/
            elif p == "r":
                if y[-1][-1][-1] in ("e", "i"): # /ɛɹ/, /ɪɹ/
                    y.append(["", "ə"]) # /ɛə/, /ɪə/
                p = ""

            # syllable-final /rl/
            elif p == "rl":
                p = "l"

            # syllable-initial consonants
            elif p not in ("b", "k", "l", "m", "n", "p", "ŋ"):
                y.append([])

            y[-1].append(p)

        _ko.append(y)

    return _ko

def syllabify_enko_phase3(_en, _ko) : # IPA to Hangeul syllables

    _ENKO = {
        **{a: b for a, b in zip(
        "abdefghiklmnoprstuvzæðŋəʃʒθ",
        "ㅏㅂㄷㅔㅍㄱㅎㅣㅋㄹㅁㄴㅗㅍㄹㅅㅌㅜㅂㅈㅐㄷㅇㅓㅅㅈㅅ")},
        **{a: b for a, b in zip(
        ("dz", "dʒ", "ts", "tʃ"),
        ("ㅈ", "ㅈ", "ㅊ", "ㅊ"))},
        **{a: b for a, b in zip(
        ("ja", "je", "ji", "jo", "ju", "jæ", "jə"),
        ("ㅑ", "ㅖ", "ㅣ", "ㅛ", "ㅠ", "ㅒ", "ㅕ"))},
        **{a: b for a, b in zip(
        ("wa", "we", "wi", "wo", "wu", "wæ", "wə"),
        ("ㅘ", "ㅞ", "ㅟ", "ㅝ", "ㅜ", "ㅙ", "ㅝ"))},
    }

    ko = ""

    for xs in _ko:
        for x in xs:

            if len(x) == 1:
                x.append("")
            if x[0][-1:] in ("j", "w"):
                x[0], j = x[0][:-1], x[0][-1]
                x[1] = j + x[1]
            if x[0] == "ʃ" and x[1]:
                x[1] = "j" + x[1]
            if x[0] == "":
                x[0] = "ㅇ"
            if x[1] == "":
                x[1] = "ㅣ" if x[0][-1] in ("ʃ", "ʒ") else "ㅡ"
            if x[1] == " ":
                x[1] = "ㅡ"

            x = [_ENKO.get(p, p) for p in x]

            if len(x) == 3:
                if x[2] == "ㅋ":
                    x[2] = "ㄱ"
                if x[2] == "ㅌ":
                    x[2] = "ㅅ"
                if x[2] == "ㅍ":
                    x[2] = "ㅂ"

            ko += jamofy.jamo_to_syl(x)

    return ko

if __name__ == "__main__":

    for line in sys.stdin:

        line = line.strip()
        en, ipa = line.split("\t")

        _ipa = syllabify_ipa(ipa)
        _en = syllabify_en(en, _ipa)
        ko = syllabify_enko(_en, _ipa)

        # print(len(_ipa), _ipa)
        # print(len(_en), _en)

        if ko == None:
            print(en, ipa, "", "", "", sep = "\t")
            continue

        _en = ".".join("".join(x) for x in _en)
        _ipa = ".".join("".join(x) for x in _ipa)

        print(en, ipa, _en, _ipa, ko, sep = "\t")
