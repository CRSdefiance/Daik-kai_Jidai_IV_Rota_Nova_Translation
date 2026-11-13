"""Bind the authored Lil B312–B319 readings to the exact clean source."""

from pathlib import Path
import subprocess
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


ROOT = Path('work/Lil254_B312_B319_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil254_clean_20261110_v1')
DRAFT_FILES = [ARCHIVE / name for name in ('B312_B315_drafts.txt', 'B316_B319_drafts.txt')]


def main():
    packet = ROOT / 'clean_source_packet.json'
    groups = load(packet)['groups']
    full_ids = {'B' + row['id'].split('_B', 1)[1]: row['id']
                for group in groups for row in group['records']}
    contexts, rows = {}, []
    for path in DRAFT_FILES:
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.startswith('@'):
                block, context = line[1:].split('|', 1)
                assert block not in contexts and context
                contexts[block] = context
            else:
                abbreviation, meaning, english = line.split('|')
                assert abbreviation.startswith(f'B{block}_')
                rows.append([full_ids[abbreviation], meaning, english])
    assert list(contexts) == list(map(str, range(312, 320)))
    assert [row[0] for row in rows] == list(full_ids.values()) and len(rows) == 254
    authored = ROOT / 'authored_B312_B319_v1.json'
    part = ROOT / 'clean_part_B312_B319_v1'
    assert not authored.exists() and not part.exists()
    save(authored, dict(
        contexts=contexts, records=rows, whole_clean_exchanges_read_before_drafting=True,
        current_English_not_consulted=True, source_gloss_precedes_independent_draft_in_each_entry=True,
        evidence={str(path): digest(path) for path in [*DRAFT_FILES, packet, Path(__file__)]}, new_credit=0,
    ))
    subprocess.run([sys.executable, '-m', 'scripts.save_clean_editorial_part_v1',
                    '--packet', str(packet), '--authored', str(authored), '--out', str(part)], check=True)
    subprocess.run([sys.executable, '-m', 'scripts.seal_clean_editorial_parts_v2',
                    '--packet', str(packet), '--parts', str(part), '--expected-records', '254'], check=True)


if __name__ == '__main__':
    main()
