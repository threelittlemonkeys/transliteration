import sys
import re
import jamofy
from levenshtein import edit_distance

# sonority sequencing principle (SSP)
# sonority hierarchy
# vowels > glides > liquids > nasals > fricatives > affricates > plosives

g2p_thesaurus = {
    "a": {"e", "i", "æ"},
    "i": {"e", "ə"},
    "o": {"a", "u", "ə"},
    "k": {"c", "q"},
    "s": {"ʒ"},
    "t": {"ð", "θ"},
    "ʃ": {"c", "t"},
}

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
    C2 = "[bcfgkps]l|[bcdfgkpt]r|[cdgkpst]w|qu|s[cfkmnpqt]"
    C3 = "s[ckp][lr]|s[ft]r|skw|squ"

    # vowels

    V1 = "[aeio]|(?<!q)u|y(?![aeou])"
    V2 = "[aeo]a|[aeio]e|[aeo][ouw]|[aeo][iy]|(?<!q)(ue|u[iy])"
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
    C2 = "[bfgkps]l|[bdfgkptθ]r|[dghkst]w|[bdfghklmnpstvzʒθ]j|dʒj|s[kmnpt]"
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

    ph = re.sub(" ?[ˈˌ.] ?", " ", ph)
    ph = ph.strip()
    ph = [x.split("_") for x in ph.split(" ")]

    return ph

def transliterate_enko(gr, ph):

    gr = syllabify_graphemes(gr)
    ph = syllabify_phonemes(ph)

    align_syllables(gr, ph)

    en = transliterate_enko_phase1(gr, ph)
    ko = transliterate_enko_phase2(en)

    return gr, ph, ko

def align_syllables(gr, ph):

    # pre-processing

    ph_idx = [0]
    ph_seq = []

    for xs in ph:
        xs = [c for x in xs for c in x]
        ph_idx += [len(xs) + ph_idx[-1]]
        ph_seq += xs

    gr_seq = [c for xs in gr for x in xs for c in x]
    gr_seq_norm = []
    gr_seq_aligned = [[] for _ in range(len(ph_seq))]

    # syllable alignment based on edit distance

    edbt = edit_distance(
        gr_seq,
        ph_seq,
        thesaurus = g2p_thesaurus,
        backtrace = True,
        verbose = False
    )[1]

    k = -1
    for i, j, *_ in edbt:
        if i in (0, k):
            continue
        k = i
        i = max(i - 1, 0)
        j = max(min(j, len(ph_seq)) - 1, 0)
        gr_seq_aligned[j].append(gr_seq[i])

    gr_seq_aligned = [
        [x for xs in gr_seq_aligned[ph_idx[i]:ph_idx[i + 1]] for x in xs]
        for i in range(len(ph_idx) - 1)
    ]

    gr[:] = ["".join(x) for x in gr_seq_aligned]

    for i in range(len(gr) - 1):

        c = re.search("[^aeiou]+$", gr[i]) # coda
        if not c:
            continue
        c = c.group()

        if gr[i + 1] and re.match("[aeiou]", gr[i + 1]):
            # gr[i] = gr[i][:-len(c)]
            # gr[i + 1] = c + gr[i + 1]
            flags.append("")

        # print(i, c, gr[i], gr[i + 1])

    # post-processing

    for i, (g, p) in enumerate(zip(gr, ph)):

        if len(g) < 2:
            continue

        # syllabic consonants

        if re.search("[bcdfgkpstz]+le", g) and (p[1] + p[2])[:2] == "əl":
            p[1] = "" # remove the schwa

        # vowel reduction

        if re.search("(?<![aeiou])i(?![aeiou])", g) and p[1] == "ə" \
        and not (i + 1 < len(gr) and gr[i + 1][:2] == "bl") \
        and not (i + 2 < len(gr) and gr[i + 1] == "bi" and gr[i + 2] == "li"):
            p[1] = "i"

        if re.search("du", g) and p[0] == "dʒ" and p[1] in ("u", "ə") and p[2] == "":
            p[0] = "dj"
            p[1] = "u"

        # TODO

        if re.search("(?<![aeiou])o$", g) and len(p) > 1 and p[1] in ("a", "ə"):
            p[1] = "ə" if p[0] == "k" else "o"
            # flags.append("") # TODO

def transliterate_enko_phase1(gr, ph):

    # consonants

    C1 = "dʒ|tʃ|[bdfghjklmnprstvwzðŋʃʒθ]"
    C2 = "[bdfghklmnpstvzʒθ]j|dʒj|[gk]w"
    C3 = "dz|ts|l[mn]|rl"

    ko = []

    for i, (g, p) in enumerate(zip(gr, ph)):

        try:
            o, n, c = p
        except: # invalid syllable
            return ""

        y = []

        # onset

        o = re.findall(f"{C2}|{C1}", o)

        if not o:
            y.append([""])

        for x in o:

            # syllable-initial /l/

            if x[0] == "l" and (y or ko):
                s = y[-1] if y else ko[-1][-1]
                if len(s) != 3:
                    if len(s) == 1:
                        s.append("")
                    s.append("l")

            # syllable-initial /m/, /n/

            if x in ("m", "n") and ko:
                s = ko[-1]
                if len(s[-1]) == 3 and s[-1][2] in ("k", "p"):
                    s.append([s[-1].pop()])

            y.append([x])

        # nucleus

        # monosyllabify non-word-final diphong /ou/

        if n == "ou" and "ow" not in g:
            n = "o"

        for x in n:
            if len(y[-1]) == 2:
                y.append([""])
            y[-1].append(x)

        # coda

        c = re.findall(f"{C3}|{C2}|{C1}", c)

        for x in c:

            # coda already occupied

            if len(y[-1]) != 2:

                # syllable-final /l/, /m/, /n/

                if x in ("l", "m", "n"):
                    if len(y[-1]) == 1:
                        y[-1].append("")
                    else:
                        k = y[-1].pop()
                        if k:
                            y.append([k, ""])
                else:
                    y.append([])

            # syllable-final /lm/, /ln/

            elif x in ("lm", "ln"):
                y[-1].append("l")
                y.append(["l", "ə"])
                x = x[1]

            # syllable-final /r/

            elif x == "r":
                if y[-1][-1][-1] in ("e", "i"): # /ɛɹ/, /ɪɹ/
                    y.append(["", "ə"]) # /ɛə/, /ɪə/
                x = ""

            # syllable-final /rl/

            elif x == "rl":

                x = "l"

            # syllable-initial consonants

            elif x not in ("b", "k", "l", "m", "n", "p", "ŋ"):
                y.append([])

            y[-1].append(x)

        ko.append(y)

    return ko

def transliterate_enko_phase2(en): # IPA to Hangeul syllables

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

    for xs in en:
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

            if len(x) == 3: # TODO
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

        gr = ".".join("".join(x) for x in gr)
        ph = ".".join("".join(x) for x in ph)

        if not flags:
            pass # continue

        print("!" if flags else "", line, gr, ph, ko, sep = "\t")

# TODO
# terrorist
# hotdog
# accidental
# fuel
# nibble
# approximate
# population
# juang
# bilingual
# national
# exactly
# directionless
# scribed
# women
# hardened
# mature
# misanthrope
# breakout
# discover
# careful
# business
