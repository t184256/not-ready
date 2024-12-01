#!/usr/bin/env python

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(
    description='Run languagetool, filter out false positives.'
)
parser.add_argument('--lang')
parser.add_argument('--false-positives')
parser.add_argument('--disabled-rules')
parser.add_argument('--dictionary')
parser.add_argument('--unused', choices=['ignore', 'remove', 'error'])
parser.add_argument('files', nargs='+', help='files to process')
args = parser.parse_args()


def word_in(w, text):
    if re.search(r'\b' + w + r'\b', text):
        return True
    if w.endswith('--'):
        if re.search(r'\b' + w + r'(\W|$)', text):
            return True
    if w.startswith('--'):
        if re.search(r'(\W|^)' + w + r'\b', text):
            return True
    return False


def findfile(stem):
    if args.lang and os.path.exists(f'.ltex/ltex.{stem}.{args.lang}.txt'):
        return f'.ltex/ltex.{stem}.{args.lang}.txt'


FALSE_POSITIVES = \
    args.false_positives or findfile('hiddenFalsePositives') or None
DISABLED_WORDS = args.dictionary or findfile('dictionary') or None
DISABLED_RULES = args.disabled_rules or findfile('disabledRules') or None

print(f'running languagetool over {args.files}, filtering out:')
if FALSE_POSITIVES:
    print(f' {FALSE_POSITIVES} false positives')
if DISABLED_RULES:
    print(f' {DISABLED_RULES} disabled rules')
if DISABLED_WORDS:
    print(f' {DISABLED_WORDS} words')

disabled_rules = []
if DISABLED_RULES:
    with open(DISABLED_RULES) as f:
        disabled_rules = f.read().strip().split('\n')

disabled_words = []
if DISABLED_WORDS:
    with open(DISABLED_WORDS) as f:
        disabled_words = f.read().strip().split('\n')

false_positives = []
false_positives_orig = {}
false_positives_keep = []
if FALSE_POSITIVES:
    with open(FALSE_POSITIVES) as f:
        for line in f.readlines():
            j = json.loads(line)
            rule, sentence, keep = j['rule'], j['sentence'], j.get('keep', 0)
            if not keep:
                assert not rule.startswith('MORFOLOGIK_RULE_')
            sentence = sentence.removeprefix(r'^\Q')
            sentence = sentence.removesuffix(r'\E$')
            false_positives.append((rule, sentence))
            false_positives_orig[(rule, sentence)] = line.strip()
            if keep == 1:
                false_positives_keep.append((rule, sentence))

stripped_files = []
text = ''
for f in args.files:
    stripped_fname = os.path.join(
        os.path.dirname(f), '.stripped.' + os.path.basename(f)
    )
    with open(stripped_fname, 'w') as sf:
        with open(f) as f_:
            skip = False
            for line in f_.readlines():
                if line.strip() == '<!-- ltex: enabled=false -->':
                    skip = True
                    sf.write('\n')
                    text += '\n'
                    continue
                if line.strip() == '<!-- ltex: enabled=true -->':
                    skip = False
                    sf.write('\n')
                    text += '\n'
                    continue
                sf.write(line if not skip else '\n')
                text += line if not skip else '\n'
    stripped_files.append(stripped_fname)

matches = []
seen_words = []
false_positives_seen = []
retries = 5
while retries:
    p = subprocess.Popen(
        ['ltex-cli',
         '--server-command-line=ltex-ls', '--hide-commands', *stripped_files],
        encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )

    try:
        outs, errs = p.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        print('... timeout')
        retries -= 1
        continue
    if errs:
        print(f'... {errs.strip()[:79].replace("\n", " ")}')
        retries -= 1
        continue
    break
assert not errs, errs
error = None
outs = outs.replace('/.stripped.', '/')

for sf in stripped_files:
    os.unlink(sf)

for line in outs.split('\n'):
    #print(line)
    m = re.match(r'(.*):(\d+):(\d+).*\[(\S+)\]', line)
    if error is None and m:
        error = m.groups()
        continue
    if error is not None:
        file, lineno, colno, rule = error
        match = line.lstrip('> .').rstrip(r' \\').replace('*', '')
        #print('!', rule, match)
        matches.append((file, lineno, colno, rule, match))
    error = None

if p.returncode == 0:
    assert not matches

text_flattened = text
text_flattened = re.sub(r'^> ', ' ', text_flattened, flags=re.MULTILINE)
text_flattened = re.sub(r'^ \.', ' ', text_flattened, flags=re.MULTILINE)
text_flattened = re.sub(r' \\$', ' ', text_flattened, flags=re.MULTILINE)
text_flattened = text_flattened.replace('\n', ' ')
text_flattened = text_flattened.replace('*', ' ')
text_flattened = re.sub(r'\s+', ' ', text_flattened)

for w in disabled_words:
    if word_in(w, text):
        if w not in seen_words:
            seen_words.append(w)

for rule, sentence in false_positives:
    sentence_flattened = re.sub(r'\s+', ' ', sentence)
    if sentence_flattened in text_flattened:
        if (rule, sentence) not in false_positives_seen:
            false_positives_seen.append((rule, sentence))
print('waiving...')


unexplained_matches = []
#waived_rules = []
waived_words = []
waived_fps = []
for file, lineno, colno, rule, match in matches:
    if rule in disabled_rules:
        #if rule not in waived_rules:
        #    waived_rules.append(rule)
        continue
    if rule.startswith('MORFOLOGIK_RULE_'):
        waived = False
        for word in disabled_words:
            if word_in(word, match.lower() if word.islower() else match):
                if word not in waived_words:
                    waived_words.append(word)
                waived = True
        if waived:
            continue
    if (rule, match) in false_positives:
        if (rule, match) not in waived_fps:
            waived_fps.append((rule, match))
        continue
    waived = False
    for fp_rule, sentence in false_positives:
        if match in sentence or sentence in match:
            if (fp_rule, sentence) not in waived_fps:
                waived_fps.append((fp_rule, sentence))
            waived = True
    if waived:
        continue
    unexplained_matches.append((file, lineno, colno, rule, match))

for file, lineno, colno, rule, match in unexplained_matches:
    print(f'{file}:{lineno}:{colno} {rule}\n{match}')

#print(f'{len(matches)} -> {len(unexplained_matches)}')

words_merged = []
for word in waived_words + seen_words:
    if word not in words_merged:
        words_merged.append(word)

fp_merged = []
for fp in false_positives_keep + waived_fps + false_positives_seen:
    if fp not in fp_merged:
        fp_merged.append(fp)

if args.unused == 'ignore':
    pass
elif args.unused == 'remove':
    #if DISABLED_RULES:
    #    with open(DISABLED_RULES, 'w') as f:
    #        for rule in waived_rules:
    #            f.write(rule + '\n')
    if DISABLED_WORDS:
        with open(DISABLED_WORDS, 'w') as f:
            for word in words_merged:
                f.write(word + '\n')
    if FALSE_POSITIVES:
        with open(FALSE_POSITIVES, 'w') as f:
            for fp in fp_merged:
                f.write(false_positives_orig[fp] + '\n')
else:  # error
    unused = False
    #for rule in disabled_rules:
    #    if rule not in waived_rules:
    #        print(f'unused disabled rule: {rule}')
    #        unused = True
    for word in disabled_words:
        if word not in words_merged:
            print(f'unused dict word: {word}')
            unused = True
    for fp in false_positives:
        if fp not in fp_merged:
            rule, match = fp
            print(f'unused false positive: [{rule}] {match}')
            unused = True
        # TODO: keep sentences that are at least present
    if unused:
        sys.exit(77)

sys.exit(1 if unexplained_matches else 0)
