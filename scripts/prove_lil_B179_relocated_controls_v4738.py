"""Bind fourteen relocated dispatches,two exact leaves,A000 and end;no C200 exists."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.research_wedding_command_v676 import walk
from scripts.prepare_lil_B179_research_v4733 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_relocated_controls_v4738')
DOC=Path('translations/lil_B179_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN)
    packet=read(doc['source_context'])
    dispatch,control=read(doc['control_contract']),read(doc['source_effect_and_predicate_contract'])
    images=[NdsImage.open(p) for p in [PARENT,ROM]]
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[179] for im in images]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==control['candidate_sha256']
    assert images[0].read_file('/__arm9__.bin')==images[1].read_file('/__arm9__.bin')
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dispatch['source_owned_adapters'].items():
        exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](images[1])
    ROOT.mkdir(parents=True)
    ctx=CurrentContext(dispatch['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']}
    spec=plan['blocks'][0]
    assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    dispatches=[];leaves=[];uis=[];effects=[]
    for record in spec['text_records']:
        value,at=bytes.fromhex(record['target_hex']),record['new_offset']
        assert new[at:at+len(value)]==value and not any(m in value[1:] for m in [b'FI',b'FA',b'FO'])
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop()
        actor=None if value[0]==254 else rows[record['id']]['source_selector']
        assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==value[1:].hex()
        assert result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        if value[0]==254:
            assert result['FE_original_null_actor_calls']
        dispatches.append(dict(id=record['id'],block=179,new_offset=at,stored_target_hex=value.hex(),**result))
    old_leaves={r['offset']:r for r in control['all2_source_current_nonrelative_nonspeech_leaves']}
    for command in spec['command_map']:
        if command['word']==0x4000:
            continue
        a,b=command['old_offset'],command['new_offset']
        previous,value=old[a:a+command['old_extent']],new[b:b+command['new_extent']]
        assert previous==value and old_leaves[a]['source_current_hex']==value.hex()
        assert old_leaves[a]['word']==command['word'] and old_leaves[a]['native_extent']==len(value)
        leaves.append(dict(block=179,word=command['word'],old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if command['word']==0xA000:
            assert a==b==8 and value.hex()=='00a0ffff01221da1'
            synthetic=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value
            pair=[]
            for label,image in zip(['current','relocated'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),synthetic)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic)
                assert len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
                pair.append(dict(version=label,**result))
            assert pair[0]['rows']==pair[1]['rows'] and pair[0]['opaque_effect_bridges']==pair[1]['opaque_effect_bridges']
            effects.append(dict(source_offset=a,target_offset=b,cases=pair,
                nondecode_effect_callee_bridged_zero_return_not_body_or_game_state_execution=True))
    assert len(dispatches)==14 and sum(d['resolved_actor_ID'] is None for d in dispatches)==1
    assert len(leaves)==2 and len(uis)==0 and len(effects)==1 and not ctx.machines
    assert [(r['word'],r['old_offset'],r['new_offset']) for r in leaves]==[(0xA000,8,8),(0,508,492)]
    assert len(spec['command_map'])==16 and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases']
    assert not spec['original2000_pause_and_resume_maps']
    paths=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all14_progressive_FE_dispatches_A000_pairs_and2_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all2_source_current_target_nonrelative_nonspeech_leaves=leaves,
        relocated_C200_pairs=uis,relocated_A000_structural_pairs=effects,
        all13_progressive_static_actors1_impersonal_null_actor_FE_and_no_FI_FA_FO_exact=True,
        original_no_relative_predicate_pause_resources_presentations_or_typed_objects_preserved=True,
        complete_linear_structural_command_map=spec['command_map'],single_end_preserved_actual_reachability_pending=True,
        source_A000_packed_operand_semantics_not_inferred=True,A000_full_body_and_actual_scene_unexecuted_by_this_probe=True,
        later_older_record0D_reaudit_stays_open=True,registered_catalog_binding=binding,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B179_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('Fourteen relocated dispatches,thirteen progressive/one impersonal FE;two exact leaves,paired A000 structural paths and single end pass. No C200. Actual scene pending.')
