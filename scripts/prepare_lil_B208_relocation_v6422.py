"""Prepare all24 source-owned object relocation and distinct stored-parity consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_relocation_tools_v6422')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/research_lil_B207_relocation_v6365.py','scripts/research_lil_B208_relocation_v6422.py',{
        'B207':'B208','relocation_v6365':'relocation_v6422','editorial_manuscript_v5.json':'editorial_manuscript_v6.json','combined_v6327':'combined_v6380','all13_five_gates_approved':'all24_five_gates_approved',
        'bank[207]':'bank[208]','row[\'block\']==207':'row[\'block\']==208','in [2,14]':'in [7,170,254]',
        '==(656,654)':'==(1188,1186)','block[654:]':'block[1186:]','len(old_commands)==15 and len(old_speeches)==13':'len(old_commands)==29 and len(old_speeches)==24',
        '[0x4000]*13+[0xA000,0]':'[0x4000]*23+[0x6005,0x632E,0x4000,0xA000,0xA000,0]',
        "value=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile).encoded":"profile=profile_for(arm,block,'FE-paper' if row['kind']=='system-FE' else 'progressive');value=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile).encoded",
        'len(patches)==13':'len(patches)==24','block[last:654]':'block[last:1186]','mapped(654)':'mapped(1186)','len(commands)==15 and len(speeches)==13':'len(commands)==29 and len(speeches)==24',
        'mapped(650)':'mapped(1182)',"struct.pack_into('<H',inverse,4,646)":"struct.pack_into('<H',inverse,4,1178)",'SC2_block207':'SC2_block208','newbank[207]':'newbank[208]','==[207]':'==[208]',
        'block=207':'block=208','source_logical_end=654':'source_logical_end=1186','source_offset=650':'source_offset=1182',
        'all13speech15commands_and_original_A000_complete_end_preserved':'all24panels29commands_four_opaque_effect_leaves_complete_end_preserved',
        'no_source_typed_menus_relative_operands_actor_style_FE_or_macros':'no_source_typed_menus_relative_operands_actor_style_or_macros_one_FE_preserved',
        'source_stored=656,source_logical=654':'source_stored=1188,source_logical=1186','target_A000=mapped(642)':'target_A000s=[mapped(1166),mapped(1174)]','inverse656_exact':'inverse1188_exact',
        "Reversibly rebuild B207's13 source-owned speeches;derive every target bound.":"Reversibly rebuild B208's24 progressive/thought/FE objects;derive every target bound."}))
    rows.append(derive('scripts/prove_lil_B205_stored_v6202.py','scripts/prove_lil_B208_stored_v6423.py',{
        'B205':'B208','stored_v6202':'stored_v6423','relocation_v6201':'relocation_v6422','current_build_native_context_v6097':'current_build_native_context_v6261b','current_V6160_native_v6168':'current_V6380_native_v6389','lil_current_font_oracles_v6122':'shady_man_font_oracles_v6263',
        '[2,15,254]':'[7,170,254]','len(cases)==17':'len(cases)==24','fresh+reused==68':'fresh+reused==96',"sum(c['consumer']=='FE-paper' for c in cases)==7":"sum(c['consumer']=='FE-paper' for c in cases)==1",
        'all17_final_stored_targets68_macro_cases_and_complete_planes':'all24_final_stored_targets96_macro_cases_and_complete_planes','current_final_stored_macro_alignment_cases=68':'current_final_stored_macro_alignment_cases=96','all17_final_targets':'all24_final_targets',
        'actual_English_B205_parrot_echoes_sounds_capture_joke_and_end_reachability_unexecuted':'actual_English_B208_pirate_sword_thought_named_FE_notice_and_end_reachability_unexecuted',
        'stored_targets=17,progressive=10,FE=7,macro_cases=68':'stored_targets=24,progressive=23,FE=1,macro_cases=96','Verify all17 final':'Verify all24 final',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_relocation_and_stored_tools.json',dict(tools=rows,all24_objects29_commands_five_source_leaves_and_complete_preambles_bound=True,original1188_stored1186_logical_tail2_and_end1182_explicit=True,no_B207_actor_FE_A000_or_target_extent_assumption_inherited=True,full_goal_complete=False));print('B20824-object/29-command reversible relocation and96 stored-alignment tools prepared;all native constants preserved.')
