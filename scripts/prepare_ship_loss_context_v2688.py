"""Fresh current source/three voice-table/name-provider binding for loss24."""
import struct
from pathlib import Path
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.ship_loss_surrender_native_plan_v1444 import compiled,IDS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ship_loss_context_v2688');BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();ledger=read('translations/editorial_review_current_v1.json');c=ledger['current_integrated_candidate']
    image=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds')
    arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source);en=current_entries(common,arm)
    stage=read(Path(c['path']).with_suffix('.manifest.json'))['relocations']['/COMMON/MESFILE.DK4']['ship_loss_surrender_editorial']
    cp=Path(stage['release_config']);config=read(cp);mp=Path(config['manuscript']);prior={r['message_id']:r for r in read(mp)['records']}
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and sha(mp.read_bytes())==config['dependencies'][config['manuscript']]
    assert set(IDS)<=set(stage['proof']['native_IDs']) and set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') in completed for n in IDS)
    for n in IDS:assert prior[n]['source_hex']==jp[n].text.hex() and compiled(prior[n])==en[n].text
    oldpath=Path('work/analysis/ship_loss_surrender_context_v1439/source_and_original_loss_surrender_context.json');old=read(oldpath)
    support=read('work/analysis/support_context_v2644c/source_context_packet.json');sp=Path(support['actual_snapshot']);raw=sp.read_bytes();assert sha(raw)==support['actual_snapshot_sha256']
    spans=[(0x72484,0x7251C),(0x7251C,0x72BE0),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x82428,0x82570)]
    for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
    cpu,get=get_machine(arm,raw);actors,fleets,captain=get(0xCB184),get(0xCB1A8),get(0x7F244);tables=[]
    for family,first,table,load,call in [('own_ship_capture',2074,0x02117AC0,0x02072988,0x02072990),('own_ship_surrender',2090,0x02117B80,0x02072B34,0x02072B3C),('enemy_ship_surrender',2098,0x02117C60,0x02072B74,0x02072B7C)]:
        members=list(struct.unpack_from('<8i',arm,table-BASE));assert members==list(range(first,first+8));choices=[]
        for identity in range(207):
            obj=actors+0x19E4 if identity==captain else actors+4+32*identity;voice=get(0x7E988,obj);n=get(0x53F4C,obj,table)
            assert get(0x7EE08,obj)==identity and n==members[voice]
            choices.append(dict(actor_ID=identity,actor_object=obj,source_voice=voice,message_ID=n))
        tables.append(dict(family=family,table=table,members=members,entry=0x53D44,parent=0x02053DB8,selector_stack_offset=0x27C,original_role=1,
            source_literal_load=load,source_call=call,all207_original_actor_choices=choices,source_null_actor_selection=get(0x53F4C,0,table)))
    names=[]
    for fleet in range(63):
        for slot in range(5):
            mobile=get(0x36C70,fleets+4+132*fleet+12+8*slot)
            if not mobile:continue
            vt=struct.unpack('<I',cpu.mem_read(mobile,4))[0];method=struct.unpack('<I',cpu.mem_read(vt+4,4))[0];ptr=get(method-BASE,mobile)
            name=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0];assert 0<len(name)<=18
            names.append(dict(fleet_index=fleet,ship_slot=slot,mobile=mobile,original_virtual_name_method=method,name_pointer=ptr,name_hex=name.hex(),name=name.decode('cp932')))
    assert len(names)==5
    boundpath=Path('work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json');bound=read(boundpath)
    assert bound['max_name_bytes_excluding_NUL']==18 and sha(Path(bound['source_report']).read_bytes())==bound['source_report_sha256']
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),source_hex=jp[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_reference=ref(en[n]),current_hex=en[n].text.hex(),current_stored_English=en[n].text.decode('ascii'))
    ROOT.mkdir(parents=True);contextpath=ROOT/'source_context_packet.json'
    scope=('Three mutually exclusive eight-voice reports in original7251C status processing,not24consecutive dialogue replies. Capture2074-2081 uses zero-crew/party eligibility and remains distinct from zero-Hull sinking. Own2090-2097andenemy2098-2105surrender require the original72484probability andparty/status/slot predicates;flagship results are handled separately. Each original53D44(role1,table,name) uses virtual-method+4 ship-name C string. Preserve explicit Admiral addresses,2091/2103/2105appearance,2099white flag then inference,and2104reported surrender intent. No sinking,crew death,permanent prize ownership orfleet-wide capitulation is added. All621actor/voice choices andlive name getters are source/CPU evidence,not activated outcomes or earned duty assignments. Stored ASCII has no authored leading guard;the original formatter supplies its guard. The18-byte captured rename bound does not certify every keyboard page or legacy name. A final row containing the complete runtime proper name plus original punctuation may be retained only with a precise per-case justification;isolated English predicates,titles and partial names still fail. Source-bound existing named-target/member controls and exhaustive current native checks support representative sampling without individual branch visits absent a distinct concrete risk.')
    save(contextpath,dict(current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        actual_snapshot=str(sp),actual_snapshot_sha256=sha(raw),historical_covering_fire_snapshot_not_selected_loss_surrender_event=True,
        voice_tables=tables,original_live_name_getters=names,physical_First_Mate_object=get(0x82428,fleets+0x2090,1),logical_First_Mate_actor_ID=get(0x82478,fleets+0x2090,1),
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],original_source_binding=str(oldpath),original_source_binding_sha256=sha(oldpath.read_bytes()),
        original_context=old['original_context'],surrender_predicate_exact_source=old['surrender_predicate_exact_source'],source_gloss_cautions=old['source_gloss_cautions'],argument_contract=old['argument_contract'],
        supported_ship_editor_bound=str(boundpath),supported_ship_editor_bound_sha256=sha(boundpath.read_bytes()),scope=scope,credit_added=0,full_goal_complete=False))
    packetpath=ROOT/'all24_clean_current_context_catalog.json'
    save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        selected_IDs=list(IDS),records=[record(n) for n in IDS],neighbors=[record(n) for n in [2058,2073,2082,2089,2106,2130]],
        registered_prose_owner_binding=dict(stage='ship_loss_surrender_editorial',config=str(cp),config_sha256=sha(cp.read_bytes()),manuscript=str(mp),manuscript_sha256=sha(mp.read_bytes()),registered_native_IDs=stage['proof']['native_IDs'],selected_IDs=list(IDS),compiler='scripts.ship_loss_surrender_native_plan_v1444.compiled'),
        source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),credit_added=0,full_goal_complete=False))
    save(ROOT/'next24_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),all24_clean_current_registered_compilers_exact=True,source_voice_choices=621,live_name_providers=len(names),unique_live_names=len({n['name_hex'] for n in names}),editor_byte_bound=18,current_blocks=sorted({en[n].block for n in IDS}),incomplete_COMMON=59,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('24clean/current paragraphs bound;621voice choices,5live providers/4names,18byte bound,COMMON22/23. No completion/event credit.')
