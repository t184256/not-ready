#!/usr/bin/env python3

import re
import shutil
import subprocess
import sys
from pathlib import Path

assert len(sys.argv) == 1 or len(sys.argv) == 3 and sys.argv[1] == '-u'

flake_nix = Path('flake.nix').read_text()
VER_REGEX = r'^\s*bookVersion = "([0-9]+\.[0-9]+\.[0-9]+)";  # scraped$'
ver_flake_nix, = re.findall(VER_REGEX, flake_nix, re.MULTILINE)

if shutil.which('git'):
    GIT_CMD = ['git', 'describe', '--tags', '--dirty=+']
    ver_git = subprocess.check_output(GIT_CMD, encoding='utf-8').strip()
    assert (
        ver_git == ver_flake_nix or
        ver_git.startswith(ver_flake_nix + '-') or
        ver_git.startswith(ver_flake_nix + '+')
    )
    ver = ver_git
else:
    ver = ver_flake_nix

if len(sys.argv) == 1:
    print(ver)
else:
    ver_file, = sys.argv[2:]
    try:
        old_contents = Path(ver_file).read_text()
    except FileNotFoundError:
        old_contents = None
    if old_contents != ver:
        Path(ver_file).write_text(ver)
