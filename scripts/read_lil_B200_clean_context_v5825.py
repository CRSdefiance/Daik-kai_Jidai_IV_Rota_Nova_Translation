"""Record the complete clean rescue/recovery/reward exchange before old English."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_clean_context_v5825')
SOURCE=Path('work/analysis/lil_B200_clean_inventory_v5824/all_clean_B200_speeches_before_predecessor_comparison.json')
GLOSSES={
    5:('Thud!', 'FE is an impact/collapse sound before13 notices the other person. Preserve the sound rather than inventing dialogue,a speaker,an injury,death,falling into water or a specific surface.'),
    9:('Ah!', '13 reacts to the collapse sound. This is a brief startled exclamation,not yet a diagnosis or an address by name.'),
    13:('...Ugh...', 'AC groans or stirs without a lexical explanation. Preserve weakness and the pauses;do not turn the sound into agreement,a name,an illness diagnosis or a report of pain in a specific body part.'),
    17:('What happened?! Are you all right?!', '13 urgently checks on AC. Preserve both questions and the initial alarm. Do not add enemy attack,poison,exhaustion,kinship or professional medical status.'),
    21:('Ugh...mm...', 'After the original scene-control transition,AC again groans or regains awareness. Keep this second distinct beat;do not delete it as a duplicate or invent an answer to the earlier questions.'),
    25:('You have come around.', '13 recognizes that AC is conscious. 気がつきましたね is an observation addressed to the recovering person,not a new injury or proof that13 provided medical treatment.'),
    29:('...Where am I?', 'AC is disoriented and asks about the present location. Preserve the opening hesitation without diagnosing amnesia or suggesting a new speaker.'),
    33:('At an inn. You had collapsed at the departure/harbor facility,so I had you brought to the inn.', '13 explains the present location and the rescue. Bind the approved game term for 出港所 from actual source/current consumers. 運ばせていただきました is polite/causative:do not insist that13 personally carried AC alone or invent assistants,transport,an innkeeper,room ownership or a precise port.'),
    37:('I see. I am sorry to have troubled you.', 'AC responds with polite regret for causing inconvenience. Preserve gratitude/apology without adding a debt amount,payment,a family relationship or a profession.'),
    40:('It was no trouble. Still,you look very unwell/pale. Rest and take it easy for a while.', '13 reassures AC,then remarks on a poor complexion and advises rest. Preserve this caring change from initial alarm. This is character dialogue,not proof of a doctor\'s diagnosis;no disease,medicine,injury severity,mandatory duration or guaranteed recovery is stated.'),
    44:('Well,I should be going. Excuse me. Take care of yourself.', '13 politely takes leave after giving reassurance. Do not make the departure complete before AC calls13 back,or add a destination,a scheduled appointment or a medical fee.'),
    47:('Ah,please wait. Are you a doctor?', 'AC calls13 back and asks about a profession. お医者様 is respectful address to a doctor,not a name or proof of status. The next reply explicitly denies it;do not call13 Doctor in labels or later speech.'),
    50:('No,I am not.', '13 directly answers the doctor question in the negative. Preserve that fact rather than hedging,suggesting a retired doctor or inventing an alternate profession.'),
    54:('I see. Well,it is not much of a thank-you,but please take this.', 'AC offers an unspecified object as thanks. お礼というほどのことでもありませんが modestly downplays the gift,not its price or power. The following original4830 operand must be mapped before item/portrait semantics;do not add a title,ownership history,money,medicine or romance.'),
    58:('No,really,please do not worry about it.', '13 first declines the offered thanks/reward. This answers AC\'s offer;do not convert it into accepting,refusing to help or an apology for doing something wrong.'),
    62:('But I would not feel right leaving it at that. Please accept it.', 'AC insists on properly thanking13. 気がすみません expresses personal dissatisfaction without reciprocating gratitude,not a threat,a demand for marriage or a claim that accepting an object cures illness. Keep the polite appeal and its link to the earlier refusal.'),
    65:('Well,if you insist,I will accept it. Please take care of yourself.', '13 yields to the repeated offer and accepts,then returns to concern for AC\'s wellbeing. Preserve the progression from refusal to acceptance without claiming a price,a transaction,medical credentials or future visits.'),
    69:('Yes,I will. Thank you very much.', 'AC acknowledges the caution and thanks13 again. Preserve the warm,polite closing;this does not establish a relationship,complete recovery or a promised voyage.'),
    72:('Carlo\'s Charm increased by1!', 'The second FE object is an explicit stat notification,unlike the initial impact sound. Bind カルロ to the native selector/catalog and the approved stat term. Preserve the named recipient,Charm and exact increment1. Do not infer what the two following A000 commands do until independently mapped.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);block=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',block,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==19 and len(d['commands'])==31
    assert len(block)==932 and end==930 and block[end:]==bytes(2) and not d['typed_choice_or_actor_style_commands']
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    assert Counter(r['source_selector'] for r in d['records'])=={19:9,172:8,254:2}
    macros={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in d['records']) for m in ['FI','FA','FO']}
    assert macros=={'FI':0,'FA':0,'FO':0}
    rows=[]
    for r in d['records']:
        row=deepcopy(r);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all19_clean_collapse_inn_recovery_declined_reward_and_Charm_glosses.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=200,records=rows,
        source_stored_bytes=932,source_logical_end=930,source_tailzeros=2,source_commands=31,
        progressive_speeches=17,FE_sound_effect_objects=1,FE_stat_notification_objects=1,source_macros=macros,
        whole_exchange_progression='An impact/collapse sound prompts13\'s startled reaction. AC groans;13 urgently asks what happened and whether AC is all right. After original scene controls,AC stirs again and13 recognizes consciousness. AC asks where this is;13 explains that AC had collapsed at the departure/harbor facility and was brought to an inn. AC apologizes for the trouble.13 reassures AC,remarks on a poor complexion,advises rest and prepares to leave. AC calls13 back and asks whether13 is a doctor;13 denies it. AC offers an unspecified token of thanks.13 initially declines. AC politely insists;13 accepts and repeats a caution to take care. AC agrees and expresses gratitude. A separate FE notification explicitly states that Carlo\'s Charm increases by1. Control-command/item meanings and native actor identities still require evidence.',
        source_FE_sound_index=5,source_FE_stat_index=72,no_parenthetical_thought_objects=True,
        source_doctor_question_explicitly_denied=True,no_specific_illness_carrying_method_or_item_title_invented=True,
        source_polite_rescue_reassurance_refusal_insistence_acceptance_progression_preserved=True,
        native_actor_names_voice_classes_role_label_stat_term_controls_scene_and_object_card_pending=True,
        prior_English_speech_unread=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B20019 clean-first glosses:collapse,inn recovery,doctor question denied,offered reward declined then accepted,Carlo Charm+1.17 progressive/two distinct FE roles;native identity/control/object context pending. No old English or credit.')
