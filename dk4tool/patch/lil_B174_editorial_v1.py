"""Atomic complete B174 localization: progressive text and source-owned control flow."""
import json
import re
import struct
from collections import Counter
from pathlib import Path

from dk4tool.dialogue import lil_B174_layout_v2 as codec
from dk4tool.dialogue.lil_B174_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH = '/data/SC2.DK4'
CONFIG = 'translations/lil_B174_editorial_release_v1.json'
SELECTORS = {2,14,26,201}
FLAGS = ['all45_structural_commands_four_relative_sites_one_predicate_verified','all33_active_speech_targets_preserved',
    'all8_leaves_two_presentations_one_resource_predicate_two_A000s_C200_and_single_end_exact','single_tail_endword_preserved',
    'no_FE_consumers_and_FI0_FA0_FO0_preserved','no_source2100_4100_or_dynamic_objects','no_source2000_pause',
    'all_four_relative_sites20_target_cases_and_both_optional_speech_paths_preserved',
    'source_predicate874_optional_Emilio_then6240_two_A000s_C200_end_preserved','representative_shared_rules_approved']
OFFLINE = ['DK4_MES_B174_R0069']


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(value, message):
    if not value:
        raise ValueError('Lil B174 ' + message)


def apply_release(image, baseline, config_path=CONFIG):
    conf = load(config_path)
    require(conf.get('format') == 'dk4-lil-B174-editorial-release-v1', 'unknown release format')
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
            and doc['all33_five_review_gates_true'], 'five-gate manuscript required')
    require(doc['reference_map'] == conf['reference_map'] and doc['reference_map_sha256'] == sha(Path(doc['reference_map']).read_bytes()), 'approved map differs')
    require(mapping['format'] == 'dk4-lil-B174-source-relocation-map-v1' and mapping['external_references_complete']
            and mapping['entry_point_offset'] == 8 and mapping['preserve_record_parity']
            and mapping['required_runtime_ARM9_sha256'] == sha(arm) and mapping['source_SC2_sha256'] == sha(source)
            and mapping['target_SC2_sha256'] == conf['target_SC2_sha256'], 'complete source map required')
    for flag in FLAGS:
        require(mapping.get(flag) is True, 'missing map approval:' + flag)
    proof_keys = ['native_font_proof', 'final_padding_proof', 'relocated_control_proof', 'representative_proof',
                  'termination_decode_proof', 'source_nameplate_consumer_proof', 'native_formatter_module', 'scoped_profile_module', 'postscene_native_state_proof']
    for key in proof_keys:
        require(sha(Path(doc[key]).read_bytes()) == doc[key + '_sha256'], 'proof differs:' + key)
    require(Path(doc['native_formatter_module']) == Path('dk4tool/dialogue/lil_B174_layout_v2.py')
            and Path(doc['scoped_profile_module']) == Path('dk4tool/dialogue/lil_B174_profile.py'), 'scoped formatter/profile required')
    native, stored, controls, sample, ends, names = [load(doc[key]) for key in proof_keys[:6]]
    observed=load(doc['postscene_native_state_proof'])
    require(observed['exact_timing_difference_counts']==dict(total=28,speech=20,control_or_end=8)
        and Counter(c['source']['word'] for c in observed['actual_timing_differences'])=={0x4000:20,0x8000:1,0x200:1,0x100:1,0x6240:1,0xA000:2,0xC200:1,0:1},
        'exact twenty speech/eight control-end timing distinction required')
    require(observed['all32_complete_held_planes_and_source_paired_regions_match'] and observed['all232_sampled_nontext_regions_equal']
        and len(observed['all232_sampled_nontext_region_checks'])==232 and observed['whole_RGB_town10810_and_final16001_equal']
        and all(observed['postscene16001_native_component_equality'].values()) and observed['postscene16001_whole1A04_actor_models_and_captain2_equal']
        and observed['PRNG_equality_or_future_world_equivalence_not_claimed'],'actual display and scoped postscene state required')
    require(observed['join_notice10570_complete_shared_text_plane_equal'] and observed['join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed']
        and observed['join_notice_full_RGB_difference_is_original_A_button_indicator']==[224,360,240,376], 'complete existing join notice and explicit indicator scope required')
    require(len(native['cases'])==33 and native['current_original_macro_alignment_calls']==264
        and native['new_current_original_macro_alignment_calls']==8 and native['reused_original_macro_alignment_calls']==256
        and native['all33_current_native_speech_planes_pass'] and native['progressive_planes']==33 and native['FE_planes']==0,'complete native progressive proof required')
    for key,count in [('source_bound_formatter_negatives',14),('source_consumer_negative_controls',17),('source_macro_preservation_negatives',0),('source_macro_absence_negatives',3)]:
        require(len(native[key])==count and all(c['rejected'] for c in native[key]),'native rejection controls differ:'+key)
    require(len(stored['final_target_parity_cases'])==33 and stored['current_final_stored_macro_alignment_cases']==132
        and stored['new_parity_macro_alignment_cases']==48 and stored['exact_byte_identical_reused_macro_alignment_cases']==84
        and stored['all33_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored native proof required')
    require(len(controls['relocated_dispatch_cases'])==33 and len(controls['relocated_predicate_pairs'])==1
        and len(controls['all8_source_current_target_nonrelative_nonspeech_leaves'])==8 and len(controls['relocated_C200_pairs'])==1
        and controls['all33_progressive_consumers_no_macros_exact'] and controls['source32_unconditional_speeches_and_optional_Emilio69_preserved']
        and controls['original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor']
        and controls['source_resource10_boundary_cases_reused_only_by_exact_words_and_runtime']
        and controls['source_two_presentation_and_two_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime']
        and len(controls['source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths'])==2
        and controls['source_packed_effect_and_predicate_semantics_not_inferred'] and controls['later_older_record0D_reaudit_stays_open'],
        'complete relocated source controls required')
    pair=controls['relocated_predicate_pairs'][0]
    require(pair['source_offset']==874 and pair['target_offset']==904 and len(pair['cases'])==2
        and all(c['native_result']==[2,1,0,0,0,0] and c['sole_scratch_restore_recovers_all4MiB_exact'] for c in pair['cases']),
        'unforced historical native predicate pair required, distinct from actual fixture result0')
    ui=controls['relocated_C200_pairs'][0]
    require(ui['source_offset']==2084 and ui['target_offset']==2202 and len(ui['cases'])==2
        and all(c['native_result']==[3,0,0,0,0,0] and c['native_extent']==2 and c['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            and len(c['source_owned_UI_writes'])==9 and c['all_other4MiB_actor_roster_event_RNG_and_models_exact']
            and c['original_input_owner_guards_and_ABI_exact'] for c in ui['cases'])
        and ui['cases'][0]['source_owned_UI_writes']==ui['cases'][1]['source_owned_UI_writes'], 'source-owned C200 request and writes required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['B174_single_end_finishes_declared_logical_end'] and ends['no_relative_destination_at_or_beyond_logical_end'], 'two guarded single-end decodes required')
    require(names['source_0E_1A_C9_selectors_are_Emilio14_Julian26_Mihwa201_not_literal_prose']
        and names['source_new_employer_and_actual_grandfather_preserved_without_romance_status_or_unconditional_date']
        and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names']=={'2':'Lil','14':'Emilio','26':'Julian','201':'Mihwa'}
        and names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','14':'Emilio Ｆerog','26':'Julian Lopes','201':'Mihwa'}, 'source-owned identities required')
    cases=names['native_eight_consumer_cases']['rows']
    require(len(cases)==8 and {c['actor_ID'] for c in cases}==SELECTORS
        and all(c['all_actor_models_and_unowned4MiB_exact'] and c['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for c in cases), 'complete original name paths required')
    owned=[c for c in cases if c['actor_ID'] in [2,14,26]];readonly=[c for c in cases if c['actor_ID']==201]
    require(len(owned)==6 and all(c['original_scratch_rings'] and c['original_getter_writes'] for c in owned),'six source-owned scratch paths required')
    require(len(readonly)==2 and all(c['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring'
        and not c['original_scratch_rings'] and not c['original_getter_writes'] for c in readonly),'two original Mihwa read-only pointers required')
    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['content_frames_each']==16001 and sample['new_emulator_runs']==2
        and sample['all32_unconditional_panels_unforced_predicate_both_effects_C200_single_end_and_normal_town_return_pass']
        and sample['optional_Emilio69_offline_native_planes_names_dispatch_and_both_operand_paths_approved']
        and sample['original45_structural_commands_and_single_declared_endword_preserved'] and sample['no_B174_source_command_omitted']
        and sample['source_predicate0_then6240_A0002068_A0002076_C2002084_and_end_executed']
        and sample['source_relative_sites882890_actual_886894938_offline_native_only'] and sample['actual_source_0100_extent52_and_relocated_extent62_distinguished']
        and sample['actual_VM_descriptor_last_result0_preserved_through_type3_C200_and_end'] and sample['single_end2086_actual']
        and sample['original_B22_four_A000_initialization_commands_retained'] and sample['no_source_pause_invented_and_original_C200_retained']
        and sample['all232_sampled_nontext_regions_and_whole_RGB_town10810_and_final16001_equal']
        and sample['postscene16001_five_native_components_whole_actor_model_and_captain2_equal']
        and sample['complete_existing_join_notice_and_first_J_preserved']
        and sample['source_packed_predicate_and_A000_semantics_not_inferred'] and sample['PRNG_and_future_world_equality_not_claimed']
        and sample['no_open_translation_specific_display_or_control_finding']
        and sample['no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim']
        and sample['actual_selected_B174_source_events']==[] and sample['offline_only_display_IDs']==OFFLINE,'representative actual approval required')
    paths=[p for p in sample['evidence'] if p.endswith('actual_all33_unforced_predicate_paths_effects_C200_and_end.json')]
    require(len(paths)==1,'one exact actual proof required');actual=load(paths[0])
    require(sha(Path(paths[0]).read_bytes())==sample['evidence'][paths[0]] and not actual['failures'] and not actual['paired_region_differences']
        and actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==32 and actual['offline_only_display_IDs']==OFFLINE
        and len(actual['versions'])==2 and {v['case'] for v in actual['versions']}=={'clean_Japanese','reviewed_English'}
        and actual['actual_result_words_are_player_descriptor_command_type_and_persistent_VM_last_result'], 'two complete actual paths required')
    require([v['fixture_exit_frame'] for v in actual['versions']]==[10776,10774],'source/English exits differ from observed pair')
    for version in actual['versions']:
        require(version['frames']==16001 and version['single_source_end_offset']==2086 and len(version['selected_B22_command_pairs'])==51
            and version['unforced_predicate_result']==0 and version['actual_predicate']['result_words']==[2,0]
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and [r['original_source_offset'] for r in version['actual_source_A000s']]==[2068,2076]
            and [r['result_words'] for r in version['actual_source_A000s']]==[[3,0],[3,0]]
            and [r['original_source_offset'] for r in version['actual_source_relative_commands']]==[882,890]
            and all(r['result_words']==[3,0] and r['extent']==r['independently_verified_native_extent'] for r in version['actual_source_relative_commands'])
            and version['source_A000_hex_by_offset']=={'2068':'00a0ffff020cc960','2076':'00a0ffff1a100120'}
            and version['source_predicate_hex']=='0080ffff0efe0030'
            and [r['word'] for r in version['actual_presentation_commands']]==[0x6000,0x6240]
            and version['actual_presentation_commands'][-1]['result_words']==[3,0]
            and [r['word'] for r in version['actual_resources']]==[0x6340]
            and len(version['actual_source_C200'])==1 and version['actual_source_C200'][0]['original_source_offset']==2084
            and version['actual_source_C200'][0]['result_words']==[3,0]
            and [r['source_offset'] for r in version['unvisited_declared_source_objects']]==[886,894,938], 'actual predicate/effect/C200/relative/end scope differs')
    require([v['actual_source_relative_commands'][1]['extent'] for v in actual['versions']]==[52,62], 'source and relocated actual skip extents required')
    require(len(native['review_sheets'])==5 and len(sample['viewed_actual_sheets'])==6,'all viewed sheets required')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require((sheet.get('viewed') is True or sheet.get('viewed_in_full_current_turn') is True)
            and sheet['review'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet changed')
    rows = doc['records']
    require(len(rows) == len({row['id'] for row in rows}) == 33 and {row['source_selector'] for row in rows} == SELECTORS, '33 exact speech records required')
    require(Counter(row['kind'] for row in rows) == {'progressive': 33}
            and Counter(row['editorial_decision'] for row in rows) == {'revise': 23, 'retain-wording': 10}, 'source/decision scope differs')
    require(set(sample['actual_sampled_display_IDs']) == {row['id'] for row in rows} - set(OFFLINE)
            and len(sample['represented_reviewed_display_IDs']) == 33, 'actual display keys differ')
    require(len(mapping['blocks']) == 1 and mapping['blocks'][0]['block'] == 174, 'one exact block required')
    spec = mapping['blocks'][0]
    old_blocks = list(IlnkContainer.parse(source).blocks)
    block, original = old_blocks[174], IlnkContainer.parse(japanese).blocks[174]
    require(len(old_blocks) == 336 and sha(block) == spec['source_block_sha256'] and block[:4] == b'CS\0\1', 'source block differs')
    fonts = {case['id']: case for case in native['cases']}
    refs = {ref['id']: ref for ref in spec['text_records']}
    require(set(fonts) == set(refs) == {row['id'] for row in rows}, 'native/reference coverage differs')
    require(len({case['id'] for case in controls['relocated_dispatch_cases']}) == 33
            and all(case['resolved_actor_ID'] == (None if case['source_selector'] == 254 else case['source_selector'])
                    and case['registered_catalog_match'] is None for case in controls['relocated_dispatch_cases']), 'individual dispatch coverage differs')
    patches, changes, macros = [], [], Counter()
    for row in rows:
        ident, case, ref = row['id'], fonts[row['id']], refs[row['id']]
        require(row['actual_B22_display_fixture_observed']==(ident not in OFFLINE)
            and row['offline_only_native_display_checked']==(ident in OFFLINE)
            and row['current_native_UI_body_explicit_unexecuted_boundary']==(ident in OFFLINE), 'individual actual/offline scope differs')
        if ident in OFFLINE:
            require(row['source_selector']==14 and row['ancestor_0100_offsets']==[890], 'source conditional Emilio binding required')
        fe = row['kind'] == 'system-FE'
        require(case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
                and case['all_visible_origins_zero_and16px_rows_within4rows']
                and sum(len(pipe['cases']) for pipe in case['current_native_macro_pipelines']) == 8, 'individual glyph/alignment proof differs')
        require(not fe and case['complete_native_independent216x64_plane_equal'], 'one progressive216x64 consumer required')
        at, sa = row['current_reference']['offset'], row['source_reference']['offset']
        old, raw = bytes.fromhex(row['current_hex']), bytes.fromhex(row['source_hex'])
        require(row['block'] == 174 and row['file_path'] == PATH and row['source_selector'] == raw[0] == old[0]
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
        changes.append(dict(id=ident, block=174, kind=row['kind'], old_offset=at, new_offset=ref['new_offset'], old_bytes=len(old), new_bytes=len(value)))
    require(not macros, 'complete macro scope differs')
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
    require(len(edges)==4 and [e['offset'] for e in edges]==[882,886,890,938]
        and len(spec['target_native_skip_cases'])==20 and len(logical)==mapped(end)<0x2400,'complete relative scope required')
    for edge in edges:
        cases=[c for c in spec['target_native_skip_cases'] if c['new_offset']==edge['new_offset']]
        require(len(cases)==5 and {c['last_result'] for c in cases}=={0,1,2,3,0xFFFFFFFF},'five original results per relative site required')
        for case in cases:
            last=case['last_result'];taken=edge['word']==0x100 or (edge['word']==0x200 and last==0) or (edge['word']==0x300 and last==1) or (edge['word']==0x400 and last==2)
            destination=edge['new_matched_skip_target'] if taken else edge['new_unmatched_next']
            require(edge['new_offset']+case['native_extent']==destination and case['source_target_preserved_at_mapped_native_boundary']
                and case['ABI_all4MiB_owner_stream_result_length_and_guards_exact'],'source-bound relative operand case differs')
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
    require(len(commands) == 45 and sum(command['word'] == 0x4000 for command in commands) == 33, 'native command scope differs')
    boundaries = {command['new_offset'] for command in commands}
    require(all(edge['new_matched_skip_target'] in boundaries and edge['new_unmatched_next'] in boundaries for edge in edges), 'relative destination leaves commands')
    for command in commands:
        a, b = command['old_offset'], command['new_offset']
        require(command['word'] == struct.unpack_from('<H', block, a)[0] == struct.unpack_from('<H', target, b)[0], 'mapped opcode differs')
        require(mapped(a) == b and mapped(a + command['old_native_extent']) - b == command['new_native_extent'], 'mapped boundary differs')
        if command['word'] == 0x4000:
            require(block[a:a + 6] == target[b:b + 6], 'speech preamble differs')
        elif command['word'] in [0x100, 0x200, 0x300, 0x400]:
            require(block[a:a + 2] == target[b:b + 2], 'relative opcode differs')
        else:
            require(block[a:a + command['old_native_extent']] == target[b:b + command['new_native_extent']], 'opaque numeric leaf differs')
    stops=[c for c in commands if c['word']==0]
    require([c['old_offset'] for c in stops]==[2086] and len(stops)==1 and stops[0]['new_offset']==2204
        and stops[0]['new_offset']+4==len(logical) and target[2204:2208]==bytes(4),'single source end differs')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]
        ==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]
    exact=[(8,'0060'),(10,'4063'),(874,'0080ffff0efe0030'),(2066,'4062'),
        (2068,'00a0ffff020cc960'),(2076,'00a0ffff1a100120'),(2084,'00c2'),(2086,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'eight complete source leaves differ')
    require([c['word'] for c in leaves]==[0x6000,0x6340,0x8000,0x6240,0xA000,0xA000,0xC200,0]
        and sum(c['word']==0xC200 for c in commands)==1 and all(c['word'] not in [0x2000,0x2100,0x4100] for c in commands), 'complete source predicate/effect/C200/no-pause scope required')
    restored = bytearray(logical)
    struct.pack_into('<H', restored, 4, end - 8)
    for edge in edges:
        struct.pack_into('<H', restored, edge['new_offset'] + 2, edge['source_span'])
    for patch in reversed(patches):
        at = mapped(patch['start'])
        restored[at:at + len(patch['value'])] = patch['old']
    require(bytes(restored) == block[:end], 'inverse does not restore every predecessor byte')
    new_blocks = list(old_blocks)
    new_blocks[174] = target
    result = IlnkContainer(new_blocks).to_bytes()
    require(sha(result) == conf['target_SC2_sha256']
            and [index for index, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a != b] == [174], 'whole SC2 target differs')
    image.replace_file(PATH, result)
    return dict(source_SC2_sha256=sha(source), target_SC2_sha256=sha(result), required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'], reference_map=conf['reference_map'], changed_records=changes,
        blocks=[dict(block=174, source_sha256=sha(block), target_sha256=sha(target), source_bytes=len(block), target_bytes=len(target),
                     relative_operands=4, source_commands=45, inverse_restores_every_original_logical_byte=True)],
        all335_other_SC2_blocks_unchanged=True, all33_progressive_speeches_zero_macros_resource_optional_Emilio_two_A000s_C200_and8_leaves_preserved=True,
        actual_two_retained_B22_fixtures_and_postscene_exported_state_not_natural_source_activation=True,
        native_code_and123040_staged_payload_unchanged=True)
