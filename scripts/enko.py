import sys
import re
import jamofy

# sonority sequencing principle (SSP)
# sonority hierarchy
# vowels > glides > liquids > nasals > fricatives > affricates > plosives

def normalize(x):

    x = re.sub(r"\s+", " ", x).strip()

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

def syllabify_graphemes(gr):

    # onsets

    C1 = "[bcdgkprstw]h|([bdfgjklmnprstxvz])\\2|[bcdfghjklmnpqrstvwxyz]"
    C2 = "[bcfgkps]l|[bcdfgkpt]r|[cdgkpst]w|s[cfkmnpqt]"
    C3 = "s[ckp][lr]|s[ft]r|skw"

    # vowels

    V1 = "[aeiou]|y(?![aeou])"
    V2 = "[aeo]a|[aeiou]e|[aeo][ouw]|[aeou][iy]"
    V3 = "(?<=[st])io(?=n)"

    # grapheme segmentation

    gr = normalize(gr)
    gr = re.sub(f" ?({V3}|{V2}|{V1})", r" _\1_", gr)

    # onset maximalization
    gr = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", gr)
    gr = re.sub("^([^ ]+) ", r"\1", gr)

    # coda concatenation

    gr = re.sub("(_[^ ]+)(( [^ _]+)+)(?=[ ])", concat_coda, gr)

    # post-processing

    gr = gr.strip()
    gr = [x.split("_") for x in gr.split(" ")]

    return gr

def syllabify_phonemes(ph):

    # onsets

    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bfgkps]l|[bdfgkptθ]r|[dgkst]w|[bdfghklmnpstvzʒθ]j|dʒj|s[kmnpt]"
    C3 = "s[kmpt]j|s[kp][lr]|s[ft]r|skw"

    # vowels

    V1 = "[aeiouæə]" # monophthongs
    V2 = "[aoə][iu]|ei|[eiu]ə" # diphthongs
    V3 = "[aeo]iə|[aoə]uə" # triphthongs

    # phoneme segmentation

    ph = normalize(ph)
    ph = re.sub(f" ?({V2}|{V1})", r" _\1_", ph)

    # onset maximalization

    ph = re.sub(f" ?({C3}|{C2}|{C1}) _", r" \1_", ph)

    # coda concatenation

    ph = re.sub("(_[^ ˈˌ.]+)(( [^ _]+)+)(?=[ ˈˌ.])", concat_coda, ph)

    # post-processing

    ph = re.sub(" ?[ˈˌ] ?", " ", ph)
    ph = ph.strip()
    ph = [x.split("_") for x in ph.split(" ")]

    return ph

def transliterate_enko(gr, ph):

    gr = syllabify_graphemes(gr)
    ph = syllabify_phonemes(ph)

    align_syllables(gr, ph)

    ko = transliterate_enko_phase1(ph)
    ko = transliterate_enko_phase2(ko)

    return gr, ph, ko

def align_syllables(gr, ph):

    if len(gr) == 1:
        return

    if len(gr) - len(ph) < 2:
        return

    print(len(gr), gr)
    print(len(ph), ph)
    for s in ph:
        print(s)
    print()

    for i, (a, b) in enumerate(zip(gr, ph)):

        if not i:
            continue

        if len(a) < 2 or len(b) < 2:
            continue

        if b[2] and b[2][0] == "r":
            pass # continue

        # vowel reduction

        '''
        if a[1] == "i" and b[0][-1:] not in ("j", "ʃ", "ʒ") and b[1] == "ə" \
        and not (len(gr) > i + 1 and "".join(gr[i + 1])[:3] == "ble"):
            b[1] = "i"
            flags.add("VR")
        '''

        # syllabic consonants

        if re.match("[bcdfgkpstz]le", a[0] + a[1]) \
        and (b[1] + b[2])[:2] == "əl":
            b[1] = "" # remove the schwa

def transliterate_enko_phase1(ph):

    # consonants

    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bdfghklmnpstvzʒθ]j|dʒj|[gk]w"
    C3 = "dz|ts|l[mn]|rl"

    ko = []

    for i, x in enumerate(ph):

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

            if p[0] == "l" and (y or ko):
                s = y[-1] if y else ko[-1][-1]
                if len(s) != 3:
                    if len(s) == 1:
                        s.append("")
                    s.append("l")

            # syllable-initial /m/, /n/

            if p in ("m", "n") and ko:
                s = ko[-1]
                if len(s[-1]) == 3 and s[-1][2] in ("k", "p"):
                    s.append([s[-1].pop()])

            y.append([p])

        # nucleus

        # non-word-final diphong /ou/

        if (c or i < len(ph) - 1) and n == "ou":
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
                    else:
                        k = y[-1].pop()
                        if k:
                            y.append([k, ""])
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

        ko.append(y)

    return ko

def transliterate_enko_phase2(_ko): # IPA to Hangeul syllables

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

        flags = []

        line = line.strip()
        gr, ph = line.split("\t")
        gr, ph, ko = transliterate_enko(gr, ph)

        if not ko:
            # print(gr, ph, "", "", "", sep = "\t")
            continue

        if len(gr) == len(ph):
            continue

        gr = ".".join("".join(x) for x in gr)
        ph = ".".join("".join(x) for x in ph)

        if flags:
            pass

        # print(line, gr, ph, ko, sep = "\t")

# TODO
# hotdog
# accidental
# fuel
# nibble
# approximate
