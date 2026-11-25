"""Current16 source records,two original consumers and live-name provider catalog."""
import struct
from pathlib import Path
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.ship_sinking_native_plan_v1330 import compiled
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ship_sinking_context_v2681');BASE=0x02000000;IDS=list(range(2058,2074))
if __name__=='__main__':
    assert not ROOT.exists();ledger=read('translations/editorial_review_current_v1.json');c=ledger['current_integrated_candidate']
    image=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds');arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    source=clean.read_file('/__arm9__.bin');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source);en=current_entries(common,arm)
    manifest=read(Path(c['path']).with_suffix('.manifest.json'));stage=manifest['relocations']['/COMMON/MESFILE.DK4']['ship_sinking_editorial']
    cp=Path(stage['release_config']);config=read(cp);mp=Path(config['manuscript']);prior={r['message_id']:r for r in read(mp)['records']}
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and sha(mp.read_bytes())==config['dependencies'][config['manuscript']]
    assert set(IDS)<=set(stage['proof']['native_IDs']) and set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') in completed for n in IDS)
    for n in IDS:assert prior[n]['source_hex']==jp[n].text.hex() and compiled(prior[n])==en[n].text
    oldpath=Path('work/analysis/ship_sinking_context_v1325/source_and_consumer_binding.json');old=read(oldpath)
    support=read('work/analysis/support_context_v2644c/source_context_packet.json');sp=Path(support['actual_snapshot']);raw=sp.read_bytes();assert sha(raw)==support['actual_snapshot_sha256']
    spans=[(0x72660,0x72BD8),(0x753F0,0x75560),(0x564C8,0x565B0),(0x55DC4,0x55E6C),(0x53D44,0x54058),(0x2E5D4,0x2E5F8)]
    for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
    cpu,get=get_machine(arm,raw);actors,fleets,captain=get(0xCB184),get(0xCB1A8),get(0x7F244);tables=[]
    for table,entry,parent,slot in [(0x021179C0,0x53D44,0x02053DB8,0x27C),(0x02117A80,0x53F0C,0x02053F40,0x274)]:
        members=list(struct.unpack_from('<8i',arm,table-BASE));assert members==list(range(2058 if table==0x021179C0 else 2066,(2058 if table==0x021179C0 else 2066)+8))
        choices=[]
        for identity in range(207):
            obj=actors+0x19E4 if identity==captain else actors+4+32*identity;voice=get(0x7E988,obj);n=get(0x53F4C,obj,table)
            assert get(0x7EE08,obj)==identity and n==members[voice]
            choices.append(dict(actor_ID=identity,actor_object=obj,source_voice=voice,message_ID=n))
        tables.append(dict(table=table,members=members,entry=entry,parent=parent,selector_stack_offset=slot,all207_original_actor_choices=choices,
            source_null_actor_selection=get(0x53F4C,0,table)))
    names=[]
    for fleet in range(63):
        for slot in range(5):
            mobile=get(0x36C70,fleets+4+132*fleet+12+8*slot)
            if not mobile:continue
            vt=struct.unpack('<I',cpu.mem_read(mobile,4))[0];method=struct.unpack('<I',cpu.mem_read(vt+4,4))[0];ptr=get(method-BASE,mobile)
            name=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0];assert 0<len(name)<=18
            names.append(dict(fleet_index=fleet,ship_slot=slot,mobile=mobile,original_virtual_name_method=method,name_pointer=ptr,name_hex=name.hex(),name=name.decode('cp932')))
    assert names
    ownmobile=get(0x36C70,fleets+4+132+12)
    gunners=[dict(source_argument=i,actor_object=get(0x55DC4,ownmobile,i)) for i in range(12)]
    for gun in gunners:
        obj=gun['actor_object'];gun['actor_ID']=get(0x7EE08,obj) if obj else None;gun['enemy_notice_ID']=get(0x53F4C,obj,0x02117A80)
    boundpath=Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json');bound=read(boundpath);assert bound['max_name_bytes_excluding_NUL']==18
    assert sha(Path(bound['source_report']).read_bytes())==bound['source_report_sha256']
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),source_hex=jp[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_reference=ref(en[n]),current_hex=en[n].text.hex(),current_stored_English=en[n].text.decode('ascii'))
    ROOT.mkdir(parents=True);contextpath=ROOT/'source_context_packet.json'
    save(contextpath,dict(current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        actual_snapshot=str(sp),actual_snapshot_sha256=sha(raw),historical_covering_fire_snapshot_not_sinking_event=True,
        voice_tables=tables,original_live_name_getters=names,own_current_mobile=ownmobile,original_actor_getter_argument_cases=gunners,
        physical_First_Mate_object=get(0x82428,fleets+0x2090,1),logical_First_Mate_actor_ID=get(0x82478,fleets+0x2090,1),
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        original_source_binding=str(oldpath),original_source_binding_sha256=sha(oldpath.read_bytes()),
        supported_ship_editor_bound=str(boundpath),supported_ship_editor_bound_sha256=sha(boundpath.read_bytes()),
        scope='Two independent eight-voice families,not16consecutive replies.2058-2065 reports a named vessel sinking/going under;the original status loop and side predicate choose when role1 speaks.2066-2073 announces an enemy vessel sunk after original projectile damage takes positive Hull to zero;the original firing-ship actor getter55DC4 supplies the direct speaker. Both take exactly one original virtual-method+4 ship-name C string. The original active/Hull/side predicates and post-message control code are unchanged. Preserve progressive2059 versus completed sinking,explicit Admiral addresses,passive was sunk versus excited success,and no crew-death or whole-fleet victory claims. All414voice choices,current live name providers and copied-state getter arguments are offline/source evidence,not activated sinking or earned staffing. The captured editor bound is18bytes excluding NUL;it does not certify arbitrary legacy names or every keyboard page. Prior gunnery pilots did not observe a sinking notice and must not be counted as one. Reuse source-bound named-ship/direct/member/common-panel representative evidence under the user sampling policy;do not require individual conditional activation unless a distinct concrete display/control risk remains.',
        credit_added=0,full_goal_complete=False))
    packetpath=ROOT/'all16_clean_current_context_catalog.json'
    save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),selected_IDs=IDS,records=[record(n) for n in IDS],neighbors=[record(n) for n in [2052,2057,2074,2082,2130]],
        registered_prose_owner_binding=dict(stage='ship_sinking_editorial',config=str(cp),config_sha256=sha(cp.read_bytes()),manuscript=str(mp),manuscript_sha256=sha(mp.read_bytes()),
            registered_native_IDs=stage['proof']['native_IDs'],selected_IDs=IDS,compiler='scripts.ship_sinking_native_plan_v1330.compiled'),
        source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),credit_added=0,full_goal_complete=False))
    save(ROOT/'next16_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),all16_clean_current_registered_compilers_exact=True,
        source_voice_choices=414,live_name_providers=len(names),unique_live_names=len({n['name_hex'] for n in names}),editor_byte_bound=18,
        source_getter_argument_cases=12,no_actual_sinking_or_new_completion_credit=True,incomplete_COMMON=75,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'Next16bound:414voice choices,{len(names)}live providers/{len(set(n["name_hex"] for n in names))}names,12getter arguments and18byte editor bound. No sinking activation/completion credit.')
