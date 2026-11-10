"""Complete clean book-handoff/chase exchange before reading predecessor English."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_clean_context_v5956')
SOURCE=Path('work/analysis/lil_B202_clean_inventory_v5955/all_clean_B202_speeches_before_predecessor_comparison.json')
GLOSSES={
5:('Hey,you!','9D abruptly calls to02. The familiar direct address establishes neither a name nor an existing acquaintance. Preserve the sudden interruption.'),
9:('Hm?','02 responds to being addressed. A brief questioning reaction,not agreement to take an item.'),
13:('I am giving you this,so use it however you like!','9D presents an unspecified object and relinquishes its use. This speech does not name the object,explain ownership or call it stolen. Preserve the emphatic unsolicited handoff before the chase interruption.'),
16:('Huh?','02 is surprised by the unsolicited offer. Keep this separate beat before a different speaker interrupts.'),
20:('Ah! There you are! Wait,you!','93 spots the fleeing9D and gives a rough order to stop. いやがった/待ちやがれ convey aggressive familiar speech. Do not invent a crime,law-enforcement role,rank or threat beyond the stated pursuit.'),
23:('H-huh?','02 becomes more bewildered as the pursuit interrupts. Preserve the escalating confusion and repeated/startled question rather than a factual explanation.'),
27:('See you!','9D gives a casual abrupt farewell. The departure follows the shouted pursuit;do not invent destination,escape success or a promise to return.'),
31:('Wait,you!','93 repeats the rough command to stop. Preserve this separate pursuit beat and distinct speaker,not a response by02.'),
35:('W-what is going on?!','02 reacts to the unexplained handoff and commotion. The emotional progression is surprise to exasperated bewilderment,not recognition of a known criminal.'),
39:('What are you doing,Admiral?','12 addresses02 with explicit 提督 and asks what is happening. Bind actual actor/name/voice before target prose;do not assume this is the Carlo19 from B201.'),
43:('Somehow,this got shoved onto me...','02 says the item was forcibly/insistently handed over,with a sense that it happened to her unexpectedly. Preserve passive unwilling involvement without inventing physical assault or a prior request.'),
47:('What is it?','12 asks what the object is. No earlier shared recognition or certainty is implied.'),
51:('A book...I think?','02 tentatively identifies the object as a book. Keep the uncertainty and pause;do not insert a specific title before the next speaker reads it.'),
55:('Let me see. A Dictionary of Glassmaking...','12 examines it and reads 『ガラスの製法辞典』. Preserve glass-manufacturing methods and the reference-book form. This is a literal source gloss,not an approved final item title or proof of the existing widget name/effect.'),
58:('Hmm. Why not just keep it,since it was given to you?','12 casually suggests accepting/keeping the free object. Preserve the permissive practical attitude;do not promise legality,value,recipe effects or a bargain.'),
61:('Huh? But...','02 begins an objection. Keep the hesitation as an unfinished response,not an invented explanation of ownership,guilt or intended return.'),
65:('If someone is giving you something,you might as well take it.','12 doubles down on the general pragmatic view that a freely offered thing should be accepted. The source does not guarantee legitimate ownership or explicitly tell02 to steal.'),
68:('Oh,and let me have a look at it later,will you?','12 adds a request to see/read the book later. This reveals the personal interest behind the preceding advice. Preserve the future request without making it a demand to own the book or inventing a promised loan duration.'),
72:('...So that was what you were after.','02 recognizes the motive revealed by12 wanting to see the book. Preserve the dry payoff/realization. Do not turn it into a romantic interest,a theft accusation or an unrelated plan.')}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',b,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==19 and len(d['commands'])==26 and len(b)==588 and end==586 and b[end:]==bytes(2)
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']} and Counter(r['source_selector'] for r in d['records'])=={2:8,18:6,157:3,147:2}
    assert d['typed_choice_or_actor_style_commands']==[]
    macros={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in d['records']) for m in ['FI','FA','FO']};assert not any(macros.values())
    rows=[]
    for r in d['records']:row=deepcopy(r);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all19_clean_unsolicited_book_handoff_pursuit_and_self_interested_request_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=202,records=rows,source_stored_bytes=588,source_logical_end=586,source_tailzeros=2,source_commands=26,source_selector_counts={'2':8,'18':6,'157':3,'147':2},source_macros=macros,
        whole_exchange_progression='9D calls to02 and abruptly gives an unspecified object with permission to use it.02 is surprised.93 spots9D and repeatedly orders9D to stop;9D gives a casual farewell amid02 surprise.02 is left bewildered.12 asks what02 is doing;02 says something was forcibly handed over.12 asks what it is;02 tentatively says a book.12 examines it and reads the glassmaking-reference title.12 advises keeping something freely given,interrupting02 hesitant objection with the same pragmatic view.12 then asks to see it later;02 realizes this personal interest was the motive. No choice or FE notice appears in this stored speech inventory.',
        explicit_Japanese_book_title='ガラスの製法辞典',literal_title_gloss_not_final_item_name='A Dictionary of Glassmaking',source_title_is_spoken_here_not_inherited_from_previous_unnamed_rope_scene=True,
        source_12_not_B201_19_no_actor_identity_inherited=True,source_9D_and93_names_relationship_and_roles_unbound=True,
        no_crime_police_rank_kinship_ownership_provenance_or_guaranteed_item_effect_invented=True,
        all19_speeches_progressive_no_FE_choices_typed_styles_or_source_macros=True,
        seven_non_speech_commands_preserved_in_clean_inventory_not_interpreted_as_full_item_or_event_semantics=True,
        actual_source_activation_paths_native_names_voices_item_title_widget_and_effects_pending=True,
        no_source_prose_editorial_gates_or_completion_credit_yet=True,prior_English_speech_unread=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B20219 clean-first glosses:unsolicited book handoff,pursuit,glassmaking title and self-interested later-reading payoff. Four source selectors,no FE/macros/choices;no older English or credit.')
