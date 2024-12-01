#!/usr/bin/env python

import collections
import glob
import re
import sys

import ruamel.yaml

MAX_FINDINGS = 4
DICT_EN = 'maint/ldict.en.yml'
DICT_RU = 'maint/ldict.ru.yml'

LIZARD_WORD_REGEX_EN = r'\[([Ia-z-?\'\.#0-9 ]+)\]'
LIZARD_WORD_REGEX_RU = r'\[([а-я-?\'\.№0-9 ]+)\]'

CHAPTERS_EN = sorted(glob.glob('text/en/*.md'))
CHAPTERS_RU = sorted(glob.glob('text/ru/*.md'))
assert len(CHAPTERS_EN) == len(CHAPTERS_RU)


def load_dict(dict_fname):
    with open(dict_fname) as f:
        y = ruamel.yaml.YAML()
        stems_to_words = y.load(f)
    words_to_stems = {}
    for stem, words in stems_to_words.items():
        for word in words:
            words_to_stems[word] = stem
    return stems_to_words, words_to_stems


stems_to_words_en, _ = load_dict(DICT_EN)
stems_to_words_ru, _ = load_dict(DICT_RU)
en_ru_cross_dict = {}
for stem_en, stem_ru in zip(stems_to_words_en, stems_to_words_ru):
    words_en = stems_to_words_en[stem_en]
    words_ru = stems_to_words_ru[stem_ru]
    assert len(words_en) == len(words_ru), (words_en, words_ru)
    assert len(set(words_en)) == len(set(words_ru)), (words_en, words_ru)
    assert len(set(words_en)) == len(words_en), words_en
    assert len(set(words_ru)) == len(words_ru), words_ru
    en_ru_cross_dict.update(zip(words_en, words_ru))


def en_ru_translate(w):
    try:
        if w.endswith('-?'):
            return en_ru_cross_dict[w.removesuffix('-?')] + '-ли?'
        return en_ru_cross_dict[w]
    except KeyError:
        return


def load_words(text_fname, lizard_word_regex, lang):
    word_to_line = []
    with open(text_fname) as f:
        for i, s in enumerate(f.readlines()):
            for lw in re.findall(lizard_word_regex, s):
                word_to_line.append((lw, i + 1, s.rstrip()))
    return word_to_line


findings = 0
count_mismatches = []
for ch_en, ch_ru in zip(CHAPTERS_EN, CHAPTERS_RU):
    word_line_map_en = load_words(ch_en, LIZARD_WORD_REGEX_EN, 'en')
    word_line_map_ru = load_words(ch_ru, LIZARD_WORD_REGEX_RU, 'ru')
    ch_en_s = ch_en.removeprefix('text/').removesuffix('.md')
    ch_ru_s = ch_ru.removeprefix('text/').removesuffix('.md')
    z = zip(word_line_map_en, word_line_map_ru)
    for (word_en, lineno_en, line_en), (word_ru, lineno_ru, line_ru) in z:
        trans_ru = en_ru_translate(word_en)
        if word_ru != trans_ru:
            if findings <= MAX_FINDINGS:
                print(f'{ch_en_s}:{lineno_en} / {ch_ru_s}:{lineno_ru}: '
                      f'{word_en} -> {trans_ru} != {word_ru}')
                print(line_en)
                print(line_ru)
                print()
            findings += 1
    if len(word_line_map_en) != len(word_line_map_ru):
        count_mismatches.append((ch_en, ch_ru))
if findings > MAX_FINDINGS:
    print(f'... and {findings - MAX_FINDINGS} more mismatches')
if count_mismatches:
    print('... and count mismatches in:')
    for ch_en, ch_ru in count_mismatches:
        print(f'    {ch_en} vs {ch_ru}')
sys.exit(0 if not findings else 1)
