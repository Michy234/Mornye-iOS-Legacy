#!/usr/bin/env python3
"""Reject bundles or embedded Mach-O binaries requiring newer than iOS 15."""
import plistlib
import re
import subprocess
import sys
from pathlib import Path

from check_backend_ios import MACHO_MAGICS


def version(value):
    parts = tuple(int(n) for n in value.split('.'))
    return (parts + (0, 0, 0))[:3]


def check_minos(output, path):
    values = re.findall(r'^\s*(?:minos|version)\s+(\d+(?:\.\d+)+)', output, re.M)
    if not values:
        raise ValueError(f'{path}: no minimum OS load command')
    for value in values:
        if version(value) > version('15.0'):
            raise ValueError(f'{path}: requires iOS {value}')


def audit(app):
    count = 0
    for path in app.rglob('*'):
        if not path.is_file():
            continue
        if path.name == 'Info.plist':
            info = plistlib.loads(path.read_bytes())
            minimum = info.get('MinimumOSVersion')
            if minimum and version(minimum) > version('15.0'):
                raise ValueError(f'{path}: requires iOS {minimum}')
        with path.open('rb') as stream:
            magic = stream.read(4)
        if magic in MACHO_MAGICS:
            output = subprocess.check_output(['xcrun', 'vtool', '-show-build', str(path)], text=True)
            check_minos(output, path)
            count += 1
    if not count:
        raise ValueError('No Mach-O binaries found')
    print(f'Verified {count} Mach-O binaries: minimum OS <= iOS 15.0')


if __name__ == '__main__':
    audit(Path(sys.argv[1]))
