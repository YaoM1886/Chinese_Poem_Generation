import re
from pypinyin import pinyin, Style
import zhconv


# 将一句诗转换为声调形式，1、2、3、4代表四声，0表示无法识别
def extra_shengdiao(sentence):
    s_list = pinyin(sentence, style=Style.TONE2, heteronym=True)
    s_sd = []
    for i in range(7):
        try:
            # 多音字取第一个声调
            pin = s_list[i][0]
        except:
            # 如果字符无法辨识，设音调为0
            pin = '0'
        try:
            sd = re.search('\d', pin).group()
            s_sd.append(sd)
        except:
            # 如果拼音中无音调信息
            s_sd.append('0')

    return s_sd


# 将extra_shengdiao()中的结果转换为平仄，1、2声为平'p'，3、4声为仄'z'，'n'表示无法识别
def shengdiao_pingze(list):
    # 1、2声为平，3、4声为仄
    pingze = []
    for s in list:
        if s == '1' or s == '2':
            pingze.append('p')
        elif s == '3' or s == '4':
            pingze.append('z')
        else:
            pingze.append('n')
    return pingze


# 比较两个列表的平仄，一个字符符合加1分
def compare(list1, list2):
    score = 0
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            # 如果2、4句韵脚押平，得分加7
            if i in [13, 27] and list1[i] == 'p':
                score = score + 7
            else:  # 其他字符如果平仄符合，得分加1
                score = score + 1
    # 28基础分，12韵脚分
    return score


# 计算诗的平仄得分
def pingze(s1, s2, s3, s4):
    # 输入平仄列表，如['z', 'z', 'p', 'p', 'z', 'z', 'p']
    # 四种类别：1平起首句入韵式；2平起首句不入韵式；3仄起首句入韵式；4仄起首句入韵式
    # 用b表示平仄均可
    # 第一句不管1、3平仄，用于类别1、2、4
    # p1_124=list('b')+s1[1]+list('b')+s1[3:7]
    p1_124 = s1
    p1_124[0] = 'b'
    p1_124[2] = 'b'
    # 第一句不管1平仄，用于类别3
    p1_3 = s1
    p1_3[0] = 'b'

    # 第二句不管1平仄，用于类别1、2
    p2_12 = s2
    p2_12[0] = 'b'

    # 第二句不管1、3平仄，用于类别3、4
    p2_34 = s2
    p2_34[0] = 'b'
    p2_34[2] = 'b'

    # 第三句不管1、3平仄，用于类别1、2、3、4
    p3_1234 = s3
    p3_1234[0] = 'b'
    p3_1234[2] = 'b'

    # 第四句不管1、3平仄，用于类别1、2
    p4_12 = s4
    p4_12[0] = 'b'
    p4_12[2] = 'b'

    # 第四句不管1平仄，用于类别3、4
    p4_34 = s4
    p4_34[0] = 'b'

    # 类型1
    poem1 = p1_124 + p2_12 + p3_1234 + p4_12
    # 类型2
    poem2 = p1_124 + p2_12 + p3_1234 + p4_12
    # 类型3
    poem3 = p1_3 + p2_34 + p3_1234 + p4_34
    # 类型4
    poem4 = p1_124 + p2_34 + p3_1234 + p4_34

    # 类型1标准
    c1 = ['b', 'p', 'b', 'z', 'z', 'p', 'p',
          'b', 'z', 'p', 'p', 'z', 'z', 'p',
          'b', 'z', 'b', 'p', 'p', 'z', 'z',
          'b', 'p', 'b', 'z', 'z', 'p', 'p']

    # 类型2标准
    c2 = ['b', 'p', 'b', 'z', 'p', 'p', 'z',
          'b', 'z', 'p', 'p', 'z', 'z', 'p',
          'b', 'z', 'b', 'p', 'p', 'z', 'z',
          'b', 'p', 'b', 'z', 'z', 'p', 'p']

    # 类型3标准
    c3 = ['b', 'z', 'p', 'p', 'z', 'z', 'p',
          'b', 'p', 'b', 'z', 'z', 'p', 'p',
          'b', 'p', 'b', 'z', 'p', 'p', 'z',
          'b', 'z', 'p', 'p', 'z', 'z', 'p']

    # 类型4标准
    c4 = ['b', 'z', 'b', 'p', 'p', 'z', 'z',
          'b', 'p', 'b', 'z', 'z', 'p', 'p',
          'b', 'p', 'b', 'z', 'p', 'p', 'z',
          'b', 'z', 'p', 'p', 'z', 'z', 'p']

    score1 = compare(poem1, c1)
    score2 = compare(poem2, c2)
    score3 = compare(poem3, c3)
    score4 = compare(poem4, c4)
    score = max(score1, score2, score3, score4)

    return score


# plist 诗句，i 诗的编号
def pz_score(plist, i):
    # 繁转简
    plist = zhconv.convert(plist, 'zh-cn')

    # 第一句 0-7；第二句：8-15；第三句：16-23 第四句：24-31 []左闭右开
    p_1 = plist[0:7]
    p_2 = plist[8:15]
    p_3 = plist[16:23]
    p_4 = plist[24:31]

    p_1_sd = extra_shengdiao(p_1)
    p_1_pz = shengdiao_pingze(p_1_sd)
    p_2_sd = extra_shengdiao(p_2)
    p_2_pz = shengdiao_pingze(p_2_sd)

    p_3_sd = extra_shengdiao(p_3)
    p_3_pz = shengdiao_pingze(p_3_sd)

    p_4_sd = extra_shengdiao(p_4)
    p_4_pz = shengdiao_pingze(p_4_sd)

    pz = pingze(p_1_pz, p_2_pz, p_3_pz, p_4_pz)
    # 将诗的编号：得分写入字典
    return pz / 40


def print_poem(num=10):

    flist = open('./similar_output.txt', 'rU', encoding='UTF-8').readlines()
    rtn = ""
    scoredict = {}
    for i in range(int(len(flist) / 3)):
        plist = flist[3 * i].strip('\n') + flist[3 * i + 1]
        scoredict[i] = pz_score(plist, i)

    sort_scoredict = sorted(scoredict.items(), key=lambda item: item[1], reverse=True)

    for m in range(num):
        # 诗的编号
        num = sort_scoredict[m][0]
        # 诗的得分
        score = sort_scoredict[m][1]
        if score >= 0.8:
            # 输出诗的得分
            t = 'score: '+ str(score) + '\n'
            poem = flist[3 * num].strip('\n') + flist[3 * num + 1]
            poem = zhconv.convert(poem, 'zh-cn')
            # 输出诗
            t += poem + '\n'
            rtn += t
        else:
            break
    return rtn


if __name__ == '__main__':
    print_poem(10)
