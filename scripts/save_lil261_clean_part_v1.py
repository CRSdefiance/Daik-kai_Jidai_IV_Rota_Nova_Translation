"""Bind a complete set of Lil source-first drafts to the clean packet."""

import argparse
from pathlib import Path
import subprocess
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


ROOT = Path('work/Lil261_B323_B335_clean_20261110')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drafts', type=Path, nargs='+', required=True)
    parser.add_argument('--part', required=True)
    args = parser.parse_args()
    packet = ROOT / 'clean_source_packet.json'
    groups = load(packet)['groups']
    ids = {'B' + row['id'].split('_B', 1)[1]: row['id'] for group in groups for row in group['records']}
    contexts, records = {}, []
    for path in args.drafts:
        block = None
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.startswith('@'):
                block, context = line[1:].split('|', 1)
                assert block not in contexts and context
                contexts[block] = context
                continue
            short, meaning, english = line.split('|')
            assert short.startswith(f'B{block}_')
            records.append([ids[short], meaning, english])
    expected = [row['id'] for group in groups if str(group['block']) in contexts for row in group['records']]
    assert [row[0] for row in records] == expected
    authored = ROOT / f'authored_{args.part}.json'
    out = ROOT / f'clean_part_{args.part}'
    assert not authored.exists() and not out.exists()
    save(authored, dict(contexts=contexts, records=records, whole_clean_exchanges_read_before_drafting=True,
        current_English_not_consulted=True, source_gloss_precedes_independent_draft_in_each_entry=True,
        evidence={str(path): digest(path) for path in [*args.drafts, packet, Path(__file__)]}, new_credit=0))
    subprocess.run([sys.executable, '-m', 'scripts.save_clean_editorial_part_v1', '--packet', str(packet),
                    '--authored', str(authored), '--out', str(out)], check=True)


if __name__ == '__main__':
    main()
