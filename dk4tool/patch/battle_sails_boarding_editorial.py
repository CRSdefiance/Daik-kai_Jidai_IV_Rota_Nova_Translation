"""Complete24 battle SailHandling/Boarding comments within the preserved proven single8KiB cache."""

import struct
from types import FunctionType
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import SINGLE, entries, repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_survey_lookout_editorial import current_entries as previous_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.battle_sails_boarding_layout_v945 import compiled
from scripts.verify_village_wrap_v608 import read

IDS=tuple(range(1733,1757))
SOURCE_COMMON='d3b972355a4b415a520fdbc17799302819d6dbb62cb8e551b700954851d3fa6f'
SOURCE_ARM='d26c8eb2aafe4054c126cd73fc99638b6429115d70f437f1268201e6fb084972'
CONFIG='translations/battle_sails_boarding_editorial_release_v1.json'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['encoder']=='dialogue-relocatable-v1' and doc['consumer_layout_profile']=='deck-battle-sails-boarding-visible-v1'
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
        assert row['source_native_macros']==(['IC'] if n==1747 else [])
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
        'all3644_other_message_strings_exact':True,'opaque_payload_IDs':sorted(opaque),
        'all_opaque_payloads_and_unselected_blocks_exact':True,'all_other_ARM9_bytes_except_metadata_exact':True,
        'all_section_BSS_startup_cache_arena_and123040_staged_bounds_unchanged':True,
        'single_cache_may_increase_file_reads':True,'actual_RGB_gameplay_not_claimed_by_this_stage':True,
        'experimental':True,'full_goal_complete':False}


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-battle-sails-boarding-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    manuscript=Path(config['manuscript']);assert sha(manuscript.read_bytes())==config['manuscript_sha256']
    doc=read(manuscript);draft=Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes())==doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(draft)['records']]
    for key in ('native_context_proof','native_font_proof','visual_review_proof','ordinary_context_supplement'):
        assert sha(Path(doc[key]).read_bytes())==doc[key+'_sha256']
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);visual=read(doc['visual_review_proof'])
    cases=context['all150_original_battle_helper_main_and_ordinary_control_selections'];assert len(cases)==150
    battle=[r for r in cases if r['case']!='main_ordinary_working_control']
    ordinary=[r for r in cases if r['case']=='main_ordinary_working_control']
    assert len(battle)==100 and len(ordinary)==50
    assert {r['selected_message_ID'] for r in battle}==set(IDS)
    assert all(r['isolated_CPU_mode_fields8_12']==[0,1] for r in battle)
    assert all(r['isolated_CPU_mode_fields8_12']==[0,0] for r in ordinary)
    for r in cases:
        role=r['source_role_type'];assert role in (0,7)
        suffix=8+r['actor_ID'] if r['actor_ID']<4 else r['native_voice_class']
        first={0:1523,7:1535}[role] if r['case']=='main_ordinary_working_control' else {0:1733,7:1745}[role]
        assert r['selected_message_ID']==first+suffix
    assert fonts['manuscript_sha256']==sha(draft.read_bytes()) and len(fonts['cases'])==24
    assert visual['native_font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes())
    assert visual['all24_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert fonts['all24_source_numeric_selection_complete_ABI_words_and_visible_ink_pass']
    assert fonts['four_original_actual_captain_states_used_no_captain_ID_substitution'] and fonts['complete_windward_mast_coordination_IC_I_duel_and_all_source_words_pass']
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and compiled(row).hex()==case['text_hex']
        for gate in ('full252x96_native_and_independent_canvas_equal','independent_authored_words_at_x0_12px_rows_match_every_pixel',
                     'bitmap_and_input_guards_exact','all_body_ink_inside_registered216x36_crop','original_working_selector_selected_battle_message'):assert case[gate]
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256'] and proof['directory_sha256']==config['directory_sha256']
    copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(c) and copies['ARM9_sha256']==sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass'] and copies['callee_saved_ABI_and_stack_pass']
    supplement=read(doc['ordinary_context_supplement'])
    assert supplement['candidate_sha256']==doc['current_ROM_sha256']
    assert supplement['established_roles']=={'SailHandling':0,'Boarding':7}
    assert supplement['mast_crew_metonymy_supported_by_help125']
    assert supplement['source1736_conditional_expected_evasion_not_invulnerability']
    assert supplement['source1739_risk_not_guaranteed_hit']
    assert supplement['source1754_personal_tactical_judgment_not_universal_duel_rule']
    pronoun_path=Path(supplement['source_pronoun_proof'])
    assert sha(pronoun_path.read_bytes())==supplement['source_pronoun_proof_sha256']
    pronouns=read(pronoun_path)
    assert pronouns['candidate_sha256']==doc['current_ROM_sha256'] and pronouns['ARM9_sha256']==SOURCE_ARM
    assert pronouns['source1747_hex']==next(r['source_hex'] for r in doc['records'] if r['message_id']==1747)
    assert pronouns['IC_is_first_person_not_actor_name'] and pronouns['source1747_first_person_leads_hand_to_hand_combat']
    assert pronouns['four_genuine_captain_states_no_actor_ID_replacement']
    assert pronouns['producer_sha256']==sha(Path('scripts/probe_battle_boarding_pronoun_v943.py').read_bytes())
    assert [r['actor_ID'] for r in pronouns['all25_current_and_clean_parser_control_cases']]==list(range(25))
    for r in pronouns['all25_current_and_clean_parser_control_cases']:
        assert len(r['variants'])==2 and all(v['source_output_guards_and_ABI_pass'] for v in r['variants'])
    for name,digest in supplement['established_term_documents'].items():assert sha(Path(name).read_bytes())==digest
    assert context['no_Sera_special_role15_override_for_roles0_or7']
    assert context['source_activity0_working_not_activity1_separate_helper126A8']
    audit=read(config['native_consumer_audit']);assert audit['batch_sha256']==sha(manuscript.read_bytes())
    assert audit['blocking_errors']==audit['unwaived_warnings']==0 and len(audit['records'])==24
    assert audit['target_COMMON_sha256']==sha(c) and audit['target_ARM9_sha256']==sha(a)
    return c,a,proof
