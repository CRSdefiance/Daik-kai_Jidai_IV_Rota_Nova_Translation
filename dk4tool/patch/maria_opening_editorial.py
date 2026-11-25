"""Source-bound CS0101 B33 editorial compiler with six proven presentation selectors."""
import json
import re
import struct
from itertools import pairwise
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.maria_opening_profile import profile_for
from dk4tool.dialogue.qa import audit_relocatable_dialogue_record
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH = '/data/SC3.DK4'
CONFIG = 'translations/maria_opening_editorial_release_v1.json'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(condition, message):
    if not condition:
        raise ValueError('Maria opening ' + message)


def mapped(patches, offset):
    delta = 0
    for patch in patches:
        require(not patch['start'] < offset < patch['end'], 'unclassified interior reference')
        if offset >= patch['end']:
            delta += len(patch['new']) - len(patch['old'])
    return offset + delta


def apply_release(image, baseline, config_path=CONFIG):
    config = load(config_path)
    require(config.get('format') == 'dk4-maria-opening-editorial-release-v1', 'unknown release format')
    for path, digest in config['dependencies'].items():
        require(sha(Path(path).read_bytes()) == digest, 'reviewed dependency differs: ' + path)
    before_file = image.read_file(PATH)
    arm = image.read_file('/__arm9__.bin')
    require(sha(before_file) == config['source_SC3_sha256'], 'current SC3 differs')
    require(sha(arm) == config['required_runtime_ARM9_sha256'], 'runtime differs')
    require(sha(baseline.read_file(PATH)) == config['canonical_SC3_sha256'], 'canonical SC3 differs')
    require(sha(Path(config['clean_ROM']).read_bytes()) == config['clean_ROM_sha256'], 'clean ROM differs')
    clean_file = NdsImage.open(config['clean_ROM']).read_file(PATH)
    require(sha(clean_file) == config['clean_SC3_sha256'], 'clean SC3 differs')
    doc, mapping = map(load, (config['manuscript'], config['reference_map']))
    validate_natural_dialogue_batch(doc)
    require(doc['encoder'] == 'dialogue-relocatable-v1' and doc['dialogue_profile'] == 'maria-story-shared-events-live'
            and doc.get('scoped_native_profile') == 'maria-opening-editorial-native-v1'
            and doc.get('formatting_review_pending') is False, 'complete scoped formatting required')
    require(mapping.get('format') == 'dk4-maria-opening-source-relocation-map-v1'
            and mapping.get('external_references_complete') is True
            and mapping.get('preserve_record_parity') is True and mapping.get('entry_point_offset') == 8
            and mapping.get('all_native_formatting_typed_reference_and_representative_actual_gates_pass') is True,
            'complete native reference and representative actual contract required')
    for key in ('source_SC3_sha256', 'target_SC3_sha256'):
        require(mapping[key] == config[key], 'map/file lock differs')
    actual = load(doc['actual_representative_proof'])
    require(actual.get('all38_speeches85_commands_and_normal_Hangzhou_return') is True
            and actual.get('actual_all_six_presentation_states_and_complete_native_planes_match') is True
            and actual.get('existing_isolated_system_unlock_save_not_earned_and_no_savestate_story_location_RNG_funds_outcome_fixture') is True
            and actual.get('complete_matching_speech_panels', 0) >= 35,
            'source-bound representative actual coverage required')
    require(actual['research_ROM_sha256'] == config['tested_research_ROM_sha256'], 'actual research ROM differs')
    packet = load(doc['source_packet'])
    require(sha(Path(doc['source_packet']).read_bytes()) == doc['source_packet_sha256'], 'source packet differs')
    specs = {33: packet}
    container, japanese = map(IlnkContainer.parse, (before_file, clean_file))
    require(len(container.blocks) == len(japanese.blocks) == 303, 'route block count differs')
    require(len(doc['records']) == len({r['id'] for r in doc['records']}) == 38, 'complete38 speech identities required')
    require([b['block'] for b in mapping['blocks']] == [33], 'complete B33 required')
    require({r['block'] for r in doc['records']} == {33}, 'speech block ownership differs')
    changes, reports = [], []
    progressive = modal_count = commands_count = edges_count = 0
    for spec in mapping['blocks']:
        number = spec['block']
        block, original = container.blocks[number], japanese.blocks[number]
        require(sha(block) == spec['source_block_sha256'] and sha(original) == spec['clean_block_sha256'],
                'exact current/clean block required')
        rows = [r for r in doc['records'] if r['block'] == number]
        refs = {r['id']: r for r in spec['text_records']}
        require(len(rows) == len(refs) == {33: 38}[number], 'complete block speech coverage required')
        patches = []
        for row in rows:
            ident = row['id']
            require(row.get('editorial_decision') in ('revise', 'retain-wording')
                    and (row['editorial_decision'] != 'retain-wording'
                         or bool(str(row.get('fresh_retained_wording_justification', '')).strip())),
                    'explicit revision or justified retention required')
            require(row['file_path'] == PATH and ident in refs, 'speech ownership differs')
            ref = refs[ident]
            for data, key, hexkey, indexkey in (
                (block, 'current_reference', 'current_text_hex', 'record_index'),
                (original, 'source_reference', 'source_hex', 'source_record_index'),
            ):
                at = row[key]['offset']
                raw = bytes.fromhex(row[hexkey])
                require(data[at:at + len(raw)] == raw and data[at + len(raw)] == 0, 'exact source text differs: ' + ident)
                require(row[indexkey] == data[:at].count(b'\0') == row[key]['segment_index'], 'source/current NUL index differs')
                header = row[key]['header_offset']
                require(at == header + 5 and data[header:header + 6].hex() == row['source_complete_preamble_hex'],
                        'complete speech preamble differs')
            require(bytes.fromhex(row['source_hex'])[1:].decode('cp932') == row['source_Japanese'], 'Japanese metadata differs')
            require(re.findall('FI|FA|FO', row['source_Japanese'])
                    == re.findall(r'\{MACRO:(FI|FA|FO)\}', row['english']), 'source substitutions differ')
            prefix = row['source_presentation_prefix_hex']
            modal = prefix == 'fe'
            require(prefix in ('03', '0a', '0b', '0c', '15', '4a'), 'unmapped presentation selector')
            marker = '{SPEAKER:' + prefix.upper() + '}'
            require(row['english'].startswith(marker), 'authored speaker differs')
            start = row['current_reference']['header_offset']
            require(start == ref['old_command_offset'], 'command reference differs')
            old = block[start:start + ref['old_native_extent']]
            require(old[:6].hex() == ref['source_preamble_hex'] and old[5:6].hex() == prefix, 'native preamble differs')
            require(row['target_command_offset'] == ref['new_command_offset']
                    and row['target_record_index'] == ref['new_record_index'], 'target metadata differs')
            require(not modal and ref['final_parity_native_plane_exact'] is True,
                    'separate consumer or final parity proof differs')
            profile = profile_for(arm, block, number, modal=modal)
            encoded = encode_relocatable_dialogue(bytes.fromhex(row['current_text_hex']), row['english'], profile)
            require(encoded.encoded[:1] == bytes.fromhex(prefix), 'compiled selector differs')
            allowed = set(row.get('qa_waivers', []))
            require(not allowed, 'unreviewed warning waiver')
            qa = audit_relocatable_dialogue_record(bytes.fromhex(row['current_text_hex']), row['english'], profile)
            require(not [i for i in qa['issues'] if i['severity'] == 'error' or (i['severity'] == 'warning' and i['code'] not in allowed)], 'unreviewed formatting diagnostic')
            payload = encoded.encoded[1:]
            value = payload + (b' ' if len(payload) % 2 != len(bytes.fromhex(row['current_text_hex'])[1:]) % 2 else b'')
            target = old[:6] + value + b'\0'
            target += b'\0' * (-len(target) % 2)
            require(value.hex() == ref['target_text_excluding_speaker_hex'] and target.hex() == ref['target_hex']
                    == row['target_native_command_hex'], 'reviewed compiled target differs')
            patches.append({'start': start, 'end': start + len(old), 'old': old, 'new': target})
            progressive += int(not modal)
            modal_count += int(modal)
            if target != old:
                changes.append({'id': ident, 'file_path': PATH, 'block': number, 'old_offset': start,
                                'new_offset': ref['new_command_offset'], 'old_bytes': len(old), 'new_bytes': len(target)})
        patches.sort(key=lambda p: p['start'])
        require(all(a['end'] <= b['start'] for a, b in pairwise(patches)), 'speech patches overlap')
        end = 8 + struct.unpack_from('<H', block, 4)[0]
        require(block[:4] == b'CS\1\1' and end <= len(block) and not any(block[end:]), 'original CS extent differs')
        parts, last = [], 0
        for patch in patches:
            parts.extend((block[last:patch['start']], patch['new']))
            last = patch['end']
        parts.append(block[last:end])
        logical = bytearray(b''.join(parts))
        require(len(logical) == mapped(patches, end) and len(logical) < 0x2400, 'native cache/mapped extent exceeded')
        commands, edges = spec['mapped_native_commands'], spec['relative_skip_fixups']
        native = specs[number]['native_commands']['current']['commands']
        require(len(commands) == len(native) == {33: 85}[number], 'complete native command map required')
        require(len(edges) == {33: 0}[number], 'complete relative-site map required')
        require({r['offset'] for r in edges} == {r['offset'] for r in native if r['word'] in (0x100, 0x200, 0x300, 0x400)},
                'relative site identities differ')
        boundaries = {r['old_offset'] for r in commands} | {end}
        for edge in edges:
            at = edge['offset']
            require(struct.unpack_from('<HH', block, at) == (edge['word'], edge['source_span']), 'stored skip differs')
            old_target = at + 4 + edge['source_span']
            require(old_target == edge['source_matched_target'] and old_target in boundaries
                    and at + 4 == edge['source_unmatched_next'] and at + 4 in boundaries, 'source skip target differs')
            new_at, new_target = mapped(patches, at), mapped(patches, old_target)
            span = new_target - new_at - 4
            require(new_at == edge['new_offset'] and new_target == edge['new_matched_target']
                    and new_at + 4 == edge['new_unmatched_next'] and span == edge['target_span']
                    and 0 <= span <= 0xFFFF and span % 2 == 0, 'target skip mapping differs')
            struct.pack_into('<H', logical, new_at + 2, span)
        for command, source in zip(commands, native, strict=True):
            at, new_at = command['old_offset'], command['new_offset']
            require(at == source['offset'] and command['word'] == source['word']
                    and command['old_native_extent'] == source['native_extent']
                    and command['source_0100_ancestors'] == source['ancestor_0100_offsets'], 'original command mapping differs')
            require(new_at == mapped(patches, at)
                    and mapped(patches, at + command['old_native_extent']) - new_at == command['new_native_extent'], 'command extent differs')
            require(struct.unpack_from('<H', block, at)[0] == struct.unpack_from('<H', logical, new_at)[0] == command['word'],
                    'native command word differs')
            require(command['target_0100_ancestors'] == [mapped(patches, a) for a in command['source_0100_ancestors']], 'nested owner differs')
            if command['word'] == 0x4000:
                require(block[at:at + 6] == logical[new_at:new_at + 6], 'complete native speech preamble changed')
            elif command['word'] not in (0x100, 0x200, 0x300, 0x400):
                require(block[at:at + command['old_native_extent']] == logical[new_at:new_at + command['new_native_extent']],
                        'unowned opaque command changed')
        struct.pack_into('<H', logical, 4, len(logical) - 8)
        target = bytes(logical) + b'\0' * (-len(logical) % 4)
        require(target.hex() == spec['target_hex'] and sha(target) == spec['target_block_sha256'], 'final target block differs')
        for ref in refs.values():
            at = ref['new_offset']
            require(at == ref['new_command_offset'] + 5 and target[:at].count(b'\0') == ref['new_record_index'], 'final NUL index differs')
        container.blocks[number] = target
        reports.append({'block': number, 'old_bytes': len(block), 'new_bytes': len(target), 'growth_bytes': len(target) - len(block)})
        commands_count += len(commands)
        edges_count += len(edges)
    require((progressive, modal_count, commands_count, edges_count) == (38, 0, 85, 0), 'complete family totals differ')
    output = container.to_bytes()
    require(sha(output) == config['target_SC3_sha256'], 'final route differs from actual-tested research')
    # The sole mutation follows every source, review, native, actual and target guard.
    image.replace_file(PATH, output)
    return {
        'format': 'dk4-maria-opening-editorial-release-v1', 'manuscript': config['manuscript'],
        'reference_map': config['reference_map'], 'changed_records': changes, 'blocks': reports,
        'source_SC3_sha256': sha(before_file), 'target_SC3_sha256': sha(output),
        'compiled_progressive_records': 38, 'separate_FE_records': 0, 'typed_commands': 85, 'relative_sites': 0,
        'all302_other_blocks_all_other_files_components_preserved': True,
        'complete_native_and_practical_representative_actual_evidence_bound': True,
        'sole_SC3_mutation_after_all_guards': True,
    }
