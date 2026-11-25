"""Read the full cough/almond-remedy exchange from clean Japanese before old prose."""
from pathlib import Path
from copy import deepcopy
import struct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B187_clean_context_v5187')
SOURCE=Path('work/analysis/lil_B187_clean_inventory_v5186/all_clean_B187_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('My cough has been bad lately. Cough,cough.',
        '9B opens with a recent persistent/bad cough and audible coughing. Preserve the discomfort without inventing a duration,fever,diagnosis,contagion source or gameplay penalty. Bind actor155 before assigning a role or personal name.'),
    10:('Are you all right?',
        '57 responds with direct concern. It is a natural brief question within the exchange,not a diagnosis or a formal medical role. Bind actor87 before choosing identity.'),
    14:('Yes,I am all right. It is a little hard/uncomfortable,though. Cough,cough.',
        '9B reassures the companion while qualifying the reassurance with discomfort and continued coughing. Preserve this modest tension. No severe breathing emergency,complete recovery or objective health judgment is established.'),
    17:('Come to think of it,I have been seeing quite a few people coughing lately.',
        '57 recalls observing other people coughing. Keep the recent personal observation;do not upgrade it to a verified epidemic,universal illness or narrator statement.'),
    20:('Could some nasty illness be going around?',
        '9B speculates with a question. Preserve uncertainty and the colloquial worried tone;do not assert a named disease or proven outbreak.'),
    24:('I heard somewhere that there is a good medicine/remedy.',
        '57 recalls hearsay from an unspecified place. The medicine is not named or clinically verified. Do not invent a physician,shop,source town or recommendation to the real reader.'),
    27:('Really? What is the medicine called? Cough,cough.',
        '9B reacts with interest and asks its name. Keep the cough and practical name question;no medicine has been bought,taken or shown to work for this speaker.'),
    30:('I forgot its name,but I hear it uses almonds.',
        '57 explicitly cannot recall the name and reports the ingredient. Preserve both the knowledge gap and reportedness. Almonds are not themselves identified as the complete named medicine,and no dose or preparation is supplied.'),
    33:('Almonds?',
        '9B gives a small surprised/questioning echo. It sets up the explanation of why 57 remembered the ingredient;do not expand it into disbelief or a new medical claim.'),
    37:('I thought,Oh,they use something like almonds?,so that stuck in my memory.',
        '57 remembered because using almonds was surprising. Keep the quoted reaction and its causal link to remembering. Do not turn memory of an unusual ingredient into expertise,a forgotten recipe or proof of efficacy.'),
    41:('Does that work? Cough,cough.',
        '9B asks about effectiveness,still coughing. Preserve the question rather than answering it or asserting a cure. Its referent is the reported unnamed almond-containing remedy.'),
    45:('They say it works unbelievably well,so it is selling very well.',
        '57 relays a reported claim of striking effectiveness and strong sales. Preserve both source-explicit details and their causal connection without sanitizing them away or upgrading hearsay to narrator-confirmed medical efficacy,guaranteed recovery,prices,scarcity or profit.'),
    48:('I see. Then I will try looking for it.',
        '9B decides to look for the remedy. This is an intention to search,not a completed purchase,use,transaction or recovery. Do not specify a shop or journey.'),
    52:('I will look for it too.',
        '57 offers a parallel search. Preserve willingness without inventing a promise to buy it,a cure,a specific destination,kinship or a formal duty.'),
    56:('Thanks. Cough,cough.',
        '9B thanks the companion while still coughing. The continuing cough matters:the scene has not shown treatment or recovery. Keep the casual gratitude and audible reaction.'),
    60:('Almonds may become popular in Malacca.',
        'The separate null-actor FE forecasts possible popularity. Bind approved Malacca/Almonds names before English comparison. It does not prove the earlier scene location,an earned boom,confirmed medical efficacy,a specific completed remedy or trading profit.'),
}

if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);block=bytes.fromhex(source['clean_block_hex'])
    assert source['read_no_predecessor_English'] and source['physical_speech_objects']==16 and len(source['commands'])==19
    assert set(GLOSSES)=={r['source_record_index'] for r in source['records']}
    assert [(c['offset'],c['word'],c['whole_command_hex']) for c in source['commands'] if c['word']!=0x4000]==[
        (8,0xA000,'00a0ffff014e2fa1'),(672,0xC200,'00c2'),(674,0,'00000000')]
    assert len(block)==680 and 8+struct.unpack_from('<H',block,4)[0]==678 and block[678:]==bytes(2)
    rows=[]
    for original in source['records']:
        row=deepcopy(original);gloss,note=GLOSSES[row['source_record_index']]
        row.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all16_clean_exchange_and_fresh_glosses.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=187,records=rows,
        physical_speech_objects=16,source_commands=19,source_stored_bytes=680,source_logical_end=678,source_alignment_tailzeros=2,
        complete_exchange_progression='9B complains of a bad recent cough;57 asks with concern;9B reassures but admits discomfort;57 recalls other coughing people;9B wonders about illness;57 recalls a good remedy;9B asks its name;57 forgot the name but heard it uses almonds;9B echoes the surprising ingredient;57 explains why that detail stuck;9B asks whether it works;57 relays exceptional effectiveness and strong sales;both intend to look for it;9B thanks the companion while still coughing;a separate tentative Malacca almond-fashion notice closes.',
        source_fact_boundaries=[
            'Bind selectors9B155 and5787 names/voices before choosing profession,rank,relationship or personal names. No kinship or physician role is supplied by this exchange.',
            'Personal observation and speculative illness question are distinct from a verified outbreak or diagnosis.',
            'The unnamed remedy reportedly uses almonds. Preserve the forgotten name,surprised memory trigger,reported effectiveness and reported strong sales. Do not invent a recipe,dose,cure,price,scarcity or profit.',
            'Both later replies express intention to search;continued coughing and gratitude do not show a completed purchase,use or recovery.',
            'The impersonal Almonds/Malacca notice remains prospective and does not establish the earlier conversation location or earned fashion.',
            'This block has19 linear commands,leading A0008,C200672,end674 and two tailzeros. Do not inherit B186 one700 predicate,six relative sites,three alternatives or its two exact R13 wrap exceptions.',
        ],
        read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B187:16 fresh clean-only glosses as one exchange;reported almond-remedy claims/search intentions remain distinct. No old English read or credit.')
