"""Read the complete cooking-and-friendship exchange before earlier English."""
from pathlib import Path
from copy import deepcopy
import struct
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B193_clean_context_v5446')
SOURCE=Path('work/analysis/lil_B193_clean_inventory_v5445/all_clean_B193_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('Ah,that was delicious. This is the first time I have had such wonderful cooking.','SelectorA6/166 praises the meal just enjoyed with genteel emphatic delight. Preserve the first-person first-time superlative without inventing a particular dish,ingredient,restaurant,host,kinship or status;bind actual roles/voices first.'),
    10:('It really was. It had an exciting,stimulating flavor.','A7/167 agrees and emphasizes the stimulating flavor. The later chili explanation supplies culinary context;do not invent a medical effect,exact heat level,recipe or health benefit.'),
    14:('Tell me,how do you make food this delicious?','166 asks about how to prepare the excellent food. This is a cooking question,not a trading or purchase tip,an economic mechanic or a request to change the menu.'),
    17:('Heh heh,the secret is this.','A8/168 gives a softly amused reveal and refers to an object/ingredient disclosed next. No source item-presentation command exists;do not invent a visible held item,gesture,shop or completed handover.'),
    21:('A questioning reaction.','166 responds with a lone question mark before the explanation. Preserve curious puzzlement;do not add a factual guess or identity.'),
    25:('It is called chili pepper. I hear it is a kind of spice. It goes very well with the ingredients around here.','168 namesトウガラシ,marks the spice classification as something heard,and praises compatibility with local ingredients. Bind actual commodity versus category and approved spelling. Preserve reportedness without invented recipe,origin,ingredient list,amount or delivery.'),
    29:('Oh,but is it not expensive?','166 asks with polite concern about cost. Preserve the actual price question without an invented amount,market trend,scarcity,profit or purchasing action.'),
    33:('Not particularly.','168 says the expense is not that great. Do not upgrade the relative reassurance to free,universally cheap,guaranteed supply or a narrator-verified market price.'),
    37:('Oh,then that is a relief. Perhaps I will try using it in tonight’s cooking.','166 is reassured and considers using the ingredient for tonight’s meal. Keep tentative intention and tonight;no purchase,completed preparation or commercial order occurs.'),
    40:('I would like to make it too.','167 also expresses a desire to cook. Do not turn this into wanting to buy or sell the spice or food.'),
    44:('Then,shall I teach you how to cook with it now?','168 politely offers immediate instruction in preparation. Preserve now and the offer/question,not a completed lesson,compulsory instruction,recipe steps or trading advice.'),
    47:('Oh,really!?','166 reacts with delighted surprise to the offer. Preserve the emotional progression,not doubt about price or a new claim.'),
    51:('How kind of you.','167 appreciates the offer. Source tone is courteous and warm;do not invent a fee,obligation or repayment.'),
    55:('Of course. We are friends,after all.','168 explicitly grounds willingness in friendship. Friendship is source-supported here;do not omit it under a blanket relationship prohibition or add kinship,romance,rank or a prior-history claim.'),
    59:('Chili pepper may become popular in 京城.','Separate impersonal FE is prospective. Bind approved commodity/city names against clean/current native references before localization. Do not rename the historical place by assumption,certify the earlier household location or claim earned fashion,shortage,price growth or profit.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex'])
    assert d['read_no_predecessor_English'] and len(d['records'])==15 and len(d['commands'])==18
    assert len(b)==668 and 8+struct.unpack_from('<H',b,4)[0]==666 and b[666:]==bytes(2)
    assert [(c['offset'],c['word'],c['whole_command_hex']) for c in d['commands'] if c['word']!=0x4000]==[(8,0xA000,'00a0ffff011d39a1'),(660,0xC200,'00c2'),(662,0,'00000000')]
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    rows=[]
    for original in d['records']:
        row=deepcopy(original);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[row['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all15_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=193,records=rows,physical_speech_objects=15,source_commands=18,
        source_stored_bytes=668,source_logical_end=666,source_alignment_tailzeros=2,source_selectors_hex=['A6','A7','A8','FE'],source_selectors_decimal=[166,167,168,254],
        complete_exchange_progression='166 and167 praise the meal;166 asks about preparation;168 reveals the secret ingredient;166 questions;168 names chili pepper and its reportedly spice classification and local compatibility;166 worries about price;168 reassures;166 considers tonight’s cooking;167 also wants to cook;168 offers immediate instruction;166 is delighted;167 thanks the kindness;168 explicitly cites friendship;a separate prospective chili/京城 forecast follows.',
        source_fact_boundaries=[
            'Bind exact A6/A7/A8(decimal166/167/168) roles,names and voices before authoring. Genteel sentence endings do not independently prove class,gender,rank,kinship or marriage.',
            'Review the full three-person progression as cooking,ingredient explanation,cost concern,reassurance,tentative household use,teaching offer,gratitude and explicit friendship. Do not change preparation into commodity trading advice.',
            'Preserve the first-time meal praise,stimulating flavor,reportedly spice classification,local compatibility,price question and relative reassurance as character statements. No quantities,recipe,origin,health claim,shortage,profit or narrator market certification.',
            'Tonight and now are source-explicit. Intentions and an offered lesson are not completed cooking,purchase,trade,instruction or ingredient transfer.',
            'Friendship is explicit inお友達;preserve it without inventing kinship,romance,employment,new rank or specific prior history.',
            'Bind approvedトウガラシ and京城 names before comparing prior English. FE stays prospective and does not prove earlier location or earned fashion.',
            'Preserve all18 linear commands,15 complete speech preambles,A0008 raw00a0ffff011d39a1,C200660,end662,668 stored/666 logical bytes and2 tailzeros. No predicates,relative branches or item presentation are supplied.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B193:15 clean-only whole-exchange glosses preserve cooking,price concern,teaching offer and explicit friendship. No earlier English or credit.')
