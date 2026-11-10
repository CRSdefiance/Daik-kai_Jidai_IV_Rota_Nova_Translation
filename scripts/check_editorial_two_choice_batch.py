"""Run the established two-choice checks on each complete reviewed menu object."""
import argparse
from copy import deepcopy
from pathlib import Path
import subprocess
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['manuscript', 'release', 'startup', 'out']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    doc = load(args.manuscript)
    groups = {}
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            ref = row['source_reference']
            groups.setdefault((ref['block'], ref['command_offset']), []).append(row)
    assert groups and all(len(rows) == 2 for rows in groups.values())
    assert sum(map(len, groups.values())) == doc['typed_choice_objects']
    args.out.mkdir(parents=True)
    objects = []
    for (block, offset), rows in groups.items():
        subset = deepcopy(doc)
        subset.update(records=rows, blocks=[block], total_editorial_objects=2,
                      physical_speech_objects=0, ordinary_speech_objects=0,
                      personality_alternatives=0, personality_alias_slots=0,
                      typed_choice_objects=2, typed_choice_commands=1,
                      revised=sum(r['decision'] == 'revision' for r in rows),
                      retained=sum(r['decision'] == 'retention' for r in rows),
                      subset_of=str(args.manuscript), subset_of_sha256=sha(args.manuscript.read_bytes()))
        path = args.out / f'B{block}_C{offset}_manuscript.json'
        save(path, subset)
        out = args.out / f'B{block}_C{offset}'
        subprocess.run([sys.executable, 'scripts/check_editorial_two_choice_display.py',
                        '--manuscript', str(path), '--release', str(args.release),
                        '--startup', str(args.startup), '--out', str(out)], check=True)
        receipt = out / 'menu_provider_and_planes.json'
        proof = load(receipt)
        objects.append(dict(block=block, source_command_offset=offset,
                            record_ids=[r['id'] for r in rows],
                            receipt=str(receipt), receipt_sha256=sha(receipt.read_bytes()),
                            compiled_path=str(out / 'compiled_choice_object.bin'),
                            compiled_sha256=sha((out / 'compiled_choice_object.bin').read_bytes()),
                            review_sheet=proof['review_sheet']))
    save(args.out / 'complete_choice_objects.json', dict(
        manuscript=str(args.manuscript), manuscript_sha256=sha(args.manuscript.read_bytes()),
        objects=objects, physical_caption_records=2 * len(objects),
        native_provider_alignments=6 * len(objects), bridged_modal_returns=18 * len(objects),
        complete_caption_style_planes=8 * len(objects),
        all_checks_pass=True, direct_view_pending=True, actual_gameplay=False,
        stored_integration_and_actual_controller_still_pending=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [Path(__file__), Path('scripts/check_editorial_two_choice_display.py')]}))
    print(dict(menus=len(objects), caption_records=2 * len(objects), all_native_checks_pass=True), flush=True)


if __name__ == '__main__':
    main()
