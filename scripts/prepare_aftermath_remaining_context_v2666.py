"""Bind the34 unfinished aftermath records to current source and original events."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.research_battle_aftermath_context_v1248 import source_prefix
from scripts.search_reports_native_consumers_v1662 import assigned_role
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/aftermath_remaining_context_v2666');BASE=0x02000000
IDS=[*range(1994,2011),*range(2022,2038),2192]
TABLES=[('town_surrender_report',0x02117640),('enemy_flagship_defeated',0x021176A0),
        ('own_flagship_flooding',0x021176E0),('surrender_demand',0x021177E0),('own_ship_surrender_reply',0x02117840)]

if __name__=='__main__':
    assert not ROOT.exists()
    ledger=read('translations/editorial_review_current_v1.json');candidate=ledger['current_integrated_candidate']
    clean=NdsImage.open('work/clean.nds');rom=NdsImage.open(candidate['path'])
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source);en=current_entries(common,arm)
    manifest=read(Path(candidate['path']).with_suffix('.manifest.json'));stage=manifest['relocations']['/COMMON/MESFILE.DK4']['battle_aftermath_editorial']
    cp=Path(stage['release_config']);config=read(cp);mp=Path(config['manuscript']);doc=read(mp)
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and sha(mp.read_bytes())==config['manuscript_sha256']
    assert set(IDS)<=set(stage['proof']['native_IDs']) and set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') in completed for n in IDS)
    prior={r['message_id']:r for r in doc['records']}
    for n in IDS:assert jp[n].text.hex()==prior[n]['source_hex'] and compiled(prior[n])==en[n].text
    oldpath=Path('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json');old=read(oldpath)
    bindingpath=Path('work/analysis/battle_aftermath_bindings_v1249/source_context_complete.json');binding=read(bindingpath)
    support=read('work/analysis/support_context_v2644c/source_context_packet.json');sp=Path(support['actual_snapshot']);raw=sp.read_bytes()
    assert sha(raw)==support['actual_snapshot_sha256']
    spans=[(0x71968,0x71A40),(0x72368,0x723C4),(0x717F8,0x718D4),(0x53D44,0x53DCC),
           (0x53F0C,0x54058),(0xB2B60,0xB2C08),(0x82428,0x825E4)]
    for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=get(0x7F244);world=get(0xCB178);fleetroot=get(0xCB1A8)
    tables=[]
    for family,table in TABLES:
        values=list(struct.unpack_from('<8i',arm,table-BASE));assert arm[table-BASE:table-BASE+32]==source[table-BASE:table-BASE+32]
        choices=[]
        for identity in range(207):
            obj=actors+0x19E4 if identity==captain else actors+4+identity*32
            voice=get(0x7E988,obj);n=get(0x53F4C,obj,table);assert n==(values[voice] if values[voice]>=0 else values[0])
            choices.append(dict(actor_ID=identity,actor_object=obj,source_voice=voice,message_ID=n,original_minus1_fallback=values[voice]<0))
        tables.append(dict(family=family,table=table,members=values,all207_original_actor_choices=choices))
    assigned,fixture=assigned_role(arm,raw,1,18,actors+4+18*32)
    towncases=[]
    for oldtown in old['all114_original_town_surrender_exchange_prefixes']:
        index=oldtown['town_index'];town=world+4+108*index;vt=struct.unpack('<I',cpu.mem_read(town,4))[0]
        getter=struct.unpack('<I',cpu.mem_read(vt+8,4))[0];ptr=get(getter-BASE,town);name=bytes(cpu.mem_read(ptr,96)).split(b'\0')[0]
        assert name.hex()==oldtown['town_name_hex'] and index<114
        calls,_,_=source_prefix(arm,raw,0x71968,(0,town),BASE+0x719F8)
        assigned_calls,_,_=source_prefix(arm,assigned,0x71968,(0,town),BASE+0x719F8)
        assert len(calls)==1 and calls[0]['entry']==BASE+0x53D44 and calls[0]['arguments'][:3]==[1,0x02117640,ptr]
        assert [(r['entry'],r['arguments'][1]) for r in assigned_calls]==[(BASE+0x53F0C,0x021177E0),(BASE+0x53FE4,2192),(BASE+0x53F0C,0x02117640)]
        assert assigned_calls[0]['arguments'][0]==assigned_calls[2]['arguments'][0]==actors+4+18*32
        towncases.append(dict(town_index=index,town_object=town,name=name.decode('cp932'),name_hex=name.hex(),native_name_getter=getter,
            town_speaker_actor_ID=get(0x7EE08,assigned_calls[1]['arguments'][0]),town_speaker_object=assigned_calls[1]['arguments'][0],
            unassigned_original_report_only_calls=calls,assigned_original_three_turn_calls=assigned_calls,
            no_actual_surrender_or_emulator_event_claim=True))
    assert len(towncases)==114 and {r['town_index'] for r in towncases}==set(range(114))
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),source_hex=jp[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_reference=ref(en[n]),current_hex=en[n].text.hex(),current_stored_English=en[n].text.decode('ascii'))
    ROOT.mkdir(parents=True)
    contextpath=ROOT/'source_context_packet.json';save(contextpath,dict(current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_snapshot=str(sp),actual_snapshot_sha256=sha(raw),
        snapshot_is_historical_covering_fire_not_town_surrender=True,voice_tables=tables,
        all114_current_native_town_names_and_two_original_exchange_paths=towncases,CPU_assigned_First_Mate_fixture=fixture,
        actual_physical_First_Mate_object=get(0x82428,fleetroot+0x2090,1),actual_logical_First_Mate_fallback=get(0x82478,fleetroot+0x2090,1),
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        previous_context=str(oldpath),previous_context_sha256=sha(oldpath.read_bytes()),complete_source_binding=str(bindingpath),complete_source_binding_sha256=sha(bindingpath.read_bytes()),
        original_city_ship_surrender_enclosing_bindings=binding['city_and_ship_original_bindings'],
        scope='Five alternative report/demand/reply tables plus scalar2192,not a34line conversation. Town surrender uses the original CTown name and original town representative2192. With a physical First Mate,71968 emits that member demand,representative white-flag reply,and the same member town-name report. When the physical First Mate is empty,it emits only the original role1 fallback report. All114town names and both source exchange paths are freshly executed in copied RAM. The one original-setter duty-byte fixture is CPU-only. Flagship defeated/flooding reports use distinct outcome paths;own ship surrender replies have their separately mapped enclosing battle caller. No cause,casualties,death,new ranks,ownership or gameplay outcome may be invented. Current prose is already registered but these34 are source/prose drafts,not completed editorial records. Fresh individual review and necessary native/representative/release checks remain required.',
        credit_added=0,full_goal_complete=False))
    packetpath=ROOT/'all34_clean_current_context_catalog.json';save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        selected_IDs=IDS,records=[record(n) for n in IDS],neighbors=[record(n) for n in [2011,2016,2038,2046,2114,2130,2138]],
        registered_prose_owner_binding=dict(stage='battle_aftermath_editorial',config=str(cp),config_sha256=sha(cp.read_bytes()),manuscript=str(mp),manuscript_sha256=sha(mp.read_bytes()),registered_native_IDs=stage['proof']['native_IDs'],selected_IDs=IDS,compiler='scripts.battle_aftermath_native_plan_v1255.compiled'),
        source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),credit_added=0,full_goal_complete=False))
    save(ROOT/'next34_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),all34_exact_clean_current_and_registered_compilers_match=True,
        current_source_voice_choices=1035,current_town_source_exchange_prefixes=228,current_town_names=114,
        no_new_actual_event_or_completion_credit=True,incomplete_COMMON=109,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Next34 bound:1035source voice choices,114native town names,228original exchange paths;zero added credit.')
