"""Bind final18 Maria dispatched bodies/voices and25 relocated normal ends."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_papal_trade_consumers_v7627b import expanded_zero_macro_body
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.create_Maria_B207_reference_v7698 import ROM,PARENT,PLAN
from scripts.draft_Maria_B207_prose_v7687 import MANUSCRIPT,CONSUMERS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_relocated_controls_v7703')
CONTROLS=Path('work/analysis/maria_B207_controls_v7686b/Maria_CS0101_50_fresh_seeded_ends_two_exact_isolated_effect_reuses.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,consumers,controls,doc=map(read,[PLAN,CONSUMERS,CONTROLS,MANUSCRIPT]);image,parent=NdsImage.open(ROM),NdsImage.open(PARENT)
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256'] and image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')
    g=mapping['groups'][0];block=IlnkContainer.parse(image.read_file(g['file_path'])).blocks[207]
    assert sha(block)==g['research_block_sha256'] and len(block)==1472 and g['research_logical_end']==1470 and block[1470:]==bytes(2) and block[:4]==b'CS\1\1'
    ns={**inherited.__dict__,'CATALOG_LOOKUP':{},'route':3,'route_mask':8}
    for name in ['bind_current_catalog','install_boundaries','dispatch']:exec(compile(consumers['source_owned_dispatch_adapters'][name],__file__+'::Maria-'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image);assert binding['route']==3 and binding['route_mask']==8
    ns['expanded_current_body']=FunctionType(expanded_zero_macro_body.__code__,ns,argdefs=expanded_zero_macro_body.__defaults__)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(doc['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context');rows=[]
    for ref,row in zip(g['text_records'],doc['records'],strict=True):
        at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);prefix=row['source_selector']
        assert block[at:at+len(value)+1]==value+b'\0' and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        result=ctx.execute(ns['dispatch'],prefix,value[1:]);ctx.machines.pop()
        assert result['resolved_actor_ID']==prefix and result['source_voice_class']=={19:7,104:0}[prefix] and result['registered_catalog_match'] is None
        assert next(v for v in result['boundaries'] if v['kind']=='unexecuted-progressive-body')['text_hex']==value[1:].hex()
        rows.append(dict(id=row['id'],file_path=g['file_path'],new_offset=at,target_hex=value.hex(),**result))
    effect=g['original_A000_map'][0];assert effect['source_offset']==1456 and effect['target_offset']==1458 and block[1458:1466].hex()==effect['source_hex']=='00a0ffff6a000110'
    assert len(controls['two_exact_isolated_A000_structural_cases'])==2 and all(c['source_command_hex']==effect['source_hex'] for c in controls['two_exact_isolated_A000_structural_cases'])
    env=dict(end_case.__globals__);exec(compile(controls['source_owned_seeded_end_adapter'],__file__+'::relocated-normal-end','exec'),env)
    end=g['complete_end_map'][0]['target_offset'];assert end==1466 and block[end:end+4]==bytes(4) and block[end+4:]==bytes(2)
    ends=[env['end_case'](ctx.arm,block,end,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]
    assert len(rows)==18 and len(ends)==25 and all(not e['flagged_terminal'] and e['native_result']==[0,e['initial_value_word'],0,0,0,0] for e in ends) and not ctx.machines
    save(ROOT/'Maria18_final_dispatches_two_effect_reuses25_relocated_seeded_ends.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),current_name_catalogue_binding=binding,dispatch_cases=rows,source_exact_isolated_A000_reuse=controls['two_exact_isolated_A000_structural_cases'],source_A000_offset=1456,target_A000_offset=1458,target_normal_end_offset1466_four_bytes=True,target_two_byte_storage_tail_separately_bound=True,normal_terminal_seed_cases=ends,all18_complete_preambles_actor_voices_zero_macros_andfinal_body_bytes_bound=True,fresh_relocated_normal_end_cases=25,distinct_CS0101_preserved=True,isolated_opaque_effects_exact_reuse_not_full_VM_item_blessing_orreward_semantics=True,no_ROM_code_RNG_roles_roster_event_funds_orresults_forced=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,optional_scene_gameplay_andregistered_release_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [PLAN,CONSUMERS,CONTROLS,MANUSCRIPT,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('Maria18 final dispatches and25 relocated normal ends pass;A0001456->1458/end1464->1466/two-byte storage tail distinct. Full effects/actual gameplay remain scoped.')
