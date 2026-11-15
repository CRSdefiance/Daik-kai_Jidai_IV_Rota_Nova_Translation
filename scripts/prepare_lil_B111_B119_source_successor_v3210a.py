"""Preserve the failed D0 assumption and bind each real source selector."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/map_lil_B111_B119_source_v3210.py')
NEW=Path('scripts/map_lil_B111_B119_source_v3210b.py')
ROOT=Path('work/analysis/lil_B111_B119_source_tools_v3210a')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    old="assert value.hex()==c['whole_command_hex'] and value[:2]==b'\\0\\x41' and value[18:20]==b'\\0\\xd0'"
    new="assert value.hex()==c['whole_command_hex'] and value[:2]==b'\\0\\x41' and value[18]==0 and all(r['source_selector']==value[19] for r in obj['records'])"
    assert text.count(old)==1
    text=text.replace(old,new).replace('lil_B111_B119_source_v3210','lil_B111_B119_source_v3210b')
    text=text.replace("version=label,style_index=i,","version=label,style_index=i,source_selector=value[19],")
    text=text.replace('source_dynamic_CF_D0_context_and_native_voice_mapping_pending','source_dynamic_selectors_context_and_native_voice_mapping_pending')
    anchor='        source_4100_is_actor_style_alternatives_not_player_choices=True,'
    assert text.count(anchor)==1
    text=text.replace(anchor,"        distinct_actor_style_presentation_selectors=sorted({r['source_selector'] for r in alternatives}),\n"+anchor)
    NEW.write_text(text,encoding='utf-8')
    source=read('work/analysis/lil_4100_alternatives_v3156/all14_clean_current_eight_style_alternatives.json')
    selectors=[dict(block=o['block'],command_offset=o['command_offset'],
        source_selector=o['versions'][0]['source_selector']) for o in source['objects'] if o['block']>=111]
    assert sorted({r['source_selector'] for r in selectors})==[208,209,214,215,220]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_selector_successor_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),source_objects=selectors,
        finding='The next six actor-style objects useD0,D1,D6,D7,DC;thecompleted prior eight objects allusedD0. Clean/current headers areexact;bind realselectors instead of assumingD0. Allnew dynamic-role consumers andcurrent identities require fresh binding before prose/display approval.',
        no_ROM_runtime_prose_registry_ledger_or_editorial_credit_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
