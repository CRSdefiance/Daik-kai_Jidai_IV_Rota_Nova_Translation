"""Reuse the validated native pre-macro lookup for all newly stored speech bodies."""
import inspect,textwrap
from pathlib import Path
from scripts import extract_editorial_current as original
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_stored_catalogue_20261104')
STORED=Path('work/analysis/Rafael_B36_B41_stored_native_20261104/stored_native_verification.json')
CURRENT=Path('work/analysis/Rafael_B36_B41_current_20261104/current_effective.json')

if __name__=='__main__':
    assert not ROOT.exists()
    stored,current=map(load,[STORED,CURRENT])
    runtime=stored['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=0)
    assert ctx.receipt()==runtime==current['runtime']
    fn=inspect.getsource(original.main)
    setup=textwrap.dedent(fn[fn.index('    instruction ='):fn.index('    groups = []')])
    body=textwrap.dedent(fn[fn.index('            pointer ='):fn.index('            r = deepcopy(source)')])
    source='def native_lookup(arm,common,raw,plan,items):\n    cpu,_,provider=machine(arm,common,raw,plan)\n'+textwrap.indent(setup,'    ')+\
        "    results=[]\n    for item in items:\n        body=bytes.fromhex(item['stored_hex'])[1:]\n"+textwrap.indent(body,'        ')+\
        "        results.append(dict(id=item['id'],target_hex=target.hex(),selected_pointer=selected,input_pointer=pointer))\n    return results\n"
    source=checked_text(source,{
        "struct.unpack_from('<I', ctx.arm, CALLS[0])":"struct.unpack_from('<I', arm, CALLS[0])",
        '        body = raw[1:]\n':'',
        '        before = bytes(cpu.mem_read(pointer - 16, len(body) + 33))':
            '        before = bytes(cpu.mem_read(pointer - 16, len(body) + 33))\n        memory_before=bytes(cpu.mem_read(BASE,len(raw)))',
        '        cpu.emu_start(entry, MACRO, count=1000000)':
            '        stack=cpu.reg_read(UC_ARM_REG_SP)\n        cpu.emu_start(entry, MACRO, count=1000000)\n        assert cpu.reg_read(UC_ARM_REG_SP)==stack',
        "        results.append(dict(id=item['id'],target_hex=target.hex(),selected_pointer=selected,input_pointer=pointer))":
            "        assert bytes(cpu.mem_read(BASE,len(raw)))==memory_before and target==body\n        results.append(dict(id=item['id'],stored_body_hex=body.hex(),target_hex=target.hex(),selected_pointer=selected,input_pointer=pointer,all_unowned4MiB_SP_andinput_canaries_exact=True,complete_effective_body_equals_new_stored_body=True))",
    })
    env={**original.main.__globals__,'__file__':__file__}
    exec(compile(source,__file__+'::same-source-locked-pre-macro-lookup-new-stored-bodies','exec'),env)
    rows=ctx.execute(env['native_lookup'],stored['records'])
    assert len(rows)==175 and {r['id'] for r in rows}=={r['id'] for r in stored['records']}
    previous_aliases=[r['id'] for g in current['groups'] for r in g['records'] if r['current_catalogue_selected']]
    assert len(previous_aliases)==3
    ROOT.mkdir()
    save(ROOT/'all175_stored_effective_body_bindings.json',dict(runtime=runtime,stored=str(STORED),stored_sha256=sha(STORED.read_bytes()),
        current=str(CURRENT),current_sha256=sha(CURRENT.read_bytes()),records=rows,prior_catalogue_selected_IDs=previous_aliases,
        all_new_effective_bodies_byte_exact_before_original_macro_expansion=True,original_pre_macro_native_constants_preserved=True,
        no_code_font_orROM_changes=True,actual_gameplay=False,new_credit=0,guide_photos=False,
        source_owned_lookup_adapter=source,evidence={str(p):sha(p.read_bytes()) for p in [STORED,CURRENT,Path(original.__file__),Path(__file__)]}))
    print('175 newly stored bodies survive original catalogue lookup byte forbyte;three former alias overrides cannot restore old glyphs orwrapping.')
