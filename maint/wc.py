#!/usr/bin/env python

import glob
import re
from pathlib import Path

LANGS = {
    'en': r"([a-zA-Z'-]+)",
    'ru': r'([а-яА-Я-]+)',
}


def wc(regex, text):
    text = re.sub(r'<!--.*-->', '', text)
    res = [r for r in re.findall(regex, text) if r.replace('-', '')]
    return len(res)


if __name__ == '__main__':
    for i, (lang, regex) in enumerate(LANGS.items()):
        files = sorted(glob.glob(f'text/{lang}/*.md'))
        if i == 0:
            print(' '.join(f'{int(re.search(r"(\d+)", fn).group(1)):4d}'
                           for fn in files))
        lens = [wc(regex, Path(fn).read_text()) for fn in files]
        print(' '.join([f'{l:4d}' for l in lens]) + ' ' + str(sum(lens)))
