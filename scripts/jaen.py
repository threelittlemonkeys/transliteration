import re

cv_map = {}

cv_map["X"] = [["あ い う え お"], ["ア イ ウ エ オ"], ["ｱ ｲ ｳ ｴ ｵ"]]
cv_map["K"] = [["か き く け こ"], ["カ キ ク ケ コ"], ["ｶ ｷ ｸ ｹ ｺ"]]
cv_map["G"] = [["が ぎ ぐ げ ご", "が ぎ ぐ げ ご"], ["ガ ギ グ ゲ ゴ", "ガ ギ グ ゲ ゴ"], ["ｶﾞ ｷﾞ ｸﾞ ｹﾞ ｺﾞ"]]
cv_map["S"] = [["さ し す せ そ"], ["サ シ ス セ ソ"], ["ｻ ｼ ｽ ｾ ｿ"]]
cv_map["Z"] = [["ざ じ ず ぜ ぞ", "ざ じ ず ぜ ぞ"], ["ザ ジ ズ ゼ ゾ", "ザ ジ ズ ゼ ゾ"], ["ｻﾞ ｼﾞ ｽﾞ ｾﾞ ｿﾞ"]]
cv_map["T"] = [["た ち つ て と"], ["タ チ ツ テ ト"], ["ﾀ ﾁ ﾂ ﾃ ﾄ"]]
cv_map["D"] = [["だ ぢ づ で ど", "だ ぢ づ で ど"], ["ダ ヂ ヅ デ ド", "ダ ヂ ヅ デ ド"], ["ﾀﾞ ﾁﾞ ﾂﾞ ﾃﾞ ﾄﾞ"]]
cv_map["N"] = [["な に ぬ ね の"], ["ナ ニ ヌ ネ ノ"], ["ﾅ ﾆ ﾇ ﾈ ﾉ"]]
cv_map["H"] = [["は ひ ふ へ ほ"], ["ハ ヒ フ ヘ ホ"], ["ﾊ ﾋ ﾌ ﾍ ﾎ"]]
cv_map["B"] = [["ば び ぶ べ ぼ", "ば び ぶ べ ぼ"], ["バ ビ ブ ベ ボ", "バ ビ ブ ベ ボ"], ["ﾊﾞ ﾋﾞ ﾌﾞ ﾍﾞ ﾎﾞ"]]
cv_map["P"] = [["ぱ ぴ ぷ ぺ ぽ", "ぱ ぴ ぷ ぺ ぽ"], ["パ ピ プ ペ ポ", "パ ピ プ ペ ポ"], ["ﾊﾟ ﾋﾟ ﾌﾟ ﾍﾟ ﾎﾟ"]]
cv_map["M"] = [["ま み む め も"], ["マ ミ ム メ モ"], ["ﾏ ﾐ ﾑ ﾒ ﾓ"]]
cv_map["Y"] = [["や  ゆ  よ"], ["ヤ  ユ  ヨ"], ["ﾔ  ﾕ  ﾖ"]]
cv_map["R"] = [["ら り る れ ろ"], ["ラ リ ル レ ロ"], ["ﾗ ﾘ ﾙ ﾚ ﾛ"]]
cv_map["W"] = [["わ ゐ  ゑ を"], ["ワ ヰ  ヱ ヲ"], ["ﾜ    ｦ"]]
cv_map["V"] = [["わ゙ ゐ゙  ゑ゙ を゙"], ["ヷ ヸ  ヹ ヺ", "ヷ ヸ  ヹ ヺ"], ["ﾜﾞ    ｦﾞ"]]
cv_map["U"] = [["  ゔ  ", "  ゔ  "], ["  ヴ  ", "  ヴ  "], ["  ｳﾞ  "]]

cv_map["x"] = [["ぁ ぃ ぅ ぇ ぉ"], ["ァ ィ ゥ ェ ォ"], ["ｧ ｨ ｩ ｪ ｫ"]]
cv_map["y"] = [["ゃ  ゅ  ょ"], ["ャ  ュ  ョ"], ["ｬ  ｭ  ｮ"]]

for c, jasss in cv_map.items():
    jasss = [[jas.split(" ") for jas in jass] for jass in jasss]
    vs = "AIUEO"
    if c in ("x", "y"):
        vs = vs.lower()
    cv_map[c] = {
        v: [[jas[i] for jas in jass if jas[i]] for jass in jasss]
        for i, v in enumerate(vs)
    }

fc_map = {}

fc_map[""] = ["", "", ""]
fc_map["t"] = ["っ", "ッ", "ｯ"]
fc_map["N"] = ["ん", "ン", "ﾝ"]

def normalize(x):
     x = re.sub("^[Xx]", "", x)
     x = x.lower()
     return x

out = []

for x1 in "XKGSZTDNHBPMYRWVUxy":
    vs = "AIUEO"
    if x1 in ("x", "y"):
        vs = vs.lower()
    for x2 in vs:
        for k, y1s in enumerate(cv_map[x1][x2]):
            for y1 in y1s:
                for x3, y2 in fc_map.items():
                    out.append((x1 + x2 + x3, y1 + y2[k]))

pl = []

for x1 in "XKGSZTDNHBPMRV":
    for k, y1s in enumerate(cv_map[x1]["U"]):
        for y1 in y1s:
            pl.append([x1 + "U", y1, k])

for x1, y1, k in pl:
    for x2, y2 in cv_map["x"].items():
        for x3, y3 in fc_map.items():
            out.append((x1 + x2 + x3, y1 + y2[k][0] + y3[k]))

pl = []

for x1 in "XKGSZTDNHBPMRV":
    for k, y1s in enumerate(cv_map[x1]["I"]):
        for y1 in y1s:
            pl.append([x1 + "I", y1, k])

for x1, y1, k in pl:
    for x2, y2 in cv_map["x"].items():
        for x3, y3 in fc_map.items():
            out.append((x1 + x2 + x3, y1 + y2[k][0] + y3[k]))
pl = []

for x1 in "KGSZTDNHBPMRV":
    for k, y1s in enumerate(cv_map[x1]["I"]):
        for y1 in y1s:
            pl.append([x1 + "I", y1, k])

for x1 in "TD":
    for k, y1s in enumerate(cv_map[x1]["E"]):
        for y1 in y1s:
            pl.append([x1 + "E", y1, k])

for x1 in "HU":
    for k, y1s in enumerate(cv_map[x1]["U"]):
        for y1 in y1s:
            pl.append([x1 + "U", y1, k])

for x1, y1, k in pl:
    for x2, y2 in cv_map["y"].items():
        if not y2[k]:
            continue
        x2 = "y" + x2
        for x3, y3 in fc_map.items():
            out.append((x1 + x2 + x3, y1 + y2[k][0] + y3[k]))

out.append(("N", "ん"))
out.append(("N", "ン"))
out.append(("N", "ﾝ"))

out.append(("t", "っ"))
out.append(("t", "ッ"))
out.append(("t", "ｯ"))
out.append(("d", "っ゙"))
out.append(("d", "ッ゙"))
out.append(("d", "ｯﾞ"))

out.append(("wa", "ゎ"))
out.append(("wa", "ヮ"))
out.append(("va", "ゎ゙"))
out.append(("va", "ヮ゙"))

out.append(("xU", "ぅ゙"))
out.append(("xU", "ゥ゙"))
out.append(("xU", "ｩﾞ"))

out.append(("ka", "ゕ"))
out.append(("ka", "ヵ"))
out.append(("ga", "ゕ゙"))
out.append(("ga", "ヵ゙"))
out.append(("ke", "ゖ"))
out.append(("ke", "ヶ"))
out.append(("ge", "ゖ゙"))
out.append(("ge", "ヶ゙"))

out.append(("YORI", "ゟ"))
out.append(("KOTO", "ヿ"))

for ja, en in out:
    print(ja, en)
