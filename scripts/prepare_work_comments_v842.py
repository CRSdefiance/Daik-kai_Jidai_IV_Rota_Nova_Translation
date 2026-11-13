"""Clean-source Shipwright/Doctor comments and original voice/protagonist mapping."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.personal_chatter_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/work_comments_v842')
ROM=Path('out/all_routes_combined_v838_candidate.nds')
MANUSCRIPT=Path('translations/work_comments_editorial_manuscript_v1.json')
IDS=tuple(range(1386,1410))
BASE=0x02000000
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

PROSE={
1386:("I'd better make some spare parts ahead of time...",'Says spare parts must be made in advance,as the speaker is doing now.','Preserve making the parts and preparing ahead;express the unfinished self-reminder naturally.','revise'),
1387:("I might as well make some spare parts...",'Decides casually to make some spare parts to have ready.','Use the natural might as well decision;do not imply that spare parts are already finished.','revise'),
1388:("This ship wears out so quickly. It's hard to keep up!",'Complains that the ship deteriorates quickly and the work is demanding.','Restore the difficulty and causal link;wears out is more faithful than a generic breaks.','revise'),
1389:("I keep making more, but they break right away!",'Complains that however many parts are made,they soon break.','Restore repeated production and quick breakage in an exasperated conversational line.','revise'),
1390:("Ow! I whacked my hand!",'Cries out after accidentally striking the speaker\'s own hand.','Whacked preserves the rough comic voice;no hammer or other specific tool is invented.','revise'),
1391:("Hmm... Nicely done.",'Quietly approves how well the work turned out.','Retain the natural understated appraisal;nicely captures the source approval without inventing an object.','retain'),
1392:("All done! I'll make lots more!",'Announces finishing and enthusiastically intends to make more and more.','Restore the energetic intention and repeated-more emphasis in natural cheerful English.','revise'),
1393:("Ah, now that's a masterpiece...",'Notices that this result is a masterpiece and admires it.','Restore the source this and admiring emphasis;the ellipsis keeps the reflective delivery.','revise'),
1394:("I'd better keep making more parts...",'Says the speaker must keep producing parts steadily.','Keep active production and continuing effort in Rafael\'s conversational self-reminder.','revise'),
1395:("I should make some spare parts while I can...",'Says spare parts should be made now while there is an opportunity.','Preserve the preparatory timing and practical resolve without adding a shortage or deadline.','revise'),
1396:("Huh? Am I doing this part right?",'Hesitates over whether this part of the work is being done correctly.','Restore uncertainty about doing the work;the source does not specifically ask where a component goes.','revise'),
1397:("I'm good at this kind of work.",'Confidently says this kind of work is a strength.','Restore actual skill,rather than only saying the work is suitable or comfortable.','revise'),
1398:("We're out of salve. I'd better make some more.",'Notices that wound medicine has run out and decides to make it.','Retain the suitable wound-remedy term salve;restore a natural complete observation and decision. This is flavor text,not a new item or inventory contract.','revise'),
1399:("So I mix this herb into the medicine...",'Confirms that this medicinal herb is to be mixed into this medicine.','Restore the omitted medicine and the self-confirming tone;avoid a repeated deictic this that sounds translated.','revise'),
1400:("Phew, it stinks! But it works.",'Remarks that the mixture smells bad but is effective.','Retain the natural odor reaction and contrast;no particular cure or guaranteed gameplay effect is added.','retain'),
1401:("Someone's always getting hurt. I'd better make some medicine.",'Says someone soon gets injured,so medicine must be made.','Restore the reason and obligation to prepare medicine instead of disconnected clipped notes.','revise'),
1402:("All right! The seasickness medicine is ready!",'Cheers that medicine for seasickness has been completed.','Restore the completed result and enthusiastic rough voice;the source does not report administering a cure.','revise'),
1403:("Hmm... Should be ready now.",'Reflects that it should be about time for the preparation to be finished.','Retain the natural contextual ellipsis and tentative should;no stronger certainty is introduced.','retain'),
1404:("Time for a taste... Yuck!",'Decides to taste the preparation and reacts to its bad taste.','Localize the casual tasting intention and prolonged disgust idiomatically,without an invented symptom.','revise'),
1405:("Hmm... The medicine seems to be ready.",'Observes that the medicine appears to be finished.','Restore the source tentative seems,which the older definite is ready omitted.','revise'),
1406:("Guys like Claudio get hurt so easily...",'Says people like Claudio readily get injured,as a reason for making medicine.','Use the established Claudio for the familiar source nickname;retain like and easily instead of making the complaint solely about him.','revise'),
1407:("I need to learn more about medicinal herbs.",'Says more knowledge of medicinal herbs must be learned.','Restore a natural first-person resolve and the medicinal purpose of the herbs.','revise'),
1408:("That's an odd color... Is this safe to drink?",'Notices a strange color and wonders whether drinking it is safe.','Use natural hesitant questions;do not invent a diagnosis or a decision to drink it.','revise'),
1409:("Xien's lessons in Chinese medicine are coming in handy.",'Says the Chinese medicine learned from Xien is proving useful.','Preserve learning from Xien and its present usefulness. Use the established native actor10 spelling Xien;do not rename him Xian or reduce the thought to medicine merely helping.','revise'),
}


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def snapshot(folder,frame):
    report=read(CAP/folder/'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    rows=report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[])
    rec=next(r for r in rows if r['frame']==frame)
    raw=Path(rec['path']).read_bytes()
    assert len(raw)==0x400000 and sha(raw)==rec['sha256'] and rec['read_only_export']
    return raw,rec


def machine_at(arm,raw):
    cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(at,*args):
        call(cpu,at,args)
        return cpu.reg_read(UC_ARM_REG_R0)
    return cpu,get


def main():
    assert not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    current,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm,source=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    spans=((0x12104,0x12920),(0x53C6C,0x53CB0),(0x53F4C,0x53F9C),(0x7E988,0x7E9A0))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    old=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    npc_table=struct.unpack_from('<I',arm,0x12834)[0]
    hero_table=struct.unpack_from('<I',arm,0x1291C)[0]
    groups={}
    for role,first in ((13,1386),(14,1398)):
        npc=struct.unpack_from('<I',arm,npc_table-BASE+role*4)[0]
        hero=struct.unpack_from('<I',arm,hero_table-BASE+role*4)[0]
        assert struct.unpack_from('<8I',arm,npc-BASE)==tuple(range(first,first+8))
        assert struct.unpack_from('<4I',arm,hero-BASE)==tuple(range(first+8,first+12))
        groups[role]={'role_ID':role,'role_label':'Shipwright' if role==13 else 'Doctor',
            'NPC_group':npc,'NPC_IDs':list(range(first,first+8)),
            'protagonist_group':hero,'protagonist_IDs':list(range(first+8,first+12))}
    raw,receipt=snapshot('personal_cabin_v840_838_Charles_after',3200)
    cpu,get=machine_at(arm,raw)
    actors=get(0xCB184)
    names={r['actor_ID']:r['name'] for r in read('work/analysis/personal_chatter_v835/native_context.json')['actor_names']}
    voices=[]
    for actor in range(4,25):
        obj=actors+4+actor*32
        voice=get(0x7E988,obj)
        assert 0<=voice<8
        for role,first in ((13,1386),(14,1398)):
            selected=get(0x53F4C,obj,groups[role]['NPC_group'])
            assert selected==first+voice
            voices.append({'actor_ID':actor,'native_name':names[actor],'voice_class':voice,
                'role_ID':role,'selected_message_ID':selected,'complete_native_helper_ABI':True})
    assert {r['voice_class'] for r in voices}==set(range(8))
    actor10=actors+4+10*32;vt=struct.unpack('<I',cpu.mem_read(actor10,4))[0]
    pointer=get(struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]-BASE,actor10)
    xien=bytes(cpu.mem_read(pointer,32)).split(b'\0')[0]
    assert xien==b'Xien'
    heroes=[]
    specs=[(0,'Rafael','personal_activity_v839_838_Rafael_later',3200),
           (1,'Hodram','personal_cabin_v840_838_Charles_after',3200),
           (2,'Lil','ceremony_Lil_approach_v825',23000),
           (3,'Maria','ceremony_Maria_approach_v825',26000)]
    for hero,name,folder,frame in specs:
        hraw,hrec=snapshot(folder,frame)
        assert hraw[0x53C6C:0x53CB0]==arm[0x53C6C:0x53CB0]
        u,hget=machine_at(arm,hraw)
        assert hget(0x7F244)==hero
        for role,first in ((13,1386),(14,1398)):
            selected=hget(0x53C6C,groups[role]['protagonist_group'])
            assert selected==first+8+hero
            heroes.append({'actual_protagonist':name,'native_captain_ID':hero,'role_ID':role,
                'selected_message_ID':selected,'read_only_RAM':hrec,'complete_native_helper_ABI':True,
                'current_immutable_code_with_original_real_protagonist_state_no_captain_substitution':True})
    native=ROOT/'native_context.json'
    save(native,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_code_spans_exact_clean':[[a,b,sha(arm[a:b])] for a,b in spans],
        'role_groups':groups,'all42_NPC_voice_selections_cover_all_eight_classes':voices,
        'all8_real_protagonist_group_selections':heroes,'NPC_source_RAM':receipt,
        'native_Xien_name':{'actor_ID':10,'given_name_pointer':pointer,'hex':xien.hex(),'name':'Xien'},
        'original_full_consumer':'12104 working-state branch ->1278C/128B4 role helpers ->53F4C NPC voice or53C6C current protagonist ->5528C',
        'body_consumer':'CDeckCabinInfoView,15334/154CC embedded6x12 font;V838 source crop216x36',
        'role13_is_Shipwright_role14_is_Doctor_room_slot_is_a_separate_value':True,
        'numeric_helper_proofs_only_not_actual_new_wording_font_or_gameplay_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    packet=[{'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
        'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),
        'current_hex':en[n].text.hex(),'current_reference':reference(en[n])} for n in range(1382,1414)]
    save(ROOT/'source_context_packet.json',{'neighbors1382_1413':packet,
        'independent_voice_variants_not_a_sequential_conversation':True,
        'self_comments_describe_work_flavor_not_new_inventory_or_treatment_commands':True})
    rows=[]
    for n,(english,meaning,note,decision) in PROSE.items():
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==en[n].text.decode('ascii').strip()
        role=13 if n<1398 else 14;first=1386 if role==13 else 1398;index=n-first
        speaker=f'Native NPC voice class{index}' if index<8 else ['Rafael','Hodram','Lil','Maria'][index-8]
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,
            'voice_class':index if index<8 else None,'protagonist_ID':index-8 if index>=8 else None,
            'speaker':speaker,'context':f'Independent {groups[role]["role_label"]} working comment. Original role{role} table selects one of8 NPC voices or the active protagonist. Adjacent storage records are alternatives for other speakers,not dialogue continuations.',
            'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),
            'canonical_source_hex':old[n].text.hex(),'current_reference':reference(en[n]),
            'current_text_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932'),
            'english':english,'source_meaning':meaning,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2',
        'target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-personnel-visible-v1',
        'review_gates':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
        'status':'24-source-prose-reviewed-native-format-and-actual-release-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_ROM':str(ROM),
        'current_ROM_sha256':sha(ROM.read_bytes()),'current_COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),
        'current_ARM9_sha256':sha(arm),'native_context_proof':str(native),'native_context_proof_sha256':sha(native.read_bytes()),
        'records':rows,'full_goal_complete':False})
    print('24 clean-source Shipwright/Doctor reviews saved:21 revisions,3 retentions.42 NPC and8 real-protagonist native selections pass. Native fonts,registered release and actual scenes remain.',flush=True)


if __name__=='__main__':main()
