"""Whole clean rigging negotiation and both purchase outcomes before previous English."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_clean_context_v5901')
SOURCE=Path('work/analysis/lil_B201_clean_inventory_v5900/all_clean_B201_speeches_before_predecessor_comparison.json')
GLOSSES={
5:('The rope for the mast is quite worn, is it not?', '69 opens with a sales observation about existing mast rigging. Preserve the stated wear without inventing imminent breakage,an inspection result,the rope\'s age or a confirmed mechanical fault.'),
8:('Is it? I think it is still all right.', '02 questions the seller\'s assessment and thinks the current rope remains usable. This sets up the later refusal rationale;do not turn it into agreeing that replacement is urgent.'),
11:('No,no,it is worn. Why not replace it with this rope? I hear it has some sort of mysterious power.', '69 insists on wear and proposes this particular replacement. なんでも...っていうんですよ reports a claim/hearsay about an unspecified unusual power. Do not confirm magic,identify the item by title or invent what it does.'),
14:('Oh! Of course,you will replace it for free,will you not?', '02 responds with a cheeky request/expectation of no charge. Preserve the free-of-charge joke and question;do not invent a prior promise,a giveaway policy or a completed purchase.'),
18:('Wh-what? Certainly not! Of course,I will give you a discount,but how about300000 gold?', '69 is flustered by the free request. 勉強 means a price concession in this sale,not studying or schooling. Preserve the exact initial300000 asking price and the transition to bargaining.'),
21:('Now,now,now! Surely you are not going to buy it at that price,Admiral?', '13 steps in with alarm at the proposed price and questions02 before any decision. 提督 is explicit source address;do not infer kinship,ownership hierarchy beyond that address or that a purchase has already happened.'),
24:('However special it may be,that price for mast rope is a bad joke.30000 gold is the most it is worth.', '13 disputes value while allowing that it is a special item. Preserve the30000 counteroffer and at-most assessment;do not add its material,origin,magical effect or claim a known market price.'),
27:('W-wait a moment! There is nothing else like it in the world. Then,how about200000 gold?', '69 objects,asserts uniqueness and lowers the asking price to200000. Preserve the seller\'s claim as speech,not independently established item lore. It is not two ropes or two items.'),
30:('50000.', '13 counters with a deliberately terse50000 offer. Keep the bargaining rhythm and exact amount;do not add an ultimatum or a completed payment.'),
34:('Hmm...150000 gold. Please,let me off at that.', '69 lowers the asking price to150000 and appeals to13 to accept it. 勘弁してください is an idiomatic negotiating plea,not forgiveness for a crime or physical threat.'),
37:('75000 gold.', '13 gives another terse counteroffer at exactly75000. Preserve this separate beat rather than merging it into the seller\'s prices.'),
41:('You have got me. Then,100000 gold. I cannot go any lower.', '69 gives a final100000 asking price and says this is the limit. Preserve concession and minimum-price intent without adding poverty,losses or a promise about the rope\'s power.'),
45:('Hmm,that is about right. What would you like to do,Admiral?', '13 accepts this as a reasonable price and defers the decision to02. The following2100 menu has only Buy/Do not buy;do not invent a delegation option or assume approval.'),
59:('Yes,leave the rest to me.', 'On the purchase branch,13 accepts the chosen course and takes charge of the remaining arrangements. Do not infer a different price,a new crewmember or a completed delivery before later speech.'),
62:('Yes,please do. I am counting on you.', '02 warmly acknowledges13\'s offer to handle matters. よろしく is contextual confidence/thanks,not a family address or a new rank.'),
69:('Then,bring the rope up to the deck.', '13 addresses69 as 親父,a familiar vendor address. This is not evidence of fatherhood. Preserve the instruction to bring the rope to the deck,without inventing a boat name,helpers or mounting method.'),
73:('Certainly. Thank you for your business.', '69 agrees and gives the standard merchant\'s thanks. Do not translate 毎度 as a claim that these characters have previously shopped together;it is conventional sales language.'),
77:('FI\'s Charm increased by1!', 'The first purchase-branch FE panel names the player through original FI and increments Charm by exactly1. Keep it as a null-actor system notice;do not replace FI with a fixed name or merge it with the next recipient.'),
80:('Carlo\'s Intelligence increased by1!', 'A separate purchase-branch FE panel names カルロ and increments 知力 by exactly1. Bind actual actor identity and approved stat terminology before English. Do not change the recipient to the captain,or treat this as the same stat as the preceding Charm notice.'),
86:('The rope is still perfectly usable. We do not have to rush to replace it,do we?', 'On the refusal branch,02 returns to the earlier belief that the existing rope is usable. Preserve rejection of urgency rather than inventing insufficient funds,a failed affordability check or denial that the special rope exists.'),
90:('Is that so? Then,I will turn it down.', '13 accepts02\'s decision and says he will decline. Preserve the future/intended act leading into the seller\'s reaction;do not change this to buying,delegating or a personal inability to pay.'),
94:('You are not buying it?! Please do not waste my time if you are only looking.', '69 is surprised and irritated at the refusal. 冷やかし is unserious browsing/teasing in a sales context,not literal cooling or an established insult about poverty.'),
97:('No,no,I really am sorry. Please forgive us.', '13 apologizes and placates69 after the refusal. Do not add a debt,a promised future sale,a gift or a family relationship. Match the light defusing tone rather than ceremonial confession.'),
100:('FI\'s Spirit increased by1!', 'The refusal branch has its own null-actor FE notice:player FI,精神,exact increment1. Bind the approved stat term;do not duplicate the purchase Charm/Carlo Intelligence notices or invent loss of an item.')}

if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);block=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',block,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==24 and len(d['commands'])==44
    assert len(block)==1452 and end==1452 and block[end:]==b''
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    assert Counter(r['source_selector'] for r in d['records'])=={105:8,2:4,19:9,254:3}
    macros={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in d['records']) for m in ['FI','FA','FO']}
    assert macros==dict(FI=2,FA=0,FO=0)
    menu=d['typed_choice_or_actor_style_commands'];assert len(menu)==1 and menu[0]['word']==0x2100
    assert menu[0]['offset']==880 and menu[0]['whole_command_hex']=='002100000600948382a40000948382ed82c882a20000'
    options=[dict(index=i,Japanese=t,source_hex=t.encode('cp932').hex(),fresh_source_gloss=g) for i,(t,g) in enumerate([('買う','Buy'),('買わない','Do not buy')])]
    rows=[]
    for r in d['records']:
        row=deepcopy(r);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all24_clean_rigging_price_negotiation_purchase_refusal_and_three_stat_glosses.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=201,records=rows,
        source_stored_bytes=1452,source_logical_end=end,source_tailzeros=0,source_commands=44,
        progressive_speeches=21,distinct_FE_stat_notifications=3,source_macros=macros,typed_two_option2100=options,
        source_selector_counts={'105':8,'2':4,'19':9,'254':3},
        whole_exchange_progression='69 says existing mast rope is worn;02 doubts replacement is needed.69 promotes a replacement with reported mysterious power.02 cheekily asks for it free.69 rejects that and asks300000.13 intervenes and counters30000. The seller counters200000,13 offers50000,the seller150000,13 offers75000,and the seller finally100000.13 regards that as reasonable and asks02 to decide. Buy:13 handles arrangements,02 agrees,the rope is requested at the deck,the seller thanks them,FI Charm+1 and Carlo Intelligence+1 appear. Do not buy:02 says current rope still works and replacement need not be rushed,13 declines,the seller complains about unserious browsing,13 apologizes,and FI Spirit+1 appears. No affordability predicate appears in this structural inventory;effect meanings and actual branch/menu flow still need independent native evidence.',
        seller_asks_and_counteroffers=[300000,30000,200000,50000,150000,75000,100000],
        mysterious_power_is_reported_not_a_specific_item_effect_or_title=True,
        source_free_request_is_a_question_not_an_earlier_promise=True,
        familiar_vendor_address_oyaji_not_a_proven_father_relation=True,
        three_distinct_system_notices_preserve_runtime_player_or_named_Carlo_recipient_and_stat=True,
        native_actor_names_voices_stat_terms_item_card_controls_payment_and_menu_paths_pending=True,
        prior_English_speech_unread=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B20124 clean-first glosses:complete rigging haggling300000 to100000,buy/refuse and three distinct stat notices. Two original FI macros;one2100 menu;no priorEnglish or credit.')
