"""Atomic complete B168 localization: progressive/FE text and source-owned control flow."""
import json
import re
import struct
from collections import Counter
from pathlib import Path

from dk4tool.dialogue import lil_B168_layout_v3 as codec
from dk4tool.dialogue.lil_B168_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH = '/data/SC2.DK4'
CONFIG = 'translations/lil_B168_editorial_release_v1.json'
SELECTORS = {2, 6, 9, 20, 76, 87, 165, 166, 254}
FLAGS = ['all82_commands12_relative_sites60_target_skips_verified', 'all54_active_speech_targets_preserved',
         'all16_leaves_three_predicates_four_resources_six_presentations_one_effect_and_two_ends_exact',
         'two_consecutive_declared_endwords_preserved', 'three_FE_null_actor_consumers_and_FI7_FA1_FO1_preserved',
         'no_source2000_2100_4100_C200_or_dynamic_objects', 'representative_shared_rules_approved']
OFFLINE = ['DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135']


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(value, message):
    if not value:
        raise ValueError('Lil B168 ' + message)


def apply_release(image, baseline, config_path=CONFIG):
    conf = load(config_path)
    require(conf.get('format') == 'dk4-lil-B168-editorial-release-v1', 'unknown release format')
    for path, digest in conf['dependencies'].items():
        require(sha(Path(path).read_bytes()) == digest, 'reviewed dependency changed:' + path)
    source = image.read_file(PATH)
    arm, common = image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source) == conf['source_SC2_sha256'] and sha(baseline.read_file(PATH)) == conf['canonical_SC2_sha256'], 'current/canonical script differs')
    require(sha(arm) == conf['required_runtime_arm9_sha256'] and sha(common) == conf['required_runtime_common_sha256'], 'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes()) == conf['clean_ROM_sha256'], 'clean input differs')
    japanese = NdsImage.open(conf['clean_ROM']).read_file(PATH)
    require(sha(japanese) == conf['clean_SC2_sha256'], 'clean script differs')
    doc, mapping = load(conf['manuscript']), load(conf['reference_map'])
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
            and doc['encoder'] == 'dialogue-relocatable-v1' and doc['formatting_review_pending'] is False
            and doc['all54_five_review_gates_true'], 'five-gate manuscript required')
    require(doc['reference_map'] == conf['reference_map'] and doc['reference_map_sha256'] == sha(Path(doc['reference_map']).read_bytes()), 'approved map differs')
    require(mapping['format'] == 'dk4-lil-B168-source-relocation-map-v1' and mapping['external_references_complete']
            and mapping['entry_point_offset'] == 8 and mapping['preserve_record_parity']
            and mapping['required_runtime_ARM9_sha256'] == sha(arm) and mapping['source_SC2_sha256'] == sha(source)
            and mapping['target_SC2_sha256'] == conf['target_SC2_sha256'], 'complete source map required')
    for flag in FLAGS:
        require(mapping.get(flag) is True, 'missing map approval:' + flag)
    proof_keys = ['native_font_proof', 'final_padding_proof', 'relocated_control_proof', 'representative_proof',
                  'termination_decode_proof', 'source_nameplate_consumer_proof', 'native_formatter_module', 'scoped_profile_module']
    for key in proof_keys:
        require(sha(Path(doc[key]).read_bytes()) == doc[key + '_sha256'], 'proof differs:' + key)
    require(Path(doc['native_formatter_module']) == Path('dk4tool/dialogue/lil_B168_layout_v3.py')
            and Path(doc['scoped_profile_module']) == Path('dk4tool/dialogue/lil_B168_profile.py'), 'scoped formatter/profile required')
    native, stored, controls, sample, ends, names = [load(doc[key]) for key in proof_keys[:6]]
    require(len(native['cases']) == 54 and native['current_original_macro_alignment_calls'] == 432
            and native['all54_current_native_speech_planes_pass'] and native['progressive_planes'] == 51 and native['FE_planes'] == 3
            and native['source_FE_null_actor_logical228x48_physical228x64_complete_one_page_proven'], 'complete native progressive/FE proof required')
    for key, count in [('source_bound_formatter_negatives', 14), ('source_consumer_negative_controls', 26), ('source_macro_preservation_negatives', 3)]:
        require(len(native[key]) == count and all(case['rejected'] for case in native[key]), 'native rejection controls differ:' + key)
    require(len(stored['final_target_parity_cases']) == 54 and stored['current_final_stored_macro_alignment_cases'] == 216
            and stored['all54_final_targets_complete_native_planes_equal_reviewed_planes'], 'complete stored native proof required')
    require(len(controls['relocated_dispatch_cases']) == 54 and len(controls['relocated_predicate_pairs']) == 3
            and len(controls['all16_source_current_target_nonrelative_nonspeech_leaves']) == 16
            and controls['all51_progressive_and3_null_actor_FE_consumers_FI7_FA1_FO1_exact']
            and controls['all_three_unforced_predicates_match_copied_source_state_without_roster_fixture']
            and all(case['current_source_case']['native_result'] == case['relocated_case']['native_result'] for case in controls['relocated_predicate_pairs'])
            and controls['later_older_record0D_reaudit_stays_open'], 'complete relocated source controls required')
    require(ends['all4_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases']) == 4
            and ends['B168_first_end_precedes_second_end_and_declared_logical_end']
            and ends['no_relative_destination_at_or_beyond_logical_end'], 'four guarded end decodes required')
    require(names['source_printable57_4C_A5_A6_selectors_preserved'] and names['generic_87_165_166_roles_bound_to_original_getters_without_personal_name_or_age_invention']
            and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names'] == {'2': 'Lil', '6': 'Julio', '9': 'Camille', '20': 'Fernando Dias', '76': 'Mikhail'}, 'source-owned identities required')
    name_cases = names['native_sixteen_consumer_cases']['rows']
    require(len(name_cases) == 16 and {case['actor_ID'] for case in name_cases} == SELECTORS - {254}
            and all(case['all_actor_models_and_unowned4MiB_exact'] and case['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for case in name_cases), 'complete original name paths required')
    require(all(not case['original_scratch_rings'] and not case['original_getter_writes'] for case in name_cases if case['actor_ID'] in [87, 165, 166]), 'generic-role read-only name paths required')
    require(sample['actual_two_disclosed_cold_boots_pass'] and sample['new_emulator_runs'] == 2
            and sample['actual51_panels_three_FE_and_normal_return_pass'] and sample['no_open_translation_specific_display_or_control_finding']
            and sample['original_three_unforced_queries_twelve_spans_and_later_effect_preserved'] and sample['no_B168_source_command_omitted']
            and sample['original_B22_four_A000_initialization_commands_retained'] and sample['actual_selected_B168_source_events'] == [], 'representative actual approval required')
    require(sample['offline_only_display_IDs'] == OFFLINE and sample['three_conditional_remarks_not_actual_or_byte_identical_reuse'], 'actual/offline distinction required')
    offline_cases = sample['offline_only_display_cases']
    require(len(offline_cases) == 3 and {case['id'] for case in offline_cases} == set(OFFLINE)
            and all(case['source_selector'] == (20 if case['id'].endswith('0135') else 6)
                    and case['actual_display_or_byte_identical_reuse_claim'] is False and case['reason'] for case in offline_cases), 'offline conditional explanations required')
    actual_paths = [path for path in sample['evidence'] if path.endswith('actual_progressive_FE_three_predicates_full_effect_and_return.json')]
    require(len(actual_paths) == 1, 'one exact actual proof required')
    actual = load(actual_paths[0])
    require(sha(Path(actual_paths[0]).read_bytes()) == sample['evidence'][actual_paths[0]] and not actual['failures']
            and not actual['paired_region_differences'] and len(actual['versions']) == 2
            and {version['case'] for version in actual['versions']} == {'clean_Japanese', 'reviewed_English'}
            and actual['complete_matching_observations'] == actual['fresh_actual_unique_speech_panels'] == 51, 'two complete actual paths required')
    require(all(version['frames'] == 20001 and version['source_end_offset'] == 2906
                and len(version['selected_B22_command_pairs']) == 81 and version['selected_B22_command_pairs'][-1]['result_words'] == [0, 0]
                and [row['result_words'] for row in version['actual_three_unforced_predicates']] == [[2, 0], [2, 0], [2, 0]]
                and version['actual_source_recruitment_effect']['original_source_offset'] == 2582
                and version['actual_source_recruitment_effect']['result_words'] == [3, 0] for version in actual['versions']), 'actual control/effect/termination results differ')
    require(len(native['review_sheets']) == 7 and len(sample['viewed_actual_sheets']) == 9, 'all viewed sheets required')
    for sheet in native['review_sheets'] + sample['viewed_actual_sheets']:
        require(sheet['review'].startswith('Viewed') and sha(Path(sheet['path']).read_bytes()) == sheet['sha256'], 'viewed sheet changed')
    rows = doc['records']
    require(len(rows) == len({row['id'] for row in rows}) == 54 and {row['source_selector'] for row in rows} == SELECTORS, '54 exact speech records required')
    require(Counter(row['kind'] for row in rows) == {'progressive': 51, 'system-FE': 3}
            and Counter(row['editorial_decision'] for row in rows) == {'revise': 28, 'retain-wording': 26}, 'source/decision scope differs')
    require(set(sample['actual_sampled_display_IDs']) == {row['id'] for row in rows} - set(OFFLINE)
            and len(sample['represented_reviewed_display_IDs']) == 54, 'actual display keys differ')
    require(len(mapping['blocks']) == 1 and mapping['blocks'][0]['block'] == 168, 'one exact block required')
    spec = mapping['blocks'][0]
    old_blocks = list(IlnkContainer.parse(source).blocks)
    block, original = old_blocks[168], IlnkContainer.parse(japanese).blocks[168]
    require(len(old_blocks) == 336 and sha(block) == spec['source_block_sha256'] and block[:4] == b'CS\0\1', 'source block differs')
    fonts = {case['id']: case for case in native['cases']}
    refs = {ref['id']: ref for ref in spec['text_records']}
    require(set(fonts) == set(refs) == {row['id'] for row in rows}, 'native/reference coverage differs')
    require(len({case['id'] for case in controls['relocated_dispatch_cases']}) == 54
            and all(case['resolved_actor_ID'] == (None if case['source_selector'] == 254 else case['source_selector'])
                    and case['registered_catalog_match'] is None for case in controls['relocated_dispatch_cases']), 'individual dispatch coverage differs')
    patches, changes, macros = [], [], Counter()
    for row in rows:
        ident, case, ref = row['id'], fonts[row['id']], refs[row['id']]
        fe = row['kind'] == 'system-FE'
        require(case['complete_native_independent_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
                and case['all_visible_origins_zero_and_native_rows_within4rows']
                and sum(len(pipe['cases']) for pipe in case['current_native_macro_pipelines']) == 8, 'individual glyph/alignment proof differs')
        require(case['geometry'] == ([228, 64] if fe else [216, 64])
                and (not fe or case['one_native_page_consumes_complete_target']), 'individual consumer geometry differs')
        at, sa = row['current_reference']['offset'], row['source_reference']['offset']
        old, raw = bytes.fromhex(row['current_hex']), bytes.fromhex(row['source_hex'])
        require(row['block'] == 168 and row['file_path'] == PATH and row['source_selector'] == raw[0] == old[0]
                and row['english'].startswith('{SPEAKER:' + format(raw[0], '02X') + '}'), 'source selector differs:' + ident)
        require((raw[0] == 254) == fe, 'FE selector/consumer mismatch:' + ident)
        require(block[at:at + len(old)] == old and original[sa:sa + len(raw)] == raw
                and block[at + len(old)] == original[sa + len(raw)] == 0 and row['current_text_hex'] == old.hex(), 'source/current text differs:' + ident)
        require(block[at - 5:at + 1] == original[sa - 5:sa + 1] == b'\0\x40\xff\xff\0' + raw[:1]
                and row['source_complete_preamble_hex'] == block[at - 5:at + 1].hex(), 'complete preamble differs:' + ident)
        require(block[:at].count(b'\0') == row['record_index'] == ref['record_index'] and ref['old_offset'] == at
                and ref['old_length'] == len(old) and row['native_display_consumer'] == ('original_null_actor_FE_5473C' if fe else 'original_progressive_54020'), 'current reference differs:' + ident)
        source_macros = re.findall(rb'FI|FA|FO', raw[1:])
        target_macros = [macro.encode('ascii') for macro in re.findall(r'\{MACRO:(FI|FA|FO)\}', row['english'])]
        require(source_macros == target_macros, 'source substitution/order differs:' + ident)
        macros.update(source_macros)
        profile = profile_for(arm, block, 'FE-paper' if fe else 'progressive')
        encoded = codec.encode_relocatable_dialogue(raw, row['english'], profile)
        require(encoded.encoded.hex() == row['compiled_hex'] == case['encoded_hex'], 'compiled English differs:' + ident)
        report = codec.audit_relocatable_dialogue_record(raw, row['english'], profile)
        require(not [issue for issue in report['issues'] if issue['severity'] in ['warning', 'error'] and not
                     (issue['severity'] == 'warning' and issue['code'] == 'line-break-count'
                      and row.get('qa_waivers') == ['line-break-count'] and row.get('qa_waiver_reason'))], 'unapproved QA:' + ident)
        value = encoded.encoded
        pad = len(value) % 2 != len(old) % 2
        value += b' ' if pad else b''
        require(value.hex() == ref['target_hex'] and len(value) == ref['new_length'] and pad == ref['parity_space_added'], 'stored target differs:' + ident)
        patches.append(dict(start=at, end=at + len(old), value=value, old=old))
        changes.append(dict(id=ident, block=168, kind=row['kind'], old_offset=at, new_offset=ref['new_offset'], old_bytes=len(old), new_bytes=len(value)))
    require(macros == {b'FI': 7, b'FA': 1, b'FO': 1}, 'complete macro scope differs')
    require(not spec['choice_commands'] and not spec['actor_style_commands'] and not spec['original2000_pause_and_resume_maps'], 'invented typed object or pause')
    patches.sort(key=lambda patch: patch['start'])
    require(all(a['end'] <= b['start'] for a, b in zip(patches, patches[1:])), 'overlapping objects')
    def mapped(offset):
        delta = 0
        for patch in patches:
            if offset < patch['start']:
                break
            require(not patch['start'] < offset < patch['end'], 'interior reference into complete text')
            if offset == patch['start']:
                return offset + delta
            delta += len(patch['value']) - (patch['end'] - patch['start'])
        return offset + delta
    end = 8 + struct.unpack_from('<H', block, 4)[0]
    require(end <= len(block) and not any(block[end:]), 'nonzero source padding')
    pieces, last = [], 0
    for patch in patches:
        pieces.extend([block[last:patch['start']], patch['value']])
        last = patch['end']
    pieces.append(block[last:end])
    logical = bytearray(b''.join(pieces))
    edges = spec['relative_skip_fixups']
    require(len(edges) == 12 and len(spec['target_native_skip_cases']) == 60 and len(logical) == mapped(end) < 0x2400, 'complete relative scope required')
    for edge in edges:
        at, target = mapped(edge['offset']), mapped(edge['matched_skip_target'])
        span = target - at - 4
        require(at == edge['new_offset'] and target == edge['new_matched_skip_target'] and span == edge['target_span']
                and struct.unpack_from('<H', block, edge['span_field_offset'])[0] == edge['source_span']
                and 0 <= span <= 65535 and span % 2 == 0, 'relative target differs')
        struct.pack_into('<H', logical, at + 2, span)
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    target = bytes(logical) + bytes(-len(logical) % 4)
    require(sha(target) == spec['target_block_sha256'], 'target block differs')
    commands = spec['mapped_native_commands']
    require(len(commands) == 82 and sum(command['word'] == 0x4000 for command in commands) == 54, 'native command scope differs')
    boundaries = {command['new_offset'] for command in commands}
    require(all(edge['new_matched_skip_target'] in boundaries and edge['new_unmatched_next'] in boundaries for edge in edges), 'relative destination leaves commands')
    for command in commands:
        a, b = command['old_offset'], command['new_offset']
        require(mapped(a) == b and mapped(a + command['old_native_extent']) - b == command['new_native_extent'], 'mapped boundary differs')
        if command['word'] == 0x4000:
            require(block[a:a + 6] == target[b:b + 6], 'speech preamble differs')
        elif command['word'] in [0x100, 0x200, 0x300, 0x400]:
            require(block[a:a + 2] == target[b:b + 2], 'relative opcode differs')
        else:
            require(block[a:a + command['old_native_extent']] == target[b:b + command['new_native_extent']], 'opaque numeric leaf differs')
    stops = [command for command in commands if command['word'] == 0]
    require([command['old_offset'] for command in stops] == [2906, 2910] and len(stops) == 2
            and stops[0]['new_offset'] + 4 == stops[1]['new_offset'] and stops[-1]['new_offset'] + 4 == len(logical)
            and all(target[command['new_offset']:command['new_offset'] + 4] == bytes(4) for command in stops), 'consecutive source ends differ')
    require([(command['old_offset'], command['new_offset'], 4) for command in stops]
            == [(item['source_offset'], item['target_offset'], item['extent']) for item in spec['original_declared_end_word_maps']], 'end map differs')
    require(sum(command['word'] == 0xA000 for command in commands) == 1
            and next(command['old_offset'] for command in commands if command['word'] == 0xA000) == 2582
            and sum(command['word'] == 0x8000 for command in commands) == 3
            and [command['word'] for command in commands if command['word'] & 0xFF00 == 0x6300] == [0x6342, 0x630B, 0x6300, 0x6301], 'effect/predicates/resource scope differs')
    restored = bytearray(logical)
    struct.pack_into('<H', restored, 4, end - 8)
    for edge in edges:
        struct.pack_into('<H', restored, edge['new_offset'] + 2, edge['source_span'])
    for patch in reversed(patches):
        at = mapped(patch['start'])
        restored[at:at + len(patch['value'])] = patch['old']
    require(bytes(restored) == block[:end], 'inverse does not restore every predecessor byte')
    new_blocks = list(old_blocks)
    new_blocks[168] = target
    result = IlnkContainer(new_blocks).to_bytes()
    require(sha(result) == conf['target_SC2_sha256']
            and [index for index, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a != b] == [168], 'whole SC2 target differs')
    image.replace_file(PATH, result)
    return dict(source_SC2_sha256=sha(source), target_SC2_sha256=sha(result), required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'], reference_map=conf['reference_map'], changed_records=changes,
        blocks=[dict(block=168, source_sha256=sha(block), target_sha256=sha(target), source_bytes=len(block), target_bytes=len(target),
                     relative_operands=12, source_commands=82, inverse_restores_every_original_logical_byte=True)],
        all335_other_SC2_blocks_unchanged=True, all54_speeches_three_FE_macros_twelve_spans_and16_leaves_preserved=True,
        actual_two_retained_B22_fixtures_not_natural_source_activation=True,
        native_code_and123040_staged_payload_unchanged=True)
