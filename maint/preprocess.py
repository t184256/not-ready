#!/usr/bin/env python

import argparse
import os
import re
import sys

import ruamel.yaml


parser = argparse.ArgumentParser(description='Preprocess my text.')
parser.add_argument('--dict')
parser.add_argument('--lang')
parser.add_argument('--format')
parser.add_argument('--book-version')
parser.add_argument('--no-process', action='append',
                    help='files to not process')
parser.add_argument('--process-meta', action='append',
                    help='files to process as metadata')
parser.add_argument('process', nargs='+', help='files to process')
args = parser.parse_args()
assert args.lang in ('en', 'ru')
assert args.format in ('pdf', 'epub', 'fb2', '80column.txt', 'freeflow.txt')

strict = os.getenv('STRICT') == '1'

if args.lang == 'en':
    lizard_word_regex = r'\[([Ia-z-?\'\.#0-9 ]+)\]'
else:
    lizard_word_regex = r'\[([а-я-?\'\.№0-9 ]+)\]'
lizard_column_regex = r'((' + lizard_word_regex + r'\s*)+)'

with open(args.dict) as f:
    y = ruamel.yaml.YAML()
    stems_words = y.load(f)
    wordlist = sum([list(x) for x in stems_words.values()], [])

for fname in args.process_meta or []:
    with open(fname) as f:
        s = f.read()
    if args.format in ('80column.txt', 'freeflow.txt'):
        if args.lang == 'en':
            s = s.replace('---\ntitle: ', 'Title: ')
            s = s.replace('\nauthor: ',
                          f'\nVersion: {args.book_version}\nAuthors: ')
            s = s.replace('[Alexander Sosedkin, Daria Sosedkina]',
                          'Alexander Sosedkin, Daria Sosedkina')
            s = s.replace('\nlang: en-GB', '')
            s = s.replace('\ninclude-before:\n  - |', '\nForetitle:')
        elif args.lang == 'ru':
            s = s.replace('---\ntitle: ', 'Название: ')
            s = s.replace('\nauthor: ',
                          f'\nВерсия: {args.book_version}\nАвторы: ')
            s = s.replace('[Александр Соседкин, Дарья Соседкина]',
                          'Александр Соседкин, Дарья Соседкина')
            s = s.replace('\nlang: ru-RU', '')
            s = s.replace('\ninclude-before:\n  - |', '\nАвантитул:')
        s = s.replace('\nrights: Creative Commons Attribution '
                      'Non-Commercial Share Alike 4.0\n', '\n')
        s = s.replace(' \\\n', '\n')
    print(s)

for fname in args.no_process or []:
    with open(fname) as f:
        s = f.read()
    print(s)

if args.format in ('epub', 'fb2'):
    for fname in args.process_meta or []:
        with open(fname) as f:
            s = f.read()
            s = s.replace('---\ntitle: ', '')
            if args.lang == 'en':
                s = s.replace('\nauthor: ',
                              f'\n\nVersion: {args.book_version}\n\nAuthors: ')
                s = s.replace('[Alexander Sosedkin, Daria Sosedkina]',
                              'Alexander Sosedkin, Daria Sosedkina')
                s = s.replace('\nlang: en-GB', '')
            elif args.lang == 'ru':
                s = s.replace('\nauthor: ',
                              f'\n\nВерсия: {args.book_version}\n\nАвторы: ')
                s = s.replace('[Александр Соседкин, Дарья Соседкина]',
                              'Александр Соседкин, Дарья Соседкина')
                s = s.replace('\nlang: ru-RU', '')
            s = s.replace('\ninclude-before:\n  - |', '\n\n')
            s = s.replace(' \\\n', '\n')
        print(s)

for fname in args.process:
    with open(fname) as f:
        s = f.read()

    def lizardize_word(match):
        word = str(match.group(1))
        w = word
        if args.lang == 'en':
            w = w.removesuffix('-?')
        elif args.lang == 'ru':
            w = w.removesuffix('-ли?')
        if args.format == 'pdf':
            if '#' in word:
                word = word.replace('#', r'\char"0023 ')
        if w not in wordlist:
            print(f'MISSING: {w}', file=sys.stderr)
            if strict:
                sys.exit(1)
            if args.format == 'pdf':
                return r'\lizardmissing{' + word + '}'
            elif args.format in ('epub', 'fb2'):
                return f'!{word}!'
        if args.format == 'pdf':
            return r'\lizardsign{' + word + '}'
        elif args.format in ('epub', 'fb2'):
            return f'[{word}]'

    def lizardize_column(match):
        lizardcol = match.group(0).rstrip()
        trailing = match.group(0).removeprefix(lizardcol)
        if args.format == 'pdf':
            return (
                r'\lizardcolumn{' +
                re.sub(lizard_word_regex, lizardize_word, lizardcol) +
                '}' + trailing
            )
        elif args.format in ('epub', 'fb2'):
            return (re.sub(lizard_word_regex,
                           lizardize_word, lizardcol) + trailing)

    if args.format in ('pdf', 'epub', 'fb2'):
        s = re.sub(lizard_column_regex, lizardize_column, s)

    s = s.replace('\n<!-- ltex: enabled=false -->\n%', ' ')
    s = s.replace('%\n<!-- ltex: enabled=true -->\n', ' ')
    s = s.replace('\n<!-- ltex: enabled=true -->\n', '\n')
    s = s.replace('\n<!-- ltex: enabled=false -->\n', '\n')
    s = s.replace('\n<!-- ltex: language=ru-RU -->\n', '\n')
    s = s.replace('\n<!-- ltex: language=en-GB -->\n', '\n')
    s = re.sub('<!-- align: .* -->', '<!-- align -->', s)
    s = s.replace('\n<!-- align -->\n', '\n')

    if args.format == 'pdf':
        if args.lang == 'en':
            s = re.sub(r'\n(".*)\n([^ \n|."])', r'\n\1\n\n\\gluepar{}\2', s)
            s = re.sub(r'\n( .*)\n([^ \n|."])', r'\n\1\n\n\\gluepar{} \2', s)
            s = re.sub(r'\n(\|.*)\n([^ \n|."])', r'\n\1\n\n\\gluepar{}\2', s)
            s = re.sub(r'\n(\..*)\n([^ \n|."])', r'\n\1\n\n\\gluepar{} \2', s)
            s = re.sub('([^\n])\n"', '\\1\n\n\\\\gluepar\\\\speechpar"', s)
            s = s.replace('\n\n"', '\n\n\\speechpar"')
            s = s.replace(' |\n', ' \\lizardsep\n')
            s = s.replace('\n|',
                          '\n\n\\nopagebreak\\gluepar\\speechpar'
                          '\\makebox[\\widthof{"}][c]{\\lizardsep}')
            ## needs 0 protrusion
            s = s.replace('...', '#%#')
            s = s.replace('\n.', '\n\n\\gluepar\\speechpar\\hphantom{"}')
            s = s.replace('#%#', '...')
            #s = s.replace(':\n"', ':\n\n"')
            #s = re.sub('([^\n])\n"', '\\1 \\\n"', s)  # ?_" -> ? \\_"
        elif args.lang == 'ru':
            # I know, it should be "--*
            s = re.sub(r'\n(-- .*)\n([^ \n-])', r'\n\1\n\n\\gluepar \2', s)
            s = re.sub(r'\n( .*)\n([^ \n-])', r'\n\1\n\n\\gluepar \2', s)
            s = re.sub(r'\n(\|.*)\n([^ \n-])', r'\n\1\n\n\\gluepar \2', s)
            s = re.sub(r'\n(\..*)\n([^ \n-])', r'\n\1\n\n\\gluepar \2', s)
            s = re.sub('([^\n])\n-- ',
                       '\\1\n\n\\\\gluepar\\\\speechpar---\\\\thinspace\n', s)
            s = s.replace('\n\n-- ', '\n\n\\speechpar---\\thinspace\n')
            s = s.replace(' |\n', ' \\mbox{\\lizardsep}\n')
            s = s.replace('\n | ',
                          '\n\n\\nopagebreak\\gluepar\\speechpar'
                          '\\makebox[\\widthof{---}][r]{\\lizardsep}'
                          '\\thinspace')
            s = s.replace(' | ', ' \\lizardsep ')
            s = s.replace('\n . ', ' \\\n\n ')
            s = re.sub('\n +-- ', '\\ --- ', s)
            s = re.sub('\n +--\n', '\\ ---\n', s)
            s = re.sub(' +-- ', ' --- ', s)
            s = re.sub(' +--\n', ' ---\n', s)
    elif args.format in ('epub', 'fb2'):
        #s = re.sub(' \\\\n', '<p>\1</p>\n')
        s = s.replace('\n\\newpage\n', '\n\n\\\n\n')
        if args.format == 'fb2':
            s = s.replace('\n\n', '\n\n\\\n\n')
        if args.lang == "en":
            #s = s.replace(':\n"', ':\n\n"')  # :_ -> :__
            #s = re.sub('([^\n])\n"', '\\1 \n\n"', s)  # ?_" -> ? __"
            s = re.sub(r'\n(".*)\n([^ \n|."])', r'\n\1\n\n\2', s)
            s = re.sub(r'\n( .*)\n([^ \n|."])', r'\1\n\n \2', s)
            s = re.sub(r'\n\|(.*)\n([^ \n|."])', r' | \1 \n\n\2', s)
            s = re.sub(r'\n\.(.*)\n([^ \n|."])', r' \1\n\n\2', s)
            s = s.replace('\n"', '\n\n"')
            s = s.replace('\n|', ' | ')
            s = s.replace('\n.', ' ')
        elif args.lang == 'ru':
            s = re.sub(r'\n(-- .*)\n([^ \n-])', r'\n\1\n\n\2', s)
            s = re.sub(r'\n( .*)\n([^ \n-])', r'\1\n\n \2', s)
            s = re.sub(r'\n \|(.*)\n([^ \n-])', r' | \1\n\n\2', s)
            s = re.sub(r'\n \.(.*)\n([^ \n-])', r' \1\n\n\2', s)
            #s = re.sub('([^\n])\n-- ', '\\1 \n\n--- ', s)
            s = s.replace('\n-- ', '\n\n--- ')
            s = s.replace('\n | ', ' | ')
            s = s.replace('\n .', ' \n  ')
            s = s.replace(' -- ', '\\ --- ')
            s = s.replace(' --\n', '\\ ---\n')
        if args.format == 'fb2':
            s = s.replace(' \\\n>', '\n>\n>')
        s = s.replace(' \\\n', '\n\n')
        s = s.replace('\n\n', '#%##%#')
        s = s.replace('\n* ', '#*#')
        s = s.replace('\n', ' ')
        s = s.replace('#%#', '\n')
        s = s.replace('#*#', '\n* ')
        s = s.replace('>  > ', '\n\n> \\\n> ')
        s = s.replace('> > ', '\n\n> \\\n> ')
    elif args.format in ('80column.txt', 'freeflow.txt'):
        s = s.replace(' \\\n', '\n')
        s = s.replace('\n\\newpage\n', '')
        s = s.replace('\n\\hrule\n', '\n---\n')
        s = s.replace('\\ ', ' ')
        assert '\\' not in s
    if args.format == '80column.txt':
        for line in s.split('\n'):
            assert len(line) <= 80, line
    if args.format == 'freeflow.txt':
        s = re.sub(r'^#(.*)', '#%##%##\\1#%#', s)
        s = s.replace('\n\n', '#%##%#')
        if args.lang == "en":
            s = s.replace('\n"', '#%#"')
            s = s.replace('\n|', ' | ')
            s = s.replace('\n.', ' ')
        elif args.lang == "ru":
            s = s.replace('\n--', '#%#--')
            s = s.replace('\n | ', ' | ')
            s = s.replace('\n . ', ' ')
        s = s.replace('\n> ', '#%#> ')
        s = s.replace('\n* ', '#%#* ')
        s = s.replace('\n', ' ')
        s = re.sub(r' +', r' ', s)
        s = s.replace('#%#', '\n')

    s = s.replace('\n@', '\n')
    s = s.replace('@', '')

    print(s + ('\n\n' if args.format in ('epub', 'fb2') else ''))
