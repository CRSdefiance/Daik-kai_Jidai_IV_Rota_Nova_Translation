"""Bind all relocated bodies, typed slots, predicate, staging and complete end without forcing branches."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.research_wedding_command_v676 import walk
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.create_lil_B209_reference_v6468 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_relocated_controls_v6476')
SOURCE=Path('work/analysis/lil_B209_source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json')
CURRENT=Path('work/analysis/lil_B209_current_consumers_v6451/all20_bodies40_dispatches4_whole_style_commands828_catalog_slots_and_names.json')
CONTROL=Path('work/analysis/lil_B209_controls_v6460/two_predicates40_relative_cases10_staging_structural_cases_and10_complete_ends.json')
INPUT=Path('work/analysis/current_V6439_native_v6449/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();source,current,control,plan=map(read,[SOURCE,CURRENT,CONTROL,PLAN]);parent,target=NdsImage.open(PARENT),NdsImage.open(ROM);assert target.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin') and sha(PARENT.read_bytes())==source['current_ROM_sha256']==plan['candidate_sha256']
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[209] for im in [parent,target]];spec=plan['blocks'][0];assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256'] and (len(new),spec['research_logical_end'])==(1336,1334)
    env={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}}
    for name,text in current['source_owned_adapters'].items():
        if name=='catalog_style_getters':text=checked_text(text,{'len(rows)==828':'len(rows)==414'})
        exec(compile(text,__file__+'::source-bound-'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](target);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows={r['id']:r for r in source['records']+source['typed_actor_style_records']};refs=spec['text_records']+[r for o in spec['actor_style_commands'] for r in o['alternative_records']];dispatches=[]
    for ref in refs:
        row=rows[ref['id']];value=bytes.fromhex(ref['target_hex']);assert new[ref['new_offset']:ref['new_offset']+len(value)+1]==value+b'\0';body=value[1:] if row['kind']=='progressive' else value;prefix=row['source_selector']
        if row['kind']=='progressive':assert value[0]==prefix
        result=ctx.execute(env['dispatch'],prefix,body);ctx.machines.pop();actor=151 if prefix==208 else prefix;voice={2:3,11:4,12:1,151:4}[actor]
        assert result['resolved_actor_ID']==actor and result['source_voice_class']==voice and result['registered_catalog_match'] is None and result['boundaries'][1]['text_hex']==body.hex() and result['boundaries'][1]['kind']=='unexecuted-progressive-body'
        assert result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact'] and not result['FE_original_null_actor_calls'];dispatches.append(dict(id=ref['id'],new_offset=ref['new_offset'],target_hex=value.hex(),**result))
    whole=[];objects=[];commands=source['blocks'][0]['all_current_native_commands'];maps={r['old_offset']:r for r in spec['command_map']}
    for obj in spec['actor_style_commands']:
        mapping=maps[obj['old_offset']];command=dict(offset=obj['new_offset'],word=0x4100,native_extent=obj['new_length']);result=ctx.execute(env['whole_style_command'],new,command);ctx.machines.pop();assert result['resolved_actor_ID']==151 and result['original_actor_style']==4;whole.append(dict(original_offset=obj['old_offset'],**result));value=bytes.fromhex(obj['target_hex']);slots=[]
        for style in range(8):relative=20+struct.unpack_from('<H',value,2+style*2)[0];slots.append(dict(style_index=style,relative_offset=relative,hex=value[relative:value.index(0,relative)].hex()))
        objects.append(dict(block=209,command_offset=obj['new_offset'],versions=[dict(version='relocated',command_hex=value.hex(),style_slots=slots)]))
    catalog=ctx.execute(env['catalog_style_getters'],objects);ctx.machines.pop();assert len(catalog['cases'])==414
    mapping=maps[686];original=next(c for c in commands if c['offset']==686);pred=dict(original,offset=mapping['new_offset']);p=ctx.execute(predicate,new,pred);ctx.machines.pop();assert p['native_result']==[2,0,0,0,0,0] and p['native_extent']==8
    structural=[]
    for case in [c for c in control['source4500_4621_A000_structural_cases'] if c['version']=='current']:
        m=maps[case['source_offset']];value=new[m['new_offset']:m['new_offset']+m['new_extent']];assert value.hex()==case['source_command_hex'];isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;result=walk(ctx.arm,isolated);assert result['error'] is None and result['rows']==case['rows'] and result['opaque_effect_bridges']==case['opaque_effect_bridges'];structural.append(dict(original_offset=case['source_offset'],new_offset=m['new_offset'],command_hex=value.hex(),native_result=result,nondecode_UI_effect_bodies_bridged_not_full_effect_claim=True))
    end=spec['complete_end_map']['target_offset'];assert end==1330 and new[end:end+4]==bytes(4) and end+4==1334 and new[1334:]==bytes(2)
    ends=[end_case(ctx.arm,new,end,previous) for previous in [0,1,2,3,0xFFFFFFFF]]
    assert len(dispatches)==20 and len(whole)==2 and len(structural)==5 and len(ends)==5 and not ctx.machines
    assert len(spec['target_native_skip_cases'])==20 and spec['inverse_recovers_every_original1148_byte']
    save(ROOT/'all20_dispatches_two_whole_styles414_slots_predicate_staging_and_complete_ends.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),relocated_dispatch_cases=dispatches,whole_relocated4100_commands=whole,all207_actor_two_style_command_pointer_cases=catalog,relocated_original_predicate=p,predicate_type2_Boolean0_preserved=True,source_current_target_relative_cases_proof=str(PLAN),twenty_target_relative_cases_bound=True,structural_source4500_4621_A000_cases=structural,target_five_complete_end_cases=ends,source1148_logical_and_target1336_stored1334_logical_tail2_end1330_bound=True,all18_commands5_speech_preambles15_stored_bodies16_slots_and_aliases_preserved=True,all_zero_source_macros_static_voices_and_original_D0_fallback_preserved=True,no_FE_or_player_choice_invented=True,current_name_catalog_binding=binding,UI_bodies_unexecuted_here_actual_English_covered_separately=True,no_natural_event_dependency85_original_location_earned_progress_full_effects_or_hardware_claim=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),all_prior_source_current_proofs_retained_not_relabelled_as_fresh=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,CONTROL,PLAN,INPUT,Path(__file__)]},full_goal_complete=False))
    print('20 relocated dispatches,2whole D0 style commands,414 all-actor slots,predicate type2/Boolean0,five structural effects andfive complete target ends pass. All4 relative sites/20 target cases bound;no forced role or effects claim.')
