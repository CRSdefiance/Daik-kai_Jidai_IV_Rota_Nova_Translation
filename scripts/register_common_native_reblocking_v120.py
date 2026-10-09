"""Register the reviewed complete B12 transform after V119's full layer stack."""
import copy
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_reblocking import plan
from dk4tool.script.common_native_repack import repack_native_records
from dk4tool.script.common_reblocking_release import apply_common_reblocking


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    manuscript = Path('translations/common_b12_complete_manuscript_v1.json')
    payload = json.loads(manuscript.read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(payload)
    parent = NdsImage.open('out/all_routes_combined_v119_candidate.nds')
    common, arm9 = parent.read_file('/COMMON/MESFILE.DK4'), parent.read_file('/__arm9__.bin')
    authored = {r['message_id']: r['english'].removesuffix('{PAD}').encode('cp932') for r in payload['records']}
    pre_manuscript = Path('translations/common_b6_question_repair_manuscript_v1.json')
    pre_payload = json.loads(pre_manuscript.read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(pre_payload)
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    clean_blocks = IlnkContainer.parse(clean.read_file('/COMMON/MESFILE.DK4')).blocks
    pre_authored = {r['message_id']: r['english'].removesuffix('{PAD}').encode('cp932') for r in pre_payload['records']}
    prefixes = {}
    for i in pre_authored:
        e = source[i]
        owner = (e.block, e.record_index)
        if owner not in prefixes:
            first = next(v for v in source if (v.block, v.record_index) == owner)
            prefixes[owner] = clean_blocks[e.block].split(b'\0')[e.record_index][:first.start]
    repaired = repack_native_records(common, arm9, pre_authored, prefixes)
    rebuilt, mapped, report = plan(repaired.common, repaired.arm9, authored)
    selected = common_message_entries(rebuilt, mapped, clean=False)
    blocks = IlnkContainer.parse(rebuilt).blocks
    owners = defaultdict(list)
    for e in selected:
        owners[e.block, e.record_index].append(e)
    records = []
    for (block, record), entries in sorted(owners.items()):
        raw = blocks[block].split(b'\0')[record]
        paragraphs = [e.text.rstrip(b' ').decode('cp932') for e in entries]
        records.append({'id': f'DK4_MES_B{block:02d}_R{record:04d}',
                        'replacement_hex': raw.hex().upper(), 'english': ' | '.join(paragraphs),
                        'display_entries': paragraphs, 'native_message_ids': [e.message_id for e in entries],
                        'entry_offsets': [e.start for e in entries], 'entry_ends': [e.end for e in entries],
                        'native_table_offsets': [e.table_offset for e in entries], 'entry_guard_bytes': 0,
                        'context': 'Complete final native layout; identities are global message IDs, not former block/record coordinates.'})
    layout_path = 'translations/common_native_reblocking_layout_v120.json'
    write_json(layout_path, {'format': 'dk4-ilnk-translation-batch-v1',
                             'content_type': 'common-native-layout-v1', 'file_path': '/COMMON/MESFILE.DK4',
                             'note': 'Audit declaration only; applied through the reviewed reblocking transform, not record replacements.',
                             'records': records})
    config_path = 'translations/common_native_reblocking_v120.json'
    config = {'format': 'dk4-common-native-reblocking-v1',
              'parent_common_sha256': sha(common), 'parent_arm9_sha256': sha(arm9),
              'parent_candidate': 'out/all_routes_combined_v119_candidate.nds',
              'manuscripts': [{'path': manuscript.as_posix(), 'sha256': sha(manuscript.read_bytes())}],
              'pre_repack_manuscripts': [{'path': pre_manuscript.as_posix(), 'sha256': sha(pre_manuscript.read_bytes())}],
              'first_reblocked_block': 12, 'expected_common_sha256': sha(rebuilt),
              'expected_arm9_sha256': sha(mapped), 'directory_sha256': report['directory_sha256'],
              'layout_batch': layout_path, 'layout_batch_sha256': sha(Path(layout_path).read_bytes())}
    write_json(config_path, config)
    # Validate source locks, editorial/prose QA, output hashes and final layout
    # through exactly the function the integrated builder will call.
    apply_common_reblocking(common, arm9, Path(config_path))
    stack_path = Path('translations/release_stack.json')
    stack = json.loads(stack_path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v119'])
    profile['common_native_reblocking'] = config_path
    profile['note'] = ('Rebuilds every V119 layer, then repairs B6 messages 468/469 and applies 77 reviewed B12 messages '
                       'through source-locked whole-record reblocking; all global messages '
                       'verified; runtime acceptance pending.')
    stack['profiles']['all-routes-unified-v120'] = profile
    write_json(stack_path, stack)
    print('Registered V120 transform: 79 reviewed messages, complete final layout, all V119 layers retained.')


if __name__ == '__main__':
    main()
