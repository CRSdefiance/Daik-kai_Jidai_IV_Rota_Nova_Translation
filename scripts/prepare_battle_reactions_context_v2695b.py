"""Fresh clean/current source and original four-table actor-choice binding."""
import struct
from pathlib import Path
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_reaction_native_plan_v1484 import compiled,IDS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reactions_context_v2695b');BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();ledger=read('translations/editorial_review_current_v1.json');c=ledger['current_integrated_candidate']
    rom=NdsImage.open(c['path']);clean=NdsImage.open('work/clean.nds');arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');source=clean.read_file('/__arm9__.bin')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source);en=current_entries(common,arm)
    stage=read(Path(c['path']).with_suffix('.manifest.json'))['relocations']['/COMMON/MESFILE.DK4']['battle_reaction_editorial']
    cp=Path(stage['release_config']);config=read(cp);mp=Path(config['manuscript']);prior={r['message_id']:r for r in read(mp)['records']}
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and sha(mp.read_bytes())==config['dependencies'][config['manuscript']]
    assert set(IDS)<=set(stage['proof']['native_IDs']) and set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not any(('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') in completed for n in IDS)
    for n in IDS:assert prior[n]['source_hex']==jp[n].text.hex() and compiled(prior[n])==en[n].text
    oldpath=Path('work/analysis/battle_reactions_context_v1479/source_and_original_reaction_context.json');old=read(oldpath)
    support=read('work/analysis/support_context_v2644c/source_context_packet.json');sp=Path(support['actual_snapshot']);raw=sp.read_bytes();assert sha(raw)==support['actual_snapshot_sha256']
    spans=[(0x65968,0x65A00),(0x65B08,0x65B90),(0x70FA0,0x71088),(0x74094,0x74328),(0x751E0,0x756FC),(0x7E0AC,0x7E158),(0x53F0C,0x53F4C)]
    for a,b in spans:assert arm[a:b]==source[a:b]==raw[a:b]
    cpu,get=get_machine(arm,raw);actors,captain=get(0xCB184),get(0x7F244);tables=[]
    for f in old['families']:
        first,table=f['first_ID'],f['table'];members=list(struct.unpack_from('<8i',arm,table-BASE));assert members==list(range(first,first+8));choices=[]
        for identity in range(207):
            obj=actors+0x19E4 if identity==captain else actors+4+32*identity;voice=get(0x7E988,obj);n=get(0x53F4C,obj,table)
            assert get(0x7EE08,obj)==identity and n==members[voice];choices.append(dict(actor_ID=identity,actor_object=obj,source_voice=voice,message_ID=n))
        tables.append(dict(first_ID=first,table=table,members=members,entry=0x53F0C,parent=0x02053F40,selector_stack_offset=0x274,original_context=f['original_context'],all207_original_actor_choices=choices,source_null_actor_selection=get(0x53F4C,0,table)))
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    def record(n):return dict(message_ID=n,file_path='/COMMON/MESFILE.DK4',source_reference=ref(jp[n]),source_hex=jp[n].text.hex(),clean_Japanese=jp[n].text.decode('cp932'),current_reference=ref(en[n]),current_hex=en[n].text.hex(),current_stored_English=en[n].text.decode('ascii'))
    ROOT.mkdir(parents=True);contextpath=ROOT/'source_context_packet.json'
    scope=('Four separate eight-voice alternative tables,not a32-line conversation.2147and2155tables are optional battle-setup callbacks gated by original RNG100==0,mood andvoice;actor24is excluded from this callback andonlyvoice2/3after mood0 andvoice4/6after mood1 are individually source-reachable through this caller. Other stored voices remain original text withnative selection proof,not a claim of callback reachability.2163table is original own-ship projectile-hit surprise/first-incident selection,withits original level/probability/mood andHP branch.2171table reports injury through the later original probability/stat branch andhealth-state update. The source reducesHPby10-14andcantransitionhealth0to2or2to3;do not force health,RNG,eligibility,mood,result or actor identities. Surprise can coexist withanoriginalHPchange butis not automatically a persistent wound report. Preserve excitement,confidence,surprise,pain,blood andregret without a named attacker,death,tactical failure,healing orguaranteed victory. All32havezero sourceprintf ormacroarguments;stored ASCII has no authored guard. Source-bound existing direct-actor/member panel controls andfocused native tests support representative sampling;individual conditional visits are required only for a distinct concrete unresolved risk.')
    save(contextpath,dict(current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_snapshot=str(sp),actual_snapshot_sha256=sha(raw),historical_covering_fire_snapshot_not_selected_reaction_event=True,
        voice_tables=tables,source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],original_source_binding=str(oldpath),original_source_binding_sha256=sha(oldpath.read_bytes()),scope=scope,credit_added=0,full_goal_complete=False))
    packetpath=ROOT/'all32_clean_current_context_catalog.json'
    save(packetpath,dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),selected_IDs=list(IDS),records=[record(n) for n in IDS],neighbors=[record(n) for n in [2138,2146,2179,2186,2187]],
        registered_prose_owner_binding=dict(stage='battle_reaction_editorial',config=str(cp),config_sha256=sha(cp.read_bytes()),manuscript=str(mp),manuscript_sha256=sha(mp.read_bytes()),registered_native_IDs=stage['proof']['native_IDs'],selected_IDs=list(IDS),compiler='scripts.battle_reaction_native_plan_v1484.compiled'),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),credit_added=0,full_goal_complete=False))
    save(ROOT/'next32_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),all32_clean_current_registered_compilers_exact=True,source_voice_choices=828,source_callback_reachability_not_assumed_for_every_stored_voice=True,zero_original_runtime_arguments=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('32clean/current reactions bound;828actor/voice choices andoriginal setup/surprise/injury branches exact. No forced health/RNG orcompletion/event credit.')
