#!/usr/bin/env python3
# find_unknown_surface.py

import csv
import re
import sys
from nltk import pos_tag, word_tokenize, download
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# 如果是第一次运行，需要下载这些资源，取消下面几行注释并执行一次：
# download('punkt')
# download('averaged_perceptron_tagger')
# download('wordnet')
# download('omw-1.4')
# download('punkt_tab')
# download('averaged_perceptron_tagger_eng')

def get_wordnet_pos(tag):
    if tag.startswith('J'): return wordnet.ADJ
    if tag.startswith('V'): return wordnet.VERB
    if tag.startswith('N'): return wordnet.NOUN
    if tag.startswith('R'): return wordnet.ADV
    return None

def main(csv_path='subtitles.csv',
         known_path='oxford5000.txt',
         output_path='unknown_words.txt'):

    # 1. 载入已知词表（全小写）
    with open(known_path, encoding='utf-8') as f:
        known = {w.strip().lower() for w in f if w.strip()}

    lemmatizer = WordNetLemmatizer()
    unknown = set()

    with open(csv_path, newline='', encoding='utf-8') as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            sentence = row.get('English Sentence','')
            tokens   = word_tokenize(sentence)
            tagged   = pos_tag(tokens)

            for token, tag in tagged:
                if not re.match(r'[A-Za-z]', token):
                    continue

                lower = token.lower()

                # —— 基础规则：原始小写形式就在已知词表里，则跳过
                if lower in known:
                    continue

                # —— Lemma 判断
                wn_pos = get_wordnet_pos(tag)
                if wn_pos:
                    lemma = lemmatizer.lemmatize(lower, pos=wn_pos)
                else:
                    lemma = lemmatizer.lemmatize(lower)

                if lemma in known:
                    continue

                # —— 后缀规则：只有当所有规则都不命中时，下文才加到 unknown
                recognized = False

                # 1) 副词 -ly
                if wn_pos == wordnet.ADV and lower.endswith('ly'):
                    if lower[:-2] in known:
                        recognized = True
                        
                # 1.5) 形容词比较级 -er
                if not recognized and wn_pos == wordnet.ADJ and lower.endswith('er'):
                    stem = lower[:-2]
                    # 例如 happier→happi/happy
                    if stem in known or (stem + 'y') in known or (stem + 'e') in known:
                        recognized = True

                # 1.6) 形容词最高级 -est
                if not recognized and wn_pos == wordnet.ADJ and lower.endswith('est'):
                    stem = lower[:-3]
                    # 例如 happiest→happi/happy
                    if stem in known or (stem + 'y') in known or (stem + 'e') in known:
                        recognized = True

                # 2) 先去掉 ing，再尝试加 e
                if not recognized and lower.endswith('ing'):
                    stem = lower[:-3]
                    if stem in known or (stem+'e') in known:
                        recognized = True

                # 3) 复数 -es（先去 -es）
                if not recognized and wn_pos == wordnet.NOUN and lower.endswith('es'):
                    if lower[:-2] in known:
                        recognized = True

                # 4) 通用复数 -s
                if not recognized and wn_pos == wordnet.NOUN and lower.endswith('s'):
                    if lower[:-1] in known:
                        recognized = True

                # 如果都没识别，则是真正的“未知”
                if not recognized:
                    unknown.add(token)

    # 写出结果
    with open(output_path, 'w', encoding='utf-8') as outf:
        for w in sorted(unknown, key=lambda x: x.lower()):
            outf.write(w+'\n')

    print(f"Found {len(unknown)} unknown surface forms → {output_path}")

if __name__=='__main__':
    if len(sys.argv)==4:
        main(*sys.argv[1:])
    else:
        main()