ic = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # initial consonants
mv = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # medial vowels
fc = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # final consonants

css = "ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅㅆ ㅇ ㅈ ㅊㅉ ㄲㅋ ㄸㅌ ㅃㅍ ㅎ".split(" ")

cv_map = dict()

cv_map["ㅏ"] = "ガ ナ ダ ラ マ バ サ ア ザ チャ カ タ パ ハ"
cv_map["ㅐㅔ"] = "ゲ ネ デ レ メ ベ セ エ ゼ チェ ケ テ ペ ヘ"
cv_map["ㅑ"] = "ギャ ニャ デャ リャ ミャ ビャ シャ ヤ ジャ チャ キャ テャ ピャ ヒャ"
cv_map["ㅒㅖ"] = "ギェ ニェ ディェ リェ ミェ ビェ シェ イェ ジェ チェ キェ ティェ ピェ ヒェ"
cv_map["ㅓㅗ"] = "ゴ ノ ド ロ モ ボ ソ オ ゾ チョ コ ト ポ ホ"
cv_map["ㅕㅛ"] = "ギョ ニョ デョ リョ ミョ ビョ ショ ヨ ジョ チョ キョ テョ ピョ ヒョ"
cv_map["ㅘ"] = "グァ ヌァ ドゥァ ルァ ムァ ブァ スァ ウァ ズァ ツァ クァ トゥァ プァ ファ"
cv_map["ㅙㅚㅞ"] = "グェ ヌェ ドゥェ ルェ ムェ ブェ スェ ウェ ズェ ツェ クェ トゥェ プェ フェ"
cv_map["ㅜㅡ"] = "グ ヌ ドゥ ル ム ブ ス ウ ズ ツ ク トゥ プ フ"
cv_map["ㅝ"] = "グォ ヌォ ドゥォ ルォ ムォ ブォ スォ ウォ ズォ ツォ クォ トゥォ プォ フォ"
cv_map["ㅟ"] = "グィ ヌィ ドゥィ ルィ ムィ ブィ スィ ウィ ズィ ツィ クィ トゥィ プィ フィ"
cv_map["ㅠ"] = "ギュ ニュ デュ リュ ミュ ビュ シュ ユ ジュ チュ キュ テュ ピュ ヒュ"
cv_map["ㅢㅣ"] = "ギ ニ ディ リ ミ ビ シ イ ジ チ キ ティ ピ ヒ"

for vs, zhs in cv_map.items():
    cv_map[vs] = {cs: zh for cs, zh in zip(css, zhs.split(" "))}

fc_map = dict()

fc_map["ㄱㄲㄳㄺㅋ"] = "ク"
fc_map["ㄷㅅㅆㅈㅊㅌㅎ"] = "ッ"
fc_map["ㄹㄼㄽㄾㅀ"] = "ル"
fc_map["ㄻㅁ"] = "ム"
fc_map["ㄴㄵㄶㅇ"] = "ン"
fc_map["ㅂㅄㄿㅍ"] = "プ"

for i in range(len(ic)):
    for j in range (len(mv)):
        cv = ""
        for vs in cv_map:
            if mv[j] in vs:
                for cs in cv_map[vs]:
                    if ic[i] in cs:
                        cv = cv_map[vs][cs]
                        break
        for k in range(len(fc)):
            s = chr(0xAC00 + i * 21 * 28 + j * 28 + k)
            if not k:
                print(s, cv, sep = "\t")
                continue
            for cs in fc_map:
                if fc[k] in cs:
                    print(s, cv + fc_map[cs], sep = "\t")
                    break
