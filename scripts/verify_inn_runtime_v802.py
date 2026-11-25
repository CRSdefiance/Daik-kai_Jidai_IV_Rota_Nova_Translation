"""Prove scoped Inn selector/storage research without a playable ROM build."""

import inspect
import struct
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch import inn_editorial_runtime as new
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts import verify_palace_runtime_v796 as prior_scope
from scripts import verify_recruitment_runtime_v771 as old_status
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_runtime_v802')
ROM=Path('out/all_routes_combined_v799_candidate.nds')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    assert sha(arm)=='9fbf8f0e8ea7e9f82d697a1938bbda7dd170bf5d15976f9334c995335e78b8e1'
    changes=new.patches(arm);target=new.apply(arm)
    restore=bytearray(target)
    for at,data in changes.items():restore[at-BASE:at-BASE+len(data)]=arm[at-BASE:at-BASE+len(data)]
    assert bytes(restore)==arm
    old_code,new_code=[MainCodeFile(v,BASE) for v in (arm,target)]
    shape=lambda code:[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert shape(old_code)==shape(new_code)
    assert bytes(old_code.sections[3].data)==bytes(new_code.sections[3].data)
    assert len(new_code.sections[3].data)-48==123040 and cache_plan(arm)==cache_plan(target)
    assert arm[new.bank.STATUS-BASE:new.bank.STATUS-BASE+80]==target[new.bank.STATUS-BASE:new.bank.STATUS-BASE+80]
    gate=new.bank.GATE-BASE
    assert target[gate:gate+168].replace(struct.pack('<I',new.CONTRACTS),struct.pack('<I',new.previous.CONTRACTS))==arm[gate:gate+168]
    # Every old contract is preserved; add only source-mapped Inn consumers.
    additions=[]
    for old,now in zip(new.previous.contract_rows(),new.contract_rows(),strict=True):
        assert old[:3]==now[:3] and set(old[3])<=set(now[3])
        added=set(now[3])-set(old[3])
        expected=set(new.ORDINARY) if now[0]==0x02054014 else set(new.YES_NO) if now[0]==0x02053FCC else {0x80E0} if now[0]==0x02053DB8 else set()
        assert added==expected
        additions.append(dict(parent=now[0],new_values=sorted(added)))
    private=read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    new_rom=NdsImage.open(ROM);new_rom.rom.arm9=target
    before_private,after_private=[census(r,[[new.CONTRACTS,new.END]],private) for r in (rom,new_rom)]
    assert sorted(r for r in before_private if not r[-1])==sorted(r for r in after_private if not r[-1])
    assert census(rom,[[new.LAST_MONTH,new.LAST_MONTH+12]],[])==[]
    span=[[new.TIME_START,new.TIME_END],[new.LAST_MONTH,new.LAST_MONTH+12]]
    before,after=[census(r,span,[]) for r in (rom,new_rom)]
    expected=[]
    for at in (0x5CB2C,0x5CB30,0x5CB34,0x5CB38):
        expected.append(['absolute','section0',BASE+at,struct.unpack_from('<I',target,at)[0],False])
    assert sorted(after)==sorted(expected)
    assert sorted(before)==read('work/analysis/inn_context_v801/baseline_and_time_ownership.json')['complete_current_reference_census']
    save(ROOT/'bounded_runtime_plan.json',dict(source_ROM_sha256=sha(ROM.read_bytes()),source_ARM9_sha256=sha(arm),research_ARM9_sha256=sha(target),
        patches=[dict(address=at,source_hex=arm[at-BASE:at-BASE+len(data)].hex(),target_hex=data.hex()) for at,data in changes.items()],
        exact_contract_additions=additions,private_span=[new.CONTRACTS,new.END],
        table_used_bytes=new.TABLE_USED,table_alignment_bytes=2,packed_phrase_indices_bytes=24,
        luxury_goods_complete_NUL_owned_source_pointer=new.LUXURY_GOODS,
        reused_unreferenced_original_Military_Investment_string_span=[new.LAST_MONTH,new.LAST_MONTH+12],
        time_owned_reference_census_before=before,time_owned_reference_census_after=after,
        private_reference_census_before=before_private,private_reference_census_after=after_private,
        exact_original_gate_instructions_and_all_seven_parent_contracts_retained=True,
        status_code_and_packed_phrase_pointer_unchanged=True,
        sections_BSS_cache_staged123040_and_all_other_bytes_preserved=True,
        source_producer_sha256=sha(Path(__file__).read_bytes()),runtime_sha256=sha(Path(new.__file__).read_bytes()),
        no_playable_ROM_build_or_gameplay_claim=True,full_goal_complete=False))
    (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').write_bytes(target)
    print('Bounded168-byte runtime and source-owned52-byte strings pass;all old contracts retained.',flush=True)
    fn=prior_scope.scope
    scoped=FunctionType(fn.__code__,{**fn.__globals__,'new':new,'ROOT':ROOT},fn.__name__,fn.__defaults__,fn.__closure__)
    scoped(target)
    proof=read(ROOT/'scope_proof.json')
    proof.update(dict(new_ordinary_IDs=list(new.ORDINARY),new_yes_no_IDs=list(new.YES_NO),new_queued_ordinary_tables=[0x021180E0],
        table_used_bytes=new.TABLE_USED,table_alignment_bytes=2,alignment_byte=None,
        twelve_phrase_indices_bytes=24,complete_luxury_goods_including_NUL_bytes=13,
        luxury_goods_source_owned_external_pointer=new.LUXURY_GOODS,
        gate_instructions_byte_identical_only_table_literal_moves=True,
        verifier_function_source_sha256=sha(inspect.getsource(fn).encode()),verifier_module_sha256=sha(Path(prior_scope.__file__).read_bytes())))
    save(ROOT/'scope_proof.json',proof)
    def make(source,changed=False,raw=None):
        cpu=prepared(source)
        if raw is not None:cpu.mem_write(BASE,raw)
        return cpu
    source=inspect.getsource(old_status.field_contracts)
    source=source.replace('u.emu_start(runtime.STATUS,STOP','u.emu_start(runtime.STATUS|1,STOP')
    source=source.replace('STACK-BASE-32:STACK-BASE','STACK-BASE-36:STACK-BASE')
    env={**old_status.__dict__,'runtime':new.bank,'make':make,'ROOT':Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(source,__file__,'exec'),env)
    cases=env['field_contracts'](target);assert len(cases)==140
    save(ROOT/'status_contracts.json',dict(count=140,cases=cases,
        all_whole8MiB_guards_original_status_labels_and_registers_SP_LR_exact=True,effective_verifier_sha256=sha(source.encode())))
    print('140 complete status/8MiB/ABI contracts pass.',flush=True)
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inn_v801_context/frame_004000_arm9_ram.bin').read_bytes()
    cpu=machine(target);cpu.mem_write(BASE,raw)
    for at,data in changes.items():
        assert raw[at-BASE:at-BASE+len(data)]==arm[at-BASE:at-BASE+len(data)]
        cpu.mem_write(at,data)
    event=0x02450000;times=[]
    for now in range(12):
        for then in range(12):
            cpu.mem_write(event,bytes(8)+bytes([then])+bytes(3))
            call(cpu,0x5CA8C,(0,event,now))
            p=cpu.reg_read(UC_ARM_REG_R0);actual=bytes(cpu.mem_read(p,128)).split(b'\0')[0]
            delta=(now-then)%12
            num=str(delta).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')
            expected=b'This month' if delta==0 else b'Last month' if delta==1 else num+b' months ago'
            assert actual==expected and len(actual)+1<=128
            times.append(dict(current_month=now,event_month=then,elapsed_months=delta,text_hex=actual.hex(),text=actual.decode('cp932')))
    for pointer,text in ((new.LAST_MONTH,b'Last month'),(new.THIS_MONTH,b'This month'),(new.MONTHS_AGO,b'%s months ago'),(new.LUXURY_GOODS,b'luxury goods')):
        assert target[pointer-BASE:pointer-BASE+len(text)+1]==text+b'\0'
        call(cpu,0xCED28,(pointer,));assert cpu.reg_read(UC_ARM_REG_R0)==len(text)
    save(ROOT/'complete_month_phrases.json',dict(cases=times,count=144,
        original_time_provider_and_full_width_number_formatter_unchanged=True,all_complete_strings_have_owned_NULs=True,
        actual_revised_inn_dialogue_and_fonts_pending=True,full_goal_complete=False))
    print('144 original calendar/month cases now produce complete month phrases;actual revised dialogue/fonts still pending.',flush=True)


if __name__=='__main__':main()
