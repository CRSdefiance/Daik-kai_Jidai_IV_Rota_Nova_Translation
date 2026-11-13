"""Current progressive76 and separate modal3 paths; complete2823 native cases."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.verify_arrival_native_v792 import prepared,format_case as modal_case,run as modal_run
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from scripts.native_call_abi_v764 import call
from unicorn.arm_const import UC_ARM_REG_R0

ROOT=Path('work/analysis/guild_courier_layouts_v2241')
DOC=Path('translations/guild_courier_contextual_editorial_manuscript_v1.json')
INPUTS=[Path('work/analysis/item_diplomacy_integration_v788/production_layout/verification.json'),Path('work/analysis/arrival_notices_v792/native_verification.json')]
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    doc=read(DOC);rows={r['message_id']:r for r in doc['records']};rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    assert sha(arm)==doc['current_ARM9_sha256']
    for n,r in rows.items():assert entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')
    snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    source=inspect.getsource(original.format_case)
    marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    n=row['message_id']
    parent,key=row['native_binding']['parent'],row['native_binding']['table_or_ID']
    for at,value in ((0x264,parent),(0x270,0),(0x274,n),(0x27C,key)):
        u.mem_write(STACK+at,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)
    for p,value in zip(pointers,values):
        assert bytes(u.mem_read(p,len(value)+1))==value+bytes(1)
'''
    assert source.count(marker)==1;source=source.replace(marker,replacement);env=dict(original.__dict__);exec(compile(source,__file__,'exec'),env);(ROOT/'progressive_formatter.py').write_text(source,encoding='utf-8')
    cases=[];findings=[];indices=[];seen=set()
    progressive=read(INPUTS[0]);modal=read(INPUTS[1]);assert len(progressive['cases'])==2774 and len(modal['layouts'])==49
    for local,c in enumerate(progressive['cases']+modal['layouts']):
        n=c['id'];r=rows[n]
        if n>=1000:
            if local%64==0:u,_=get_machine(arm,raw)
            values=tuple(bytes.fromhex(v)for v in c['source_values_hex']);result=env['format_case'](u,r,values)
            kind='actual-original-progressive-parent-and-key-dispatch'
        else:
            values=(bytes.fromhex(c['value_hex']),);result=modal_case(prepared(arm),r,values[0]);result.update(source_values_hex=[v.hex()for v in values],English_values_hex=[v.hex()for v in values],exact_printf_and_complete_words_and_guards_and_callee_saved_ABI=True)
            kind='separate-original-modal-parent546E8-ID-dispatch'
        index=len(cases);result.update(index=index,message_ID=n,values_hex=result['English_values_hex'],template_hex=entries[n].text.hex(),display_kind=kind,native_binding=r['native_binding']);cases.append(result)
        if result['findings']:findings.append(dict(index=index,message_ID=n,findings=result['findings'],lines=result['lines']))
        label=values[0]if n==1098 else None
        shape=(n,len(result['lines']),tuple(len(s.encode('cp932'))%2 for s in result['lines']),any(not v.isascii()for v in values),label)
        if shape not in seen:seen.add(shape);indices.append(index)
    assert not findings and len(cases)==2823 and {r['message_ID']for r in cases}==set(rows)
    old_arm=NdsImage.open('out/all_routes_combined_v792_candidate.nds').read_file('/__arm9__.bin');controls=[]
    probe=b' Complete courier words preserve every leading and final character.'
    for parent in(0x0205469C,0x02054720,0x02054764,0x02054014):
        for n in(346,347,348):
            before,after=modal_run(prepared(old_arm),parent,n,probe),modal_run(prepared(arm),parent,n,probe)
            assert before==after;controls.append(dict(parent=parent,ID=n,current_equals_prior_registered_modal_path=True))
    # Fresh current direct/object getters and existing virtual width; CPU object-kind input only.
    u,get=get_machine(arm,raw);obj=get(0xCB130)+4;label_cases=[]
    assert struct.unpack('<I',u.mem_read(obj,4))[0]==0x0214C618
    for label in doc['runtime_letter_labels']:
        n=label['type'];u.mem_write(obj+4,bytes([n]));expected=bytes.fromhex(label['current_hex'])
        for fn,arg in((0x93D28,obj),(0x93D5C,n)):
            before=bytes(u.mem_read(0x02000000,0x800000));call(u,fn,(arg,));p=u.reg_read(UC_ARM_REG_R0);text=bytes(u.mem_read(p,128)).split(bytes(1))[0]
            assert text==expected and bytes(u.mem_read(0x02000000,0x800000))==before
            label_cases.append(dict(type=n,getter=0x02000000+fn,pointer=p,text_hex=text.hex(),all8MiB_and_native_ABI_preserved=True))
    call(u,0x9145C,());assert u.reg_read(UC_ARM_REG_R0)==24 and arm[0x9145C:0x91464].hex()=='1800a0e31eff2fe1'
    save(ROOT/'all79_current_native_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_snapshot=snapshot,input_matrices={str(p):sha(p.read_bytes())for p in INPUTS},case_count=len(cases),progressive_cases=2774,separate_modal_cases=49,cases=cases,findings=findings,representative_full_font_indices=indices,all79_original_consumer_parent_table_or_ID_bindings_used=True,modal12_wrong_parent_controls=controls,current12_type_getter_cases=label_cases,current_virtual_document_name_width_cells=24,ordinary_class13_document_GPU_menu_not_claimed=True,prior_ordinary_selector_source_closure='work/analysis/scheme_consumer_scope_v793/source_and_native_scope.json',prior_selector_closure_sha256=sha(Path('work/analysis/scheme_consumer_scope_v793/source_and_native_scope.json').read_bytes()),all_six_labels_present_in_selected1098_full_font_samples=True,complete_native_printf_words_argument_copies_bounds_canaries_and_ABI=True,supplied_prices_faction_pairs_and23byte_modal_name_stress_not_all_eligible_or_earned=True,regular_native_machine_reset_every64_cases=True,modal_native_machine_fresh_every_case=True,full_font_visual_actual_and_reconciliation_pending=True,no_ROM_or_registry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(cases=len(cases),progressive=2774,modal=49,findings=0,font_samples=len(indices),current_type_getters=len(label_cases)),flush=True)
