import sys
import re
import math
from collections import defaultdict

ngram_size = 3
freq = [defaultdict(int) for _ in range(ngram_size)]

ambiguous_tw = set("丑乾于云亘亙伕伙佑佔余佣佩侄侖係傭儘兇克冢准凶刨刮制剋剷剿勖勗勦千卜占卹只台吁合吊向周咏咽哄唇唸啣嘗嘩噹嚐嚥嚮回困團塚壇夥夫奸姜姦姪嬝導局岳崙嶽帳干幹庄弔彌彫征御復徵志念恤悽愈慄慇慾扎托扣折捆捨採搾摺斗於曆札朮朱松栗榨欲歷殷毀氾沈沖沾泛浚淒游準溪溼濕濬瀋瀰焰煉煙熏燄燐燬燻狸獲珮琅瑯甦當疱癒發皰盡盪睏硃磷祐祕禦秘穀穫簑簽籐籤籲糰系紮綑緻繫繮罈脣臟致臺舍莊菸蓑蔔蕩薑藤蘇虱蝨術衝裊裡製複覆託証詠誌譁證讚谷谿貍賬贊跼迆迤迴週遊道郁醜采里釦鉋銜鍊鍾鏟鐘鑑鑒閤隻雕雲霉霑面韁韆颱颳飢餘饑髒髮鬆鬥鬨鬱鰲麵黴鼇")

for ln, line in enumerate(sys.stdin, 1):
    line = line.strip()

    for i in range(len(line)):
        for j in range(min(len(line) - i, ngram_size)):
            w = line[i:i + j + 1]

            if re.search("[^\u4E00-\u9FFF]", w):
                continue
            if not ambiguous_tw.intersection(w):
                continue

            freq[len(w) - 1][w] += 1

    if ln % 100000 == 0:
        print("%d lines" % ln, file = sys.stderr)

zs = [sum(x.values()) for x in freq]

for ws, z in zip(freq, zs):
    for w, f in sorted(ws.items(), key = lambda x: -x[1]):
        if f < 3:
            break
        print("%f\t%d\t%s" % (math.log(f / z), f, w))
