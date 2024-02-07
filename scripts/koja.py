ic = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # initial consonants
mv = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # medial vowels
fc = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # final consonants

css = "ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅㅆ ㅇ ㅈ ㅊㅉ ㄲㅋ ㄸㅌ ㅃㅍ ㅎ".split(" ")

cv_map = {
    "ㅏ": "ガ ナ ダ ラ マ バ サ ア ザ チャ カ タ パ ハ",
    "ㅐㅔ": "ゲ ネ デ レ メ ベ セ エ ゼ チェ ケ テ ペ ヘ",
    "ㅑ": "ギャ ニャ デャ リャ ミャ ビャ シャ ヤ ジャ チャ キャ テャ ピャ ヒャ",
    "ㅒㅖ": "ギェ ニェ ディェ リェ ミェ ビェ シェ イェ ジェ チェ キェ ティェ ピェ ヒェ",
    "ㅓㅗ": "ゴ ノ ド ロ モ ボ ソ オ ゾ チョ コ ト ポ ホ",
    "ㅕㅛ": "ギョ ニョ デョ リョ ミョ ビョ ショ ヨ ジョ チョ キョ テョ ピョ ヒョ",
    "ㅘ": "グァ ヌァ ドゥァ ルァ ムァ ブァ スァ ウァ ズァ ツァ クァ トゥァ プァ ファ",
    "ㅙㅚㅞ": "グェ ヌェ ドゥェ ルェ ムェ ブェ スェ ウェ ズェ ツェ クェ トゥェ プェ フェ",
    "ㅜㅡ": "グ ヌ ドゥ ル ム ブ ス ウ ズ ツ ク トゥ プ フ",
    "ㅝ": "グォ ヌォ ドゥォ ルォ ムォ ブォ スォ ウォ ズォ ツォ クォ トゥォ プォ フォ",
    "ㅟ": "グィ ヌィ ドゥィ ルィ ムィ ブィ スィ ウィ ズィ ツィ クィ トゥィ プィ フィ",
    "ㅠ": "ギュ ニュ デュ リュ ミュ ビュ シュ ユ ジュ チュ キュ テュ ピュ ヒュ",
    "ㅢㅣ": "ギ ニ ディ リ ミ ビ シ イ ジ チ キ ティ ピ ヒ"
}

fc_map = {
    "ㄱㄲㄳㄺㅋ": "ク",
    "ㄷㅅㅆㅈㅊㅌㅎ": "ッ",
    "ㄹㄼㄽㄾㅀ": "ル",
    "ㄻㅁ": "ム",
    "ㄴㄵㄶㅇ": "ン",
    "ㅂㅄㄿㅍ": "プ"
}

for vs, jas in cv_map.items():
    cv_map[vs] = {cs: ja for cs, ja in zip(css, jas.split(" "))}

for i in range(len(ic)):
    for j in range(len(mv)):

        for vs in cv_map:
            if mv[j] in vs:
                for cs in cv_map[vs]:
                    if ic[i] in cs:
                        cv = cv_map[vs][cs]
                        break
                break

        for k in range(len(fc)):
            ko = chr(0xAC00 + i * 21 * 28 + j * 28 + k)

            if not k:
                print(ko, cv, sep = "\t")
                continue

            for cs in fc_map:
                if fc[k] in cs:
                    print(ko, cv + fc_map[cs], sep = "\t")
                    break
