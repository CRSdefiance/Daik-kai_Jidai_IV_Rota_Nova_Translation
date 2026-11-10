"""Bind scoped names/items andfour default macros on the fresh current Maria context."""
import inspect
import struct
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B169_contextual_v1 import fields, getter
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.execute_map_entity_tooltip_copy import STACK, STOP

ROOT = Path('work/Maria_B0_B32_clean_20261109')


def main():
    out = ROOT / 'scoped_names_items_macros_reference_v1.json'
    assert not out.exists()
    drafts_path = ROOT / 'all301_clean_meanings_andindependent_drafts_v1.json'
    current_path = ROOT / 'current_v1/current_effective.json'
    drafts, current = map(load, [drafts_path, current_path])
    ctx = RegisteredRuntime(current['runtime']['release_proof'], current['runtime']['startup_proof'], captain=3)
    assert ctx.receipt() == current['runtime']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    actors = sorted({r['source_selector'] for r in drafts['records'] if r.get('source_selector',254)<207} | {31,42})
    code = checked_text(inspect.getsource(getter), {'for ident in [2,4,13,23,109]:': 'for ident in ACTORS:'})
    env = {**getter.__globals__, 'ACTORS': actors}
    exec(compile(code, __file__+'::original-intrinsic-getters-current-Maria-boundary', 'exec'), env)
    names = ctx.execute(env['names'])
    assert len(names['rows']) == 2*len(actors)
    bindings = []
    for actor in actors:
        consumers = [r for r in names['rows'] if r['actor_ID']==actor]
        assert {r['consumer'] for r in consumers} == {'progressive-nameplate','full-catalogue'}
        bindings.append(dict(actor_ID=actor, source_andcurrent_fields=fields(actor,clean,ctx),
            current_consumers=consumers, context_record_ids=[r['id'] for r in drafts['records'] if r.get('source_selector')==actor],
            referenced_in_speech_not_static_speaker_in_this_scope=actor in [31,42],
            name_localization_andfresh_display_approval_pending=True))
    labels_path = Path('translations/all_item_names_arm9_v1.json')
    labels = load(labels_path)['records']
    items = []
    for offset, expected in [(1172848,'血塗られたシャムシール'),(1173136,'妖刀村正')]:
        source_pointer, current_pointer = [struct.unpack_from('<I', data, offset)[0] for data in [clean,ctx.arm]]
        source, target = string(clean,source_pointer), string(ctx.raw,current_pointer)
        record = next(r for r in labels if r.get('offset')==offset)
        assert source['text']==expected and target['text']==record['english']
        items.append(dict(pointer_field_offset=offset,source=source,current=target,registered_record=record['id']))
    cpu, get, _ = ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    assert get(0x7F244)==3
    macros = []
    input_pointer, output_pointer = 0x02430020, 0x02431020
    for token in ['FI','FA','FO','FU']:
        cpu.mem_write(input_pointer-32,b'\xa5'*640)
        cpu.mem_write(input_pointer,token.encode()+b'\0')
        before = bytes(cpu.mem_read(input_pointer-32,640))
        cpu.mem_write(output_pointer-32,b'\xa5'*1088)
        for register,value in [(UC_ARM_REG_R0,output_pointer),(UC_ARM_REG_R1,input_pointer),(UC_ARM_REG_R2,0),
            (UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP)]:
            cpu.reg_write(register,value)
        cpu.emu_start(0x02053914,STOP,count=1000000)
        assert cpu.reg_read(UC_ARM_REG_PC)==STOP and cpu.reg_read(UC_ARM_REG_SP)==STACK
        assert cpu.reg_read(UC_ARM_REG_R0)==0
        raw = bytes(cpu.mem_read(output_pointer,1024)).split(b'\0')[0]
        assert raw and len(raw)<1024
        assert bytes(cpu.mem_read(input_pointer-32,640))==before
        assert bytes(cpu.mem_read(output_pointer-32,1088))==b'\xa5'*32+raw+b'\0'+b'\xa5'*(1055-len(raw))
        macros.append(dict(token=token,text=raw.decode('cp932'),hex=raw.hex(),bytes=len(raw),
            original_expander_no_getter_bridges=True,complete_output_NUL_input_andstack_guards_pass=True,
            scope='one aligned default-name call on current captain3; not arbitrary custom-name or all-alignment requalification'))
    assert bytes(cpu.mem_read(ctx.actor_root,0x1A04))==ctx.actor_bytes
    ctx.calls.clear()
    save(out,dict(runtime=ctx.receipt(),scoped_actors=len(actors),original_native_name_getters=2*len(actors),
        records=bindings,registered_item_names=items,default_macro_cases=macros,
        names_andterms_reference_only_not_editorial_orfont_approval=True,
        no_role214_assignment_orfuture_roster_inferred=True,no_global207_name_approval=True,
        all301_comparisons_separate_from_binding_evidence=True,
        no_ROM_orregistered_layer_changes=True,new_credit=0,
        evidence={str(p):digest(p) for p in [drafts_path,current_path,labels_path,Path(__file__)]}))
    print('Bound',len(actors),'scoped actors/',2*len(actors),'current getters;two registered items;four current Maria macro cases.')
    for row in bindings:
        print(row['actor_ID'],[(r['consumer'],r['text']) for r in row['current_consumers']])
    print('ITEMS',[(r['source']['text'],r['current']['text']) for r in items])
    print('MACROS',[(r['token'],r['text']) for r in macros])


if __name__=='__main__':
    main()
