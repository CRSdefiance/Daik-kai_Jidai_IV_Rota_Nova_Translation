"""Check all final consumers, typed aliases and both changed operand alignments without forcing state."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.create_lil_B214_reference_v6718 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_relocated_controls_v6721');SOURCE=Path('work/analysis/lil_B214_source_v6697/all17_clean_current_letter_notices_reactions_full1316_inverse.json');CURRENT=Path('work/analysis/lil_B214_consumers_v6698/all17_effective_bodies34_dispatches_two_whole_commands414_style_pointers.json');CONTROL=Path('work/analysis/lil_B214_controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models.json')
if __name__=='__main__':
    assert not ROOT.exists();source,current,control,plan=map(read,[SOURCE,CURRENT,CONTROL,PLAN]);image=NdsImage.open(ROM);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[214];spec=plan['blocks'][0]
    assert sha(PARENT.read_bytes())==source['current_ROM_sha256']==plan['candidate_sha256'] and sha(block)==spec['research_block_sha256'] and len(block)==1304
    ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}}
    for name,text in current['source_owned_adapters'].items():
        if name=='catalog_style_getters':text=checked_text(text,{'len(rows)==414':'len(rows)==207'})
        exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image);ROOT.mkdir(parents=True);ctx=CurrentContext(source['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows={r['id']:r for r in source['records']+source['typed_actor_style_records']};records=spec['text_records']+[r for s in spec['actor_style_commands'] for r in s['alternative_records']];cases=[]
    for ref in records:
        row=rows[ref['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);prefix=row['source_selector'];spoken=row['kind']=='progressive';assert block[at:at+len(value)+1]==value+b'\0'
        if spoken:assert value[0]==prefix and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        body=value[1:] if spoken else value;result=ctx.execute(ns['dispatch'],prefix,body);ctx.machines.pop();expected=151 if prefix==208 else prefix
        assert result['resolved_actor_ID']==expected and result['source_voice_class']=={2:3,4:0,23:7,208:4}[prefix] and result['registered_catalog_match'] is None
        boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');assert boundary['text_hex']==body.hex();cases.append(dict(id=row['id'],new_offset=at,target_hex=value.hex(),**result))
    obj=spec['actor_style_commands'][0];at=obj['new_offset'];command=next(c for c in spec['command_map'] if c['new_offset']==at);native=dict(offset=at,word=0x4100,native_extent=command['new_extent'],whole_command_hex=obj['target_hex'])
    whole=ctx.execute(ns['whole_style_command'],block,native);ctx.machines.pop();assert whole['resolved_actor_ID']==151 and whole['original_actor_style']==4
    value=bytes.fromhex(obj['target_hex']);slots=[]
    for style in range(8):
        relative=20+struct.unpack_from('<H',value,2+style*2)[0];body=value[relative:value.index(0,relative)];slots.append(dict(style_index=style,relative_offset=relative,hex=body.hex()))
    assert slots[2]['relative_offset']==slots[7]['relative_offset'] and len({s['relative_offset'] for s in slots})==7
    pointers=ctx.execute(ns['catalog_style_getters'],[dict(block=214,command_offset=at,versions=[dict(version='relocated-target',command_hex=value.hex(),style_slots=slots)])]);ctx.machines.pop();assert len(pointers['cases'])==207
    maps={r['old_offset']:r for r in spec['command_map']};predicates=[]
    for prior in [r for r in control['predicate_cases'] if r['version']=='current']:
        old=prior['offset'];at=maps[old]['new_offset'];command=next(c for c in source['blocks'][0]['all_current_native_commands'] if c['offset']==old);assert block[at:at+8].hex()==command['whole_command_hex'];target=dict(command,offset=at);result=ctx.execute(predicate,block,target);ctx.machines.pop()
        assert result['native_result']==prior['native_result']==[2,0,0,0,0,0] and result['sole_scratch_restore_recovers_all4MiB_exact'];writes=result['original_unaligned_operand_read_scratch_writes'];assert len(writes)==int((at+4)%4!=0)
        predicates.append(dict(source_offset=old,target_offset=at,source_operand_alignment=(old+4)%4,target_operand_alignment=(at+4)%4,original=prior,relocated=result))
    assert [(p['source_offset'],p['target_offset'],p['source_operand_alignment'],p['target_operand_alignment']) for p in predicates]==[(882,892,2,0),(1164,1150,0,2)]
    structural=[]
    for prior in [r for r in control['source4500_4621_A000_structural_cases'] if r['version']=='current']:
        mapping=maps[prior['original_offset']];at=mapping['new_offset'];raw=block[at:at+mapping['new_extent']];assert raw.hex()==prior['source_command_hex'];isolated=b'CS\0\1'+len(raw).to_bytes(2,'little')+bytes(2)+raw;result=walk(ctx.arm,isolated)
        assert result['error'] is None and result['rows']==prior['rows'] and result['opaque_effect_bridges']==prior['opaque_effect_bridges'];structural.append(dict(original_offset=prior['original_offset'],new_offset=at,source_command_hex=raw.hex(),native_result=result,opaque_effect_bodies_bridged_not_full_effect_claim=True))
    env=dict(end_case.__globals__);exec(compile(control['source_owned_seeded_end_adapter'],__file__+'::seeded-normal-end','exec'),env);assert block[1298:]==bytes(6)
    ends=[env['end_case'](ctx.arm,block,1298,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]
    assert len(cases)==17 and len(structural)==5 and len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends) and not ctx.machines
    save(ROOT/'seventeen_dispatches207_style_pointers_two_alignment_swaps_five_effects25_ends.json',dict(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),target_block_sha256=sha(block),source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),dispatch_cases=cases,original_static_voices3_0_7_and_D0_fallback4_no_catalogue_override=True,whole_4100_command=whole,eight_style_slots=slots,all207_target_style_getters=pointers,original_style2_7_alias_preserved=True,relocated_predicates=predicates,both_opposite_operand_alignment_changes_original_owned_scratch_only_restores4MiB=True,both_native_predicates_type2_Boolean0_without_forcing=True,opaque_structural_cases=structural,target_normal_end_cases=ends,target_end1298_state0_retains_existing_value_word_and_tail2=True,all27_commands_eight_relatives_typed_aliases_two_predicates_staging_A000_and_end_preserved=True,native_name_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),native_UI_bodies_unexecuted_here=True,no_role_actor_roster_RNG_or_gameplay_result_forced=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,CONTROL,PLAN,Path(__file__)]},full_goal_complete=False));print('17 final dispatches,207 target style pointers,original aliases,both opposite alignment changes,5 opaque cases and25 seeded normal ends pass.')
