"""Seal every clean speech and both choice tables before reading older English."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_clean_context_v6592')
SOURCE=Path('work/analysis/lil_B212_clean_inventory_v6591/all_clean_B212_speeches_before_predecessor_comparison.json')
GLOSSES={
5:('Hello, you two. Do you know Romance of the Three Kingdoms?', 'Friendly opening to the party about the named novel. Do not substitute a game, a history textbook, or a new relationship.'),
22:('I see. Give it a read sometime. It is entertaining.', 'The unfamiliarity response recommends reading without insulting the player or promising a reward. The branch association follows meaning; native choice results remain to be proved.'),
32:('You do? Well, well! That makes me happy. Which general is your favorite?', 'The speaker warmly welcomes shared enthusiasm and asks a question. おじさん is his self-reference, localized with I/me; it establishes no uncle relationship.'),
51:('Really? He is my favorite, too! I think we will get along.', 'Delighted recognition of a shared favorite, not a declaration of prior friendship or kinship. Zhao Yun is identified by the following speech and choice context; native routing remains pending.'),
54:('The part at Changban Bridge where he holds A-Dou to his chest and rides alone through Cao Cao\'s army is wonderful!', 'Retain the game\'s exact 長坂橋 location, 阿斗 identity, carried-to-chest detail and lone passage through Cao Cao\'s army. Do not silently correct the game using another edition of the novel, turn this into Zhang Fei\'s bridge stand, or add a historical guarantee.'),
58:('Actually, I heard a rumor that there is a legendary spear on a peninsula around here, said to have been used by Zhao Yun.', 'Preserve rumor, reputed provenance and approximate nearby peninsula. Do not invent a peninsula name, spear name, precise coordinates, ownership certainty, item acquisition or effect.'),
62:('I wanted it myself and searched hard, but never found it. I thought you might be able to find it.', 'The speaker admits an unsuccessful search and tentatively hopes the party could succeed. No completed quest, promise, known location, guaranteed find or family relationship.'),
72:('You like Guan Yu, the lord with the magnificent beard? He is not my favorite, but he is a valiant man with both wisdom and courage.', '美髭公 is Guan Yu\'s literary epithet, not a rank or relation of the guild chief. Preserve admiration despite different preferences, with neither mockery nor invented facts.'),
78:('The brilliant strategist Zhuge Kongming... yes, yes. That Chu Shi Biao brings tears to my eyes... He is probably my second favorite.', 'The narrative 諸葛孔明 and choice 諸葛亮 name the same figure using Kongming and Liang. 出師の表 is his memorial, not a novel, battle, poem or song inferred from tears. Preserve the speaker\'s emotional response and approximate second-place preference.'),
}
WHOLE=('A friendly guild chief asks whether the travelers know Romance of the Three Kingdoms. '
       'The unfamiliarity reply recommends the enjoyable book. The familiarity reply welcomes a shared interest and asks for a favorite general. '
       'The clean three-name choice offers Zhao Yun, Guan Yu and Zhuge Liang. The Zhao Yun exchange shares enthusiasm, recalls the game\'s Changban Bridge rescue description, '
       'reports a rumored legendary spear on an unspecified nearby peninsula, admits an unsuccessful search and tentatively suggests the travelers might find it. '
       'The other two speeches respectfully praise Guan Yu\'s wisdom/courage and Zhuge Kongming\'s intelligence and moving memorial while expressing different personal preferences. '
       'Review every alternative as part of this complete exchange. Choice-result routing, original event eligibility, A000 effects and native consumers are pending. '
       'おじさん repeatedly means the older speaker referring to himself; it supplies no uncle relationship. Unused actor metadata must not become a displayed name or nationality without consumer proof.')
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);block=bytes.fromhex(d['clean_block_hex']);assert d['read_no_predecessor_English'] and len(d['records'])==9 and len(d['commands'])==26 and set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    rows=[]
    for original in d['records']:
        r=deepcopy(original);g,n=GLOSSES[r['source_record_index']];assert r['source_selector']==149
        r.update(id=f"DK4_MES_B212_R{r['source_record_index']:04d}",file_path='/data/SC2.DK4',block=212,source_reference=dict(block=212,offset=r['offset'],bytes=r['bytes'],record_index=r['source_record_index'],header_offset=r['header_offset']),fresh_source_gloss=g,whole_exchange_note=n,source_meaning_reviewed=True,current_English_not_read=True,source_prose_or_completion_credit_added=0);rows.append(r)
    choices=[]
    for at,count,expected,glosses in [(64,2,['知ってるわ','知らないわ'],['Yes, I know it.','No, I do not.']),(242,3,['趙雲','関羽','諸葛亮'],['Zhao Yun','Guan Yu','Zhuge Liang'])]:
        command=next(c for c in d['commands'] if c['offset']==at);assert command['word']==(0x2100 if count==2 else 0x2200)
        offsets=struct.unpack_from('<'+'H'*count,block,at+2);base=at+2+2*count;options=[]
        for i,(delta,jp,g) in enumerate(zip(offsets,expected,glosses,strict=True)):
            start=base+delta;end=block.index(0,start);value=block[start:end];assert value.decode('cp932')==jp
            options.append(dict(id=f'DK4_MES_B212_CH{at:04d}_O{i}',index=i,source_reference=dict(block=212,command_offset=at,relative_table_field=at+2+2*i,relative_base=base,relative_offset=delta,offset=start,bytes=len(value),record_index=block[:start].count(b'\0')),source_hex=value.hex(),source_terminated_hex=block[start:end+1].hex(),Japanese=jp,fresh_source_gloss=g,current_English_not_read=True,choice_player_voice_not_actor149_nameplate=True,source_prose_or_completion_credit_added=0))
        choices.append(dict(offset=at,word=command['word'],native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex'],relative_offsets=list(offsets),strings_base=base,options=options,native_choice_results_and_skip_routing_pending=True))
    arm=NdsImage.open(d['source_ROM']).read_file('/__arm9__.bin');assert sha(arm)==d['clean_ARM9_sha256'];fields=[]
    for delta in [0,4,8]:
        at=0x120B80+149*32+delta;p=struct.unpack_from('<I',arm,at)[0];value=arm[p-0x02000000:arm.index(0,p-0x02000000)+1] if p else b''
        fields.append(dict(actor_ID=149,column=delta,pointer_field=at,pointer=p,storage_offset=p-0x02000000 if p else None,terminated_hex=value.hex(),Japanese=value[:-1].decode('cp932') if p else None))
    assert [r['Japanese'] for r in fields]==['ギルドの元締め','中国',None]
    ROOT.mkdir(parents=True);save(ROOT/'nine_clean_speeches_five_choices_full_exchange_before_old_English.json',dict(source_inventory=str(SOURCE),source_inventory_sha256=sha(SOURCE.read_bytes()),clean_ROM=d['source_ROM'],clean_ROM_sha256=d['source_ROM_sha256'],clean_block_sha256=d['clean_block_sha256'],file_path='/data/SC2.DK4',block=212,records=rows,typed_choice_commands=choices,source_commands=d['commands'],physical_speeches=9,choice_options=5,whole_exchange_context=WHOLE,clean_actor149_name_fields=fields,source_role_gloss='guild chief or guild boss; exact displayed current name and native consumers pending',self_reference_ojisan_not_invented_kinship=True,all9_speeches_and5_choice_glosses_precede_older_English=True,cultural_reference_notes=[dict(topic='出師の表',url='https://www.gutenberg.org/ebooks/30460',scope='Primary-text edition catalogue identifies the title, Zhuge Liang author and the two memorial texts. The game remains authority for this speech; no catalogue-generated historical summary is used.'),dict(topic='Romance of the Three Kingdoms / Changban',url='https://ctext.org/sanguo-yanyi/ch41',scope='403 prevented retrieval; not relied upon. Preserve exact Japanese 長坂橋 and 阿斗 rather than silently correcting its reference.')],nine_progressive_static149_no_FE_no_FI_FA_FO_claim_from_clean_speech_scan=all(not any(x in bytes.fromhex(r['source_hex'])[1:] for x in [b'FI',b'FA',b'FO']) for r in rows),native_choice_results_skip_routing_entry_effects_names_voice_layout_actual_and_release_pending=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False));print('Clean B212 whole exchange sealed: nine speeches and five choices, exact actor149 source fields, no older English read, zero completion credit.')
