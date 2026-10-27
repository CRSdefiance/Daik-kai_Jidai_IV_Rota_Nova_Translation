"""Bind ten relocated dispatches, three exact leaves and paired original control paths."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.research_wedding_command_v676 import walk
from scripts.prepare_lil_B176_research_v4579 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B176_relocated_controls_v4584')
DOC=Path('translations/lil_B176_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN)
    packet=read(doc['source_context'])
    dispatch,control=read(doc['control_contract']),read(doc['source_effect_and_predicate_contract'])
    images=[NdsImage.open(p) for p in [PARENT,ROM]]
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[176] for im in images]
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
        dispatches.append(dict(id=record['id'],block=176,new_offset=at,stored_target_hex=value.hex(),**result))
    old_leaves={r['offset']:r for r in control['all3_source_current_nonrelative_nonspeech_leaves']}
    for command in spec['command_map']:
        if command['word']==0x4000:
            continue
        a,b=command['old_offset'],command['new_offset']
        previous,value=old[a:a+command['old_extent']],new[b:b+command['new_extent']]
        assert previous==value and old_leaves[a]['source_current_hex']==value.hex()
        assert old_leaves[a]['word']==command['word'] and old_leaves[a]['native_extent']==len(value)
        leaves.append(dict(block=176,word=command['word'],old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if command['word']==0xC200:
            pair=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                cmd=dict(offset=at,word=0xC200,native_extent=2,whole_command_hex=value.hex())
                pair.append(dict(version=label,**ctx.execute(C200,block,cmd)));ctx.machines.pop()
            assert pair[0]['source_owned_UI_request_words']==pair[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            assert pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes']
            uis.append(dict(source_offset=a,target_offset=b,cases=pair))
        if command['word']==0xA000:
            assert a==b==8 and value.hex()=='00a0ffff010a0da1'
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
    assert len(dispatches)==10 and sum(d['resolved_actor_ID'] is None for d in dispatches)==1
    assert len(leaves)==3 and len(uis)==len(effects)==1 and not ctx.machines
    assert [(r['word'],r['old_offset'],r['new_offset']) for r in leaves]==[(0xA000,8,8),(0xC200,384,398),(0,386,400)]
    assert len(spec['command_map'])==13 and not spec['relative_skip_fixups'] and not spec['target_native_skip_cases']
    assert not spec['original2000_pause_and_resume_maps']
    paths=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all10_progressive_FE_dispatches_A000_C200_pairs_and3_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all3_source_current_target_nonrelative_nonspeech_leaves=leaves,
        relocated_C200_pairs=uis,relocated_A000_structural_pairs=effects,
        all9_progressive_static_actors1_impersonal_null_actor_FE_and_no_FI_FA_FO_exact=True,
        original_no_relative_predicate_pause_resources_presentations_or_typed_objects_preserved=True,
        complete_linear_structural_command_map=spec['command_map'],single_end_preserved_actual_reachability_pending=True,
        source_A000_packed_operand_semantics_not_inferred=True,A000_full_body_and_actual_scene_unexecuted_by_this_probe=True,
        later_older_record0D_reaudit_stays_open=True,registered_catalog_binding=binding,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B176_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('Ten relocated dispatches,nine progressive/one impersonal FE;three exact leaves,paired A000 structural/C200 paths and single end pass. Actual scene pending.')
