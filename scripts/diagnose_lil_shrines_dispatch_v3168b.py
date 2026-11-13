"""Current source-bound speech,FE,dynamic actor-style dispatch and predicates."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Shrines_Temples_controls_v3168b')
SOURCE=Path('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json')
INPUT=Path('work/analysis/lil_Shrines_Temples_voices_v3167/current_native_input.json')
BASE=0x02000000

def install_boundaries(cpu):
    seen=[];macros=[]
    def boundary(u,pc,size,unused):
        if pc==BASE+0x940B0:
            seen.append(dict(boundary=pc,kind='unexecuted-UI-preparation'))
        else:
            first,second=u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1)
            pointer=first if pc==BASE+0x5473C else second
            seen.append(dict(boundary=pc,kind='unexecuted-FE-modal-body' if pc==BASE+0x5473C else 'unexecuted-progressive-body',actor_object=None if pc==BASE+0x5473C else first,FE_incidental_r1=second if pc==BASE+0x5473C else None,text_hex=bytes(u.mem_read(pointer,2048)).split(bytes([0]))[0].hex()))
        u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hooks=[cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+pc,end=BASE+pc)for pc in [0x940B0,0x54020,0x5473C,0x53AC4]]
    hooks.append(cpu.hook_add(UC_HOOK_CODE,lambda u,pc,z,d:macros.append(dict(address=pc,args=[u.reg_read(r)for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]])),begin=BASE+0x24310,end=BASE+0x24310))
    return seen,macros,hooks

def dispatch(arm,common,raw,plan,prefix,body):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);captain=get(0x7F244);selected=get(0x2434C,prefix)
    actor=None if prefix==254 else root+0x19E4 if selected==captain else root+4+32*selected
    assert prefix==254 or 0<=selected<207
    inp=0x02660000;cpu.mem_write(inp-16,b'\xA5'*2080);cpu.mem_write(inp,body+bytes([0]));guard=bytes(cpu.mem_read(inp-16,2080));before=bytes(cpu.mem_read(BASE,0x400000))
    seen,macros,hooks=install_boundaries(cpu)
    try:call(cpu,0x2425C,(prefix,inp),instruction_limit=500000)
    finally:
        for hook in hooks:cpu.hook_del(hook)
    assert len(seen)==2 and seen[0]['boundary']==BASE+0x940B0 and seen[1]['boundary']==BASE+(0x5473C if prefix==254 else 0x54020) and seen[1]['actor_object']==actor
    expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
    matches=seen[1]['text_hex']==expected.hex()
    if prefix==254:assert len(macros)==1 and macros[0]['args'][2]==0
    assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(inp-16,2080))==guard
    return dict(expected_output_hex=expected.hex(),macro_output_matches_expected=matches,source_selector=prefix,resolved_actor_ID=None if prefix==254 else selected,source_voice_class=None if actor is None else get(0x7E988,actor),boundaries=seen,FE_original_null_actor_calls=macros,all4MiB_actor_role_RNG_input_and_ABI_guards_exact=True,current_executed_instruction_addresses=len(provider.executed_current))

# call is resolved here;CurrentContext replaces only machine,not original native ABI.
from scripts.native_call_abi_v764 import call

def whole_style_command(arm,common,raw,plan,block,command):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);captain=get(0x7F244);at=command['offset'];prefix=block[at+19];selected=get(0x2434C,prefix)
    assert 0<=selected<207
    actor=root+0x19E4 if selected==captain else root+4+32*selected;style=get(0x7E988,actor);assert 0<=style<8
    inp,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    cpu.mem_write(inp-16,b'\xA5'*(len(block)+32));cpu.mem_write(inp,block);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,inp+at,0,0));guard=bytes(cpu.mem_read(owner-16,64));cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4));before=bytes(cpu.mem_read(BASE,0x400000))
    seen,macros,hooks=install_boundaries(cpu)
    try:call(cpu,0x2A510,(result,owner,length,0xFFFFFFFF),instruction_limit=500000)
    finally:
        for hook in hooks:cpu.hook_del(hook)
    extent=struct.unpack('<I',cpu.mem_read(length,4))[0];assert extent==command['native_extent'] and struct.unpack('<6I',cpu.mem_read(result,24))==(3,0,0,0,0,0)
    ptr=at+20+struct.unpack_from('<H',block,at+2+style*2)[0];body=block[ptr:block.index(bytes([0]),ptr)]
    assert len(seen)==2 and seen[1]['boundary']==BASE+0x54020 and seen[1]['actor_object']==actor and seen[1]['text_hex']==body.replace(b'FI',b'Lil').hex() and not macros
    assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(inp,len(block)))==block and bytes(cpu.mem_read(owner-16,64))==guard
    for p in [inp-16,inp+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
    return dict(source_selector=prefix,resolved_actor_ID=selected,original_actor_style=style,source_text_offset=ptr,original_native_extent=extent,boundaries=seen,all4MiB_role_actor_RNG_stream_owner_result_and_ABI_guards_exact=True,current_executed_instruction_addresses=len(provider.executed_current),original_unassigned_role_fallback_not_a_fixture=True)

def catalog_style_getters(arm,common,raw,plan,objects):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);captain=get(0x7F244);before=bytes(cpu.mem_read(BASE,0x400000));rows=[]
    for obj in objects:
        for version in obj['versions']:
            value=bytes.fromhex(version['command_hex']);inp,owner=0x02660000,0x02662000
            cpu.mem_write(inp-16,b'\xA5'*(len(value)+32));cpu.mem_write(inp,value);cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,inp,0,0));guard=bytes(cpu.mem_read(owner-16,64))
            for ident in range(207):
                actor=root+0x19E4 if ident==captain else root+4+32*ident;style=get(0x7E988,actor);ptr=get(0x2A154,owner,style)
                expected=next(r for r in version['style_slots']if r['style_index']==style);assert ptr==inp+expected['relative_offset']
                assert bytes(cpu.mem_read(ptr,len(bytes.fromhex(expected['hex']))+1))==bytes.fromhex(expected['hex'])+bytes([0])
                rows.append(dict(block=obj['block'],command_offset=obj['command_offset'],version=version['version'],catalog_actor_ID=ident,original_actor_style=style,source_text_relative_offset=ptr-inp))
            assert bytes(cpu.mem_read(owner-16,64))==guard and bytes(cpu.mem_read(inp,len(value)))==value
            for p in [inp-16,inp+len(value)]:assert bytes(cpu.mem_read(p,16))==b'\xA5'*16
    assert bytes(cpu.mem_read(BASE,0x400000))==before and len(rows)==3312 and {r['original_actor_style']for r in rows}==set(range(8))
    return dict(cases=rows,all4MiB_role_actor_RNG_owner_and_input_guards_exact=True,no_actor_assigned_to_dynamic_role_or_forced_scene=True,current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');image=NdsImage.open(packet['current_ROM']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    cases=[]
    for row in packet['records']+packet['typed_actor_style_records']:
        prefix=row.get('source_selector');is_speech=row['kind']!='typed-4100-actor-style-alternative'
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            value=bytes.fromhex(row[key]);body=value[1:]if is_speech else value
            result=ctx.execute(dispatch,prefix,body);ctx.machines.pop()
            if not result['macro_output_matches_expected']:
                save(ROOT/'first_dispatch_mismatch.json',dict(id=row['id'],version=version,kind=row['kind'],body_hex=body.hex(),body_text=body.decode('cp932'),result=result,previous_passed_cases=len(cases),producer_sha256=sha(Path(__file__).read_bytes()),editorial_credit=0))
                print(row['id'],version,'INPUT',repr(body.decode('cp932')),'ACTUAL',repr(bytes.fromhex(result['boundaries'][1]['text_hex']).decode('cp932')),'EXPECTED',repr(bytes.fromhex(result['expected_output_hex']).decode('cp932')))
                raise AssertionError('Diagnostic retained;source current dispatcher mismatch')
            cases.append(dict(id=row['id'],version=version,**result))
    assert len(cases)==440 and sum(c['source_selector']==254 for c in cases)==60
    whole=[];objects=[o for b in packet['blocks']for o in b['actor_style_objects']]
    for b in packet['blocks']:
        for obj in b['actor_style_objects']:
            for version,command in [('clean','source_command'),('current','current_command')]:
                im=NdsImage.open('work/clean.nds')if version=='clean'else image;bb=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[b['block']]
                result=ctx.execute(whole_style_command,bb,obj[command]);ctx.machines.pop();whole.append(dict(block=b['block'],command_offset=obj['command_offset'],version=version,**result))
    assert len(whole)==16
    catalog=ctx.execute(catalog_style_getters,objects);ctx.machines.pop();predicates=[]
    for b in packet['blocks']:
        for c in b['all_current_native_commands']:
            if c['word']not in[0x8000,0x8100]:continue
            result=ctx.execute(predicate,blocks[b['block']],c);ctx.machines.pop();predicates.append(dict(block=b['block'],**result))
    assert len(predicates)==21 and not any(p['original_event_completion_calls']for p in predicates) and not ctx.machines
    save(ROOT/'all235_source_current_dispatch_dynamic_styles_and_predicates.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),speech_and_stored_alternative_dispatch_cases=cases,whole_original4100_command_cases=whole,all207_actor_style_source_pointer_cases=catalog,current_original_predicate_cases=predicates,
        all164speech_complete_preambles_and56_stored_alternatives_have440current_code_dispatch_cases=True,all30_FE_before_fallback208_use5473C_and24310_null_actor=True,all16_original4100_commands_select_the_actual_unforced_D0_actor_style_and_original2425C=True,
        all3312_catalog_getter_cases_cover_every_actor_style_without_role_assignment=True,all21_predicates_preserve_source_operands_results_and_unowned4MiB_with_only_original_alignment_scratch_restored=True,original_event_queries=[],
        four_source_FI_macro_occurrences_preserved_with_Lil_expansion=True,FE_incidental_r1_not_geometry=True,all_original_UI_progressive_FE_panel_bodies_explicit_unexecuted_boundaries=True,
        native_input=str(INPUT),native_input_sha256=sha(INPUT.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        typed_three_option_menus_still_require_original_VM_geometry_fonts_and_sampling_reconciliation=True,no_new_ROMS_registry_ledger_or_editorial_credit=True,actual_selected_Shrines_Temples_IDs=[],new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('440currentdispatch cases/16whole4100commands/3312catalog-style pointers/21predicates/noqueries pass. FEanddynamic sourcecontrols preserved;nativepanels andthree-choice menus stillpending;zero credit.')
