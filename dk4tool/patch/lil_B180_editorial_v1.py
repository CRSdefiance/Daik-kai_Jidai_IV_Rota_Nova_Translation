"""Atomic B180 whole-exchange localization with distinct progressive and FE contracts."""
import json
import re
import struct
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B180_layout_v1 as codec
from dk4tool.dialogue.lil_B180_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B180_editorial_release_v1.json'
SELECTORS={166,167,254}
FLAGS=['all28_structural_commands_verified', 'all11_active_speech_targets_preserved', 'all7_nonrelative_leaves_two500_predicates_three_A000_C200_end_exact', 'all10_relative_sites_and50_native_skip_cases_preserved', 'all25_mapped_structural_paths_preserve_all11_speeches', 'progressive10_impersonal_FE1_and_FI0_FA0_FO0_preserved', 'single_end572_target542_preserved', 'no_source2000_pause_2100_4100_resources_or_presentations', 'original_RNG_semantics_and_packed_effect_bytes_preserved', 'representative_actual_display_controls_and_parent_return_approved']

def load(path):
    return json.loads(Path(path).read_bytes())

def require(value,message):
    if not value:raise ValueError('Lil B180 '+message)

def apply_release(image,baseline,config_path=CONFIG):
    conf=load(config_path)
    require(conf.get('format')=='dk4-lil-B180-editorial-release-v1','unknown release format')
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'reviewed dependency changed:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(source)==conf['source_SC2_sha256'] and sha(baseline.read_file(PATH))==conf['canonical_SC2_sha256'],'current/canonical script differs')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'runtime differs')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean input differs')
    japanese=NdsImage.open(conf['clean_ROM']).read_file(PATH);require(sha(japanese)==conf['clean_SC2_sha256'],'clean script differs')
    doc,mapping=load(conf['manuscript']),load(conf['reference_map']);validate_natural_dialogue_batch(doc)
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1'
        and doc['formatting_review_pending'] is False and all(all(r['review'].values()) for r in doc['records']),'five-gate manuscript required')
    require(doc['reference_map']==conf['reference_map'] and doc['reference_map_sha256']==sha(Path(doc['reference_map']).read_bytes()),'approved map differs')
    require(mapping['format']=='dk4-lil-B180-source-relocation-map-v1' and mapping['external_references_complete']
        and mapping['entry_point_offset']==8 and mapping['preserve_record_parity'] and mapping['required_runtime_ARM9_sha256']==sha(arm)
        and mapping['source_SC2_sha256']==sha(source) and mapping['target_SC2_sha256']==conf['target_SC2_sha256'],'complete source map required')
    for flag in FLAGS:require(mapping.get(flag) is True,'missing map approval:'+flag)
    proof_keys=['native_font_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof',
        'source_nameplate_consumer_proof','native_formatter_module','scoped_profile_module','postscene_native_state_proof']
    for key in proof_keys:require(sha(Path(doc[key]).read_bytes())==doc[key+'_sha256'],'proof differs:'+key)
    require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B180_layout_v1.py')
        and Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B180_profile.py'),'scoped formatter/profile required')
    native,stored,controls,sample,ends,names=[load(doc[k]) for k in proof_keys[:6]]
    observed=load(doc['postscene_native_state_proof'])
    require(len(native['cases'])==11 and native['current_original_macro_alignment_calls']==88
        and native['complete_progressive_planes']==10 and native['complete_FE_logical_and_physical_planes']==1,'complete native consumers required')
    require(len(native['negative_controls'])==18 and all(r['rejected'] for r in native['negative_controls']),'source-consumer negatives required')
    approval=load(conf['native_approval'])
    require(len(approval['formatter_negatives'])==28 and all(r['rejected'] for r in approval['formatter_negatives']),'formatter negatives required')
    require(len(stored['final_target_parity_cases'])==11 and stored['current_final_stored_macro_alignment_cases']==44
        and stored['new_parity_macro_alignment_cases']==20 and stored['exact_byte_identical_reused_macro_alignment_cases']==24
        and stored['all11_final_targets_complete_native_planes_equal_reviewed_planes'],'complete stored proof required')
    require(len(controls['relocated_dispatch_cases'])==11 and len(controls['all7_exact_nonrelative_leaves'])==7
        and len(controls['predicate_pairs'])==2 and len(controls['C200_pairs'])==1 and len(controls['A000_structural_pairs'])==3
        and len(controls['all25_source_and_relocated_structural_paths_identical'])==25,'complete relocated controls required')
    for pair in controls['predicate_pairs']:
        require(len(pair['cases'])==2 and pair['old_offset']%4==pair['new_offset']%4==0,'source predicate alignment differs')
        a,b=pair['cases'];require(a['native_result']==b['native_result'] and a['after_seed']==b['after_seed'],'predicate pair differs')
        require(all(r['unforced_current_snapshot'] and r['full4MiB_difference_exactly_one_original_owned_RNG_word'] for r in pair['cases']),'original RNG ownership required')
    ui=controls['C200_pairs'][0]['cases']
    require(len(ui)==2 and all(r['source_owned_UI_request_words']==[1,2,13,0,0,0,1] for r in ui)
        and ui[0]['source_owned_UI_writes']==ui[1]['source_owned_UI_writes'],'isolated C200 source ownership differs')
    require(ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
        and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',572),('research',542)],'guarded end decodes required')
    require(names['approved_prose_names']=={'166':'Lady','167':'Lady'}
        and {(r['consumer'],r['actor_ID']):r['text'] for r in names['native_four_consumer_cases']['rows']}=={
            ('progressive-nameplate',166):'Lady',('full-catalogue',166):'Lady',
            ('progressive-nameplate',167):'Lady',('full-catalogue',167):'Lady'},'four original role consumers required')
    require(sample['all11_panels_ten_progressive_one_FE_selected_effect_C200_end_and_parent_return_pass']
        and sample['source_all28_commands_ten_branches_two_predicates_three_alternative_effects_preserved']
        and sample['actual_conditional_paths_verified_without_forcing_same_outcome']
        and sample['original_RNG_and_effect_state_difference_fully_disclosed_within_checked_scope']
        and sample['no_open_translation_specific_display_or_control_finding'] and not sample['offline_only_display_IDs'],'representative scope required')
    require(observed['all11_complete_held_planes_and_source_paired_regions_match']
        and observed['all11_speeches10_progressive1_impersonal_FE_actually_observed']
        and observed['nontext_equal_samples']==len(observed['all115_sampled_nontext_region_checks'])==115
        and not observed['nontext_difference_samples'] and observed['whole_RGB_final9001_equal'],'all actual panels/regions required')
    require(observed['exact_timing_difference_counts']==dict(total=12,speech=8,control_or_end=4)
        and len(observed['actual_timing_differences'])==12
        and observed['postscene9001_native_component_equality']==dict(state=True,models=True,persistent_objects=False,tasks=True,calendar=True)
        and observed['postscene9001_whole1A04_actor_models_and_captain2_equal'],'measured state/timing limits required')
    require(observed['PRNG_equality'] is False and observed['postscene9001_PRNG_seeds']==[2467799992,790984746]
        and observed['PRNG_or_future_world_equivalence_not_claimed'],'unequal original RNG outcomes must stay disclosed')
    require(len(observed['sampled_postscene_whole_RGB_differences_unmasked'])==12
        and all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in observed['sampled_postscene_whole_RGB_differences_unmasked'])
        and observed['all12_following_indicator_differences_viewed_and_retained'],'unmasked indicator differences required')
    require(len(observed['all2_actual_sheets_viewed'])==2 and len(observed['paired_full_screen_views'])==9
        and all(s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in observed['all2_actual_sheets_viewed']+observed['paired_full_screen_views'])
        and observed['actual_new_cold_boot_runs']==4 and observed['total_frames']==30004,'viewed current evidence required')
    effect=load(observed['effect_boundary_proof'])
    require(sha(Path(observed['effect_boundary_proof']).read_bytes())==observed['effect_boundary_proof_sha256']
        and effect['both_pre_effect_all_four_persistent_arrays_byte_identical']
        and effect['final_town_difference_is_exact_observed_original_effect_value']
        and effect['no_unresolved_translation_specific_state_difference_within_checked_arrays'],'actual state difference must be resolved')
    require(effect['final9001_four_array_differences']=={
        'all207_actors_and_current_captain':[],'all90_towns':[dict(offset=1294,before=59,after=61)],
        'all218_items':[],'all124_goods_and_reserved_slot':[]},'exact original-effect state difference required')
    actual=load(conf['actual_proof'])
    require(actual['complete_matching_observations']==actual['fresh_actual_unique_speech_panels']==11
        and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_display_IDs'],'two complete actual paths required')
    require(len(actual['versions'])==2 and [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[31,26]
        and [v['fixture_exit_frame'] for v in actual['versions']]==[5495,5496]
        and actual['observed_random_path_difference']['original_effects_by_case']==dict(clean_Japanese=[504],reviewed_English=[472]),'original conditional paths differ')
    for version in actual['versions']:
        require(len(version['selected_intervals'])==11 and version['single_source_end572_actually_reached']
            and version['selected_B22_command_pairs'][-1]['result_words']==[0,0]
            and version['selected_B22_command_pairs'][-1]['original_source_offset']==572
            and len(version['source_A000'])==len(version['source_C200'])==1
            and version['source_C200'][0]['UI_request_after']==[1,2,13,0,2,0,1],'actual source controls differ')
    for sheet in native['review_sheets']+sample['viewed_actual_sheets']:
        require((sheet.get('viewed') is True or sheet.get('viewed_in_full_current_turn') is True)
            and sheet['review'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'viewed sheet differs')
    rows=doc['records'];ids=[r['id'] for r in rows]
    require(len(rows)==len(set(ids))==11 and {r['source_selector'] for r in rows}==SELECTORS,'eleven exact records required')
    require(Counter(r['kind'] for r in rows)=={'progressive':10,'system-FE':1}
        and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':6},'consumer/decision scope differs')
    require(sample['actual_sampled_display_IDs']==sample['represented_reviewed_display_IDs']==ids
        and all([r['id'] for r in v['selected_intervals']]==ids for v in actual['versions']),'actual display keys differ')
    require(len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==180,'one exact block required')
    spec=mapping['blocks'][0];old_blocks=list(IlnkContainer.parse(source).blocks)
    block,original=old_blocks[180],IlnkContainer.parse(japanese).blocks[180]
    require(len(old_blocks)==336 and sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
    fonts={c['id']:c for c in native['cases']};refs={r['id']:r for r in spec['text_records']}
    require(set(fonts)==set(refs)==set(ids),'native/reference coverage differs')
    require({c['id'] for c in controls['relocated_dispatch_cases']}==set(ids)
        and all(c['resolved_actor_ID']==(None if c['source_selector']==254 else c['source_selector']) and c['registered_catalog_match'] is None
            for c in controls['relocated_dispatch_cases']),'individual dispatch scope differs')
    patches=[];changes=[];macros=Counter()
    for row in rows:
        ident=row['id'];case,ref=fonts[ident],refs[ident];fe=row['kind']=='system-FE'
        require(row['actual_B22_display_fixture_observed'] and not row['offline_only_native_display_checked']
            and not row['current_native_UI_body_explicit_unexecuted_boundary'],'individual actual scope differs')
        require(case['complete_native_independent228x48_plane_equal' if fe else 'complete_native_independent216x64_plane_equal']
            and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and_within_four_rows']
            and case['one_native_page_consumes_complete_target'] and sum(len(p['cases']) for p in case['current_native_macro_pipelines'])==8,'complete native plane differs:'+ident)
        if fe:require(all(c['null_source_actor'] for p in case['current_native_macro_pipelines'] for c in p['cases']),'FE null actor differs')
        at,sa=row['current_reference']['offset'],row['source_reference']['offset'];old,raw=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex'])
        require(row['block']==180 and row['file_path']==PATH and row['source_selector']==raw[0]==old[0]
            and row['english'].startswith('{SPEAKER:'+format(raw[0],'02X')+'}') and (raw[0]==254)==fe,'source selector differs:'+ident)
        require(block[at:at+len(old)]==old and original[sa:sa+len(raw)]==raw and block[at+len(old)]==original[sa+len(raw)]==0
            and row['current_text_hex']==old.hex(),'source/current text differs:'+ident)
        require(block[at-5:at+1]==original[sa-5:sa+1]==b'\0\x40\xff\xff\0'+raw[:1]
            and row['source_complete_preamble_hex']==block[at-5:at+1].hex(),'complete preamble differs:'+ident)
        require(block[:at].count(b'\0')==row['record_index']==ref['record_index'] and ref['old_offset']==at and ref['old_length']==len(old)
            and row['native_display_consumer']==('original_null_actor_FE_24310_then5473C' if fe else 'original_progressive_54020'),'current reference differs:'+ident)
        sm=re.findall(rb'FI|FA|FO',raw[1:]);tm=[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])]
        require(sm==tm,'source substitution/order differs:'+ident);macros.update(sm)
        profile=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'compiled English differs:'+ident)
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning'
            and i['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))],'unapproved QA:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(old)%2;value+=b' ' if pad else b''
        require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],'stored target differs:'+ident)
        if row['editorial_decision']=='retain-wording':require(row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification'],'unjustified retention')
        patches.append(dict(start=at,end=at+len(old),value=value,old=old))
        changes.append(dict(id=ident,block=180,kind=row['kind'],old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
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
    require(len(edges)==10 and [e['offset'] for e in edges]==[460, 464, 468, 480, 492, 496, 500, 512, 524, 528]
        and len(spec['target_native_skip_cases'])==50 and len(logical)==mapped(end)<0x2400,'complete relative scope required')
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
    require(len(commands) == 28 and sum(command['word'] == 0x4000 for command in commands) == 11, 'native command scope differs')
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
    require([c['old_offset'] for c in stops]==[572] and len(stops)==1 and stops[0]['new_offset']==542
        and stops[0]['new_offset']+4==len(logical) and target[542:546]==bytes(4),'single source end differs')
    require([(c['old_offset'],c['new_offset'],4) for c in stops]
        ==[(c['source_offset'],c['target_offset'],c['extent']) for c in spec['original_declared_end_word_maps']],'end map differs')
    leaves=[c for c in commands if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]
    exact=[(452,'0080fffff4010000'),(472,'00a0ffff013d0ba1'),(484,'0080fffff4010000'),
        (504,'00a0ffff013b0ba1'),(516,'00a0ffff013c0ba1'),(570,'00c2'),(572,'00000000')]
    require([(c['old_offset'],block[c['old_offset']:c['old_offset']+c['old_native_extent']].hex()) for c in leaves]==exact,'seven complete source leaves differ')
    require([c['word'] for c in leaves]==[0x8000,0xA000,0x8000,0xA000,0xA000,0xC200,0]
        and all(c['word'] not in [0x2000,0x2100,0x4100] for c in commands),'source predicate/effect/C200 scope differs')
    restored = bytearray(logical)
    struct.pack_into('<H', restored, 4, end - 8)
    for edge in edges:
        struct.pack_into('<H', restored, edge['new_offset'] + 2, edge['source_span'])
    for patch in reversed(patches):
        at = mapped(patch['start'])
        restored[at:at + len(patch['value'])] = patch['old']
    require(bytes(restored) == block[:end], 'inverse does not restore every predecessor byte')
    new_blocks = list(old_blocks)
    new_blocks[180] = target
    result = IlnkContainer(new_blocks).to_bytes()
    require(sha(result) == conf['target_SC2_sha256']
            and [index for index, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if a != b] == [180], 'whole SC2 target differs')
    image.replace_file(PATH, result)
    return dict(source_SC2_sha256=sha(source), target_SC2_sha256=sha(result), required_runtime_ARM9_sha256=sha(arm),
        manuscript=conf['manuscript'], reference_map=conf['reference_map'], changed_records=changes,
        blocks=[dict(block=180, source_sha256=sha(block), target_sha256=sha(target), source_bytes=len(block), target_bytes=len(target),
                     relative_operands=10, source_commands=28, inverse_restores_every_original_logical_byte=True)],
        all335_other_SC2_blocks_unchanged=True, all11_progressive_FE_speeches_two_predicates_three_A000_C200_ten_relative_sites_and7_leaves_preserved=True,
        actual_two_retained_B22_fixtures_and_postscene_exported_state_not_natural_source_activation=True,
        native_code_and123040_staged_payload_unchanged=True)
