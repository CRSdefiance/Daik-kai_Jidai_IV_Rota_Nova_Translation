"""Source-bound Stockholm prose compiler with typed nested relative spans.

Rebuilds from reviewed prose and original commands; no research binary is read.
Every guard runs before the sole image mutation.
"""
import json
import struct
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_stockholm_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH = '/data/SC2.DK4'
CONFIG = 'translations/lil_stockholm_editorial_release_v1.json'
HEADER = bytes.fromhex('0040ffff00')


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(condition, message):
    if not condition:
        raise ValueError('Stockholm: ' + message)


def apply_release(image, baseline, config_path=CONFIG):
    config = load(config_path)
    require(config.get('format') == 'dk4-lil-stockholm-editorial-release-v1', 'unknown release')
    for name, digest in config['dependencies'].items():
        require(sha(Path(name).read_bytes()) == digest, 'reviewed dependency differs: ' + name)
    arm = image.read_file('/__arm9__.bin')
    source = image.read_file(PATH)
    require(sha(arm) == config['required_runtime_arm9_sha256'], 'proven runtime differs')
    require(sha(source) == config['source_SC2_sha256'], 'current source differs')
    require(sha(baseline.read_file(PATH)) == config['canonical_SC2_sha256'], 'canonical source differs')
    clean_path = Path(config['clean_ROM'])
    require(sha(clean_path.read_bytes()) == config['clean_ROM_sha256'], 'clean ROM differs')
    clean = NdsImage.open(clean_path).read_file(PATH)
    require(sha(clean) == config['clean_SC2_sha256'], 'clean SC2 differs')
    doc = load(config['manuscript'])
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy'] == 'natural-dialogue-v2'
            and doc['target_locale'] == 'en-US' and doc['encoder'] == 'dialogue-relocatable-v1'
            and doc['dialogue_profile'] == 'lil-opening-editorial-native-v1'
            and doc['required_runtime_ARM9_sha256'] == sha(arm)
            and doc['formatting_review_pending'] is False, 'prose/native contract differs')
    mapping = load(config['reference_map'])
    require(mapping.get('format') == 'dk4-lil-stockholm-source-relocation-map-v1'
            and mapping.get('external_references_complete') is True
            and mapping.get('entry_point_offset') == 8
            and mapping.get('preserve_record_parity') is True
            and mapping.get('all102_original_commands_and24_typed_spans_approved') is True
            and mapping.get('representative_actual36_and_offline51_scope_approved') is True,
            'complete approved reference map required')
    actual = load(doc['actual_visual_review'])
    require(actual.get('all36_activated_revised_speeches72_holds_complete_native_independent_actual_glyphs') is True
            and actual.get('same75_original_commands_results_and_event_transitions') is True
            and actual.get('normal_discovery_docking_B27_entry_and_terminal_return_not_injected') is True,
            'representative actual proof incomplete')
    refs = {r['id']: r for r in mapping['records']}
    fonts = {r['id']: r for r in load(doc['native_font_proof'])['cases']}
    require(len(doc['records']) == len(refs) == len(fonts) == 51
            and set(refs) == set(fonts), 'exhaustive 51-record coverage differs')
    container = IlnkContainer.parse(source)
    block = container.blocks[27]
    japanese = IlnkContainer.parse(clean).blocks[27]
    require(sha(block) == mapping['source_block_sha256'] and block[:4] == b'CS\0\1', 'source block differs')
    require(sha(japanese) == mapping['clean_block_sha256'], 'clean block differs')
    end = 8 + struct.unpack_from('<H', block, 4)[0]
    require(end <= len(block) and len(block)-end <= 3 and not any(block[end:]), 'source CS extent differs')
    # Private extension must bind the original exact block before any mutation.
    profile = profile_for(arm, block)
    patches, changes, seen = [], [], set()
    for row in doc['records']:
        ident = row['id']
        require(ident in refs and ident not in seen, 'duplicate or unmapped record')
        seen.add(ident)
        ref = refs[ident]
        at = row['current_reference']['offset']
        ja = row['source_reference']['offset']
        old = bytes.fromhex(row['current_text_hex'])
        raw = bytes.fromhex(row['source_hex'])
        require(at == ref['old_offset'] and len(old) == ref['old_length']
                and block[at:at+len(old)] == old and block[at+len(old)] == 0
                and japanese[ja:ja+len(raw)] == raw and japanese[ja+len(raw)] == 0
                and block[at-5:at] == japanese[ja-5:ja] == HEADER
                and (HEADER+raw[:1]).hex() == row['source_complete_preamble_hex']
                and raw[:1] == old[:1]
                and block[:at].count(b'\0') == row['current_reference']['record_index']
                and japanese[:ja].count(b'\0') == row['record_index'], 'exact source/preamble differs: '+ident)
        compiled = encode_relocatable_dialogue(raw, row['english'], profile)
        require(compiled.encoded.hex() == row['compiled_hex'] == fonts[ident]['encoded_hex'],
                'reviewed native text differs: '+ident)
        for diagnostic in compiled.diagnostics:
            require(diagnostic.severity != 'error', 'formatting error: '+ident)
            if diagnostic.severity == 'warning':
                require(diagnostic.code in row.get('qa_waivers', []) and row.get('qa_waiver_reason'),
                        'unreviewed formatting warning: '+ident)
        value = compiled.encoded
        pad = len(value) % 2 != len(old) % 2
        if pad:
            value += b' '
        require(value.hex() == ref['target_hex'] and len(value) == ref['new_length']
                and pad == ref['parity_space_added'] and value[:1] == old[:1]
                and b'\0' not in value and len(value) % 2 == len(old) % 2,
                'mapped text/parity differs: '+ident)
        patches.append(dict(start=at, end=at+len(old), old=old, value=value, id=ident))
        changes.append(dict(id=ident, file_path=PATH, block=27, record_index=row['record_index'],
                            old_offset=at, new_offset=ref['new_offset'], old_bytes=len(old),
                            new_bytes=len(value), body_changed=old != value, parity_space_added=pad,
                            complete_six_byte_preamble_and_macros_preserved=True))
    require(seen == set(refs), 'missing record')
    patches.sort(key=lambda p: p['start'])
    require(all(a['end'] <= b['start'] for a, b in zip(patches, patches[1:])), 'overlapping patches')

    def mapped(offset):
        delta = 0
        for p in patches:
            if offset < p['start']:
                break
            require(not p['start'] < offset < p['end'], 'unclassified interior reference')
            if offset == p['start']:
                return offset+delta
            delta += len(p['value'])-len(p['old'])
        return offset+delta

    parts, last = [], 0
    for p in patches:
        require(mapped(p['start']) == refs[p['id']]['new_offset'], 'speech destination differs')
        parts.extend((block[last:p['start']], p['value']))
        last = p['end']
    parts.append(block[last:end])
    logical = bytearray(b''.join(parts))
    require(len(logical) == mapped(end) and len(logical)-8 <= 0xffff, 'resized extent differs')
    edges = mapping['relative_skip_fixups']
    require(len(edges) == len({r['offset'] for r in edges}) == 24, 'typed span inventory incomplete')
    for edge in edges:
        at = edge['offset']
        new = mapped(at)
        target = mapped(edge['matched_skip_target'])
        span = target-new-4
        require(edge['word'] in (0x100, 0x200, 0x300)
                and edge['span_field_offset'] == at+2
                and struct.unpack_from('<H', block, at)[0] == edge['word']
                and struct.unpack_from('<H', block, at+2)[0] == edge['source_span']
                and new == edge['new_offset'] and target == edge['new_matched_skip_target']
                and new+4 == edge['new_unmatched_next'] and span == edge['target_span']
                and 0 <= span <= 0xffff and span % 2 == 0, 'typed relative destination differs')
        struct.pack_into('<H', logical, new+2, span)
    struct.pack_into('<H', logical, 4, len(logical)-8)
    target = bytes(logical)+bytes(-len(logical) % 4)
    require(len(target) <= 0x2400 and sha(target) == mapping['target_block_sha256'], 'target block differs')
    commands = mapping['commands']
    require(len(commands) == len({r['old_offset'] for r in commands}) == 102, 'command inventory incomplete')
    boundaries = {r['new_offset'] for r in commands} | {len(logical)}
    edge_by_offset = {r['offset']: r for r in edges}
    for c in commands:
        old, new, extent = c['old_offset'], mapped(c['old_offset']), c['old_native_extent']
        require(new == c['new_offset'] and mapped(old+extent)-new == c['new_native_extent']
                and [mapped(a) for a in c['original_0100_ancestors']] == c['relocated_0100_ancestors']
                and struct.unpack_from('<H', block, old)[0] == c['word'], 'command map differs')
        if c['word'] in (0x100, 0x200, 0x300):
            require(old in edge_by_offset and block[old:old+2] == target[new:new+2], 'untyped relative command')
        else:
            size = 6 if c['word'] == 0x4000 else extent
            require(block[old:old+size] == target[new:new+size], 'opaque command or complete preamble changed')
    require(all(e['new_matched_skip_target'] in boundaries and e['new_unmatched_next'] in boundaries for e in edges),
            'relative target is not a native boundary')
    inverse = bytearray(logical)
    for e in edges:
        struct.pack_into('<H', inverse, e['new_offset']+2, e['source_span'])
    for p in reversed(patches):
        inverse[mapped(p['start']):mapped(p['end'])] = p['old']
    struct.pack_into('<H', inverse, 4, end-8)
    require(bytes(inverse) == block[:end], 'inverse restoration differs')
    container.blocks[27] = target
    result = container.to_bytes()
    require(sha(result) == config['target_SC2_sha256'], 'target SC2 differs')
    require([i for i, (a, b) in enumerate(zip(IlnkContainer.parse(source).blocks, container.blocks, strict=True))
             if a != b] == [27], 'unrelated block changed')
    image.replace_file(PATH, result)
    return dict(source_SC2_sha256=sha(source), target_SC2_sha256=sha(result),
                required_runtime_ARM9_sha256=sha(arm), manuscript=config['manuscript'],
                reference_map=config['reference_map'], changed_records=changes,
                only_SC2_block27_changed=True, all335_other_blocks_preserved=True,
                all51_complete_preambles_macros_and_parity_preserved=True,
                all102_commands24_typed_spans_and_inverse_reconstruction_verified=True,
                actual_speeches=36, conditional_speeches_offline_only=15,
                block_growth_bytes=len(target)-len(block))
