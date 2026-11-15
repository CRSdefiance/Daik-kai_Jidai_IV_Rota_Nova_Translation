"""Current-bound B190 dispatch, RNG, UI and all mapped structural paths."""
import itertools
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B190_predicate500_v5330 import probe500
from scripts.prove_lil_B190_C200_v5318 import C200
from scripts.research_wedding_command_v676 import walk
from scripts.prepare_lil_B190_research_v5331 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B190_relocated_controls_v5336')
DOC=Path('translations/lil_B190_editorial_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN);packet=read(doc['source_context'])
    dispatch,control,branch=map(read,[doc['control_contract'],doc['source_effect_and_predicate_contract'],doc['branch_proof']])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==control['candidate_sha256']
    images=[NdsImage.open(p) for p in [PARENT,ROM]]
    assert images[0].read_file('/__arm9__.bin')==images[1].read_file('/__arm9__.bin')
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[190] for im in images]
    spec=plan['blocks'][0];assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dispatch['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](images[1])
    ROOT.mkdir(parents=True)
    ctx=CurrentContext(dispatch['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};dispatches=[]
    for record in spec['text_records']:
        value,at=bytes.fromhex(record['target_hex']),record['new_offset']
        assert new[at:at+len(value)]==value and not any(m in value[1:] for m in [b'FI',b'FA',b'FO'])
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop()
        actor=None if value[0]==254 else rows[record['id']]['source_selector']
        assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==value[1:].hex() and result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        if value[0]==254:assert result['FE_original_null_actor_calls']
        dispatches.append(dict(id=record['id'],new_offset=at,stored_target_hex=value.hex(),**result))
    assert len(dispatches)==17 and sum(r['resolved_actor_ID'] is None for r in dispatches)==1
    original={c['offset']:c for c in packet['blocks'][0]['all_current_native_commands']}
    leaf_source={c['offset']:c for c in control['all6_source_current_nonrelative_nonspeech_leaves']}
    leaves=[];predicates=[];uis=[];effects=[]
    for c in spec['command_map']:
        if c['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        a,b=c['old_offset'],c['new_offset'];raw=old[a:a+c['old_extent']]
        assert raw==new[b:b+c['new_extent']] and raw.hex()==leaf_source[a]['source_current_hex']
        assert c['word']==leaf_source[a]['word'] and len(raw)==leaf_source[a]['native_extent']
        leaves.append(dict(word=c['word'],old_offset=a,new_offset=b,source_current_target_hex=raw.hex()))
        mapped={**original[a],'offset':b}
        if c['word'] in [0x8000,0xC200]:
            pairs=[];fn=probe500 if c['word']==0x8000 else C200
            for label,block,command in [('current',old,original[a]),('relocated',new,mapped)]:
                pairs.append(dict(version=label,**ctx.execute(fn,block,command)));ctx.machines.pop()
            if c['word']==0x8000:
                assert a%4==0 and b%4==0
                for key in ['native_result','before_seed','after_seed','roll','original_native_seed_writes','original_bounded_random_calls']:
                    assert pairs[0][key]==pairs[1][key]
                assert all(p['unforced_current_snapshot'] and p['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch'] for p in pairs)
                predicates.append(dict(old_offset=a,new_offset=b,cases=pairs))
            else:
                assert pairs[0]['source_owned_UI_request_words']==pairs[1]['source_owned_UI_request_words']==[1,2,13,0,0,0,1]
                assert pairs[0]['source_owned_UI_writes']==pairs[1]['source_owned_UI_writes']
                uis.append(dict(old_offset=a,new_offset=b,cases=pairs))
        elif c['word']==0xA000:
            isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;pairs=[]
            for label,image in zip(['current','relocated'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
                pairs.append(dict(version=label,**result))
            assert pairs[0]['rows']==pairs[1]['rows'] and pairs[0]['opaque_effect_bridges']==pairs[1]['opaque_effect_bridges']
            effects.append(dict(old_offset=a,new_offset=b,cases=pairs,effect_body_bridged_not_actual_state_execution=True))
    assert len(leaves)==6 and len(predicates)==1 and len(uis)==1 and len(effects)==3 and not ctx.machines
    mapping={c['old_offset']:c['new_offset'] for c in spec['command_map']}
    reverse={b:a for a,b in mapping.items()};new_commands={c['new_offset']:c for c in spec['command_map']}
    spoken_at={r['source_reference']['header_offset']:r['source_record_index'] for r in packet['records']}
    def path(values,relocated):
        cursor,last=8,0;visited=[];spoken=[];effects=[];ui=[];used=[]
        while True:
            source_at=reverse[cursor] if relocated else cursor
            assert source_at not in visited;visited.append(source_at)
            c=new_commands[cursor] if relocated else original[cursor];word=c['word']
            if word==0:return dict(results=list(values),source_command_offsets=visited,spoken_record_indices=spoken,A000_offsets=effects,C200_offsets=ui,predicate_results_used=used,source_end_offset=source_at)
            if word in [0x100,0x200,0x300,0x400]:
                if relocated:
                    found=[r for r in spec['target_native_skip_cases'] if r['new_offset']==cursor and r['last_result']==last]
                    assert len(found)==1;cursor+=found[0]['native_extent']
                else:
                    found=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==last]
                    assert len(found)==1;cursor=found[0]['original_next_command_offset']
                continue
            if word==0x8000:last=values[[8].index(source_at)];used.append(dict(source_offset=source_at,value=last))
            elif word==0x4000:spoken.append(spoken_at[source_at])
            elif word==0xA000:effects.append(source_at)
            elif word==0xC200:ui.append(source_at)
            cursor+=c['new_extent'] if relocated else c['native_extent']
    paths=[]
    for values in itertools.product([0,1,2,3,0xFFFFFFFF],repeat=1):
        before,after=path(values,False),path(values,True);assert before==after
        assert after['spoken_record_indices']==[r['source_record_index'] for r in packet['records']]
        assert len(after['A000_offsets'])==1 and after['C200_offsets']==[600] and after['source_end_offset']==602
        paths.append(after)
    assert len(paths)==5 and set.union(*(set(p['A000_offsets']) for p in paths))=={28,40,52}
    paths_to_hash=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(doc['branch_proof']),Path(__file__)]
    save(ROOT/'all17_dispatches_one_RNG_predicate_three_effects_C200_and5_mapped_paths.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        relocated_dispatch_cases=dispatches,all6_exact_nonrelative_leaves=leaves,predicate_pairs=predicates,C200_pairs=uis,A000_structural_pairs=effects,
        all5_source_and_relocated_structural_paths_identical=paths,all6_native_relative_sites_and30_skip_cases_bound=True,
        whole_exchange_all17_speeches_and_three_alternative_effects_preserved=True,
        unforced_CPU_snapshot_seed_transitions_not_actual_emulator_outcomes=True,source_A000_semantics_not_inferred=True,
        opaque_effect_bodies_and_actual_parent_return_unexecuted_by_this_probe=True,registered_catalog_binding=binding,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths_to_hash},actual_selected_B190_IDs=[],new_emulator_runs=0,new_review_credit=0,
        no_registry_orcompletion_change=True,full_goal_complete=False))
    print('B190 relocation:17 dispatches,6 exact leaves,1 unforced RNG predicate pair,3 opaque effect pairs,C200 and5 structural paths pass. Actual scene pending.')
