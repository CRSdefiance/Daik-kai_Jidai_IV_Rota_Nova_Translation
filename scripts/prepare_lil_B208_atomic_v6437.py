"""Derive the byte-reconstruction core and bind separate B208 observation guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.seal_lil_B208_references_v6434 import FLAGS
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B208_atomic_tools_v6437')
if __name__=='__main__':
    assert not ROOT.exists();original=Path('dk4tool/patch/lil_B207_editorial_v4.py');text=original.read_text('utf-8');header=text[:text.index('def validate_observations')];core=text[text.index('def apply_release'):];fragment=header+core;flagline=next(x for x in header.splitlines() if x.startswith('FLAGS='));ROOT.mkdir(parents=True);part=ROOT/'frozen_B207_header_and_reconstruction_core.py';part.write_text(fragment,'utf-8')
    row=derive(str(part),'dk4tool/patch/lil_B208_editorial_v1.py',{
        'Atomic thirteen-record B207 release':'Atomic24-record B208 progressive/thought/FE release',
        'lil_B207_editorial_release_v4.json':'lil_B208_editorial_release_v1.json','dk4-lil-B207-editorial-release-v4':'dk4-lil-B208-editorial-release-v1','lil_B207_layout_v2':'lil_B208_layout_v5','B207':'B208',
        flagline:'FLAGS='+repr(FLAGS),
        "PATH='/data/SC2.DK4'":"from dk4tool.patch.lil_B208_editorial_guards_v1 import validate_observations\nPATH='/data/SC2.DK4'",
        'all13_source_native_reference_and_representative_rules_approved':'all24_source_native_reference_and_representative_rules_approved',
        "'scoped_profile_module','native_formatter_module']":"'scoped_profile_module','native_formatter_module','phase_capacity_proof']",
        'proofs=validate_observations(doc,mapping,conf)':'proofs=validate_observations(doc,mapping,conf,load,require)',
        "len(rows)==len(set(ids))==13 and Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':7} and Counter(r['source_selector'] for r in rows)=={2:6,14:7} and all(r['kind']=='progressive' for r in rows)":"len(rows)==len(set(ids))==24 and Counter(r['editorial_decision'] for r in rows)=={'revise':15,'retain-wording':9} and Counter(r['source_selector'] for r in rows)=={7:12,170:11,254:1} and Counter(r['kind'] for r in rows)=={'progressive':23,'system-FE':1}",
        'exact thirteen decisions/actors':'exact24 decisions/actors/consumers','[207]':'[208]','==207':'==208','block=207':'block=208',
        '==(656,654,612,612,2,0)':'==(1188,1186,1196,1194,2,2)',
        'profile=profile_for(arm,block);patches=[]':'patches=[]',
        "        encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)":"        profile=profile_for(arm,block,'FE-paper' if row['kind']=='system-FE' else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)",
        "['complete_native_independent216x64_plane_equal','all_first_final_internal_glyphs_in_order_and_unique_cells'":"['complete_native_independent228x48_plane_equal' if row['kind']=='system-FE' else 'complete_native_independent216x64_plane_equal','all_first_final_internal_glyphs_in_order_and_unique_cells'",
        "row['native_display_consumer']=='original_progressive_54020'":"row['native_display_consumer']==('original_null_actor_FE_24310_then5473C' if row['kind']=='system-FE' else 'original_progressive_54020')",
        "di['resolved_actor_ID']==di['source_selector']==raw[0] and di['source_voice_class']=={2:3,14:6}[raw[0]]":"di['source_selector']==raw[0] and di['resolved_actor_ID']==(None if raw[0]==254 else raw[0]) and di['source_voice_class']==(None if raw[0]==254 else {7:3,170:0}[raw[0]])",
        "kind='progressive',old_offset":"kind=row['kind'],old_offset",
        "boundaries==1 and rowcount==3,'one exact boundary/three row reasons'":"boundaries==1 and rowcount==4,'one exact boundary/four row reasons'",
        'end==654 and len(block)==656':'end==1186 and len(block)==1188','mapped(end)==612':'mapped(end)==1194','target=bytes(logical)':'target=bytes(logical)+bytes(-len(logical)%4)',
        "len(commands)==15 and sum(c['word']==0x4000 for c in commands)==13,'15 commands'":"len(commands)==29 and sum(c['word']==0x4000 for c in commands)==24,'29 commands'",
        "[(642,600,'00a0ffff29000110'),(650,608,'00000000')]":"[(1118,1126,'0560'),(1120,1128,'2e63'),(1166,1174,'00a0ffff01020760'),(1174,1182,'00a0ffff28000110'),(1182,1190,'00000000')]",
        'one exact A000 and complete end':'five exact leaves including6005,632E,two A000 and complete end','every656 predecessor byte inverse':'every1188 predecessor byte inverse',
        'source_bytes=656,target_bytes=612,source_logical_end=654,target_logical_end=612':'source_bytes=1188,target_bytes=1196,source_logical_end=1186,target_logical_end=1194','source_commands=15':'source_commands=29',
        'all13_progressive_complete_preambles_one_A000_complete_end_and_zero_macros_preserved':'all23_progressive_one_FE_private_thought24_preambles_five_leaves_and_zero_macros_preserved',
        'actual13_panels51_holds_and_return_approved_with_measured_timing_RNG_prompt_and_different_final_seed_scope':'actual24_panels95_holds_and_return_approved_with_measured_timing_RNG_broader_RGB_and_different_final_states',
    })
    save(ROOT/'atomic_core_preparation.json',dict(original_module=str(original),original_sha256=sha(original.read_bytes()),fragment=str(part),fragment_sha256=sha(part.read_bytes()),derived=row,observation_guard='dk4tool/patch/lil_B208_editorial_guards_v1.py',observation_guard_sha256=sha(Path('dk4tool/patch/lil_B208_editorial_guards_v1.py').read_bytes()),reconstruction_core_native_constants_preserved=True,all24_B208_FE_thought_native_and_actual_contracts_separately_bound=True,full_goal_complete=False));print('B20824-record atomic core prepared with separate native/actual guards;no archive mutation or registration.')
