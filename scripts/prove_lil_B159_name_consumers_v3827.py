"""Probe the original progressive and full-catalogue consumers for Samwell and a witnessed Camille control."""
import inspect,struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B159_name_consumers_v3827')
SOURCE=Path('work/analysis/lil_B159_B160_source_v3825/all63_clean_current_complete_context.json')

def names(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);rows=[];initial=bytes(cpu.mem_read(0x02000000,0x400000))
    for ident in [9,22]:
        actor=root+4+32*ident
        for kind,offset in [('progressive-nameplate',0x7ED88),('full-catalogue',0x7EDD4)]:
            prior=bytes(cpu.mem_read(0x02000000,0x400000));rings=[];writes=[]
            def ring(u,pc,size,unused):
                owner=u.reg_read(UC_ARM_REG_R0);index=struct.unpack('<I',u.mem_read(owner+8,4))[0];assert index<32;rings.append(dict(owner=owner,counter_address=owner+8,source_index=index,output_slot=owner+12+index*128))
            h=cpu.hook_add(UC_HOOK_CODE,ring,begin=0x020AC000,end=0x020AC000);w=cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=0x02000000,end=0x023fffff)
            try:ptr=get(offset,actor)
            finally:cpu.hook_del(h);cpu.hook_del(w)
            data=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0];value=data.decode('cp932');assert len(rings)==1 and ptr==rings[0]['output_slot'];r=rings[0];counter=r['counter_address'];end=ptr+len(data)+1;restored=bytearray(cpu.mem_read(0x02000000,0x400000))
            for write in writes:
                if write['address']==counter:assert write['PC'] in [0x020AC00C,0x020AC020] and write['size']==4
                else:assert ptr<=write['address'] and write['address']+write['size']<=end and write['size']==1 and write['PC'] in [0x020CED7C,0x020CED90,0x020CEDAC,0x020CEDC0]
            assert struct.unpack('<I',cpu.mem_read(counter,4))[0]==(r['source_index']+1)%32
            for start,stop in [(counter,counter+4),(ptr,end)]:restored[start-0x02000000:stop-0x02000000]=prior[start-0x02000000:stop-0x02000000];cpu.mem_write(start,prior[start-0x02000000:stop-0x02000000])
            assert bytes(restored)==prior and bytes(cpu.mem_read(0x02000000,0x400000))==prior;rows.append(dict(actor_ID=ident,actor_object=actor,consumer=kind,getter=0x02000000+offset,pointer=ptr,text=value,text_hex=data.hex(),original_scratch_ring=r,source_owned_output_bytes=end-ptr,original_getter_writes=writes,all_actor_models_and_unowned4MiB_exact=True,source_owned_scratch_restoration_recovers_all4MiB=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==initial
    return dict(rows=rows,current_executed_instruction_addresses=len(provider.executed_current),all_four_source_owned_name_consumers_complete_and_scratch_owned=True)

if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);current=NdsImage.open(source['current_ROM']);arm=current.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8]==clean[0x541C0:0x541C8];ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B159_B160_source_v3825/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');native=ctx.execute(names);ctx.machines.pop();assert not ctx.machines;values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']};assert values=={(9,'progressive-nameplate'):'Camille Overijssel',(9,'full-catalogue'):'Camille Marinus Overijssel',(22,'progressive-nameplate'):'Samwell Khan',(22,'full-catalogue'):'Samwell ダ Khan'},values
    evidence=[SOURCE,Path('work/analysis/lil_B159_B160_source_v3825/voices_and_entry_evidence_rebind.json'),Path('work/analysis/lil_B158_actual_v3814/actual_consumer_sheet1.png'),Path(__file__)];save(ROOT/'source_progressive_Samwell_Khan_vs_full_catalogue_middle_field.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],ARM9_sha256=sha(arm),original_progressive_getter_7ED88_code_sha256=sha(arm[0x7ED88:0x7EDD4]),original_progressive_nameplate_callsite=0x020541C4,native_four_consumer_cases=native,approved_short_prose_name='Samwell',source_current_progressive_nameplate='Samwell Khan',current_full_catalogue_name='Samwell ダ Khan',Camille_witnessed_progressive_control='Camille Overijssel',resolution='The original progressive nameplate consumer omits the middle component. Its Samwell Khan label is complete ASCII and differs from the full catalogue consumer Samwell ダ Khan. The witnessed Camille control likewise omits Marinus. Do not infer a dialogue nameplate defect from the full-catalogue string or edit a name asset on that basis. Preserve source selector16. The mixed middle component remains an uncredited lead for remaining full-name player-facing consumers, separate from graphics and the later older-record technical re-audit.',remaining_full_name_middle_field_consumer_lead_uncredited=True,not_actual_B159_gameplay_or_full_name_UI_coverage=True,no_name_asset_prose_ROM_registry_ledger_orcredit_change=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=inspect.getsource(names),evidence={str(p):sha(p.read_bytes()) for p in evidence},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(progressive=values[22,'progressive-nameplate'],catalogue=values[22,'full-catalogue'],four_native_consumers_pass=True,whole4MiB_scratch_ownership_exact=True,actual_B159_pending=True,credit=0))
