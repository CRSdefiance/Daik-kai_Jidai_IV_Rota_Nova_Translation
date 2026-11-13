"""Prepare source-bound relocation with actual selectors and an unowned copy."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

OLD=Path('scripts/research_lil_shrines_relocation_v3193.py')
NEW=Path('scripts/research_lil_B111_B119_relocation_v3239b.py')
ROOT=Path('work/analysis/lil_B111_B119_relocation_tools_v3239')
if __name__=='__main__':
    assert not NEW.exists() and not ROOT.exists()
    t=OLD.read_text(encoding='utf-8')
    swaps={
        'lil_Shrines_Temples_relocation_v3193':'lil_B111_B119_relocation_v3239b',
        'lil_shrines_temples_editorial_manuscript_v7.json':'lil_B111_B119_editorial_manuscript_v5.json',
        'lil_shrines_temples_actor_style_manuscript_v5.json':'lil_B111_B119_actor_style_manuscript_v4.json',
        "MENU=Path('translations/lil_shrines_temples_choice_manuscript_v4.json')":"MENU=None",
        'all_routes_combined_v3144_candidate.nds':'all_routes_combined_v3204_candidate.nds',
        'doc,voice,menu=map(read,[DOC,VOICE,MENU])':"doc,voice=map(read,[DOC,VOICE]);menu={'records':[]}",
        "assert old[:2]==b'\\0\\x41' and old[18:20]==b'\\0\\xd0'":"assert old[:2]==b'\\0\\x41' and old[18]==0 and all(r['source_selector']==old[19] for r in rows)",
        "fonts[row['id']]['encoded_hex']=='d0'+value.hex()":"fonts[row['id']]['encoded_hex']==format(old[19],'02x')+value.hex()",
        'virtual_D0_excluded_from_stored_body':'actual_virtual_prefix_excluded_from_stored_body',
        "len(target_speeches)==len(texts)":"len(target_speeches)==sum(c['word']==0x4000 for c in spec['all_current_native_commands'])",
        'assert len(results)==10 and sum(len(r[\'text_records\']) for r in results)==164':'assert len(results)==9 and sum(len(r[\'text_records\']) for r in results)==116',
        "sum(len(r['actor_style_commands']) for r in results)==8":"sum(len(r['actor_style_commands']) for r in results)==6",
        "sum(len(c['alternative_records']) for r in results for c in r['actor_style_commands'])==56":"sum(len(c['alternative_records']) for r in results for c in r['actor_style_commands'])==34",
        "sum(len(r['choice_commands']) for r in results)==5":"sum(len(r['choice_commands']) for r in results)==0",
        "sum(len(r['relative_skip_fixups']) for r in results)==114":"sum(len(r['relative_skip_fixups']) for r in results)==64",
        "sum(len(r['target_native_skip_cases']) for r in results)==570":"sum(len(r['target_native_skip_cases']) for r in results)==320",
        "sum(len(r['command_map']) for r in results)==421":"sum(len(r['command_map']) for r in results)==305",
        'range(101,111)':'range(111,120)',
        "choices=str(MENU),choices_sha256=sha(MENU.read_bytes()),":"no_player_choice_objects=True,",
        'all164speech_56aliased_alternatives_15choice_labels_and114_relative_operands_preserved':'all116speech_34aliased_alternatives_no_choices_and64_relative_operands_preserved',
        'all570_relocated_native_skip_cases_match_original_target_mapping':'all320_relocated_native_skip_cases_match_original_target_mapping',
        'all326_other_SC2_blocks_exact':'all327_other_SC2_blocks_exact',
        '421commands/114spanfixups/570nativecases/164speeches/8aliasedstyleobjects/5three-optionmenus;inverse bytes and326otherblocks exact. Research only.':'305physicalcommands/64spanfixups/320nativecases/116active speeches/6aliasedstyleobjects;unowned32copy/inversebytes/327otherblocks exact. Research only.'}
    for a,b in swaps.items():assert a in t,a;t=t.replace(a,b)
    anchor="        target_commands,target_speeches=inventory(arm,target)"
    assert t.count(anchor)==1
    t=t.replace(anchor,"""        unowned=None
        if number==115:
            at=spec['unowned_appended_copy_original_offset'];length=1886;new_at=mapped(at)
            assert old_end-at==length and source[at:old_end]==target[new_at:new_at+length]
            assert sha(target[new_at:new_at+length])==spec['unowned_appended_copy_current_sha256']
            unowned=dict(old_offset=at,new_offset=new_at,bytes=length,sha256=sha(source[at:old_end]),all32_physical_copy_speeches_byte_exact=True,canonical_SC3_B97_32_editorial_targets_still_uncredited=True)
"""+anchor)
    anchor="            text_records=texts,actor_style_commands=styles,choice_commands=choices,relative_skip_fixups=fixups,"
    assert t.count(anchor)==1
    t=t.replace(anchor,"            unowned_appended_copy=unowned,\n"+anchor)
    NEW.write_text(t,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_relocation_tools_provenance.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),all_actual_variable_prefixes_and_unowned1886byte_copy_guarded=True,no_executed_producer_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Source-bound relocation successor prepared for116active speech/34alternatives/32unowned copy speeches.')
