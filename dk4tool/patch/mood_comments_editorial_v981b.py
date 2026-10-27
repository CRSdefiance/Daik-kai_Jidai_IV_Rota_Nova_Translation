"""Complete39 mood0/4/5 comments within the preserved proven single8KiB cache."""

import struct
from types import FunctionType
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import SINGLE, entries, repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.illness_critical_editorial import current_entries as previous_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.mood_comments_layout_v980 import compiled
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(1833,1872))
SOURCE_COMMON='97e35ed3e2ea00ea1f46cf5d9e40eb22093956df9b4785d36b6e9b9bade73251'
SOURCE_ARM='ae387dd92e66ee580a5a48f5b7196fcbcdaefc3d40112338106e6ebe35f753db'
CONFIG='translations/mood_comments_editorial_release_v1.json'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['encoder']=='dialogue-relocatable-v1' and doc['consumer_layout_profile']=='deck-mood-comments-visible-v1'
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
        assert row['physical_condition_ID']==0 and row['mood_ID'] in (0,4,5) and row['role_ID_is_CPU_layout_fixture_only_not_source_semantics']
        authored[n]=compiled(row)
    # Reviewed retained strings need no replacement. Keep their complete original
    # copy spans, including nontext bytes after the owned NUL.
    authored={n:payload for n,payload in authored.items() if payload!=before[n].text}
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
        'all3629_other_message_strings_exact':True,'opaque_payload_IDs':sorted(opaque),
        'all_opaque_payloads_and_unselected_blocks_exact':True,'all_other_ARM9_bytes_except_metadata_exact':True,
        'all_section_BSS_startup_cache_arena_and123040_staged_bounds_unchanged':True,
        'single_cache_may_increase_file_reads':True,'actual_RGB_gameplay_not_claimed_by_this_stage':True,
        'experimental':True,'full_goal_complete':False}


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-mood-comments-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    for key in ('native_context_proof','native_font_proof','visual_review_proof','source_context_supplement'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    cases=context['all225_original_direct_main_battle_and_ordinary_mood_selections'];assert len(cases)==225
    assert context['source_mood_IDs']==[0,4,5] and context['source_physical_condition0_required_for_mood_selection']
    assert context['four_genuine_protagonists_and21_NPCs_no_ID_replacement'] and context['Sera_normal_mood1_2_3_direct_helper_not_executed']
    assert {r['selected_message_ID'] for r in cases}==set(IDS)
    labels=('direct_mood_helper','main_battle_mood_priority','main_ordinary_mood_priority')
    assert {(r['actor_ID'],r['case'],r['isolated_CPU_mood']) for r in cases}=={(n,label,mood) for n in range(25) for label in labels for mood in (0,4,5)}
    for r in cases:
        mood=r['isolated_CPU_mood'];nfirst,hfirst,sera={0:(1833,1841,1845),4:(1846,1854,1858),5:(1859,1867,1871)}[mood]
        expected=sera if r['actor_ID']==24 else hfirst+r['actor_ID'] if r['actor_ID']<4 else nfirst+r['native_voice_class']
        assert r['isolated_CPU_condition']==0 and r['selected_message_ID']==expected
        assert r['source_condition_byte_offset']==6 and r['source_mood_byte_offset']==7 and r['source_mood_getter_calls']>0
        assert r['job_role_getter_not_called'] and r['original_selector_and_callee_saved_ABI_pass']
        assert r['only_declared_condition_mood_and_mode_fields_change'] and r['other30_actor_bytes_and_all_other_source_RAM_exact']
        assert r['isolated_CPU_mode_fields8_12']==([0,0] if r['case']=='main_ordinary_mood_priority' else [0,1])
    priority=context['all75_physical_condition1_priority_controls'];assert len(priority)==75
    assert {(r['actor_ID'],r['isolated_CPU_mood']) for r in priority}=={(n,mood) for n in range(25) for mood in (0,4,5)}
    for r in priority:
        expected=1793 if r['actor_ID']==24 else 1789+r['actor_ID'] if r['actor_ID']<4 else 1781+r['native_voice_class']
        assert r['isolated_CPU_condition']==1 and r['selected_message_ID']==expected and r['source_mood_getter_calls']==0 and r['physical_priority_bypasses_mood_getter']
        assert r['original_selector_and_callee_saved_ABI_pass'] and r['job_role_getter_not_called']
    normal=context['all72_direct_NPC_hero_normal_mood1_2_3_no_message_controls'];assert len(normal)==72
    assert {(r['actor_ID'],r['isolated_CPU_mood']) for r in normal}=={(n,mood) for n in range(24) for mood in (1,2,3)}
    assert all(r['selected_message_ID'] is None and r['isolated_CPU_condition']==0 and r['original_selector_and_callee_saved_ABI_pass'] for r in normal)
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==39 and fonts['complete_native_font_cases']==78
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes()) and visual['all39_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all39_source_numeric_selection_complete_ABI_words_and_visible_ink_pass'] and fonts['ordinary_and_battle_each_mood0_4_5_controls_equal']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['Sera24_special1845_1858_1871_included']
    prior_path=Path(fonts['prior_native_font_proof']);assert sha(prior_path.read_bytes())==fonts['prior_native_font_proof_sha256']
    prior=read(prior_path);assert prior['candidate_sha256']==doc['current_ROM_sha256'] and prior['manuscript_sha256']==sha(draft.read_bytes())
    assert prior['producer_sha256']==sha(Path('scripts/probe_mood_comments_fonts_v979.py').read_bytes())
    assert fonts['preserved_byte_identical_native_font_cases']==76 and fonts['new_native_font_cases']==2 and fonts['only_changed_compiled_IDs']==[1853]
    for row,case,old in zip(doc['records'],fonts['cases'],prior['cases'],strict=True):
        n=row['message_id'];expected_mood=0 if n<1846 else 4 if n<1859 else 5
        assert n==case['message_id']==old['message_id'] and case['physical_condition_ID']==row['physical_condition_ID']==0 and case['mood_ID']==row['mood_ID']==expected_mood
        assert case['all_body_ink_inside_registered216x36_crop'] and case['both_original_selectors_full_canvas_and_words_equal']
        if n!=1853:
            for key,value in old.items():
                if key!='preview':assert case[key]==value
            assert all(v['text_hex']==compiled(row).hex() for v in old['ordinary_and_battle_font_controls'])
        else:assert case['case_origin']['reexecuted_for_changed_automatic_wrap']
        variants=case['ordinary_and_battle_font_controls'];assert [v['mode'] for v in variants]==['ordinary','battle']
        for v in variants:
            assert compiled(row).hex()==v['text_hex'] and v['mood_fixture']['CPU_mood']==expected_mood and v['mood_fixture']['physical_condition_preserved']==0
            assert v['mood_fixture']['other31_actor_bytes_and_all_other_CPU_RAM_exact']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'independent_authored_words_at_x0_12px_rows_match_every_pixel','bitmap_and_input_guards_exact','original_mood_selector_selected_expected_message'):assert v[gate]
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    supplement=read(doc['source_context_supplement'])
    assert supplement['candidate_sha256']==doc['current_ROM_sha256'] and supplement['source_mood0_positive4_dejected5_panic']
    assert supplement['physical_condition0_required_and_condition1_preempts_mood'] and supplement['independent_alternatives_not_consecutive_dialogue']
    assert supplement['no_IC_native_macro_in_selected_Japanese'] and len(supplement['all39_source_IC_macros'])==39 and all(r['IC_count']==0 for r in supplement['all39_source_IC_macros'])
    assert supplement['literal_Japanese_first_person_preserved_as_natural_English'] and supplement['independent1843_1844_and1855_1856_not_split_words']
    assert supplement['obsolete_full_width_I_entries']==[1845,1846,1858] and supplement['nonverbal_English_equivalents']=={'1855':'...','1871':'@#$*!!'}
    assert supplement['no_spoken_words_added_to_silence_or_comic_symbols'] and supplement['source1868_and1870_are_personal_self_calming']
    assert supplement['Sera_direct_normal_moods_not_used_outside_original_contract']
    for name,digest in supplement['established_term_documents'].items():assert sha(Path(name).read_bytes())==digest
    audit=read(config['native_consumer_audit']);assert audit['batch_sha256']==sha(manuscript.read_bytes())
    assert audit['blocking_errors']==audit['unwaived_warnings']==0 and len(audit['records'])==39
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
