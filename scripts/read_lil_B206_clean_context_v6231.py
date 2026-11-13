"""Gloss the complete ceramic-earring sales exchange and both choices before older English."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_clean_context_v6231')
SOURCE=Path('work/analysis/lil_B206_clean_inventory_v6230/all_clean_B206_speeches_before_predecessor_comparison.json')
GLOSSES={
5:('I have something good. Would you like to buy it?','173 initiates the sales approach. Keep the offer as a pitch,not an independently confirmed valuable treasure or an unsolicited purchase already made.'),
9:('What do you mean,something good?','07 asks what the seller is offering. The source voice is curious;do not turn this into an agreement to buy or an unrelated request for a favor.'),
13:('This,here.','173 presents the object. The following Lil recognition identifies earrings. The native picture command and its item data still require binding;do not infer ownership,authenticity or an effect from this short line.'),
17:('What? What is it? Oh,earrings.','Lil joins the inspection and recognizes earrings. Preserve the shift from curiosity to recognition without adding an assumed gift recipient or a specific material before the seller names it.'),
20:('Exactly. Ceramic earrings.','173 explicitly identifies the material. Keep ceramic consistent with the clean item title;do not replace it with an unsupported gold,gemstone or magical material.'),
24:('They do not seem all that unusual to me.','07 questions the seller\'s implied specialness. This is the buyer\'s skeptical impression,not proof that the item is a fake or a dismissal of the cultural material.'),
28:('Heh heh heh. These are not just ordinary earrings,you know.','173 responds to skepticism by hinting at a special story. Keep the chuckle and persuasive voice without inventing fraud as narrator fact or adding an aristocratic title.'),
32:('Really? I do not see anything particularly different about them.','Lil remains unconvinced by appearance. Keep both the question and the lack of an obvious unusual feature;do not imply she has independently tested the claimed power.'),
36:('They belonged to a dancer said to be the greatest in the world. Legend says that if you wear them and dance,you can charm any man.','The seller frames the dancer\'s reputation as what was said and the charm effect as a legend. Preserve those qualifications,the act of wearing them while dancing,and the explicit any-man claim. Do not identify a historical dancer,assert real magic or promise that the earrings improve dancing skill.'),
39:('Dancing? I will pass. Christina,what about you?','Lil declines the dancing proposition and asks Christina for her reaction. Preserve the addressed established name;do not invent a romantic partner,occupation,relationship or a separate purchase decision here.'),
42:('I might consider it if they made me a better dancer... But there is no man whose attention I want badly enough to go that far.','Christina distinguishes improved dancing from the seller\'s promised attraction. Preserve the conditional interest and her present lack of a man she wants to attract at that cost. Do not add a relationship history,sexual identity,permanent rejection of romance or actual skill boost.'),
46:('Wearing them yourself is not the only way to use them. Give them as a present to a woman at the tavern and she will be won over at once. You will become friendly with her right away.','The seller shifts tactics after the women show little interest in charming men. This is another sales claim,not a guaranteed narrator effect. 酒場にいる女 is a woman at the tavern;bind the game context before deciding whether a more specific occupational label is supported. Do not invent sex,marriage,employment or a relationship already achieved.'),
49:('Friendly? And what would we do after becoming friendly?','Christina asks the practical point of making friends. Preserve the echo and follow-up question;do not turn it into acceptance of a romantic or sexual proposition.'),
53:('Once you are friendly,you can hear all sorts of information. Women at taverns know a great deal of information.','The seller explains the proposed information-gathering benefit. Preserve that rationale as his persuasive account. Do not add a particular secret,quest,faction reward or a guaranteed completed information transfer.'),
68:('See? So you understand now?','This positive-response continuation follows the first choice. The seller seeks confirmation of his pitch. Native choice-result routing remains to be proved;do not infer that payment or acquisition has happened.'),
71:('So,how much?','Lil moves to the price after the favorable first response. This short natural question preserves her practical focus without implying agreement to pay any amount.'),
75:('Then I will ask for9000 gold. It is a rock-bottom price. I will not discount it by even a coin.','Preserve exactly9000 gold,the exaggerated loss-making/rock-bottom sales claim and refusal to lower the price. 出血価格 is an idiom,not literal bloodshed. ビタ一文 emphasizes not one coin;do not introduce a different currency,extra fee,actual discount or a proved fair valuation.'),
90:('You have a discerning eye. Here are the ceramic earrings.','The sale-success continuation flatters the customer and hands over the named item. Keep ceramic earrings consistent. Actual inventory/payment commands remain unforced and require observation;the line itself is not proof that every effect has completed.'),
97:('...Looks like I misjudged you. Go away. I am not selling them to you.','One refusal continuation reverses the flattering tone and withdraws the sale. Do not invent that the player lacks money,attempted fraud or received a refund. Preserve the seller\'s change of attitude and dismissal.'),
100:('Wait,that is rude! You were the one who approached us!','Christina objects to the seller\'s insulting dismissal and points out that he initiated contact. Preserve that complaint without inventing a debt,family tie or new insult.'),
103:('Hmph. I have no use for cheapskates. Get out of here.','The seller explicitly calls the customers stingy and dismisses them brusquely. Keep the rudeness in character without adding profanity,violence,rank or a literal proof of their finances.'),
106:('I would not buy from you anyway!','Christina rejects the seller in return. 願い下げ is a refusal to have anything to do with the offer,not a refund request or a line about a desire being granted.'),
117:('...I am not selling to someone who still does not understand after all that. Go away.','The other refusal continuation reacts to a lack of understanding/appreciation of the pitch. Preserve the sales withdrawal and dismissal;do not automatically label it an affordability failure or invent which menu result caused it before native routing is bound.'),
120:('Huh? What exactly are you trying to say? That man really puts me in a bad mood.','Christina responds to the other dismissal with incomprehension and irritation. Preserve both the direct question and subsequent remark about the man. 気分悪い is annoyance here,not a new physical illness or injury.'),
}
CHOICE_GLOSSES={
852:[('なるほど','I see.','The first response acknowledges the information-gathering explanation;it does not agree to an unknown price or confirm the earrings\' legend.'),('だから？','So?','The second response challenges the point of the pitch. Preserve its skeptical tone and option order rather than changing it into a purchase refusal before the price is given.')],
1020:[('買った！','I will take them!','This accepts the offered ceramic earrings after the explicit9000-gold price. Preserve acceptance in option0;do not add haggling,credit or a request for a gift.'),('高い…','That is expensive...','This comments that the price is high. Keep the objection in option1 rather than silently replacing the label with a different affordability claim or a request for a lower counteroffer.')],
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',b,4)[0];counts=Counter(c['word'] for c in d['commands'])
    assert d['read_no_predecessor_English'] and len(d['records'])==24 and len(d['commands'])==42 and len(b)==1524 and end==1522 and b[end:]==bytes(2)
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']} and Counter(r['source_selector'] for r in d['records'])=={173:13,7:7,2:4}
    assert counts[0x2100]==2 and counts[0x2200]==counts[0x4100]==counts[0x8000]==counts[0xC200]==counts[0x2000]==0 and counts[0xA000]==3
    relative=[c for c in d['commands'] if c['word'] in [0x100,0x200,0x300,0x400]];assert len(relative)==8
    macros={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in d['records']) for m in ['FI','FA','FO']};assert macros==dict(FI=0,FA=0,FO=0)
    rows=[]
    for old in d['records']:
        r=deepcopy(old);r.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(r)
    choices=[]
    for c in d['typed_choice_or_actor_style_commands']:
        at=c['offset'];table=list(struct.unpack_from('<2H',b,at+2));assert c['word']==0x2100 and table==[0,10]
        for option,(jp,gloss,note) in enumerate(CHOICE_GLOSSES[at]):
            off=at+6+table[option];raw=b[off:b.index(0,off)];assert raw.decode('cp932')==jp
            choices.append(dict(id=f'DK4_CHOICE_B206_C{at}_O{option}',command_offset=at,option_index=option,source_reference=dict(offset=off,bytes=len(raw)),source_record_index=b[:off].count(b'\0'),source_hex=raw.hex(),source_Japanese=jp,fresh_source_gloss=gloss,whole_exchange_note=note))
    arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');actors=[]
    for i in [2,7,173]:
        fs=[]
        for delta in [0,4,8]:
            pointer=struct.unpack_from('<I',arm,TABLE+i*32+delta)[0];fs.append(None if not pointer else cstring(arm,pointer-BASE)[:-1].decode('cp932'))
        actors.append(dict(actor_ID=i,clean_name_fields=fs))
    assert [r['clean_name_fields'] for r in actors]==[['リル','アーゴット',None],['クリスティナ','エルネコ',None],['怪しい人','アラブ水夫',None]]
    p=struct.unpack_from('<I',arm,0x11E210+138*24)[0];item=cstring(arm,p-BASE)[:-1].decode('cp932');assert item=='陶器のイヤリング'
    ROOT.mkdir(parents=True);save(ROOT/'all24_clean_earring_pitch_purchase_refusal_and4_choice_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=206,records=rows,typed_choice_glosses=choices,source_objects=28,source_speeches=24,source_choice_objects=2,source_choice_labels=4,source_native_commands=42,source_selectors=[2,7,173],source_selector_counts={'2':4,'7':7,'173':13},source_macros=macros,source_FE_objects=0,source_relative_sites=8,source_A000=3,source_stored_bytes=1524,source_logical_end=1522,source_tailbytes=2,source_end_word_offset=1518,source_actor_fields=actors,source_item138=item,
        whole_exchange_progression='A seller approaches Christina and Lil with ceramic earrings. Both are skeptical. He invokes a world-famous dancer and a legend about charming men by wearing them while dancing. Lil passes;Christina would consider better dancing but has no man whose attention she wants that badly. He shifts to giving them to a woman at a tavern to win her friendship and obtain information. The first choice acknowledges or challenges that rationale. A favorable continuation leads to the9000-gold,not-one-coin-less price and a second acceptance/high-price choice. Success flatters the buyer and names the handed-over earrings. Other continuations dismiss the customers,with Christina objecting or returning the rebuff. The exact menu-result/cancel/effect routing remains unproved and must not be inferred from stored order.',
        name_localization_leads='Lil and Christina use established clean proper-name fields.173 primary怪しい人 marks a dubious/suspicious person;the complete exchange establishes selling behavior. Review a natural speaker label in context,not a mechanical internal-record description. The secondaryアラブ水夫 is metadata,not automatically a spoken nationality,profession or added nameplate. No age,marriage,kinship or rank is inferred.',
        no_invented_dancer_identity_magical_fact_dance_skill_boost_romantic_relationship_profession_or_affordability_failure=True,
        all24_speech_and4_label_glosses_before_predecessor_English=True,prior_English_speech_unread=True,native_choice_count_getters_selection_cancel_fonts_and_routing_pending=True,source_actors_voices_picture_resource_effect_and_actual_scene_pending=True,no_ROM_registry_ledger_or_review_credit_change=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('B206 clean-first28 glosses:24 speeches/four labels,two menus,eight relative sites,three actors and9000-gold ceramic-earring pitch. Earlier English unread;no credit.')
