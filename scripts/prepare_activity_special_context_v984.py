"""Complete source context for17 activity,Chapel-refusal and special-character lines."""
import struct,unicodedata
from pathlib import Path
from shutil import copy2
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_work_comments_v842 import snapshot,machine_at
from scripts.verify_personal_gameplay_v841 import rtti
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_v984')
ROM=Path('out/all_routes_combined_v981_candidate.nds')
BASE=0x02000000
SPEAKERS={1872:15,1873:14,1874:22,1875:11,1876:20,1877:6,1878:17,1879:25,1880:12,
          1881:25,1882:26,1883:27,1884:27,1885:25,1886:26,1887:27,1888:27}

def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1157 and ledger['records_with_source_and_prose_pass']==1160
    prior_path=Path('work/analysis/next_comments_v983/source_selection_research.json');prior=read(prior_path)
    rom,clean=map(NdsImage.open,(ROM,'work/clean.nds'));arm,jp=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())==prior['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(prior['all52_activity2_direct_and_main_priority_cases'])==52 and len(prior['all16_special_ordinary_battle_direct_and_main_bit2_controls'])==16
    spans=((0x13450,0x13720),(0x15DE4,0x15ED0),(0x7AD4,0x7B3C),(0x139A0,0x13D78),(0x15334,0x154E8))
    for a,b in spans:assert arm[a:b]==jp[a:b]
    raw,receipt=snapshot('mood_comments_v982_975_CaptainSilent',16100)
    parents=[i for i in range(0,len(raw)-0x2198,4) if raw[i:i+4]==struct.pack('<I',0x02130EF0) and raw[i+0x2194:i+0x2198]==struct.pack('<I',0x021314E8)]
    assert len(parents)==1;parent=BASE+parents[0]
    assert rtti(raw,0x02130EF0)=='18CDeckPersonnelView' and rtti(raw,0x021314E8)=='18CDeckCabinInfoView'
    cpu,get=machine_at(arm,raw);actors=get(0xCB184);names={}
    for actor in sorted(set(SPEAKERS.values())):
        obj=actors+4+actor*32;vt=struct.unpack('<I',cpu.mem_read(obj,4))[0]
        fn=struct.unpack('<I',cpu.mem_read(vt+32,4))[0];ptr=get(fn-BASE,obj)
        text=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0]
        names[actor]={'actor_ID':actor,'native_name':unicodedata.normalize('NFKC',text.decode('cp932')),
            'name_hex':text.hex(),'getter':fn,'name_pointer':ptr,'original_actor_object':obj,'actor_record_sha256':sha(bytes(cpu.mem_read(obj,32)))}
    assert {n:names[n]['native_name'] for n in (12,17,25,26,27)}=={12:'Yukihisa',17:'Al',25:'Yifa',26:'Julian',27:'Aziza'}
    legality=[]
    for actor in (4,12,17,25):
        for role in (2,5,18):
            u,get=machine_at(arm,raw);result=get(0x15DE4,actor,role)
            expected=0 if role==5 or (actor in (12,17,25) and role==18) else 1
            assert result==expected
            legality.append({'actor_ID':actor,'role_ID':role,'original_15DE4_result':result,'original_ABI_stack_pass':True})
    refusals=[]
    for actor,expected in ((12,1880),(17,1878),(25,1879)):
        u,get=machine_at(arm,raw);controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller);actors=get(0xCB184)
        fields={model+0x1E+12:bytes([18]),parent+0x40:struct.pack('<2I',actor,32)}
        for at,data in fields.items():u.mem_write(at,data)
        prepared=bytes(u.mem_read(BASE,len(raw)))
        allowed={at+i for at,data in fields.items() for i in range(len(data))}
        changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,prepared,strict=True)) if a!=b]
        assert all(r['address'] in allowed for r in changes)
        calls=[];refresh=[];assignment=[]
        def speech(cpu,pc,size,unused):
            calls.append({'actor_object':cpu.reg_read(UC_ARM_REG_R0),'message_ID':cpu.reg_read(UC_ARM_REG_R1)})
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        def repaint(cpu,pc,size,unused):refresh.append(pc);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        hooks=[u.hook_add(UC_HOOK_CODE,speech,begin=BASE+0x53FE4,end=BASE+0x53FE4),
            u.hook_add(UC_HOOK_CODE,repaint,begin=BASE+0x13724,end=BASE+0x13724),
            u.hook_add(UC_HOOK_CODE,lambda *args:assignment.append(True),begin=BASE+0x82BB8,end=BASE+0x82BB8)]
        occupants=bytes(u.mem_read(controller+6,31));records=bytes(u.mem_read(actors+4,28*32))
        try:get(0x13450,parent,12)
        finally:
            for hook in hooks:u.hook_del(hook)
        assert calls==[{'actor_object':actors+4+actor*32,'message_ID':expected}] and len(refresh)==1 and not assignment
        assert bytes(u.mem_read(controller+6,31))==occupants and bytes(u.mem_read(actors+4,28*32))==records
        refusals.append({'actor_ID':actor,'name':names[actor]['native_name'],'requested_role':18,'slot':12,
            'original_owner':parent,'owner_RTTI':'18CDeckPersonnelView','selection_entry':BASE+0x13450,
            'CPU_widget_selected_actor_and_empty_previous_slot32_and_destination_Chapel_type_only':changes,
            'all_other4MiB_RAM_exact_before_call':True,'original_legality_and_actor_specific_refusal_calls':calls,
            'dialogue_dispatcher':BASE+0x53FE4,'original_final_repaint_intercepted_not_UI_display_credit':True,
            'all28_actor_records_and31_room_occupants_preserved_no_assignment_performed':True,
            'original_ABI_and_stack_pass':True,'not_actual_gameplay_or_modal_font_proof':True})
    records=[]
    for row in prior['records_and_immediate_neighbors']:
        row=dict(row);n=row['message_id']
        if n in SPEAKERS:
            row.update(actor_ID=SPEAKERS[n],speaker=names[SPEAKERS[n]]['native_name'],
                consumer='assignment-refusal-modal' if 1878<=n<=1880 else 'Deck-CabinInfoView',
                source_family='activity2-post-event' if n<1878 else 'Chapel-assignment-refusal' if n<1881 else 'special-ordinary-personal' if n<1885 else 'special-battle-personal')
        records.append(row)
    proof={**prior,'additional_clean_source_spans':[[a,b,sha(arm[a:b])] for a,b in spans],
        'prior_research_proof':str(prior_path),'prior_research_proof_sha256':sha(prior_path.read_bytes()),
        'original_actor_name_getters':names,'actor_by_message_ID':SPEAKERS,
        'all12_original_actor_role_legality_controls':legality,'all3_original_Chapel_assignment_refusal_owner_and_speaker_calls':refusals,
        'Chapel18_refusal_not_an_across_the_board_Taoist_training_ban':True,
        'activity2_is_original_post_event_state_after139EC_not_a_new_scold_button':True,
        'special_actor27_bit2_meaning_uninterpreted_both_source_wordings_preserved':True,
        'source_modal_dispatcher53FE4_distinct_from_Deck_embedded_body':True,
        'records_and_immediate_neighbors':records,'completed_entries_added':0,'source_prose_reviews_added':0,
        'all17_prose_native_layout_actual_integration_pending':True,'producer_sha256':sha(Path(__file__).read_bytes())}
    proof.pop('Chapel_exception_menu_owner_arguments_actor_predicates_and_dismissal_still_unmapped',None)
    proof['original_Chapel_owner_actor_predicates_and_dispatch_mapped_but_actual_dismissal_pending']=True
    save(ROOT/'source_context_packet.json',proof)
    doc=Path('docs/activity_special_v984_source_context.md');assert not doc.exists()
    with doc.open('x',encoding='utf-8') as f:f.write('# V984: activity,Chapel refusal and special-character contexts\n\n52 activity2 controls and16 special ordinary/battle controls from V983 remain hash-locked. Twelve original role-legality calls and three complete original personnel-assignment refusal calls add exact Chapel18 owner,actor pointer and speech IDs:Al17->1878,Yifa25->1879,Yukihisa12->1880. No assignment occurs;all28 actor records and31 room occupants remain exact. Only declared CPU widget selection,previous-slot sentinel and room type are changed. Speech/repaint boundaries are intercepted for numeric selection only;no actual modal display or dismissal credit.\n\nOriginal virtual name getters identify Angelo15,Emilio14,Samwell22,Jam11,Fernando20,Julio6,Al17,Yifa25,Yukihisa12,Julian26 and Aziza27. The actual captain remains1 and no actor identity is replaced. Activity2 is the original post-event state after139EC,not a newly invented Scold button. Ordinary and battle special statements are independent alternatives,with both original actor27 bit2 outcomes preserved without guessing a story/gender explanation.\n\nAll17 prose,fonts,actual representative scenes,registered integration and exact patch remain pending. V981 stays current;1157 complete and1160 source/prose reviewed. Separate graphics,raw coverage and later older-record re-audit remain open.\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V984 Activity special source context');assert not archive.exists();rows=[]
    for source in (ROOT/'source_context_packet.json',Path(__file__),doc):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert source.read_bytes()==target.read_bytes();rows.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':rows,'all_hashes_verified':True,'no_completion_credit':True})
    print('17 contexts mapped:52 activity controls,16 special controls,12 legality controls and3 original Chapel refusals;prose/font/actual credit pending.')

if __name__=='__main__':main()
