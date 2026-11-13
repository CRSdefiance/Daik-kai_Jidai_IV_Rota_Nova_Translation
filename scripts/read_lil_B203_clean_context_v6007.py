"""Read the entire clean cordyceps/book negotiation before older English."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_clean_context_v6007')
SOURCE=Path('work/analysis/lil_B203_clean_inventory_v6006/all_clean_B203_speeches_before_predecessor_comparison.json')
GLOSSES={
5:('What on earth is this?!','4C reacts with surprise or alarm to an unidentified thing. The archaic colloquial じゃ voice must be bound to the actual actor; do not borrow a previous old speaker or invent a rank.'),
9:('What is wrong?','02 asks about the reaction. Keep this first inquiry distinct from her later questions about the specimen and the offered object.'),
13:('This, here!','4C points to the thing causing the reaction. The object remains unnamed; no specific book or disease is introduced here.'),
17:('...Is there a bug in it?','02 tentatively asks about an insect. Preserve the question and uncertainty; the text does not establish an infestation or contaminated food.'),
21:('But there is something like strange grass growing on it.','4C adds an observation that complicates the insect identification. Keep the apparent grass growth and colloquial older voice without adding a biological explanation absent from the exchange.'),
24:('You are right.','02 confirms the visual observation, not a diagnosis or an identification already known to her.'),
28:('That is something called cordyceps.','AA names 冬虫夏草. Keep the culturally specific substance; bind its display terminology independently before final prose. No source speaker has yet identified a book or named an item title.'),
31:('!?','4C reacts with startled surprise to AA identifying it. Preserve this separate nonverbal beat and its assigned speaker.'),
35:('In China, it is highly valued as medicine.','AA explains the substance in a Chinese medicinal context. Preserve this character statement and the China reference without adding modern medical advice, proven efficacy, rarity or a specific cure.'),
38:('This is medicine?','02 is surprised that the strange specimen has a medicinal use. Keep the questioning response rather than treating her as already knowledgeable.'),
42:('Hmm, medicine, you say...','4C becomes interested in the medicinal angle. This prepares the later interest in reading; do not add a profession, secret motive or plan to manufacture a remedy.'),
46:('That is right. Here, I will give you this.','AA confirms and offers something. The demonstrative does not itself identify or name the offered object. Preserve the offer as a gift, separate from the later negotiated payment.'),
50:('What is this?','02 asks about the newly offered thing. Do not collapse this with the earlier specimen question or insert a title before AA explains it.'),
54:('It contains various writings about materials that can be used as medicine.','AA describes a reference work about medicinal materials. The source has no explicit title in this speech. Bind any actual picture, catalog name and item identity separately; do not call it a recipe, guaranteed cure or cordyceps itself.'),
57:('Is it all right for me to accept something that looks so expensive?','02 is reluctant to take a valuable-looking gift. Preserve apparent expense and her concern; no exact market value or prior debt is stated.'),
60:('I no longer need it, so I will give it to you.','AA reassures her with a personal reason. Preserve that AA no longer needs the object; do not invent retirement, inheritance, a relationship, permanent loss of ability or a hidden obligation.'),
63:('But...','02 hesitates. Keep the unfinished objection without supplying a moral explanation the source does not state.'),
67:('Ho ho ho. Your companion seems to want it.','AA gently teases while observing 4C interest. 連れ means a companion here, not a spouse, servant, apprentice, rank or newly established family relationship.'),
70:('Huh? No, well... I just wanted to have a look at that book.','4C is caught showing interest and admits wanting to read the book. Preserve the embarrassed denial/hesitation and modest reading request; do not turn it into a request to own it or explain why this speaker wants it.'),
74:('I know. Please let me have it for 1,000 gold.','02 proposes paying instead of taking it free. Preserve the initiative, 1,000 amount and request. This is spoken negotiation, not proof that the engine deducts that sum.'),
77:('Ho ho ho. In that case, 100 gold will do.','AA counters with a much lower 100, retaining the amused generous tone. Keep the factor-of-ten difference; do not silently normalize it to 1,000 or invent a reason for the discount.'),
80:('FI charm has increased by 1!','FE is a system notice, not AA or 4C speech. Preserve runtime FI and the stated charm increase of exactly one. Native notice consumer, substitution and the underlying effect commands remain to be verified independently.')}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',b,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==22 and len(d['commands'])==31 and len(b)==816 and end==814 and b[end:]==bytes(2)
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']} and Counter(r['source_selector'] for r in d['records'])=={76:6,2:8,170:7,254:1}
    assert d['typed_choice_or_actor_style_commands']==[]
    macros={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in d['records']) for m in ['FI','FA','FO']};assert macros=={'FI':1,'FA':0,'FO':0}
    rows=[]
    for r in d['records']:
        row=deepcopy(r);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'all22_clean_cordyceps_book_offer_and1000_to100_negotiation_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=203,records=rows,source_stored_bytes=816,source_logical_end=814,source_tailzeros=2,source_commands=31,source_selector_counts={'76':6,'2':8,'170':7,'254':1},source_macros=macros,
        whole_exchange_progression='4C is surprised by a specimen;02 asks what is wrong. They notice an insect with apparent grass growing on it. AA identifies cordyceps and says it is valued as medicine in China.02 is surprised and4C becomes interested. AA offers an object and describes writings about medicinal materials.02 hesitates to accept something valuable;AA says it is no longer needed. AA teases that02 companion wants it;4C awkwardly admits wanting to read the book.02 proposes paying1000 gold;AA laughingly accepts100 instead. A separate FE/FI notice states charm increased by1.',
        exact_explicit_source_substance='冬虫夏草',substance_gloss_not_final_widget_or_item_title='cordyceps',source_does_not_speak_an_explicit_book_title=True,
        source_speakers_4C_AA_not_inherited_from_B202=True,source_names_roles_voices_relationships_and_name_consumers_unbound=True,
        no_invented_profession_kinship_rank_ownership_provenance_or_guaranteed_medical_item_effect=True,
        source21_progressive_speeches_one_FE_FI_notice_zero_FA_FO_choices_or_typed_styles=True,
        nine_non_speech_commands_preserved_not_interpreted_as_full_payment_effect_or_event_semantics=True,
        non_speech_source_offsets=[334,738,740,742,778,786,794,802,810],complete_end_word_offset=810,
        actual_source_activation_paths_native_names_voices_item_identity_widget_payment_and_effects_pending=True,
        no_source_prose_editorial_gates_or_completion_credit_yet=True,prior_English_speech_unread=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B20322 clean-first glosses:cordyceps,medicinal-material reference book,gift hesitation,companion interest,1000-to100 negotiation,and FE/FI charm+1. Names/item/effects unbound;no older English or credit.')
