import json


def poem_translate(int_file, text_file):

    with open("n_to_char.json", 'r', encoding='UTF-8') as f:
        n_to_char = json.load(f)

    with open(int_file, 'r', encoding='UTF-8') as load_f:
        with open(text_file, 'w', encoding='UTF-8') as out_f:
            for line in load_f.readlines():
                n_poem = line[:-1].strip().split()
                char_poem = [n_to_char[n] for n in n_poem if n in n_to_char]
                if len(char_poem) < 20:
                    continue
                poem = []
                i = 0
                while i < 28:
                    poem.append(char_poem[i])
                    if (i+1) % 14 == 0:
                        poem.append('。\n')
                    elif (i+1) % 7 == 0:
                        poem.append('，')
                    i += 1
                str_poem = ''.join(poem)+'\n'
                out_f.write(str_poem)

if __name__ == '__main__':

    # 输入文件名，包含待翻译的纯数字文本
    int_file = "./i_output.txt"
    # 输出文件名，这里是输出的绝句文本
    poem_file = "./poem_output.txt"
    poem_translate(int_file, poem_file)
    # 输出诗歌文本，见根目录
