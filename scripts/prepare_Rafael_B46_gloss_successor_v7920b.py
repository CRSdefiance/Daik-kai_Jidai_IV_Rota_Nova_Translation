"""Preserve the failed panel-count diagnostic; include both original typed choices."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_gloss_tools_v7920b');assert not root.exists()
    menus="""    block=bytes.fromhex(g['clean_block_hex']);menu=next(c for c in g['commands'] if c['word']==0x2100)
    assert menu['offset']==256 and menu['native_extent']==36 and menu['whole_command_hex']==block[256:292].hex()
    assert block[256:262].hex()=='002100000e00' and block[274:276]==block[290:292]==b'\\0\\0'
    choices=[]
    for option,at,end,japanese,gloss in [
        (0,262,274,'お願いします','A polite acceptance of Julio\\'s offer to explain the other actions available at sea: asks him to go ahead. Preserve gratitude/politeness without inventing a command rank.'),
        (1,276,290,'もう大丈夫です','A polite decline of the offered explanation: says the speaker can manage now/does not need more help. This is not a health report or an assertion that every mechanic has already been demonstrated.')]:
        raw=block[at:end];assert raw.decode('cp932')==japanese
        choices.append(dict(id=f'DK4_MENU_B46_O0256_{option}',file_path='/data/SC0.DK4',block=46,kind='typed-menu-2100-choice',
            command_offset=256,option_index=option,source_reference=dict(block=46,command_offset=256,offset=at,bytes=len(raw),record_index=block[:at].count(b'\\0')),
            source_hex=raw.hex(),source_Japanese=japanese,source_terminator_hex=block[end:end+2].hex(),
            source_gloss=gloss,full_clean_exchange_context=EXCHANGE,source_gloss_not_current_English_derived=True,
            source_choice_order_preserved=True,current_English_body_unread=True,source_native_menu_owner_returns_branches_geometry_andcurrent_comparison_pending=True,new_credit=0))
    ROOT.mkdir(parents=True)
"""
    row=derive('scripts/gloss_Rafael_B46_clean_v7920.py','scripts/gloss_Rafael_B46_clean_v7920b.py',{
        'Rafael_B46_clean_gloss_v7920':'Rafael_B46_clean_gloss_v7920b',
        'fourteen distinct FE system panels':'two polite menu choices accepting or declining the explanation, followed by twelve distinct FE system panels',
        "sum(r['source_selector']==254 for r in rows)==14":"sum(r['source_selector']==254 for r in rows)==12",
        '    ROOT.mkdir(parents=True)\n':menus,
        '24_fresh_clean_exchange_glosses_before_current_English.json':'24_speeches2_choices_fresh_clean_glosses_before_current_English.json',
        "route_identity='Rafael',records=rows":"route_identity='Rafael',records=rows,menu_choices=choices,typed_menu_source=menu,source_units_pending_review=26",
        'fresh_clean_glosses=24,FE_system_panels=14':'fresh_clean_speech_glosses=24,fresh_clean_menu_choice_glosses=2,FE_system_panels=12',
        '24 fresh clean B46 glosses/14 distinct FE panels, complete B38 context. Current English unread; no credit.':'24 fresh clean B46 speech glosses/12 FE panels/two choices, complete B38 context. Current English unread; no credit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',dict(derivation=row,
        preserved_failed_producer='scripts/gloss_Rafael_B46_clean_v7920.py',
        failure='The assert expecting14 FE panels failed before output. Actual complete inventory has24 speeches,12 FE panels andone two-choice2100 menu.',
        failure_not_counted_aspassing_negative_orreview_credit=True,new_credit=0))
