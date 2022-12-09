ic = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ" # initial consonants
mv = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ" # medial vowels
fc = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ" # final consonants

css = ["ㄱㄲ", "ㄴ", "ㄷㄸ", "ㄹ", "ㅁ", "ㅂㅃ", "ㅅㅆ", "ㅇ", "ㅈㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

cv_map = dict()

cv_map["ㅏㅑㅘ"] = "加纳达拉马巴萨阿贾查卡塔帕哈"
cv_map["ㅐㅒㅔㅖㅙㅚㅞ"] = "盖内戴莱梅贝塞埃杰切凯泰佩黑"
cv_map["ㅓㅕㅝ"] = "格讷德勒默伯瑟厄哲彻克特珀赫"
cv_map["ㅗㅛ"] = "戈诺多洛莫博索奥佐乔科托波霍"
cv_map["ㅜㅠㅡ"] = "古努杜卢穆布苏乌朱楚库图普胡"
cv_map["ㅟㅢㅣ"] = "吉尼迪利米比西伊吉奇基蒂皮希"

for vs, zhs in cv_map.items():
    cv_map[vs] = {cs: zh for cs, zh in zip(css, zhs)}

cvc_map = dict()

cvc_map[("ㅏㅑㅘ", "ㄴㄵㄶ")] = "甘南丹兰曼班尚安詹钱坎坦潘汉"
cvc_map[("ㅏㅑㅘ", "ㅇ")] = "冈南当朗芒邦尚昂章昌康唐庞杭"
cvc_map[("ㅓㅕㅝ", "ㄴㄵㄶㅇ")] = "根嫩登伦门本申恩真琴肯滕彭亨"
cvc_map[("ㅟㅢㅣ", "ㄴㄵㄶ")] = "金宁丁林明宾欣因金钦金廷平欣"
cvc_map[("ㅟㅢㅣ", "ㅇ")] = "京宁丁林明宾兴英京青金廷平兴"
cvc_map[("ㅗㅛㅜㅠㅡ", "ㄴㄵㄶㅇ")] = "贡农敦伦蒙本顺温准春昆通蓬洪"

for vcs, zhs in cvc_map.items():
    cvc_map[vcs] = {cs: zh for cs, zh in zip(css, zhs)}

fc_map = dict()

fc_map["ㄱㄲㄳㄺㅋ"] = "克"
fc_map["ㄷㅅㅆㅈㅊㅌㅎ"] = "特"
fc_map["ㄹㄼㄽㄾㅀ"] = "尔"
fc_map["ㄻㅁ"] = "姆"
fc_map["ㄴㄵㄶㅇ"] = "恩"
fc_map["ㅂㅄㄿㅍ"] = "普"

for i in range(19):
    for j in range (21):
        cv = ""
        for vs in cv_map:
            if mv[j] in vs:
                for cs in cv_map[vs]:
                    if ic[i] in cs:
                        cv = cv_map[vs][cs]
                        break
        for k in range(28):
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
                            break
            if cvc:
                print(s, cvc, sep = "\t")
            else:
                for cs in fc_map:
                    if fc[k] in cs:
                        print(s, cv + fc_map[cs], sep = "\t")
                        break
