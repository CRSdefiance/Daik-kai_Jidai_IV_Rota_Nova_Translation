"""Research whole-record COMMON reblocking without changing executable code.

This produces analysis artifacts only, never a playable release. The integrated
builder must separately implement and verify this format before it is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_reblocking import plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', required=True, type=Path)
    parser.add_argument('--manuscript', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    current, clean = NdsImage.open(args.candidate), NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    manuscript = json.loads(args.manuscript.read_text(encoding='utf-8'))
    authored = {}
    for row in manuscript['records']:
        i = row['message_id']
        if bytes.fromhex(row['source_hex']) != source[i].text:
            raise ValueError('Manuscript differs from clean native source')
        if i in authored:
            raise ValueError('Duplicate authored message ID')
        if re.findall(r'%[sdi]', row['english']) != re.findall(r'%[sdi]', source[i].text.decode('cp932')):
            raise ValueError('Runtime argument count/type/order differs from clean source')
        authored[i] = row['english'].removesuffix('{PAD}').encode('cp932')
    common, arm9, report = plan(current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin'), authored)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, data in [('common.bin', common), ('arm9.bin', arm9)]:
        (args.out / name).write_bytes(data)
    report['parent_candidate'] = args.candidate.as_posix()
    report['manuscript'] = args.manuscript.as_posix()
    report['expected_common_sha256'] = hashlib.sha256(common).hexdigest()
    report['expected_arm9_sha256'] = hashlib.sha256(arm9).hexdigest()
    (args.out / 'plan.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'relocations'}, indent=2))


if __name__ == '__main__':
    main()
