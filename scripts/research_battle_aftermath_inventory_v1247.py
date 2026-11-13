"""58 source battle-aftermath/city-defense messages and1872 native selections.

Source table membership is executed, not inferred from literal ordering.
PC-relative pointer users are caller leads until enclosing functions are mapped.
No new prose, native layout approval or completed editorial credit is produced.
"""
from pathlib import Path
from dataclasses import asdict
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_special_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_aftermath_source_v1247')
BASE=0x02000000
TABLES=(('enemy_surrender_report',0x02117640,1994,2000),
    ('enemy_flagship_defeated',0x021176A0,2000,2006),
    ('own_flagship_flooding',0x021176E0,2006,2011),
    ('enemy_flagship_boarding_capture',0x02117740,2011,2016),
    ('own_crew_lost_abandon_ship',0x02117760,2016,2022),
    ('surrender_demand',0x021177E0,2022,2030),
    ('own_ship_surrender_reply',0x02117840,2030,2038),
    ('city_defense_challenge',0x021178C0,2038,2046),
    ('enemy_flagship_fled_victory',0x02117900,2046,2052))


def main():
    assert not ROOT.exists()
    source_path=Path('work/clean.nds');current_path=Path('out/all_routes_combined_v1224_candidate.nds')
    clean,current=NdsImage.open(source_path),NdsImage.open(current_path)
    source,arm=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    assert sha(source_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(current_path.read_bytes())=='cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd'
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    ledger=read('translations/editorial_review_current_v1.json')
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not done.intersection(range(1994,2052))
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_011782_arm9_ram.bin')
    raw=snapshot.read_bytes();cpu,get=get_machine(arm,raw)
    actors=get(0xCB184);objects=[actors+4+i*32 for i in range(207)]+[actors+0x19E4]
    ids=[get(0x7EE08,o) for o in objects]
    assert len(set(ids))==207 and ids[-1]==1
    tables=[];records=[];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for family,table,first,end in TABLES:
        at=table-BASE
        values=struct.unpack_from('<8i',source,at)
        assert arm[at:at+32]==source[at:at+32]
        assert {v for v in values if v>=0}==set(range(first,end)),(family,values)
        selections=[]
        for slot,obj in enumerate(objects):
            voice=get(0x7E988,obj);n=get(0x53F4C,obj,table)
            assert 0<=voice<8 and n==(values[voice] if values[voice]>=0 else values[0])
            selections.append({'actor_slot':slot,'actor_ID':ids[slot],'actor_object':obj,
                'voice_class':voice,'message_ID':n})
        assert {r['message_ID'] for r in selections}==set(range(first,end))
        null=get(0x53F4C,0,table);assert null==values[0]
        pointers=[BASE+i for i in range(0,len(source)-3,4) if struct.unpack_from('<I',source,i)[0]==table]
        loads=[]
        for pc in range(0x800,min(0x110000,len(source)-3),4):
            word=struct.unpack_from('<I',source,pc)[0]
            if word&0x0F7F0000!=0x051F0000:continue
            target=pc+8+(word&4095)*(1 if word&(1<<23) else -1)
            if not 0<=target<len(source)-3 or struct.unpack_from('<I',source,target)[0]!=table:continue
            instruction=next(decoder.disasm(source[pc:pc+4],BASE+pc))
            assert instruction.mnemonic.startswith('ldr') and '[pc' in instruction.op_str
            window=[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                for off in range(max(0x800,pc-32),min(pc+96,len(source)-3),4)
                for i in decoder.disasm(source[off:off+4],BASE+off)]
            loads.append({'instruction':BASE+pc,'literal':BASE+target,'register':(word>>12)&15,
                'source_instructions':window,'enclosing_function_and_executed_call_arguments_pending':True})
        tables.append({'family':family,'table':table,'source_eight_signed_members':list(values),
            'native_message_IDs':list(range(first,end)),'all208_original_selections':selections,
            'null_actor_original_fallback':null,'aligned_pointer_reference_leads':pointers,
            'PC_relative_LDR_pointer_user_leads':loads})
        for n in range(first,end):
            records.append({'message_ID':n,'source_family':family,'source_voice_table':table,
                'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},
                'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
                'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},
                'current_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932'),
                'source_voice_classes':[i for i,v in enumerate(values) if v==n],
                'original_consumers_runtime_arguments_and_natural_prose_review_pending':True})
    assert len(records)==58 and sum(len(t['all208_original_selections']) for t in tables)==1872
    ROOT.mkdir(parents=True)
    proof=ROOT/'source_context_inventory.json'
    save(proof,{'source_ROM':str(source_path),'source_ROM_sha256':sha(source_path.read_bytes()),
        'current_ROM':str(current_path),'current_ROM_sha256':sha(current_path.read_bytes()),
        'current_COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'current_ARM9_sha256':sha(arm),
        'snapshot':str(snapshot),'snapshot_sha256':sha(raw),'records':records,'voice_tables':tables,
        'all1872_original_voice_choices_and_nine_null_fallbacks_execute':True,
        'all58_additional_to_completed1260_without_duplicate_credit':True,
        'PC_relative_pointer_users_are_leads_not_complete_context_approval':True,
        'current_2046_victory_capture_is_a_context_lead_not_new_translation_gameplay':
            'E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_010982_navigation.png',
        'no_prose_manuscript_ROM_or_completion_credit_change':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger['next_battle_aftermath_source_inventory_v1247']={'proof':str(proof),
        'native_message_IDs':list(range(1994,2052)),'families':9,'original_source_voice_selections':1872,
        'prose_and_context_approval_pending':True,'completed_entries':0}
    save('translations/editorial_review_current_v1.json',ledger)
    print('58 next shared messages,nine source tables,1872 native selections;caller/argument/prose review open;no completion credit.',flush=True)


if __name__=='__main__':main()
