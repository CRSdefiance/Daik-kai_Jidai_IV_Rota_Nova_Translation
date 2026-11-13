"""Read the complete letter, reactions and automatic notices before predecessor English."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B214_complete_clean_v6694/all17_clean_objects_ten_speeches_seven_voice_bodies_eight_slots.json')
ROOT=Path('work/analysis/lil_B214_clean_context_v6695')
SPEECH={
34:('Admiral, I am writing to you from a road leading to Rome.','The letter addresses 提督 and locates its writer on a road leading to Rome. Do not assert that he is already in Rome, name a particular road or add a military rank beyond established terminology.'),
38:('Walking along this road, one inevitably hears stories of the missionaries of long ago who overcame many persecutions as they worked to spread their faith.','伝道師たち, 数々の迫害 and 布教 support missionaries, repeated persecution and evangelizing. This is the writer recounting what he hears, with いやおうなしにも suggesting that these stories are hard to avoid; do not turn it into hostility toward believers or an independently verified history lesson.'),
41:('I have no interest in matters of faith, but I did hear one intriguing story.','The contrast explains why a nonreligious topic seeker passes along the clue. Preserve lack of interest without adding contempt, a declared religious identity or a new personal history.'),
44:('Apparently, a sword once owned by Judas, one of Jesus\'s twelve disciples, still lies somewhere associated with him.','The source supplies Jesus, twelve disciples, Judas, the sword\'s former ownership and a vague place connected with Judas. Preserve the hearsay and indefinite location. Do not add a named site, country, burial, Biblical episode, historical authentication or certain present possession.'),
48:('Because Judas betrayed Jesus, people find the sword unsettling simply because he owned it, and no one is willing to seek it out.','Keep the causal connection between betrayal, former ownership and people\'s aversion. The fear is attributed to people; do not assert an actual curse or a property of the sword. 手に入れようとしません means they do not try to acquire it, not that acquisition is technically impossible.'),
51:('I hear, however, that the sword has a keen edge and is very finely made. The sword itself bears no guilt, and I think it would be worth looking for.','The writer separates an object from its former owner\'s wrongdoing. Preserve hearsay about sharpness/quality and a reasoned recommendation rather than a guarantee, reward, inventory transfer or attack-stat claim.'),
62:('Still, the devout Manuel would probably be uncomfortable hearing this story.','信心深い explicitly describes Manuel as devout, and 嫌がりそう is the writer\'s expectation, not a confirmed refusal. The next stored reply softens this expectation. Do not invent a clerical office, nationality, kinship or hostility.'),
68:('I will write again if I learn anything else. Signed: ジェナス・パサー.','Polite letter closing promises contact if there is further news, not a fixed date or certain new discovery. Preserve the full signature identity; exact current surname/first-name spelling and consumer review remain pending. Source blank line and long indentation are letter staging, to review under its actual consumer rather than mechanically copying whitespace.'),
75:('Huh, Judas\'s sword. It is just like ジェナス not to judge it unfairly merely because it belonged to a traitor.','Lil is conversational and recognizes the writer\'s characteristic open-mindedness. 色眼鏡で見ない is not literally colored glasses. Preserve her amused familiarity without inventing a relationship or implying that she approves of betrayal.'),
87:('...Well, I am not absolutely opposed, either. Judas did repent in the end, after all. I will leave it to you, Admiral.','The speaker qualifies opposition and defers the decision. Preserve his own statement about repentance as character dialogue, without adding theological judgment, a church office, doctrine or historical correction. Do not turn this into enthusiastic endorsement. Its native conditional path is not yet proven; do not assume every stored response and all style variants play in one linear sequence.')}
INTRO={
20:('Admiral, a letter from ジェナス has arrived.','Neutral polite delivery notice.'),
60:('Admiral, a missive from ジェナス has arrived.','書簡 and 届いております give a more formal manner; preserve natural formality rather than Japanese syntax.'),
102:('Admiral, a letter has arrived from ジェナス.','Conversational polite notice ending よ. Styles 2 and 7 share one stored body; preserve the alias and count the physical object once.'),
140:('Admiral, a letter for you from ジェナス.','お手紙です is a courteous concise announcement, without a new relationship or literal honorific.'),
170:('Admiral, a letter from ジェナス has arrived.','Rougher confident ますぜ voice, without invented pirate dialect or nationality.'),
208:('Admiral, a letter from ジェナス has arrived.','届いておる distinguishes the register, without proving the dynamically selected speaker\'s age or biography.'),
244:('Admiral! A letter from ジェナス!','Drawn-out ていとくー and simple friendly ending give an excited accessible delivery. Preserve enthusiasm without misspelling names or inventing a child relationship.')}
WHOLE='''One automatic crew notice announces a letter from ジェナス; eight style slots select seven distinct stored notices, with styles 2/7 aliased. These are not player choices. Eight consecutive actor4 speeches form a letter written from a road leading to Rome: unavoidable missionary stories lead the writer, despite his lack of interest in faith, to a rumor about Judas\'s finely made sword. People shun it because of its former owner; the writer argues that the sword itself is not guilty and recommends looking for it. He anticipates devout Manuel\'s discomfort and closes with a full signature. Lil warmly recognizes his refusal to judge the object by its owner. A stored actor23 reply qualifies opposition, mentions Judas\'s repentance and leaves the decision to the admiral. Preserve the movement from report through practical reasoning to a respectful qualification. Read the religious references as the characters\' source statements, without expanding or silently correcting doctrine/history. No exact site, magic, acquisition, reward, date, new relationship or clerical/military rank is supplied. Native control paths, dynamic D0 speakers, voices, names, signature layout, current effective English, full consumers and actual coverage remain pending.'''
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);assert d['prior_English_unread'] and d['total_editorial_objects']==17
    image=NdsImage.open(d['source_ROM']);arm=image.read_file('/__arm9__.bin');names=[]
    for ident in [2,4,23]:
        fields=[]
        for delta in [0,4,8]:
            field=TABLE+ident*32+delta;pointer=struct.unpack_from('<I',arm,field)[0]
            if not pointer:fields.append(dict(field_offset=field,column=delta,source_null=True));continue
            raw=cstring(arm,pointer-BASE);fields.append(dict(field_offset=field,column=delta,pointer=pointer,source_storage_offset=pointer-BASE,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
        names.append(dict(actor_ID=ident,clean_fields=fields))
    rows=[]
    for r in d['records']+d['typed_actor_style_records']:
        r=deepcopy(r);gloss,note=SPEECH[r['source_record_index']] if r['kind']=='progressive' else INTRO[r['source_reference']['offset']-r['command_offset']]
        r.update(fresh_source_gloss=gloss,whole_exchange_note=note,whole_exchange_context=WHOLE,source_meaning_reviewed=True,current_English_not_read=True,source_prose_or_completion_credit_added=0);rows.append(r)
    assert len(rows)==17 and len({r['id'] for r in rows})==17
    ROOT.mkdir(parents=True);save(ROOT/'all17_clean_letter_reaction_and_notice_glosses_before_old_English.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),whole_exchange_context=WHOLE,records=rows,source_actor_name_fields=names,source_commands=27,source_progressive_speeches=10,source_typed_commands=1,source_typed_stored_alternatives=7,source_style_slots=8,source_typed_D0_selectors=[208],all17_clean_objects_read_before_prior_English=True,prior_English_unread=True,no_English_manuscript_or_wording_decisions_yet=True,all_source_context_prose_name_and_native_gates_pending=True,full_signature_source='ジェナス・パサー',signature_blank_line_indentation_and_native_consumer_pending=True,source_religious_statements_not_expanded_or_silently_corrected=True,no_current_English_or_historical_translation_consulted=True,new_review_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False))
    print('All17 clean objects glossed as one letter/reaction exchange; eight original style slots/seven bodies and full signature preserved. Older English unread; zero credit.')
