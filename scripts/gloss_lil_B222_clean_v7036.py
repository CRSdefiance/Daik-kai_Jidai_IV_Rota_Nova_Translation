"""Read/gloss the entire clean sunset/Noritsune exchange before predecessor English."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_clean_context_v7036')
SOURCE=Path('work/analysis/lil_B222_clean_inventory_v6964/all_clean_B222_speeches_before_predecessor_comparison.json')
CONTEXT='''Actor16 is silently watching the sunset. Lil notices,addresses him by his source given nameゲルハルト and casually asks what is wrong. He respectfully addresses his fleet leader as提督 and admits that a story he heard here in Japan has moved him,unusually for him. Lil asks whether she knows the man. He places the military commander Noritsune hundreds of years in the past. Lil asks what made him remarkable. He tells the whole decline of an unnamed formerly glorious clan through repeated defeats,contrasts Noritsune's courage with his unflattering judgment of the other clansmen,reports seven ships crossed in the final naval battle toward the enemy commander's vessel,and then the exhausted man's disappearance into the strait with two enemy soldiers under his arms and his gleaming armor. The numbers,uncertain report markers and the strait/armor wording matter. He then expresses his own admiration using a dated East/West generalization;this remains his viewpoint rather than objective narrator history or an innate trait of a people. Lil broadens the thought to extraordinary heroes in every country. He agrees that an island nation should not be underestimated. Lil laughs and teases his soft spot for such stories;only the following parenthesized assessment of his frightening appearance and pure heart is explicitly private. She then quietly repeats the strait and splendid armor details. This is an implied armor/treasure lead,not an explicit plan to steal,recover,equip or acquire it. He catches himself for talking at length and proposes returning to work. Preserve the movement from silence and unexpected emotion through martial admiration to friendly teasing and Lil's reflective armor interest. Neither an invented romance nor ridicule of his sincerity belongs in the exchange.'''
GLOSSES={
5:('A silent pause: two Japanese ellipsis marks.','Reticence at the sunset;do not invent tears,a spoken word or a timed pause length.'),
9:('Oh,ゲルハルト? What is the matter,standing there looking at the sunset like that?','Lil notices an unusual quiet moment and asks casually;no romantic invitation or illness is stated.'),
13:('提督... I heard a story about a certain man here in Japan,and,quite unlike me,it seems to have stirred me deeply...','Respectful fleet-leader address and self-conscious emotion.提督 is the source word;the final address must follow approved project usage without inventing a commissioned naval rank.胸が熱くなる describes being moved,not fever or romantic attraction.'),
17:('Hmm. Is he someone I know too?','An ordinary curious question before she learns he lived centuries earlier.'),
20:('He was a military commander hundreds of years ago. The man\'s name is Noritsune.','武将 supports military commander/warrior,not a newly invented court or naval rank. Keep the given nameノリツネ without adding a surname,clan,dates or outside biography.'),
23:('What was so remarkable about him?','Lil invites the explanation;do not make it a skeptical insult or declare a supernatural ability.'),
27:('He belonged to a clan that once enjoyed great glory. But it lost repeated battles against rival forces and was gradually driven toward annihilation.','Unnamed clan and rival forces. Preserve the progression of defeats;do not name a dynasty,family,enemy faction or historical war from external knowledge.'),
30:('Among his feeble clansmen,who were being cut down one after another,he alone stood against the enemy bravely...','軟弱 is the speaker\'s unflattering assessment. Preserve his contrast without adding cowardice,treachery,dishonor or a formal rank.'),
33:('They say that during the final naval battle,he leapt across seven ships toward the vessel carrying the enemy commander.','Explicitly reported tradition,exactly seven vessels. It does not state that he killed the commander,reached that vessel or crossed a measured distance.'),
37:('But at last his strength gave out. With two enemy soldiers held under his arms,he disappeared into the depths of the strait,gleaming armor and all—or so the story goes...','Exactly two soldiers,one under each arm,is supported by両脇. Preserve the tentative report marker. No deliberate-suicide motive,named strait,death method beyond the disappearance,or recovered armor is added.'),
40:('To think that a small country in the East could have produced a man with such nerve... I feel I have seen the very spirit of the people of the East.','A historically situated character\'s admiring but generalizing East/West viewpoint. Keep that characterization without endorsing it as narrator fact,adding a racial slur or intensifying it into biological claims.'),
44:('Every country has extraordinary heroes like that,doesn\'t it?','Lil broadens the conversation to heroes everywhere;she does not certify an ethnic trait or add a specific national stereotype.'),
47:('Yes. Even an island nation should not be underestimated.','Keep the respectful agreement and island-country comparison without adding backwater,primitive,exotic or other contempt not stated.'),
50:('Hehe... Soゲルハルト has a soft spot for stories like this. (He looks frightening,but he has a pure heart.)','The laugh and first observation are outside parentheses;the assessment in parentheses is private. This is affectionate teasing of his sensitivity,not an invented relationship,childishness or gullibility.'),
54:('...Into the strait... gleaming armor and all... hmm.','Reflective repetition with its armor-interest subtext. Do not turn the implication into an explicit diving plan,guaranteed find,coordinates,item stat or acquisition.'),
57:('How unlike me—I have gone on at length. Shall I/we get back to work?','Self-conscious recovery from a long emotional story. Japanese leaves the final subject implicit;natural final English must avoid inventing an order to the fleet leader or a new assigned job.')}
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);clean=Path(packet['source_ROM'])
    assert sha(clean.read_bytes())==packet['source_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image=NdsImage.open(clean);arm=image.read_file('/__arm9__.bin');block=bytes.fromhex(packet['clean_block_hex'])
    assert sha(arm)==packet['clean_ARM9_sha256'] and sha(block)==packet['clean_block_sha256']
    assert len(packet['records'])==16 and set(GLOSSES)=={r['source_record_index'] for r in packet['records']}
    rows=[]
    for record in packet['records']:
        row=deepcopy(record);at=row['offset'];raw=bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[at-5:at+1].hex()==row['complete_preamble_hex']
        assert raw[1:].decode('cp932')==row['Japanese']
        row.update(id=f'DK4_MES_B222_R{row["source_record_index"]:04d}',file_path='/data/SC2.DK4',block=222,
            source_reference=dict(block=222,offset=at,bytes=len(raw),record_index=row['source_record_index'],header_offset=at-5),
            fresh_source_gloss=GLOSSES[row['source_record_index']][0],whole_exchange_note=GLOSSES[row['source_record_index']][1],
            whole_exchange_context=CONTEXT,source_meaning_reviewed=True,predecessor_English_not_read=True,new_review_credit=0)
        rows.append(row)
    fields={}
    for ident in [2,16]:
        parts=[]
        for column in [0,4,8]:
            field=0x120B80+ident*32+column;p=struct.unpack_from('<I',arm,field)[0]
            if not p:parts.append(dict(column=column,pointer_field=field,source_null=True));continue
            at=p-0x02000000;end=arm.index(0,at);value=arm[at:end+1]
            parts.append(dict(column=column,pointer_field=field,source_pointer=p,source_storage_offset=at,source_terminated_hex=value.hex(),Japanese=value[:-1].decode('cp932')))
        fields[str(ident)]=parts
    ROOT.mkdir(parents=True);save(ROOT/'all16_clean_sunset_Noritsune_armor_glosses_before_old_English.json',dict(source_inventory=str(SOURCE),source_inventory_sha256=sha(SOURCE.read_bytes()),
        source_ROM=str(clean),source_ROM_sha256=packet['source_ROM_sha256'],file_path='/data/SC2.DK4',block=222,clean_block_sha256=sha(block),
        records=rows,clean_actor_name_fields=fields,whole_exchange_context=CONTEXT,
        all16_clean_speeches_glossed_together_before_old_English=True,exact_seven_vessels_two_soldiers_unnamed_clan_strait_hearsay_and_private_parentheses_preserved=True,
        no_outside_history_rank_relationship_named_strait_clan_date_find_or_stat_invented=True,
        East_West_and_clansman_judgments_remain_character_viewpoints=True,
        predecessor_current_consumers_name_localization_controls_native_actual_and_registered_release_pending=True,
        source_A000_and_full_normal_end_recorded_not_effect_semantics_or_natural_activation=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sixteen B222 clean-Japanese glosses complete before predecessor English;all broader contextual/native/release gates remain pending.No completion credit.',flush=True)
