"""Fresh clean-Japanese whole-exchange gloss before any current B46 English exposure."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_clean_gloss_v7920b')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
CONTEXT=Path('work/analysis/Rafael_B46_clean_context_v7919/complete_clean_SC0_B38_EV0_andcoverage_before_current_English.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7917/verified_handoff.json')
GLOSSES={
15:"Actor05 exhales in relief and says that thanks to ハイレディン they escaped with their lives. This is gratitude for an actual rescue, not proof of family, formal alliance or command hierarchy.",
18:"Rafael quietly agrees, trailing off. Preserve the subdued, preoccupied response after the danger rather than making him exuberant.",
23:"Julio says that at this rate the time when an enemy fleet challenges them to a fight may arrive sooner than expected. The enemy initiates the challenge; this is a warning about approaching danger, not encouragement to attack immediately.",
27:"Julio considers it best to teach Rafael the other things they can do at sea. The instruction follows his concern about their preparedness, without adding a rank or family relationship.",
41:"Julio announces an explanation of three actions: looking around at sea, initiating a battle, and searching. Do not imply that these are the only possible actions at sea.",
44:"Julio explains that to see detailed information about a nearby town or fleet, or to start a battle themselves, they must designate that specific target.",
47:"Julio says that searching along the coast can uncover various things. The possibility is conditional, not a guaranteed discovery, cash reward or instruction to search the open water.",
51:"The system panel explains that at sea the player can inspect information about nearby towns and fleets.",
54:"Pressing the Y button displays a magnifying-glass mark. The magnifying glass indicates information mode. Keep both the button and the meaning of the icon.",
58:"To inspect information, place the magnifying glass on a town or fleet and press A. Preserve both eligible target types and the confirmation button.",
62:"The system panel says that from a ship the player can also initiate battle against another fleet or a town. Do not erase town attacks or imply only defensive battles.",
65:"While the magnifying glass is displayed, pressing L changes the mark to a sword. The sword indicates battle mode. This is the particular information-to-battle transition.",
68:"To initiate battle, place the sword on the town or fleet and press A. Preserve the chosen target and confirmation, not automatic attack merely from switching modes.",
72:"To search at sea for items or supplies, press R while the magnifying glass is displayed. Preserve R, the starting information mode and both items and supplies.",
76:"A gray frame appears. This is the search mark and indicates search mode. Do not turn its color or shape into an invented button or cursor.",
80:"The search covers land within the gray frame; press A. Preserve land as the search area, not the sea or every visible object, and the confirmation button.",
83:"The player can switch among information, battle and search modes with L and R. The next two panels separately specify each direction.",
87:"L cycles in this order: information, then battle, then search. Preserve the exact order. The source list does not itself need an invented fourth entry.",
91:"R, or alternatively Y, cycles in this order: information, then search, then battle. Preserve the alternative Y button and the reverse order relative to L.",
95:"Julio asks how that was and whether Rafael understood. It is a check that the explanation made sense, not a claim that the player has demonstrated the mechanics.",
98:"Rafael politely says yes and thanks him. Preserve the respectful, appreciative reply without adding a familial title or military form of address.",
105:"Julio accepts the answer and cautions him emphatically never to let his guard down at sea. Keep the sober warning after the tutorial rather than inventing a new threat.",
109:"Rafael answers yes. The brief acknowledgment naturally responds to Julio's warning; no additional promise or invented action is supplied.",
117:"Rafael's private thought trails off: someday, surely... The desired future outcome remains unstated in this record. Do not complete it as revenge, defeating Spain, becoming the greatest merchant or any other invented objective.",
}
EXCHANGE="""The original EV0 event46/category5/action47 selects SC0 B46 and requires event38. Event38/category3/action39 selects B38 and requires event37. These are source dependencies, not proof of immediate chronology, current port, natural activation or every outer condition. In the complete clean B38 exchange a Spanish fleet threatens the Portuguese youths over an allegation of collusion with pirates; Rafael fears their current strength may be insufficient. ハイレディン appears, rejects needing children's help against Pedro, intervenes, orders Rafael away, and Rafael thanks him and calls for escape. The stored exchange also includes the Spanish commander's withdrawal and threat. Branch selection, names/getters and actual behavior still require independent mapping.

B46 opens with actor05's relief that ハイレディン saved their lives. Rafael agrees pensively. Julio warns that an enemy challenge may come sooner than expected and decides to explain other actions at sea. His overview leads into two polite menu choices accepting or declining the explanation, followed by twelve distinct FE system panels describing information, battle and search, targets, confirmations, marks and the opposite L/R cycle orders (Y also follows R's order). Julio then checks understanding, receives Rafael's polite thanks, warns him not to relax at sea, and receives a short acknowledgment. Rafael ends with an unfinished private future hope. Preserve the emotional movement from relief and unease to practical teaching and renewed caution. Do not turn system instruction into character speech, assign FE a character, add family/rank, guarantee discoveries, omit town attacks or finish the private thought."""
if __name__=='__main__':
    assert not ROOT.exists()
    source,context,prior=map(read,[SOURCE,CONTEXT,PRIOR])
    ledger=Path('translations/editorial_review_current_v1.json')
    assert sha(ledger.read_bytes())==prior['ledger_sha256'] and prior['completed']==6950
    g=source['groups'][0];c=context['groups'][0]
    assert g['block']==46 and len(g['records'])==24 and g['completed_coverage_overlap']==0 and not source['inventory_failures']
    assert c['block']==38 and len(c['records'])==23 and not context['inventory_failures']
    assert len(g['commands'])==37 and len(c['commands'])==48
    assert g['source_event_records'][0]['must_be_completed']==[38] and c['source_event_records'][0]['must_be_completed']==[37]
    assert {r['source_record_index'] for r in g['records']}==set(GLOSSES)
    rows=[]
    for original in g['records']:
        row=deepcopy(original);index=row['source_record_index']
        assert row['current_English_body_unread'] and row['source_Japanese'] and row['source_decode_error'] is None
        row.update(source_gloss=GLOSSES[index],full_clean_exchange_context=EXCHANGE,
            source_gloss_mode='freshly authored from complete clean Japanese before current English',
            source_gloss_not_current_English_derived=True,current_English_body_unread=True,
            whole_source_exchange_andoriginal_prerequisite_reread=True,
            source_native_names_roles_controls_display_andcurrent_comparison_pending=True,new_source_prose_orcompletion_credit=0)
        rows.append(row)
    assert sum(r['source_selector']==254 for r in rows)==12
    assert {r['source_selector'] for r in rows}=={0,5,6,254}
    block=bytes.fromhex(g['clean_block_hex']);menu=next(c for c in g['commands'] if c['word']==0x2100)
    assert menu['offset']==256 and menu['native_extent']==36 and menu['whole_command_hex']==block[256:292].hex()
    assert block[256:262].hex()=='002100000e00' and block[274:276]==block[290:292]==b'\0\0'
    choices=[]
    for option,at,end,japanese,gloss in [
        (0,262,274,'お願いします','A polite acceptance of Julio\'s offer to explain the other actions available at sea: asks him to go ahead. Preserve gratitude/politeness without inventing a command rank.'),
        (1,276,290,'もう大丈夫です','A polite decline of the offered explanation: says the speaker can manage now/does not need more help. This is not a health report or an assertion that every mechanic has already been demonstrated.')]:
        raw=block[at:end];assert raw.decode('cp932')==japanese
        choices.append(dict(id=f'DK4_MENU_B46_O0256_{option}',file_path='/data/SC0.DK4',block=46,kind='typed-menu-2100-choice',
            command_offset=256,option_index=option,source_reference=dict(block=46,command_offset=256,offset=at,bytes=len(raw),record_index=block[:at].count(b'\0')),
            source_hex=raw.hex(),source_Japanese=japanese,source_terminator_hex=block[end:end+2].hex(),
            source_gloss=gloss,full_clean_exchange_context=EXCHANGE,source_gloss_not_current_English_derived=True,
            source_choice_order_preserved=True,current_English_body_unread=True,source_native_menu_owner_returns_branches_geometry_andcurrent_comparison_pending=True,new_credit=0))
    ROOT.mkdir(parents=True)
    save(ROOT/'24_speeches2_choices_fresh_clean_glosses_before_current_English.json',dict(
        format='dk4-source-first-whole-exchange-gloss-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC0.DK4',block=46,route=0,route_identity='Rafael',records=rows,menu_choices=choices,typed_menu_source=menu,source_units_pending_review=26,
        complete_clean_source_group=deepcopy(g),prerequisite_complete_clean_source_group=deepcopy(c),
        fresh_clean_speech_glosses=24,fresh_clean_menu_choice_glosses=2,FE_system_panels=12,source_selectors=[0,5,6,254],
        complete_clean_exchange_andprerequisite_read_before_current_English=True,
        current_English_bodies_unread=True,localized_English_manuscript_not_yet_authored=True,
        names_controls_branch_predicates_native_current_effective_comparison_actual_andrelease_pending=True,
        exact_L_information_battle_search_andR_orY_information_search_battle_order_preserved=True,
        opening_rescue_anduncompleted_final_private_thought_preserved=True,
        no_natural_activation_current_location_full_mechanics_orcompleted_editorial_claim=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTEXT,PRIOR,Path(__file__)]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('24 fresh clean B46 speech glosses/12 FE panels/two choices, complete B38 context. Current English unread; no credit.')
