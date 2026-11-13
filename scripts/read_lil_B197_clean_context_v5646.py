"""Read the whole clean book-seller exchange before any earlier English prose."""
import struct
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_clean_context_v5646')
SOURCE=Path('work/analysis/lil_B197_clean_inventory_v5645/all_clean_B197_speeches_before_predecessor_comparison.json')
GLOSSES={
 5:('Hey,you handsome fellow over there.','A9 addresses15 with a familiar,flirtatious compliment. Bind original actor names/roles/voices before gendering or naming the seller. 色男 is a handsome/charming man in this address,not a new profession or relationship.'),
 9:('Do you mean me?','15 checks whether the seller is addressing them. Keep the question and measured first-person voice;bind the original actor rather than the player captain.'),
 14:('Would you buy this book for8500 in money?','The seller offers one book for the exact asking amount8500. Bind the approved money term,original menu and financial/effect controls. This is an offer,not proof of a paid sale,affordability or item identity.'),
 17:('What kind of book is it?','15 asks about the book content before deciding. Do not imply that the book has already been opened,bought or read.'),
 21:('It is an Indian classic about the love between a celestial maiden and a sage or hermit. How about it?','Preserve India,classical literature and the specific otherworldly maiden/ascetic love story. 天女 and仙人 require culturally respectful English. Do not invent a title,author,Sanskrit name,religion,canon,nationality for the seller or a Western angel/wizard identity. The seller describes the book;later dialogue questions whether the seller is a celestial maiden without confirming it.'),
 24:('Admiral,what should we do?','15 explicitly addresses提督 and asks for a decision. Preserve the source title here without inventing kinship,rank or employment elsewhere. The following original2200 three-label menu must determine the actual response paths.'),
 45:('I will take it.','15 accepts on this branch. Preserve polite,composed acceptance;do not invent a gift recipient,prior agreement or separate price.'),
 49:('I hope you get to fall in love with a celestial maiden too.','The seller makes a teasing,wish-like connection to the book romance. Theも matters. This is a personal hope,not a guaranteed encounter or already established romance.'),
 53:('Unfortunately,I am not interested.','15 gives a courteous lack-of-interest refusal on this branch. Do not replace it with lack of money or an accusation of poor book quality.'),
 57:('Oh,my. What a waste,when you are such a handsome man.','The seller responds with playful disappointment and another compliment. Preserve the teasing connection to interest/romance,without inventing age,availability,a relationship or objective loss.'),
 64:('No,I will pass.','15 politely declines on a separate branch. Keep this distinct from the explicit lack-of-interest refusal and the later inability-to-afford explanation.'),
 68:('I see. That is a shame. I will find someone else to buy it.','The seller is disappointed and intends to sell to another person. No second customer or completed other sale is present.'),
 74:('I would like to buy it,but I do not have that much money.','15 expresses willingness but inability to afford the large sum. Preserve both desire and financial limitation. Bind native source conditions and whose funds are consulted;do not infer debt,poverty,a demand for charity or a deception.'),
 77:('I see.','The seller acknowledges the explanation without an added insult,pitying diagnosis or new question.'),
 81:('I am sorry I cannot meet your expectations.','15 gives a formal,considerate apology after the seller acknowledgment. Keep the personal courtesy rather than inventing a promise,prior relationship or payment commitment.'),
 85:('Then I will give it to you.','The seller offers the book as a gift. Distinguish this from a paid purchase and future sale elsewhere. Item acquisition and eligibility still require original control proof.'),
 89:('What!?','15 reacts with surprise to the offered gift. Preserve the short exclamation and emotional turn rather than adding an explanation or protest.'),
 93:('Heh heh... Next time,I would like to fall in love with a man like you.','The seller laughs softly and expresses a wish about a future romance with someone like15. Keep今度は,the hypothetical wish and男. Do not declare an existing romance,marriage,kinship,a reincarnation backstory or a confirmed supernatural identity.'),
 97:('S-she or they vanished...','15 stammers and reacts to the disappearance. Japanese omits the subject;bind original seller role and surrounding context before choosing English pronouns. Do not add a flash,spell,death or transport destination.'),
 101:('Could that have been a celestial maiden...? Heh... What a foolish thought.','15 entertains a tentative supernatural explanation,then dismisses the thought. Preserve the question/doubt,self-directed dismissal and restrained laugh. Do not certify that the seller was a celestial maiden,make the whole exchange a dream or turn the final self-reproach into an insult at someone else.'),
 109:('Ian\'s Charm increased by1!','FE explicitly namesイアン and魅力 plus one;there is no FI token. Bind the original actor name and approved stat label,branch ownership and null-actor FE pipeline. Do not substitute the captain or claim every purchase/refusal grants the point.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);block=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',block,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==21 and len(d['commands'])==39
    assert len(block)==880 and end==878 and block[end:]==bytes(2)
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    assert {r['source_selector'] for r in d['records']}=={169,21,254}
    assert not any(m in bytes.fromhex(r['source_hex']) for r in d['records'] for m in [b'FI',b'FA',b'FO'])
    menu=deepcopy(d['typed_choice_or_actor_style_commands']);assert len(menu)==1 and menu[0]['word']==0x2200 and menu[0]['offset']==230
    raw=bytes.fromhex(menu[0]['whole_command_hex']);assert struct.unpack_from('<4H',raw)==(0x2200,0,8,18)
    labels=[v.decode('cp932') for v in raw[8:].split(b'\0') if v];assert labels==['買う','買わない','断る']
    menu[0].update(source_labels=labels,fresh_literal_glosses=['Buy','Do not buy','Decline'],source_three_options_not_collapsed_to_two=True,
        exact_visible_options_selection_cancellation_and_branch_funds_contract_pending=True)
    rows=[]
    for r in d['records']:
        row=deepcopy(r);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(row)
    counts=Counter(format(c['word'],'04X') for c in d['commands'])
    ROOT.mkdir(parents=True);save(ROOT/'all21_clean_exchange_three_labels_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=197,records=rows,choices=menu,physical_speech_objects=21,physical_choice_objects=1,choice_labels=3,
        source_commands=39,source_command_counts=dict(counts),source_stored_bytes=880,source_logical_end=878,source_alignment_tailzeros=2,
        source_selectors_decimal=[169,21,254],source_FI_macros=0,source_FA_macros=0,source_FO_macros=0,source_asking_amount=8500,
        complete_exchange_progression='A9 calls15 handsome and offers a book for8500.15 asks what kind;A9 describes an Indian classic about a celestial maiden and an ascetic lover.15 asks the Admiral to decide. The original three-label menu leads to distinct acceptance and teasing wish,lack-of-interest refusal and playful disappointment,polite decline and future sale elsewhere,and an inability-to-afford exchange culminating in an unexpected gift,flirtatious wish,disappearance,tentative celestial-maiden speculation and self-directed dismissal. A separate FE explicitly names Ian and Charm plus one. Native control mapping must establish exact menu/result/funds path relationships and the final notice ownership.',
        source_fact_boundaries=['Preserve India and the literary/cultural celestial-maiden/ascetic context without inventing a title,author,religion,canon or Western angel/wizard equivalence.',
            'The seller explicitly compliments a man and wishes for a future romance with a man like the listener. Bind original actors/roles/voices before choosing names or seller pronouns. No established romance,kinship,marriage,employment or reincarnation history is supplied.',
            'The later celestial-maiden identity is a character question followed by self-dismissal. The disappearance is reported in dialogue;its visuals and mechanism need actual observation. Do not certify supernatural identity or a dream.',
            'Preserve exact8500 offer and original three labels/indices. Do not collapse Buy/Do-not-buy/Decline or infer affordability,gifting or conditional branch relationships from prose alone.',
            'Keep polite lack of interest,polite declining,willingness-but-inability-to-afford,considerate apology,gift,surprise,soft teasing wish,stammer and doubtful self-reproach as a complete emotional progression.',
            'The final FE explicitly names Ian and Charm plus one without FI. Bind its source branch,actor name/stat and native modal path;do not apply it to all outcomes.',
            'Source880/878 bytes plus two tailzeros contains39 commands,one2200 menu,three0100 containers plus0200/0300/0400,five A000 effects,4821,4720,4735,6003,632E and one final end. Do not inherit B196 six2100 menus/seven ends or earlier linear shape.'],
        read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B197 clean-only:21 speech glosses/three literal labels,Indian classic/celestial-maiden context,8500 offer,gift and doubtful disappearance.39 commands;2200 and funds/effect branches pending.No prior English or credit.')
