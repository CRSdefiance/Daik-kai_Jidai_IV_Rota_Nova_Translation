"""Read the complete clean exchange before any predecessor English comparison."""
from copy import deepcopy
from pathlib import Path
import struct
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B207_clean_inventory_v6335/all_clean_B207_speeches_before_predecessor_comparison.json')
ROOT=Path('work/analysis/lil_B207_clean_context_v6336')
GLOSSES={
5:("Admiraaal... There's a weapon I want.","Actor14 approaches Lil with an elongated,informal request. The written hiragana address explicitly means admiral;the drawn-out sounds convey an eager,pleading manner. Do not invent an age,lisp,kinship or a different military rank. The weapon has not yet been named or obtained."),
8:("Huh?","Lil's short surprised/questioning response invites clarification. It is not agreement to acquire anything."),
12:("You see,I want a weapon because I want to get stronger too.","He explains his personal wish to become stronger. Preserve the inclusive too and naive eagerness;do not turn this into a claim about an existing skill/stat increase or already owning the weapon."),
15:("You don't mean some food named Weapon,do you? ...I'm joking. So,what is that weapon's name?","Lil makes a food-related joke about the word weapon,then explicitly says she is joking and asks its name. Review the entire three-beat reply together. Do not replace the joke with unrelated sarcasm,an assertion that he is stupid,or a different requested food. The source's reassuring correction is part of her playful relationship with this companion,without proving family or romantic ties."),
19:("The Axe of the Minotaur!","He enthusiastically names the requested weapon:ミノタウロスの斧. Minotaur is the conventional English mythical name;the genitive relationship and axe must remain. Check the existing player-facing item/terminology consumers before choosing final English. Do not substitute an unrelated weapon or claim it has been acquired."),
23:("That's quite a name. It must be a hefty weapon. You seem to be the only one who could use something like that. So,where is it?","Lil reacts to the imposing name,infers a bulky/hefty weapon,and speculates that he alone seems able to use it,before asking its location. Preserve the conjectural language;this is character banter,not a mechanically proven exclusive-equipment restriction. Do not invent an attack value,known design,magical effect or established ownership."),
26:("Who knows... They say the Minotaur lived on this island long ago. That's all I know.","He does not know the weapon's location. He reports hearsay about the Minotaur's past presence on this island and admits that is his entire clue. The source says this island,not a named city/island. Do not add Crete,a labyrinth,cave,ruins,a coordinate,burial or a confirmed weapon location. Keep past tense and hearsay rather than treating the creature as currently present."),
30:("Hmm. Well,I'll look for it for you if I feel like it.","Lil gives a distinctly qualified,casual offer. If I feel like it is the condition on searching and must survive the later repetition. She does not promise a search,a successful find or a gift."),
33:("Hooray!","He immediately celebrates the tentative offer. This premature enthusiasm sets up Lil's correction;do not add a successful acquisition or interpret this as a quest reward notice."),
37:("I said,if I feel like it.","Lil repeats the exact qualification to check his overenthusiasm. Keep the callback recognizable and gently corrective rather than converting it to a firm refusal or an unconditional promise."),
41:("Still,hooray!","He continues celebrating despite the qualification. Preserve the contrast and cheerful stubbornness;do not make him say he ignored,failed to understand or rejected a different condition."),
45:("And I haven't decided that I'll give it to you,either.","Lil adds a second limit:even finding the weapon does not mean she has decided to hand it to him. Preserve her undecided stance;do not turn it into an absolute refusal,an assertion it already belongs to her,a sale,a price,a competition or a promise to keep it."),
48:("Aww...","His final drawn-out disappointed response completes the joke after the repeated celebrations. Do not invent a spoken argument,insult,whimpering action or narrator event.")}
CONTEXT="""Actor14,whose clean name fields areエミリオ/フェローグ,asks Lil for a weapon in an informal,drawn-out,eager voice. Lil first queries him,then playfully links his weapon request to food,explicitly says she is kidding,and asks its name. He namesミノタウロスの斧. Lil infers an imposing weapon and that he seems uniquely capable of using it,then asks where it is. His entire clue is hearsay that the Minotaur lived on this island long ago. She offers to search only if she feels like it. He celebrates;she repeats the condition;he celebrates anyway. She then warns that she has not decided to give it to him,and he ends disappointed. The exchange depends on his premature enthusiasm and her two separate qualifications,not on a guaranteed search,find,gift or acquisition. No explicit relationship,age,exclusive equipment mechanic,stat gain,price or named location is established. All13 progressive speeches and the following A000/complete end must be preserved."""
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);assert d['read_no_predecessor_English'] and len(d['records'])==13 and set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    source=Path(d['source_ROM']);assert sha(source.read_bytes())==d['source_ROM_sha256'];arm=NdsImage.open(source).read_file('/__arm9__.bin');names=[]
    for ident in [2,14]:
        fields=[]
        for delta in [0,4,8]:
            field=TABLE+ident*32+delta;pointer=struct.unpack_from('<I',arm,field)[0]
            if not pointer:fields.append(dict(field_offset=field,column=delta,source_null=True));continue
            value=cstring(arm,pointer-BASE);fields.append(dict(field_offset=field,column=delta,pointer=pointer,source_storage_offset=pointer-BASE,terminated_hex=value.hex(),Japanese=value[:-1].decode('cp932')))
        names.append(dict(actor_ID=ident,clean_fields=fields))
    rows=[]
    for r in d['records']:
        r=deepcopy(r);gloss,note=GLOSSES[r['source_record_index']];r.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(r)
    block=bytes.fromhex(d['clean_block_hex']);logical=8+struct.unpack_from('<H',block,4)[0]
    assert (len(block),logical)==(656,654) and block[654:]==bytes(2) and len(d['commands'])==15
    assert Counter(r['source_selector'] for r in rows)=={14:7,2:6} and d['source_controls']==[0,0x4000,0xA000] and not d['typed_choice_or_actor_style_commands']
    assert [(c['offset'],c['whole_command_hex']) for c in d['commands'] if c['word']!=0x4000]==[(642,'00a0ffff29000110'),(650,'00000000')]
    assert all(not any(m in bytes.fromhex(r['source_hex'])[1:] for m in [b'FI',b'FA',b'FO']) for r in rows)
    ROOT.mkdir(parents=True);save(ROOT/'all13_clean_weapon_request_conditional_search_gift_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),clean_block_sha256=d['clean_block_sha256'],whole_exchange_context=CONTEXT,records=rows,source_actor_name_fields=names,
        source_stored_bytes=656,source_logical_end=654,source_tail_bytes=2,source_commands=15,source_speeches=13,source_selectors=[2,14],source_nontext_leaves=[dict(offset=642,hex='00a0ffff29000110',meaning='Uninterpreted original A000 operand;entry/effect contract still to be mapped.'),dict(offset=650,hex='00000000',meaning='Complete four-byte end,followed by two stored alignment bytes.')],
        source_item_mention='ミノタウロスの斧',source_item_English_term_pending_current_consumer_review=True,typed_choice_glosses=[],source_macro_counts=dict(FI=0,FA=0,FO=0),
        all13_clean_speeches_read_as_one_exchange=True,source_gloss_precedes_older_English_comparison=True,prior_English_speech_unread=True,no_new_English_manuscript_or_wording_decisions=True,
        actor_name_localization_native_voice_entry_effect_control_and_display_contracts_pending=True,all207_names_aliases_and_full_editorial_objective_open=True,new_review_credit=0,new_ROMs=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False))
    print('Clean B207 whole-exchange gloss:13 speeches,656 stored/654 logical/tail2,15 commands,actors2/14,no choices/macros/FE. Search and gift remain qualified;older English not read.')
