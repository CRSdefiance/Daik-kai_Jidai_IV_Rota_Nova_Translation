"""Preserve the executed B49 controls producer;derive a trusted independent callable reader."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Hodram_B49_controls_tools_v8440')
SOURCE=Path('scripts/prove_Hodram_B49_controls_v8401d.py')
TARGET=Path('dk4tool/patch/hodram_B49_controls_v1.py')

if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists();text=SOURCE.read_text(encoding='utf8')
    prefix=text[text.index("if __name__=='__main__':"):text.index("    ns={**inherited")]
    replacement='''def check_controls(data,rows,parent,reference,rebuilt,native,load,require):
    mapping,current,source,display,stored=[data[k] for k in ['relocation','current','source_controls','source_display','stored']]
    assert stored['relocation_sha256']==sha(MAP.read_bytes())
    image=parent;assert sha(bytes(image.rom.save()))==mapping['candidate_sha256']
    g=mapping['groups'][0];block=rebuilt['target_block'];assert sha(block)==g['target_block_sha256']==stored['research_block_sha256']
    assert image.read_file('/__arm9__.bin')==reference.read_file('/__arm9__.bin')
    trusted=load(CONTROLS)
    require(sha(CONTROLS.read_bytes())==TRUSTED[str(CONTROLS)],'trusted original source control artifact')
    for key in ['source_owned_entry_adapter','source_owned_skip_probe','source_owned_query_probe']:
        require(source[key]==trusted[key],'exact trusted original control adapter:'+key)
    trusted_adapter('dispatch',display['source_owned_dispatch_adapters']);trusted_adapter('macro_body',display['source_owned_macro_body_adapter'])
    trusted_adapter('picture',source['source_owned_picture_adapter']);trusted_adapter('seeded_end',source['source_owned_seeded_end_adapter'])
'''
    suffix=text[text.index("    save(ROOT/'stored_controls.json'"):]
    final='''    require(catalogue==data['controls']['registered_current_catalogue_binding'],'complete current native catalogue binding')
    for key,actual in [('final_dispatches',dispatches),('original_nonrelative_nonspeech_nonmenu_control_maps',controls),('relocated_relative_cases',branches),('relocated_query_cases',queries),('relocated_picture_andhide_boundary_cases',pictures),('normal_seeded_ends',ends)]:
        require(data['controls'][key]==actual,'every independent stored control field:'+key)
    for dispatch in dispatches:
        boundary=next(b for b in dispatch['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if dispatch['final_stored_hex'].startswith('fe') else 'unexecuted-progressive-body'))
        require(boundary['text_hex']==native['bodies']['revised_English'][dispatch['id']]['expanded_body'].hex(),'fresh independently computed native body expansion:'+dispatch['id'])
    context_temporary.cleanup()
    return dict(independent_final_dispatches=len(dispatches),original_null_FE_calls=1,relative_sites=len(branches),native_relative_cases=sum(len(r['cases']) for r in branches),raw_query_cases=len(queries),picture_hide_boundaries=len(pictures),nonrelative_nonspeech_nonmenu_controls=len(controls),normal_seeded_ends=len(ends),original_EV1_entries=len(events),opaque_structural_decode_pairs=len(opaque),no_new_actual_scene_effect_semantics_earned_inventory_orouter_eligibility_claim=True,new_emulator_runs=0)
'''
    extra='''    en=dict(native_entry.__globals__);exec(compile(source['source_owned_entry_adapter'],__file__+'::trusted-entry','exec'),en)
    sk=dict(native_skip.__globals__);exec(compile(source['source_owned_skip_probe'],__file__+'::trusted-skip','exec'),sk)
    qp=dict(probe.__globals__);exec(compile(source['source_owned_query_probe'],__file__+'::trusted-query','exec'),qp)
    events=source['source_event_records'];assert [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in events]==[(48,48,[]),(49,49,[48])]
    entry=ctx.execute(en['native_entry'],image.read_file('/data/EV1.DK4'),events);ctx.machines.pop();require(entry==source['original_EV1_entry'],'original EV1 getter fields for prerequisite48/event49')
    branches=[];byoffset={c['offset']:c for c in g['all_target_commands']};boundaries=set(byoffset)|{g['target_logical_end']}
    for fix,declared in zip(g['relative_fixups'],g['relocated_skip_cases'],strict=True):
        result=ctx.execute(sk['native_skip'],block,byoffset[fix['new_offset']]);ctx.machines.pop()
        require(result==declared and all(c['next_offset'] in boundaries and c['next_offset']==(fix['new_matched_skip_target'] if c['taken'] else fix['new_unmatched_next']) for c in result['cases']),'fresh relocated native branch endpoints/ABI/value fields')
        branches.append(result)
    opaque=[];cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for declared in source['isolated_opaque_effect_structural_pairs']:
        raw=bytes.fromhex(declared['source_command_hex']);isolated=b'CS\\0\\1'+struct.pack('<H',len(raw))+bytes(2)+raw
        versions=[]
        for label,code in [('clean-decoder',cleanarm),('current-decoder',image.read_file('/__arm9__.bin'))]:versions.append(dict(version=label,**walk(code,isolated)))
        require(versions==declared['versions'],'original paired opaque structural decoder fields without invented effect semantics');opaque.append(versions)
    require(len(opaque)==7,'all seven original opaque effects')
'''
    result=derive(SOURCE,TARGET,{
        'from pathlib import Path':'from pathlib import Path\nimport struct\nfrom tempfile import TemporaryDirectory\nfrom dk4tool.patch.hodram_B49_native_guards_v1 import trusted_adapter,CONTROLS,TRUSTED\nfrom scripts.prove_lil_B234_entry_v7576 import native_entry\nfrom scripts.prove_Maria_story_branches_v7741 import native_skip\nfrom scripts.research_wedding_command_v676 import walk',
        prefix:replacement,
        "    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')":"    context_temporary=TemporaryDirectory(prefix='Hodram-B49-controls-');ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',Path(context_temporary.name)/'current_context')\n"+extra,
        "result=ctx.execute(probe,block,after)":"result=ctx.execute(qp['probe'],block,after)",
        suffix:final,
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,all_native_addresses_values_andmultiplicity_preserved=True,producer8401d_preserved=True,new_credit=0))
    print('Prepared independent original B49 control reader;no emulator replay.')
