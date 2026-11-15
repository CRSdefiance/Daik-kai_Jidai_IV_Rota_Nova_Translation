"""Complete13 physical-condition2/3 wound comments within the preserved proven single8KiB cache."""

import struct
from types import FunctionType
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import SINGLE, entries, repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.physical_fatigue_editorial import current_entries as previous_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.physical_wounds_layout_v968b import compiled
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(1794,1807))
SOURCE_COMMON='6a28049eb78ff373429dc842c41091a5e84a66310a968dc53c31f84a241b0aca'
SOURCE_ARM='442cceda91451657292c3da92fe73b7ad1469b3723036457d30a6a622b0e22e0'
CONFIG='translations/physical_wounds_editorial_release_v1.json'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['encoder']=='dialogue-relocatable-v1' and doc['consumer_layout_profile']=='deck-physical-wounds-visible-v1'
    assert tuple(r['message_id'] for r in doc['records'])==IDS
    assert doc['current_COMMON_sha256']==SOURCE_COMMON and doc['current_ARM9_sha256']==SOURCE_ARM
    clean,canonical=map(NdsImage.open,('work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    jp=parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    accepted=parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    before=previous_entries(common,arm);authored={}
    for row in doc['records']:
        n=row['message_id']
        assert row['source_hex']==jp[n].text.hex() and row['canonical_source_hex']==accepted[n].text.hex()
        assert row['current_text_hex']==before[n].text.hex() and row['native_argument_count']==0
        assert row['source_native_macros']==[]
        assert row['physical_condition_IDs']==[2,3] and row['role_ID_is_CPU_layout_fixture_only_not_source_semantics']
        authored[n]=compiled(row)
    pack=FunctionType(repack.__code__,{**repack.__globals__,'previous_entries':previous_entries})
    before,blocks,first,last,selected,opaque,groups,attempts=pack(common,arm,authored)
    target,rebuilt,fields=bytearray(arm),list(blocks),[]
    for block,(group,body) in zip(range(first,last+1),groups,strict=True):
        rebuilt[block]=body;at=parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH',target,at,group[0][0],len(body));fields.append((at,4))
        for n,offset,payload in group:
            at=parser.TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,offset);fields.append((at,2))
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target)
    directory=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET]);after=entries(c,a,directory)
    assert len(before)==len(after)==3668
    assert all(b.text==authored.get(e.message_id,e.text) for e,b in zip(before,after,strict=True))
    assert all(blocks[n]==rebuilt[n] for n in range(41) if not first<=n<=last)
    for n,payload in opaque.items():
        e=after[n];assert rebuilt[e.block][e.block_offset:e.copy_end]==payload
    restored=bytearray(a)
    for at,size in fields:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==arm and cache_plan(a)==cache_plan(arm)
    old,new=MainCodeFile(arm,0x02000000),MainCodeFile(a,0x02000000)
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in old.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in new.sections]
    assert old.sections[3].data==new.sections[3].data and len(new.sections[3].data)-48==123040
    return c,a,{'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS if before[n].text!=after[n].text],
        'reviewed_native_IDs':list(IDS),'metadata_fields':fields,'directory_sha256':directory,
        'repacked_block_range':[first,last],'packing_attempts':attempts,'repacked_native_IDs':[e.message_id for e in selected],
        'repacked_block_lengths':[len(rebuilt[b]) for b in range(first,last+1)],
        'existing_single_cache_code_hex_preserved':SINGLE.hex(),
        'single8192_input_reuses_original_two4096_allocation':True,'output512_and216x36_crop_unchanged':True,
        'all3655_other_message_strings_exact':True,'opaque_payload_IDs':sorted(opaque),
        'all_opaque_payloads_and_unselected_blocks_exact':True,'all_other_ARM9_bytes_except_metadata_exact':True,
        'all_section_BSS_startup_cache_arena_and123040_staged_bounds_unchanged':True,
        'single_cache_may_increase_file_reads':True,'actual_RGB_gameplay_not_claimed_by_this_stage':True,
        'experimental':True,'full_goal_complete':False}


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-physical-wounds-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    for key in ('native_context_proof','native_font_proof','visual_review_proof','source_context_supplement'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    cases=context['all150_original_direct_main_battle_and_ordinary_wound_selections'];assert len(cases)==150
    assert context['source_condition_IDs']==[2,3] and context['Sera24_special_ID']==1806
    assert context['condition2_3_wound_NPC_IDs']==list(range(1794,1802)) and context['condition2_3_genuine_protagonist_IDs']==list(range(1802,1806))
    assert context['four_genuine_protagonists_and21_NPCs_no_ID_substitution'] and context['job_role_and_mood_getters_not_called']
    assert {r['selected_message_ID'] for r in cases}==set(IDS) and {r['actor_ID'] for r in cases}==set(range(25))
    assert {r['isolated_CPU_condition'] for r in cases}=={2,3}
    for r in cases:
        assert r['source_condition_byte_offset']==6 and r['job_role_and_mood_getters_not_called']
        assert r['original_native_selector_and_callee_saved_ABI_pass'] and r['only_declared_CPU_condition_and_mode_fields_changed']
        assert r['actor_other31_bytes_and_all_other_source_RAM_preserved']
        expected=1806 if r['actor_ID']==24 else 1802+r['actor_ID'] if r['actor_ID']<4 else 1794+r['native_voice_class']
        assert r['selected_message_ID']==expected
        assert r['isolated_CPU_mode_fields8_12']==([0,0] if r['case']=='main_ordinary_status_priority' else [0,1])
    healthy=context['all25_healthy_direct_helper_no_message_controls'];fatigue=context['all25_condition1_prior_fatigue_discriminating_controls']
    assert len(healthy)==len(fatigue)==25 and {r['actor_ID'] for r in healthy}=={r['actor_ID'] for r in fatigue}==set(range(25))
    assert all(r['isolated_CPU_condition']==0 and r['selected_message_ID'] is None and r['original_native_selector_and_callee_saved_ABI_pass'] for r in healthy)
    for r in fatigue:
        expected=1793 if r['actor_ID']==24 else 1789+r['actor_ID'] if r['actor_ID']<4 else 1781+r['native_voice_class']
        assert r['isolated_CPU_condition']==1 and r['selected_message_ID']==expected and r['original_native_selector_and_callee_saved_ABI_pass']
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==13 and fonts['complete_native_font_cases']==52
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes())
    assert visual['all13_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all13_source_numeric_selection_complete_ABI_words_and_visible_ink_pass'] and fonts['ordinary_and_battle_both_condition2_3_controls_equal']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['Sera24_special1806_included']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and case['physical_condition_IDs']==row['physical_condition_IDs']==[2,3]
        assert case['all_body_ink_inside_registered216x36_crop'] and case['all_four_original_selectors_full_canvas_and_words_equal']
        variants=case['condition2_3_ordinary_and_battle_font_controls'];assert [v['mode'] for v in variants]==['ordinary_condition2','battle_condition2','ordinary_condition3','battle_condition3']
        for v in variants:
            assert compiled(row).hex()==v['text_hex'] and v['physical_condition_fixture']['CPU_condition'] in (2,3)
            assert v['physical_condition_fixture']['other31_actor_bytes_and_all_other_CPU_RAM_exact']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact','original_physical_selector_selected_condition2_3_message'):assert v[gate]
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    supplement=read(doc['source_context_supplement'])
    assert supplement['candidate_sha256']==doc['current_ROM_sha256']
    assert supplement['source_condition2_and3_share_these_dialogue_alternatives'] and supplement['other_condition_effects_not_claimed_identical']
    assert supplement['physical_status_precedes_job_mood_and_battle_work'] and supplement['independent_alternatives_not_consecutive_dialogue']
    assert supplement['no_IC_native_macro_in_selected_Japanese'] and all(r['IC_count']==0 for r in supplement['all13_source_IC_macros'])
    assert supplement['literal_Japanese_first_person_preserved_as_natural_English'] and supplement['source1802_But_I_and1797_unfinished_clause_preserved']
    assert supplement['source1804_personal_pain_and_admiral_responsibility_preserved'] and supplement['source1798_spit_remedy_is_character_speech']
    for name,digest in supplement['established_term_documents'].items():assert sha(Path(name).read_bytes())==digest
    audit=read(config['native_consumer_audit']);assert audit['batch_sha256']==sha(manuscript.read_bytes())
    assert audit['blocking_errors']==audit['unwaived_warnings']==0 and len(audit['records'])==13
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
