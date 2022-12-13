ic = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # initial consonants
mv = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # medial vowels
fc = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # final consonants

css = "ㄱㄲ ㄴ ㄷㄸ ㄹ ㅁ ㅂㅃ ㅅㅆ ㅇ ㅈㅉ ㅊ ㅋ ㅌ ㅍ ㅎ".split(" ")

cv_map = dict()

cv_map["ㅏㅑㅘ"] = "加納達拉馬巴薩阿賈查卡塔帕哈"
cv_map["ㅐㅒㅔㅖㅙㅚㅞ"] = "蓋內戴萊梅貝塞埃傑切凱泰佩黑"
cv_map["ㅓㅕㅝ"] = "格訥德勒默伯瑟厄哲徹克特珀赫"
cv_map["ㅗㅛ"] = "戈諾多洛莫博索奧佐喬科託波霍"
cv_map["ㅜㅠㅡ"] = "古努杜盧穆布蘇烏朱楚庫圖普胡"
cv_map["ㅟㅢㅣ"] = "吉尼迪利米比西伊吉奇基蒂皮希"

for vs, zhs in cv_map.items():
    cv_map[vs] = {cs: zh for cs, zh in zip(css, zhs)}

cvc_map = dict()

cvc_map[("ㅏㅑㅘ", "ㄴㄵㄶ")] = "甘南丹蘭曼班尚安詹錢坎坦潘漢"
cvc_map[("ㅏㅑㅘ", "ㅇ")] = "岡南當朗芒邦尚昂章昌康唐龐杭"
cvc_map[("ㅓㅕㅝ", "ㄴㄵㄶㅇ")] = "根嫩登倫門本申恩真琴肯滕彭亨"
cvc_map[("ㅟㅢㅣ", "ㄴㄵㄶ")] = "金寧丁林明賓欣因金欽金廷平欣"
cvc_map[("ㅟㅢㅣ", "ㅇ")] = "京寧丁林明賓興英京青金廷平興"
cvc_map[("ㅗㅛㅜㅠㅡ", "ㄴㄵㄶㅇ")] = "貢農敦倫蒙本順溫準春昆通蓬洪"

for vcs, zhs in cvc_map.items():
    cvc_map[vcs] = {cs: zh for cs, zh in zip(css, zhs)}

fc_map = dict()

fc_map["ㄱㄲㄳㄺㅋ"] = "克"
fc_map["ㄷㅅㅆㅈㅊㅌㅎ"] = "特"
fc_map["ㄹㄼㄽㄾㅀ"] = "爾"
fc_map["ㄻㅁ"] = "姆"
fc_map["ㄴㄵㄶㅇ"] = "恩"
fc_map["ㅂㅄㄿㅍ"] = "普"

for i in range(len(ic)):
    for j in range(len(mv)):
        cv = ""
        for vs in cv_map:
            if mv[j] in vs:
                for cs in cv_map[vs]:
                    if ic[i] in cs:
                        cv = cv_map[vs][cs]
        for k in range(len(fc)):
            s = chr(0xAC00 + i * 21 * 28 + j * 28 + k)
            if not k:
                print(s, cv, sep = "\t")
                continue
            cvc = ""
            for vcs in cvc_map:
                if mv[j] in vcs[0] and fc[k] in vcs[1]:
                    for cs in cvc_map[vcs]:
                        if ic[i] in cs:
                            cvc = cvc_map[vcs][cs]
            if cvc:
                print(s, cvc, sep = "\t")
                continue
            for cs in fc_map:
                if fc[k] in cs:
                    print(s, cv + fc_map[cs], sep = "\t")
