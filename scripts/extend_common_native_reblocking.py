"""Extend a complete registered reblocking transform with reviewed manuscripts."""
import argparse
import copy
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.bgm_title_tracking import apply_probe
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_reblocking import plan
from dk4tool.script.common_native_repack import repack_native_records
from dk4tool.script.common_reblocking_release import (
    apply_common_reblocking,
    read_preserved_neighbors,
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent-profile', required=True)
    parser.add_argument('--manuscript', type=Path, action='append', required=True)
    parser.add_argument('--release-version', type=int, required=True)
    parser.add_argument('--reviewed', action='store_true')
    parser.add_argument('--compact-existing-english-padding', action='store_true')
    parser.add_argument('--preserve-native-message', type=int, action='append', default=[])
    parser.add_argument('--preservation-reason')
    parser.add_argument('--translate-preserved-native-message', type=int, action='append', default=[])
    parser.add_argument('--bgm-title-tracking-renderer', action='store_true')
    args = parser.parse_args()
    stack_path = Path('translations/release_stack.json')
    stack = json.loads(stack_path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles'][args.parent_profile])
    previous = json.loads(Path(profile['common_native_reblocking']).read_text(encoding='utf-8'))
    config = copy.deepcopy(previous)
    if args.bgm_title_tracking_renderer:
        config['bgm_title_tracking_renderer'] = True
    if args.compact_existing_english_padding:
        config['compact_existing_english_padding'] = True
    for path in args.manuscript:
        config['manuscripts'].append({'path': path.as_posix(), 'sha256': sha(path.read_bytes())})
    clean = NdsImage.open('work/clean.nds')
    source_common = clean.read_file('/COMMON/MESFILE.DK4')
    source = common_message_entries(source_common, clean.read_file('/__arm9__.bin'))

    def load(declarations):
        result = {}
        for declaration in declarations:
            raw = Path(declaration['path']).read_bytes()
            if sha(raw) != declaration['sha256']:
                raise ValueError('Inherited or new manuscript hash differs')
            payload = json.loads(raw)
            if args.reviewed:
                validate_natural_dialogue_batch(payload)
            for row in payload['records']:
                i = row['message_id']
                if i in result or bytes.fromhex(row['source_hex']) != source[i].text:
                    raise ValueError('Duplicate ID or changed clean source')
                result[i] = row['english'].removesuffix('{PAD}').encode('cp932')
        return result

    authored = load(config['manuscripts'])
    pre_authored = load(config.get('pre_repack_manuscripts', []))
    if authored.keys() & pre_authored.keys():
        raise ValueError('Duplicate pre-repack and reblocking IDs')
    parent = NdsImage.open(config['parent_candidate'])
    common, arm9 = parent.read_file('/COMMON/MESFILE.DK4'), parent.read_file('/__arm9__.bin')
    if sha(common) != config['parent_common_sha256'] or sha(arm9) != config['parent_arm9_sha256']:
        raise ValueError('Registered parent differs')
    stage_common, stage_arm9 = common, arm9
    if pre_authored:
        blocks = IlnkContainer.parse(source_common).blocks
        prefixes = {}
        for i in pre_authored:
            e = source[i]
            owner = e.block, e.record_index
            first = next(v for v in source if (v.block, v.record_index) == owner)
            prefixes[owner] = blocks[e.block].split(b'\0')[e.record_index][:first.start]
        stage = repack_native_records(common, arm9, pre_authored, prefixes)
        stage_common, stage_arm9 = stage.common, stage.arm9
    current = common_message_entries(stage_common, stage_arm9, clean=False)
    if args.translate_preserved_native_message:
        retiring = set(args.translate_preserved_native_message)
        declarations = config.get('preserved_native_neighbors', [])
        if (not retiring <= {r['message_id'] for r in declarations}
                or not retiring <= authored.keys()):
            raise ValueError('Retired preservation requires an inherited lock and new authored translation')
        # Verify the old full source/current locks before explicitly replacing
        # them with new source-locked authored rows. Reviewed registration also
        # requires all five editorial gates on those rows.
        read_preserved_neighbors(declarations, source, current, authored.keys() - retiring)
        config['preserved_native_neighbors'] = [r for r in declarations if r['message_id'] not in retiring]
    if args.preserve_native_message:
        if not args.preservation_reason or not args.preservation_reason.strip():
            raise ValueError('Preserved neighbors require a written reason')
        declarations = config.setdefault('preserved_native_neighbors', [])
        for i in args.preserve_native_message:
            if not 0 <= i < len(source):
                raise ValueError('Preserved native ID is outside the source map')
            declarations.append({'message_id': i, 'source_hex': source[i].text.hex(),
                                 'current_hex': current[i].text.hex(),
                                 'status': 'untranslated-renderer-classification-pending',
                                 'reason': args.preservation_reason})
    preserved = read_preserved_neighbors(config.get('preserved_native_neighbors', []),
                                         source, current, authored)
    rebuilt, mapped, report = plan(stage_common, stage_arm9, authored, config['first_reblocked_block'],
                                  compact_existing_english_padding=config.get('compact_existing_english_padding', False),
                                  preserved=preserved)
    if config.get('bgm_title_tracking_renderer', False):
        if not set(range(3251, 3289)) <= authored.keys():
            raise ValueError('BGM renderer requires all 38 complete titles')
        mapped = apply_probe(mapped)
        report.update({'executable_code_unchanged': False,
                       'common_loader_selector_code_unchanged': True,
                       'bgm_title_ascii_advance': 5})
    analysis = Path(f'work/analysis/common_reblock_v{args.release_version}')
    analysis.mkdir(parents=True, exist_ok=True)
    (analysis / 'COMMON.bin').write_bytes(rebuilt)
    (analysis / 'ARM9.bin').write_bytes(mapped)
    write_json(analysis / 'plan.json', report)
    print(f"All {report['all_native_messages_compared']} selections compared; directory {report['directory_sha256']}")
    if not args.reviewed:
        print('Research plan only; review previews and register the independently verified directory hash before integration.')
        return
    selected = common_message_entries(rebuilt, mapped, clean=False)
    owners = defaultdict(list)
    for e in selected:
        owners[e.block, e.record_index].append(e)
    blocks = IlnkContainer.parse(rebuilt).blocks
    records = []
    for (block, record), entries in sorted(owners.items()):
        raw = blocks[block].split(b'\0')[record]
        paragraphs = [e.text.rstrip(b' ').decode('cp932') for e in entries]
        records.append({'id': f'DK4_MES_B{block:02d}_R{record:04d}',
                        'replacement_hex': raw.hex().upper(), 'english': ' | '.join(paragraphs),
                        'display_entries': paragraphs, 'native_message_ids': [e.message_id for e in entries],
                        'entry_offsets': [e.start for e in entries], 'entry_ends': [e.end for e in entries],
                        'native_table_offsets': [e.table_offset for e in entries], 'entry_guard_bytes': 0,
                        'context': 'Complete final native layout; global IDs preserve source identity after reblocking.'})
    layout_path = f'translations/common_native_reblocking_layout_v{args.release_version}.json'
    write_json(layout_path, {'format': 'dk4-ilnk-translation-batch-v1',
                             'content_type': 'common-native-layout-v1', 'file_path': '/COMMON/MESFILE.DK4',
                             'note': 'Audit declaration only; applied through the reviewed complete transform.',
                             'records': records})
    config.update({'expected_common_sha256': sha(rebuilt), 'expected_arm9_sha256': sha(mapped),
                   'directory_sha256': report['directory_sha256'], 'layout_batch': layout_path,
                   'layout_batch_sha256': sha(Path(layout_path).read_bytes())})
    config_path = Path(f'translations/common_native_reblocking_v{args.release_version}.json')
    write_json(config_path, config)
    apply_common_reblocking(common, arm9, config_path)
    profile['common_native_reblocking'] = config_path.as_posix()
    profile['note'] = (f'Extends {args.parent_profile} with clean-source reviewed native manuscripts; '
                       'reconstructs all inherited layers and authored messages; runtime acceptance pending.')
    stack['profiles'][f'all-routes-unified-v{args.release_version}'] = profile
    write_json(stack_path, stack)
    print(f'Registered V{args.release_version}: {len(authored) + len(pre_authored)} reviewed authored messages')


if __name__ == '__main__':
    main()
