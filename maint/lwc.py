#!/usr/bin/env python

import argparse
import collections
import re
import sys

import ruamel.yaml


parser = argparse.ArgumentParser(description='Count lizard word usages.')
parser.add_argument('--dict')
parser.add_argument('--lang')
parser.add_argument('process', nargs='+', help='files to process')
args = parser.parse_args()
assert args.lang in ('en', 'ru')

if args.lang == 'en':
    lizard_word_regex = r'\[([Ia-z-?\'\.#0-9 ]+)\]'
else:
    lizard_word_regex = r'\[([а-я-?\'\.№0-9 ]+)\]'
lizard_column_regex = r'((' + lizard_word_regex + r'\s*)+)'

with open(args.dict) as f:
    y = ruamel.yaml.YAML()
    stems_to_words = y.load(f)
wordlist = set(sum([list(x) for x in stems_to_words.values()], []))
words_to_stems = {}
for stem, words in stems_to_words.items():
    for word in words:
        words_to_stems[word] = stem


def lizardize_word(w):
    if args.lang == 'en':
        w = w.removesuffix('-?')
    elif args.lang == 'ru':
        w = w.removesuffix('-ли?')
    return w


per_stem = collections.defaultdict(list)
per_word = collections.defaultdict(list)
words = []
for fname in args.process:
    with open(fname) as f:
        s = f.read()
    for lw in re.findall(lizard_word_regex, s):
        word = lizardize_word(lw)
        words.append(word)

for word in words:
    stem = words_to_stems[word]
    per_stem[stem].append(word)
    per_word[word].append(word)

for stem_len, stem in sorted([(len(l), s) for s, l in per_stem.items()],
                             reverse=True):
    print(stem_len, stem)

print('---')

unused = [lw for lw in wordlist if lw not in words]
if unused:
    print('unused:', ', '.join(unused))

missing = [lw for lw in words if lw not in wordlist]
if missing:
    print('missing:', ', '.join(missing))
    sys.exit(1)
