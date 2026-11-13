"""Read-only trace of actual FI/FA virtual getters, preserving the original macro ABI checks."""
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B31_B53_registered_route_context_v8781 import RouteCurrentContext,BASE
from scripts.generic_name_macro_owned_v5886b import expand as original_expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_source_macros_v8797')
DISPLAY=Path('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json')
NAMES=Path('work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json')
INPUT=Path('work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();display,names,inp=map(read,[DISPLAY,NAMES,INPUT]);image=NdsImage.open(inp['current_ROM'])
    arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    # These source spans and call sites were first inspected in the original ARM
    # disassembly; compare whole source/current bytes before observing them.
    start,end=0x53914,0x53AC4;assert arm[start:end]==clean[start:end]
    sites={BASE+0x539D0:('FI','call'),BASE+0x539D4:('FI','returned'),BASE+0x539E4:('FA','call'),BASE+0x539E8:('FA','returned')}
    for pc,(macro,kind) in sites.items():
        if kind=='call':assert arm[pc-BASE:pc-BASE+4]==bytes.fromhex('31ff2fe1')
    original=display['source_owned_progressive_adapter']
    hook="""    macro_trace=[]
    def observe(u,pc,size,unused):
        if pc not in MACRO_SITES:return
        macro,kind=MACRO_SITES[pc]
        if kind=='call':macro_trace.append(dict(macro=macro,kind=kind,PC=pc,actor_object=u.reg_read(UC_ARM_REG_R0),virtual_getter=u.reg_read(UC_ARM_REG_R1)))
        else:
            pointer=u.reg_read(UC_ARM_REG_R0);value=bytes(u.mem_read(pointer,128)).split(b'\\0')[0]
            macro_trace.append(dict(macro=macro,kind=kind,PC=pc,pointer=pointer,value_hex=value.hex(),value=value.decode('cp932')))
    trace_hook=cpu.hook_add(UC_HOOK_CODE,observe)
"""
    adapter=checked_text(original,{
        '    h=cpu.hook_add(UC_HOOK_CODE,lambda':hook+'    h=cpu.hook_add(UC_HOOK_CODE,lambda',
        'finally:cpu.hook_del(h)':'finally:cpu.hook_del(h);cpu.hook_del(trace_hook)',
        'return dict(original_selector=identity':'return dict(native_macro_getter_trace=macro_trace,original_selector=identity',
    })
    env={**original_expand.__globals__,'MACRO_SITES':sites,'UC_ARM_REG_R0':UC_ARM_REG_R0,'UC_ARM_REG_R1':UC_ARM_REG_R1}
    exec(compile(adapter,__file__+'::original-readonly-macro-trace','exec'),env)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    captain=next(r['actor_object'] for r in names['ten_source_selector_voices']['rows'] if r['source_selector']==1)
    vtable=int.from_bytes(ctx.raw[captain-BASE:captain-BASE+4],'little');bindings={}
    for macro,slot,field in [('FI',0x20,'given'),('FA',0x24,'surname')]:
        getter=int.from_bytes(ctx.raw[vtable-BASE+slot:vtable-BASE+slot+4],'little')
        value=next(f for r in names['exact_current_RAM_fields']['rows'] if r['actor_ID']==1 for f in r['fields'] if f['kind']==field)
        row=next(r for r in display['records'] if macro.encode('ascii') in bytes.fromhex(r['source_hex'])[1:])
        body=bytes.fromhex(row['source_hex'])[1:];result=ctx.execute(env['expand'],body,row['source_selector']);ctx.machines.pop()
        calls=[r for r in result['native_macro_getter_trace'] if r['macro']==macro and r['kind']=='call'];returned=[r for r in result['native_macro_getter_trace'] if r['macro']==macro and r['kind']=='returned']
        assert len(calls)==len(returned)==4 and all(r['actor_object']==captain and r['virtual_getter']==getter for r in calls)
        assert all(r['value_hex']==value['actual_current_RAM_string_hex'] for r in returned)
        bindings[macro]=dict(source_ID=row['id'],source_reference=row['source_reference'],source_selector=row['source_selector'],captain_object=captain,
            vtable=vtable,virtual_slot=slot,actual_virtual_getter=getter,original_component=field,default_value=returned[0]['value'],four_original_alignments=result)
    assert not ctx.machines and bindings['FI']['default_value']=='Hodram' and bindings['FA']['default_value']=='Bergstrom'
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);lines=[f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in decoder.disasm(arm[start:end],BASE+start)]
    dis=ROOT/'original_macro_parser_source_current_equal.txt';dis.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'FI_given_FA_surname_original_virtual_getter_trace.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],bindings=bindings,
        entire_original_macro_parser_span=dict(start=start,end=end,sha256=sha(arm[start:end])),disassembly=str(dis),disassembly_sha256=sha(dis.read_bytes()),
        FI_andFA_source_referents_proved_by_original_captain_virtual_slots_not_coincidentally_equal_strings=True,
        FO_has_no_source_occurrence_in_this_batch_not_newly_traced=True,default_values_not_all_custom_name_length_orparity_coverage=True,
        all_original_macro_ABI_scratch_ring_input_output_unowned_memory_guards_preserved=True,
        trace_hooks_read_only_no_original_state_roster_name_orpredicate_forcing=True,
        current_B54_B60_English_dialogue_bodies_unconsulted=True,new_emulator_runs=0,new_credit=0,no_ROM_orledger_change=True,full_goal_complete=False,
        source_owned_traced_adapter=adapter,evidence={str(p):sha(p.read_bytes()) for p in [DISPLAY,NAMES,INPUT,Path(__file__)]}))
    print('Actual source FI->captain given/Hodram andFA->captain surname/Bergstrom proved byvirtualgetter calls/8guarded alignments. No faction-name inference,customname claim,gameplay,ROM orcredit.',flush=True)
