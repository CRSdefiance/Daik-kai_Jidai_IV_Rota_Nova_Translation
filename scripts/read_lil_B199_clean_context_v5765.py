"""Fresh clean-first whole-exchange glosses for the portrait,chase and misunderstood book gift."""
from copy import deepcopy
from collections import Counter
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_clean_context_v5765')
SOURCE=Path('work/analysis/lil_B199_clean_inventory_v5764/all_clean_B199_speeches_before_predecessor_comparison.json')
GLOSSES={
 5:('By the way,who is the man in this portrait?', 'Speaker16 asks09 about the depicted adult man. おじさん is a familiar adult-male reference here,not evidence of an uncle or other kinship. Do not add painter,owner,rank or a historically corrected identity.'),
 9:('That is a man named ロッコ＝アレムケル.', '09 gives the depicted man\'s explicit name. Bind the approved full spelling from the game\'s clean/current name fields before localized prose;do not invent a title or a relationship to the party.'),
 12:('Hmm. Is he famous?', '16 follows the identification with casual curiosity. Keep this question about reputation,not admiration,recognition or a claim that16 already knows him.'),
 16:('Yes. I would say he is fairly well known among 航海士.', '09 gives a qualified assessment among seafaring/navigation professionals. Preserve かな and なかなか rather than declaring universal fame or assigning an Admiral rank. Bind the approved contextual crew term.'),
 19:('What are you two whispering about in front of a picture of a man like that?! I am going on ahead!', '02 interrupts the two-speaker conversation,annoyed at being left waiting. そんなおじさん is a dismissive familiar reference,not a relative. Preserve the threat to move ahead without inventing jealousy,a romantic triangle or an unseen argument.'),
 23:('Sorry. I am coming now.', '09 apologizes and promises to follow. This responds to02\'s impatience;it is not the later apology about tidying or the supposed gift.'),
 27:('Yeah. I will be right there,fatty!', '16 teases02 with the explicit body-size insult おでぶ. Keep the source comic provocation without erasing it,escalating to sexual/protected-class abuse or making the narrator certify02\'s physique. Do not invent a nickname history or a family bond.'),
 31:('Samwell! I will knock you flying!!', '02 explicitly names Samwell and threatens cartoonish retaliation in response to the insult. Bind the selector/name relationship rather than inheriting it. No weapon,severe injury,death or real-world instruction is added.'),
 34:('GANG! CRASH! CLATTER! CLUNK!', 'FE supplies four successive impact/clatter onomatopoeia. These are sound-effect text,not a stat notice or a named speaker. Preserve four beats without specifying which objects break,what is thrown or whether anyone is injured.'),
 37:('FI! Do not throw things! Ow!', '09 calls the runtime FI name,tells that person not to throw objects,and reacts to being struck or pained. Preserve the exact FI substitution and ow beat. Do not replace FI with fixed Lil,add an injury or say Samwell threw the objects.'),
 40:('Where are you throwing that? I am over here!', '16 taunts the thrower about missing him. Preserve his teasing evasion without adding a weapon,a hit or an invitation to injure anyone. This follows09\'s complaint and keeps the source comic escalation.'),
 43:('Come back here!!', '02 pursues or calls after the evasive16 with an elongated emphatic wait. Preserve the emotional peak without adding a new destination or capture.'),
 47:('Sigh. I am always the one who has to clean up.', '09\'s weary aside follows the chase. It is the scene\'s transition toward discovering the book. Preserve the recurring grievance as his own observation,not proof of employment,servitude or a household arrangement.'),
 50:('Hm! What is this?', '09 notices something while dealing with the aftermath. Keep the deictic question and surprise. Do not identify the object before his next line or add a precise discovery location.'),
 54:('This book looks very old.', '09 explicitly identifies an apparently old book. Keep the appearance judgment,not a proven date,author,title,ownership or magical property.'),
 58:('Camille! What are you doing? Come on!', '02 returns or calls09 onward,explicitly using Camille\'s name. The exact native actor binding remains to be checked. Preserve her brisk summons;do not turn it into a romantic address or an order based on an invented rank.'),
 62:('Oh,where is Samwell?', '09 asks about the person02 had been chasing. Keep the whereabouts question and mild surprise. No actual hiding place,departure or injury is established.'),
 66:('I do not know anything about that jerk!', '02 gives an irritated dismissive answer about Samwell. In context 知らない is not denial of ever knowing him or a literal breakup. Preserve the huff without inventing a new relationship or a completed punishment.'),
 70:('(He got away from her again. Samwell is quick on his feet.)', '09\'s private parenthetical thought links the answer to the preceding chase. Preserve another successful escape and Samwell\'s agility as his reflection. Do not make this audible to02 or invent cowardice,combat skill or a romantic escape.'),
 73:('What?!', '02 challenges09\'s visible reaction or perceived amusement. Preserve the sharp response without claiming she heard the private thought.'),
 77:('N-nothing.', '09 stammers while denying that anything is wrong or being said. Keep the nervous contrast with his earlier composed explanation;do not add a confession or a second speaker.'),
 81:('Hmph! Stop grinning!', '02 objects to09\'s expression. Preserve the stated visible amusement without assigning its cause to romance or adding an insult.'),
 84:('S-sorry. Oh,right,this...', '09 apologizes and redirects attention to the object he found. The deictic introduction is interrupted or trailing;do not say he chose,bought,wrapped or intended a present.'),
 88:('What is this? A present?', '02 proposes the gift interpretation as a question. It has not been offered as a gift by09. Preserve the misunderstanding instead of silently confirming the premise.'),
 91:('N-no,that is not what...', '09 immediately tries to deny or correct the gift interpretation. Keep the stammer and unfinished correction;he does not reject02 or express dislike.'),
 95:('It looks rather old,but it is unusual for you to give me a present,Camille!', '02 continues under her gift interpretation despite the attempted correction. Preserve her own statement about an unusual gift and the apparent age. Do not make the narrator or09 confirm prior romance,rare affection,ownership or a deliberate gift purchase.'),
 99:('That is not what...', '09 again tries to correct the same misunderstanding. This repetition is deliberate dialogue progression,not duplicated prose to delete. Do not turn it into a new explanation that02 actually hears.'),
 103:('Thank you.', '02 warmly thanks09 while still treating the object as a present. The tone changes from irritation to appreciation;preserve that turn without adding love,a promise or an established partnership.'),
 107:('Ah...yeah.', '09 gives a hesitant acknowledgment after his failed attempts to correct her. Preserve the awkward acceptance without retroactively turning the discovery into his planned present.'),
 111:('Let us go!', '02 resumes the forward movement with a brisk,inclusive invitation. Preserve its energy without adding a destination,command hierarchy or new event.'),
 115:('(Is this really all right...?)', '09 ends with a private,uncertain thought about the unresolved gift misunderstanding. Keep the question and parentheses;do not resolve the ownership,romance,item identity or moral issue for him.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);block=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',block,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==31 and len(d['commands'])==47
    assert len(block)==1168 and end==1166 and block[end:]==bytes(2) and not d['typed_choice_or_actor_style_commands']
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    assert Counter(r['source_selector'] for r in d['records'])=={22:4,9:15,2:11,254:1}
    macros={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in d['records']) for m in ['FI','FA','FO']}
    assert macros=={'FI':1,'FA':0,'FO':0}
    rows=[]
    for r in d['records']:
        row=deepcopy(r);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all31_clean_portrait_chase_found_book_and_misunderstood_gift_glosses.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=199,records=rows,
        source_stored_bytes=1168,source_logical_end=1166,source_tailzeros=2,source_commands=47,
        progressive_speeches=30,FE_sound_effect_objects=1,source_macros=macros,
        whole_exchange_progression='Two speakers discuss the identity and reputation of a man in a portrait.02 impatiently calls them onward.16 answers with a body-size taunt;02 names Samwell and threatens retaliation. Four FE impact sounds,09\'s FI-addressed plea to stop throwing objects and16\'s evasive taunt lead into02\'s chase.09 complains about always cleaning up and notices an apparently old book.02 calls Camille onward;09 asks about Samwell,receives an irritated answer and privately concludes that the quick Samwell escaped again.02 challenges09\'s grin;his apology and trailing introduction of the found object are mistaken for a gift. He twice tries to correct that interpretation.02 appreciates the unusual present,thanks him and moves on;09 remains privately uncertain.',
        parenthetical_thought_source_indices=[70,115],source_sound_effect_index=34,
        native_actor_names_voice_classes_portrait_identity_terms_controls_pause_and_object_card_pending=True,
        source_unplanned_found_object_not_a_planned_romantic_gift=True,
        source_ojisan_not_uncle_and_explicit_body_size_tease_not_narrator_fact=True,
        native_FI_not_replaced_with_fixed_Lil=True,
        prior_English_speech_unread=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B19931 clean-first glosses:portrait,reputation,teasing/chase,four sound beats,found old book and unresolved gift misunderstanding. One FI,two private thoughts;native identity/control/object context pending. No old English or credit.')
