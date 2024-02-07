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
    V = "[aeou]y|[aeiou]+|y(?![aeou])"

    # phoneme segmentation
    _en = normalize(en)
    _en = re.sub(f" ?({V})", r" _\1_", _en)

    # onset maximalization
    _en = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", _en)

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

    # consonants
    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bdfghklmnpstvzʒθ]j|dʒj|[gk]w"
    C3 = "dz|ts|l[mn]"

    _ko = []

    for i, x in enumerate(_ipa):

        try:
            o, n, c = x
        except: # invalid syllable
            return None

        y = []

        # onset

        o = re.findall(f"{C2}|{C1}", o)

        if not o:
            y.append([""])

        for p in o:

            # syllable-initial /l/
            if p == "l":
                s = y[-1] if y else _ko[-1][-1] if _ko else None # last syllable
                if s and len(s) != 3:
                    if len(s) == 1:
                        s.append("")
                    s.append("l")

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
                y.append([])

            # syllable-final /lm/, /ln/
            elif p in ("lm", "ln"):
                y[-1].append("l")
                y.append(["l", "ə"])
                p = p[1]

            # syllable-final /r/
            elif p == "r":
                if y[-1][-1] == "e": # air /ɛɹ/ -> /ɛəɹ/
                    y.append(["", "ə"])
                p = ""

            # syllable-initial consonants
            elif p[-1] not in ("b", "k", "l", "m", "n", "p", "ŋ"):
                y.append([])

            y[-1].append(p)

        _ko.append(y)

    ko = ipa_to_hangeul(_en, _ko)

    return ko

def ipa_to_hangeul(_en, _ko) : # IPA to Hangeul syllables

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
        _ko = syllabify_enko(_en, _ipa)

        if _ko == None:
            print(en, ipa, sep = "\t")
            continue

        print(_ipa)

        _en = ".".join("".join(x) for x in _en)
        _ipa = ".".join("".join(x) for x in _ipa)

        print(en, ipa, _en, _ipa, _ko, sep = "\t")