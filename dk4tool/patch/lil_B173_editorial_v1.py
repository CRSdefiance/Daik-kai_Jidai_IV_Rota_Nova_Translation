"""Atomic complete B173 localization: progressive text and source-owned control flow."""
import json
import re
import struct
from collections import Counter
from pathlib import Path

from dk4tool.dialogue import lil_B173_layout_v1 as codec
from dk4tool.dialogue.lil_B173_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH = '/data/SC2.DK4'
CONFIG = 'translations/lil_B173_editorial_release_v1.json'
SELECTORS = {2,202}
FLAGS = ['all23_structural_commands_four_relative_sites_one_predicate_verified','all11_active_speech_targets_preserved',
    'all8_leaves_two_presentations_two_resources_predicate_two_A000s_and_single_end_exact','single_tail_endword_preserved',
    'no_FE_consumers_and_FI0_FA0_FO0_preserved','no_source2100_4100_or_dynamic_objects','no_source2000_pause_or_C200',
    'all_four_relative_sites20_target_cases_and_both_suffix_paths_preserved',
    'source_A000720_predicate728_conditional_A000748_then6240_and_end_preserved','representative_shared_rules_approved']
OFFLINE = []


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(value, message):
    if not value:
        raise ValueError('Lil B173 ' + message)


def apply_release(image, baseline, config_path=CONFIG):
    conf = load(config_path)
    require(conf.get('format') == 'dk4-lil-B173-editorial-release-v1', 'unknown release format')
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
            and doc['all11_five_review_gates_true'], 'five-gate manuscript required')
    require(doc['reference_map'] == conf['reference_map'] and doc['reference_map_sha256'] == sha(Path(doc['reference_map']).read_bytes()), 'approved map differs')
    require(mapping['format'] == 'dk4-lil-B173-source-relocation-map-v1' and mapping['external_references_complete']
            and mapping['entry_point_offset'] == 8 and mapping['preserve_record_parity']
            and mapping['required_runtime_ARM9_sha256'] == sha(arm) and mapping['source_SC2_sha256'] == sha(source)
            and mapping['target_SC2_sha256'] == conf['target_SC2_sha256'], 'complete source map required')
    for flag in FLAGS:
        require(mapping.get(flag) is True, 'missing map approval:' + flag)
    proof_keys = ['native_font_proof', 'final_padding_proof', 'relocated_control_proof', 'representative_proof',
                  'termination_decode_proof', 'source_nameplate_consumer_proof', 'native_formatter_module', 'scoped_profile_module', 'postscene_native_state_proof']
    for key in proof_keys:
        require(sha(Path(doc[key]).read_bytes()) == doc[key + '_sha256'], 'proof differs:' + key)
    require(Path(doc['native_formatter_module']) == Path('dk4tool/dialogue/lil_B173_layout_v1.py')
            and Path(doc['scoped_profile_module']) == Path('dk4tool/dialogue/lil_B173_profile.py'), 'scoped formatter/profile required')
    native, stored, controls, sample, ends, names = [load(doc[key]) for key in proof_keys[:6]]
    observed=load(doc['postscene_native_state_proof'])
    require(observed['exact_timing_difference_counts']==dict(total=16,speech=8,control_or_end=8)
        and Counter(c['source']['word'] for c in observed['actual_timing_differences'])=={0x4000:8,0xA000:2,0x8000:1,0x200:1,0x300:1,0x100:1,0x6240:1,0:1},
        'exact eight speech/eight control-end timing distinction required')
    require(observed['all11_complete_held_planes_and_source_paired_regions_match'] and observed['all115_sampled_nontext_regions_equal']
        and len(observed['all115_sampled_nontext_region_checks'])==115 and observed['whole_RGB_town5530_and_final9001_equal']
        and all(observed['postscene9001_native_component_equality'].values()) and observed['postscene9001_whole1A04_actor_models_and_captain2_equal']
        and observed['PRNG_equality_or_future_world_equivalence_not_claimed'],'explicit actual display and postscene state scope required')
    require(len(native['cases'])==11 and native['current_original_macro_alignment_calls']==88 and native['all11_current_native_speech_planes_pass']
        and native['progressive_planes']==11 and native['FE_planes']==0,'complete native progressive proof required')
    for key,count in [('source_bound_formatter_negatives',14),('source_consumer_negative_controls',13),('source_macro_preservation_negatives',0),('source_macro_absence_negatives',3)]:
        require(len(native[key])==count and all(c['rejected'] for c in native[key]),'native rejection controls differ:'+key)
    require(len(stored['final_target_parity_cases'])==11 and stored['current_final_stored_macro_alignment_cases']==44
        and stored['new_parity_macro_alignment_cases']==24 and stored['exact_byte_identical_reused_macro_alignment_cases']==20
        and stored['all11_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored native proof required')
    require(len(controls['relocated_dispatch_cases'])==11 and len(controls['relocated_predicate_pairs'])==1
        and len(controls['all8_source_current_target_nonrelative_nonspeech_leaves'])==8 and not controls['relocated_C200_pairs']
        and controls['all11_progressive_consumers_no_macros_exact']
        and controls['original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor']
        and controls['source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime']
        and controls['source_two_presentation_and_two_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime']
        and len(controls['source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths'])==2
        and controls['source_packed_effect_and_predicate_semantics_not_inferred'] and controls['later_older_record0D_reaudit_stays_open'],
        'complete relocated source controls required')
    pair=controls['relocated_predicate_pairs'][0]
    require(pair['source_offset']==728 and pair['target_offset']==760 and len(pair['cases'])==2
        and all(c['native_result']==[2,1,0,0,0,0] and c['sole_scratch_restore_recovers_all4MiB_exact'] for c in pair['cases']),
        'unforced relocated predicate pair required')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(ends['cases'])==2
        and ends['B173_single_end_finishes_declared_logical_end'] and ends['no_relative_destination_at_or_beyond_logical_end'],
        'two guarded single-end decodes required')
    require(names['source_CA_selector_is_Reika202_not_text_to_strip']
        and names['source_unnamed_feminine_voice_binds_native_Reika_without_invented_role']
        and names['source_uncertain_smooth_talking_man_report_does_not_confirm_Julian_identity_or_current_location']
        and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names']=={'2':'Lil','202':'Reika'}
        and names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','202':'Reika'},'source-owned identities required')
    cases=names['native_four_consumer_cases']['rows']
    require(len(cases)==4 and {c['actor_ID'] for c in cases}==SELECTORS
        and all(c['all_actor_models_and_unowned4MiB_exact'] and c['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for c in cases),
        'complete original name paths required')
    owned=[c for c in cases if c['actor_ID']==2];readonly=[c for c in cases if c['actor_ID']==202]
    require(len(owned)==2 and all(c['original_scratch_rings'] and c['original_getter_writes'] for c in owned),'two original Lil scratch paths required')
    require(len(readonly)==2 and all(c['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring'
        and not c['original_scratch_rings'] and not c['original_getter_writes'] for c in readonly),'two original Reika read-only pointers required')
    require(sample['actual_two_disclosed_content_cold_boots_pass'] and sample['content_frames_each']==9001 and sample['new_emulator_runs']==2
        and sample['all11_progressive_panels_unforced_predicate_both_effects_single_end_and_normal_town_return_pass']
        and sample['original23_structural_commands_and_single_declared_endword_preserved'] and sample['no_B173_source_command_omitted']
        and sample['source_A000720_then_predicate1_then_A0007486240_and_end_executed']
        and sample['source_relative_sites736740756_actual_744_offline_native_only']
        and sample['actual_VM_descriptor_last_result1_preserved_through_type3_and_end'] and sample['single_end762_actual']
        and sample['original_B22_four_A000_initialization_commands_retained'] and sample['no_source_pause_or_C200_invented']
        and sample['all115_sampled_nontext_regions_and_whole_RGB_town5530_and_final9001_equal']
        and sample['postscene9001_five_native_components_whole_actor_model_and_captain2_equal']
        and sample['source_packed_predicate_and_A000_semantics_not_inferred'] and sample['PRNG_and_future_world_equality_not_claimed']
        and sample['no_open_translation_specific_display_or_control_finding']
        and sample['no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim']
        and sample['actual_selected_B173_source_events']==[] and sample['offline_only_display_IDs']==[],'representative actual approval required')
    paths=[p for p in sample['evidence'] if p.endswith('actual_all11_unforced_predicate_paths_effects_and_end.json')]
    require(len(paths)==1,'one exact actual proof required');actual=load(paths[0])
    require(sha(Path(paths[0]).read_bytes())==sample['evidence'][paths[0]] and not actual['failures'] and not actual['paired_region_differences']
        and actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==11
        and len(actual['versions'])==2 and {v['case'] for v in actual['versions']}=={'clean_Japanese','reviewed_English'}
        and actual['actual_result_words_are_player_descriptor_command_type_and_persistent_VM_last_result'], 'two complete actual paths required')
    require([v['fixture_exit_frame'] for v in actual['versions']]==[5496,5493],'source/English exits differ from observed pair')
    for version in actual['versions']:
        require(version['frames']==9001 and version['single_source_end_offset']==762 and len(version['selected_B22_command_pairs'])==31
            and version['unforced_predicate_result']==1 and version['actual_predicate']['result_words']==[2,1]
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,1]
            and [r['original_source_offset'] for r in version['actual_source_A000s']]==[720,748]
            and [r['result_words'] for r in version['actual_source_A000s']]==[[3,0],[3,1]]
            and [r['original_source_offset'] for r in version['actual_source_relative_commands']]==[736,740,756]
            and all(r['result_words']==[3,1] for r in version['actual_source_relative_commands'])
            and version['source_A000_hex_by_offset']=={'720':'00a0ffff010b39a2','748':'00a0ffff010cca60'}
            and version['source_predicate_hex']=='0080ffff000cca70'
            and [r['word'] for r in version['actual_presentation_commands']]==[0x6000,0x6240]
            and version['actual_presentation_commands'][-1]['result_words']==[3,1]
            and [r['word'] for r in version['actual_resources']]==[0x6329,0x6340]
            and [r['source_offset'] for r in version['unvisited_declared_source_objects']]==[744],
            'actual unforced predicate/effect/relative/termination results differ')
    require(len(native['review_sheets'])==2 and len(sample['viewed_actual_sheets'])==2,'all viewed sheets required')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require(sheet['review'].startswith('Viewed') and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet changed')
    rows = doc['records']
    require(len(rows) == len({row['id'] for row in rows}) == 11 and {row['source_selector'] for row in rows} == SELECTORS, '11 exact speech records required')
    require(Counter(row['kind'] for row in rows) == {'progressive': 11}
            and Counter(row['editorial_decision'] for row in rows) == {'revise': 8, 'retain-wording': 3}, 'source/decision scope differs')
    require(set(sample['actual_sampled_display_IDs']) == {row['id'] for row in rows} - set(OFFLINE)
            and len(sample['represented_reviewed_display_IDs']) == 11, 'actual display keys differ')
    require(len(mapping['blocks']) == 1 and mapping['blocks'][0]['block'] == 173, 'one exact block required')
    spec = mapping['blocks'][0]
    old_blocks = list(IlnkContainer.parse(source).blocks)
    block, original = old_blocks[173], IlnkContainer.parse(japanese).blocks[173]
    require(len(old_blocks) == 336 and sha(block) == spec['source_block_sha256'] and block[:4] == b'CS\0\1', 'source block differs')
    fonts = {case['id']: case for case in native['cases']}
    refs = {ref['id']: ref for ref in spec['text_records']}
    require(set(fonts) == set(refs) == {row['id'] for row in rows}, 'native/reference coverage differs')
    require(len({case['id'] for case in controls['relocated_dispatch_cases']}) == 11
            and all(case['resolved_actor_ID'] == (None if case['source_selector'] == 254 else case['source_selector'])
                    and case['registered_catalog_match'] is None for case in controls['relocated_dispatch_cases']), 'individual dispatch coverage differs')
    patches, changes, macros = [], [], Counter()
    for row in rows:
        ident, case, ref = row['id'], fonts[row['id']], refs[row['id']]
        fe = row['kind'] == 'system-FE'
        require(case['complete_native_independent216x64_plane_equal'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
                and case['all_visible_origins_zero_and16px_rows_within4rows']
                and sum(len(pipe['cases']) for pipe in case['current_native_macro_pipelines']) == 8, 'individual glyph/alignment proof differs')
        require(not fe and case['complete_native_independent216x64_plane_equal'], 'one progressive216x64 consumer required')
        at, sa = row['current_reference']['offset'], row['source_reference']['offset']
        old, raw = bytes.fromhex(row['current_hex']), bytes.fromhex(row['source_hex'])
        require(row['block'] == 173 and row['file_path'] == PATH and row['source_selector'] == raw[0] == old[0]
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
        changes.append(dict(id=ident, block=173, kind=row['kind'], old_offset=at, new_offset=ref['new_offset'], old_bytes=len(old), new_bytes=len(value)))
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
    require(len(edges)==4 and [e['offset'] for e in edges]==[736,740,744,756]
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
    require(len(commands) == 23 and sum(command['word'] == 0x4000 for command in commands) == 11, 'native command scope differs')
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
    require([c['old_offset'] for c in stops]==[762] and len(stops)==1 and stops[0]['new_offset']==794
        and stops[0]['new_offset']+4==len(logical) and target[794:798]==bytes(4),'single source end differs')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]
        ==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]
    exact=[(8,'0060'),(10,'2963'),(12,'4063'),(720,'00a0ffff010b39a2'),(728,'0080ffff000cca70'),
        (748,'00a0ffff010cca60'),(760,'4062'),(762,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'eight complete source leaves differ')
    require([c['word'] for c in leaves]==[0x6000,0x6329,0x6340,0xA000,0x8000,0xA000,0x6240,0]
        and all(c['word'] not in [0x2000,0x2100,0x4100,0xC200] for c in commands),'source effects/predicate/no-pause scope differs')
    restored = bytearray(logical)
    struct.pack_into('<H', restored, 4, end - 8)
    for edge in edges:
        struct.pack_into('<H', restored, edge['new_offset'] + 2, edge['source_span'])
    for patch in reversed(patches):
        at = mapped(patch['start'])
        restored[at:at + len(patch['value'])] = patch['old']
    require(bytes(restored) == block[:end], 'inverse does not restore every predecessor byte')
    new_blocks = list(old_blocks)
    new_blocks[173] = target
    result = IlnkContainer(new_blocks).to_bytes()
    require(sha(result) == conf['target_SC2_sha256']
            and [index for index, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a != b] == [173], 'whole SC2 target differs')
    image.replace_file(PATH, result)
    return dict(source_SC2_sha256=sha(source), target_SC2_sha256=sha(result), required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'], reference_map=conf['reference_map'], changed_records=changes,
        blocks=[dict(block=173, source_sha256=sha(block), target_sha256=sha(target), source_bytes=len(block), target_bytes=len(target),
                     relative_operands=4, source_commands=23, inverse_restores_every_original_logical_byte=True)],
        all335_other_SC2_blocks_unchanged=True, all11_progressive_speeches_zero_macros_resources_predicate_relative_suffix_two_A000s_and8_leaves_preserved=True,
        actual_two_retained_B22_fixtures_and_postscene_exported_state_not_natural_source_activation=True,
        native_code_and123040_staged_payload_unchanged=True)
