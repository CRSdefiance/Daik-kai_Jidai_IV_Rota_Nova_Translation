"""Source-bound complete B44 editorial layer and two inherited skip repairs."""
import json
import re
import struct
from itertools import pairwise
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.rafael_opening_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH = '/data/SC0.DK4'
CONFIG = 'translations/rafael_opening_editorial_release_v1.json'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(condition, message):
    if not condition:
        raise ValueError('Rafael opening ' + message)


def mapped(patches, offset):
    delta = 0
    for patch in patches:
        require(not patch['start'] < offset < patch['end'], 'unclassified interior reference')
        if offset >= patch['end']:
            delta += len(patch['new']) - len(patch['old'])
    return offset + delta


def apply_release(image, baseline, config_path=CONFIG):
    config = load(config_path)
    require(config.get('format') == 'dk4-rafael-opening-editorial-release-v1', 'unknown release format')
    for path, digest in config['dependencies'].items():
        require(sha(Path(path).read_bytes()) == digest, 'reviewed dependency differs: ' + path)
    before_file = image.read_file(PATH)
    arm = image.read_file('/__arm9__.bin')
    require(sha(before_file) == config['source_SC0_sha256'], 'current SC0 differs')
    require(sha(arm) == config['required_runtime_ARM9_sha256'], 'runtime differs')
    require(sha(baseline.read_file(PATH)) == config['canonical_SC0_sha256'], 'canonical SC0 differs')
    require(sha(Path(config['clean_ROM']).read_bytes()) == config['clean_ROM_sha256'], 'clean ROM differs')
    clean_file = NdsImage.open(config['clean_ROM']).read_file(PATH)
    require(sha(clean_file) == config['clean_SC0_sha256'], 'clean SC0 differs')
    doc, menu, mapping = map(load, (config['manuscript'], config['choices'], config['reference_map']))
    validate_natural_dialogue_batch(doc)
    validate_natural_dialogue_batch(menu)
    require(doc['encoder'] == 'dialogue-relocatable-v1' and doc['dialogue_profile'] == 'raphael-story-live'
            and doc.get('scoped_native_profile') == 'rafael-opening-editorial-native-v1'
            and doc.get('formatting_review_pending') is False, 'complete scoped formatting required')
    require(menu['encoder'] == 'dialogue-fixed-v1' and menu.get('formatting_review_pending') is False,
            'complete typed choice review required')
    require(mapping.get('format') == 'dk4-rafael-opening-source-relocation-map-v1'
            and mapping.get('external_references_complete') is True
            and mapping.get('preserve_record_parity') is True
            and mapping.get('entry_point_offset') == 8
            and mapping.get('all_native_formatting_typed_reference_and_both_actual_choice_gates_pass') is True,
            'complete typed reference and actual contract required')
    for key in ('source_SC0_sha256', 'target_SC0_sha256'):
        require(mapping[key] == config[key], 'map/file lock differs')
    actual0, actual1 = map(load, (doc['actual_choice0_proof'], doc['actual_choice1_proof']))
    require(actual0.get('actual_repaired_outer0100_length72_and_cleanup6742') is True
            and actual0.get('both_guided_instructions_four_holds_complete_native_actual_ink') is True
            and actual0.get('both_actual_branches_union115_source_speeches') is True
            and actual1.get('actual_choice1_result_2_1_and_repaired0300_jump_to6674') is True
            and actual1.get('revised_R0479_two_holds_complete_native_actual_pixels') is True
            and actual1.get('unchanged_FE_money_notice_actual_complete_native_mode1_ink') is True,
            'both source-bound actual choices required')
    require(actual0['research_ROM_sha256'] == actual1['research_ROM_sha256']
            == config['tested_research_ROM_sha256'], 'actual research ROM differs')
    container, japanese = map(IlnkContainer.parse, (before_file, clean_file))
    block, original = container.blocks[44], japanese.blocks[44]
    require(len(container.blocks) == len(japanese.blocks) == 343, 'complete route block count differs')
    require(sha(block) == mapping['source_block_sha256'] and sha(original) == mapping['clean_block_sha256'],
            'exact current/clean B44 required')
    profile = profile_for(arm, block)
    require(len(doc['records']) == len(mapping['text_records']) == 115 and len(menu['records']) == 2,
            'complete115 speeches andtwo labels required')
    require(len({row['id'] for row in doc['records']}) == 115, 'speech identities overlap')
    refs = {row['id']: row for row in mapping['text_records']}
    patches, changes = [], []
    unchanged_fe = 0
    for row in doc['records']:
        ident = row['id']
        ref = refs[ident]
        require(row['file_path'] == PATH and row['block'] == 44, 'speech ownership differs')
        for data, refkey, hexkey, indexkey in (
            (block, 'current_reference', 'current_text_hex', 'record_index'),
            (original, 'source_reference', 'source_hex', 'source_record_index'),
        ):
            at = row[refkey]['offset']
            raw = bytes.fromhex(row[hexkey])
            require(data[at:at + len(raw)] == raw and data[at + len(raw)] == 0, 'exact source text differs: ' + ident)
            zero = raw[:1] == b'\0'
            index = data[:at].count(b'\0') + int(zero)
            require(row[indexkey] == index == row[refkey]['segment_index'], 'source/current NUL index differs: ' + ident)
            header = row[refkey]['header_offset']
            require(at == header + 5 and data[header:header + 6].hex() == row['source_complete_preamble_hex'],
                    'complete speech preamble differs: ' + ident)
        require(re.findall('FI|FA|FO', row['source_Japanese'])
                == re.findall(r'\{MACRO:(FI|FA|FO)\}', row['english']), 'source substitutions differ: ' + ident)
        require(bytes.fromhex(row['source_hex'])[1:].decode('cp932') == row['source_Japanese'],
                'clean Japanese prose metadata differs: ' + ident)
        prefix = row['source_presentation_prefix_hex']
        start = row['current_reference']['header_offset']
        require(start == ref['old_command_offset'], 'command reference differs: ' + ident)
        old = block[start:start + ref['old_native_extent']]
        require(old[:6].hex() == ref['source_preamble_hex'], 'native prefix differs: ' + ident)
        require(prefix == old[5:6].hex() and row['target_command_offset'] == ref['new_command_offset']
                and row['target_record_index'] == ref['new_record_index'], 'speaker/target metadata differs: ' + ident)
        marker = '{SPEAKER:' + prefix.upper() + '}'
        require(row['english'].startswith(marker), 'authored speaker differs: ' + ident)
        if prefix == 'fe':
            require(ident == 'DK4_MES_B44_R0264' and ref.get('unchanged_FE_separate_display_pending') is True,
                    'only original money FE consumer allowed')
            require(row['english'] == '{SPEAKER:FE}Received 30,000 gold!'
                    and ref['target_hex'] == old.hex() == row['target_native_command_hex'], 'FE must remain exact')
            unchanged_fe += 1
            continue
        require(prefix in ('00', '04', '05', '06'), 'unmapped progressive speaker')
        source_raw = bytes.fromhex(row['current_text_hex'])
        markup = row['english']
        if prefix == '00':
            source_raw = source_raw[1:]
            markup = markup.removeprefix(marker)
        encoded = encode_relocatable_dialogue(source_raw, markup, profile)
        allowed = set(row.get('qa_waivers', []))
        require(allowed <= {'weak-line-ending'} and (not allowed or ident == 'DK4_MES_B44_R0327'),
                'unreviewed warning waiver')
        payload = encoded.encoded if prefix == '00' else encoded.encoded[1:]
        if prefix != '00':
            require(encoded.encoded[0] == int(prefix, 16), 'compiled speaker differs')
        old_text = bytes.fromhex(row['current_text_hex'])[1:]
        value = payload + (b' ' if len(payload) % 2 != len(old_text) % 2 else b'')
        target = old[:6] + value + b'\0'
        target += b'\0' * (-len(target) % 2)
        require(value.hex() == ref['text_hex'] and target.hex() == ref['target_hex']
                == row['target_native_command_hex'], 'native reviewed target differs: ' + ident)
        require(ref.get('final_parity_native_plane_equals_reviewed_plane') is True
                and len(value) % 2 == len(old_text) % 2, 'final parity proof required')
        patches.append({'start': start, 'end': start + len(old), 'old': old, 'new': target})
        if target != old:
            changes.append({'id': ident, 'file_path': PATH, 'block': 44,
                            'old_offset': start, 'new_offset': ref['new_command_offset'],
                            'old_bytes': len(old), 'new_bytes': len(target)})
    require(len(patches) == 114 and unchanged_fe == 1, 'complete progressive/separate-modal ownership required')
    patches.sort(key=lambda p: p['start'])
    require(all(a['end'] <= b['start'] for a, b in pairwise(patches)), 'speech patches overlap')
    for row in menu['records']:
        require(row['file_path'] == PATH and row['block'] == 44, 'choice ownership differs')
        for data, refkey, hexkey in ((original, 'source_reference', 'source_hex'),
                                    (block, 'current_reference', 'current_text_hex')):
            at = row[refkey]['offset']
            value = bytes.fromhex(row[hexkey])
            require(data[at:at + len(value)] == value and data[at + len(value)] == 0, 'choice reference differs')
        text = row['english'].removesuffix('{PAD}').encode('ascii')
        require(text.hex() == row['current_text_hex'] and text in (b'Ask him.', b'Prepare alone.'),
                'typed original choice labels must remain exact')
    end = 8 + struct.unpack_from('<H', block, 4)[0]
    require(block[:4] == b'CS\0\1' and end <= len(block) and not any(block[end:]), 'original CS extent differs')
    parts, last = [], 0
    for patch in patches:
        parts.extend((block[last:patch['start']], patch['new']))
        last = patch['end']
    parts.append(block[last:end])
    logical = bytearray(b''.join(parts))
    require(len(logical) == mapped(patches, end) and len(logical) < 0x2400, 'native cache or mapped extent exceeded')
    commands = mapping['mapped_native_commands']
    require(len(commands) == 182 and len({r['old_offset'] for r in commands}) == 182,
            'complete182-command mapping required')
    edges = mapping['relative_skip_fixups']
    require(len(edges) == 4 and {r['offset'] for r in edges} == {6442, 6446, 6604, 6680},
            'complete four relative sites required')
    require({r['offset']: r['classified_intended_source_span'] for r in edges}
            == {6442: 4, 6446: 158, 6604: 76, 6680: 0}, 'clean-derived intended source targets differ')
    require(sum(r['inherited_stale_span_explicitly_repaired'] for r in edges) == 2,
            'both inherited stale operands require explicit repair')
    boundaries = {r['old_offset'] for r in commands} | {end}
    for edge in edges:
        at = edge['offset']
        require(struct.unpack_from('<HH', block, at) == (edge['word'], edge['actual_source_span']), 'stored skip differs')
        intended = at + 4 + edge['classified_intended_source_span']
        require(intended == edge['intended_source_matched_target'] and intended in boundaries,
                'intended source target differs')
        new_at = mapped(patches, at)
        new_target = mapped(patches, intended)
        span = new_target - new_at - 4
        require(new_at == edge['new_offset'] and new_target == edge['new_matched_skip_target']
                and new_at + 4 == edge['new_unmatched_next'] and span == edge['target_span']
                and 0 <= span <= 0xFFFF and span % 2 == 0, 'target skip mapping differs')
        struct.pack_into('<H', logical, new_at + 2, span)
    for command in commands:
        at = command['old_offset']
        new_at = mapped(patches, at)
        require(new_at == command['new_offset']
                and mapped(patches, at + command['old_native_extent']) - new_at == command['new_native_extent'],
                'command extent mapping differs')
        require(struct.unpack_from('<H', block, at)[0] == struct.unpack_from('<H', logical, new_at)[0]
                == command['word'], 'native command word differs')
        require(command['target_0100_ancestors'] == [mapped(patches, a) for a in command['source_0100_ancestors']],
                'nested command owner differs')
        if command['word'] == 0x4000:
            require(block[at:at + 6] == logical[new_at:new_at + 6], 'complete native speech preamble changed')
        elif command['word'] not in (0x100, 0x200, 0x300):
            require(block[at:at + command['old_native_extent']]
                    == logical[new_at:new_at + command['new_native_extent']], 'unowned opaque command changed')
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    target = bytes(logical) + b'\0' * (-len(logical) % 4)
    for ref in mapping['text_records']:
        start = ref['new_command_offset']
        at = start + 5
        index = target[:at].count(b'\0') + int(target[at] == 0)
        require(index == ref['new_record_index'], 'final source/current NUL index differs')
    require(sha(target) == mapping['target_block_sha256'], 'final B44 differs from actual-tested research')
    container.blocks[44] = target
    output = container.to_bytes()
    require(sha(output) == config['target_SC0_sha256'], 'final route differs from actual-tested research')
    # All source,review,control,layout,target and runtime guards precede this sole mutation.
    image.replace_file(PATH, output)
    return {
        'format': 'dk4-rafael-opening-editorial-release-v1',
        'manuscript': config['manuscript'], 'choices': config['choices'],
        'reference_map': config['reference_map'], 'changed_records': changes,
        'blocks': [{'block': 44, 'old_bytes': len(block), 'new_bytes': len(target),
                    'growth_bytes': len(target) - len(block)}],
        'source_SC0_sha256': sha(before_file), 'target_SC0_sha256': sha(output),
        'compiled_progressive_records': 114, 'exact_unchanged_FE_records': 1,
        'reviewed_choice_labels': 2, 'typed_commands': 182, 'relative_sites': 4,
        'explicit_inherited_relative_repairs': [r for r in edges if r['inherited_stale_span_explicitly_repaired']],
        'all342_other_blocks_all_other_files_components_preserved': True,
        'complete_source_native_and_both_actual_choice_evidence_bound': True,
        'sole_SC0_mutation_after_all_guards': True,
    }
