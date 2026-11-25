"""Bind all final B221 bodies, exact A000 and complete seeded normal ends after relocation."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.create_lil_B221_reference_v6997 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_relocated_controls_v7000')
SOURCE=Path('work/analysis/lil_B221_source_v6967/sixteen_clean_current_Crusades_Saladin_context_four_relative_sites_one_choice.json')
CURRENT=Path('work/analysis/lil_B221_consumers_v6968/fourteen_effective_bodies28_dispatches_three_actors_six_name_consumers.json')
CONTROL=Path('work/analysis/lil_B221_controls_v6971/two_A000_structural_cases50_normal_seeded_ends_choice_and_relatives_separate.json')
CHOICES=Path('work/analysis/lil_B221_stored_choices_v6996/one_final_typed_object_two_references_and_both_even_alignments.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,current,control,plan,choices=map(read,[SOURCE,CURRENT,CONTROL,PLAN,CHOICES])
    image=NdsImage.open(ROM);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[221];spec=plan['blocks'][0]
    assert sha(PARENT.read_bytes())==source['current_ROM_sha256']==plan['candidate_sha256']
    assert sha(block)==spec['research_block_sha256'] and len(block)==1224 and len(spec['command_map'])==21
    assert len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20
    assert choices['relocation_plan_sha256']==sha(PLAN.read_bytes())
    ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}}
    for name,text in current['source_owned_dispatch_adapters'].items():
        exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext(source['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    rows={r['id']:r for r in source['records']};cases=[]
    for ref in spec['text_records']:
        row=rows[ref['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);prefix=row['source_selector']
        assert block[at:at+len(value)+1]==value+b'\0' and value[0]==prefix
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        body=value[1:];assert not any(k in body for k in [b'FI',b'FA',b'FO'])
        result=ctx.execute(ns['dispatch'],prefix,body);ctx.machines.pop()
        assert result['resolved_actor_ID']==prefix and result['source_voice_class']=={2:3,17:4,85:0}[prefix]
        assert result['registered_catalog_match'] is None
        boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body')
        assert boundary['text_hex']==body.hex()
        cases.append(dict(id=row['id'],new_offset=at,target_hex=value.hex(),**result))
    prior=next(r for r in control['source_A000_structural_cases'] if r['version']=='current-English')
    effect=spec['original_A000_map'][0];at=effect['target_offset'];raw=block[at:at+8]
    assert at==1212 and raw.hex()==prior['source_command_hex']=='00a0ffff47000110'
    isolated=b'CS\0\1'+len(raw).to_bytes(2,'little')+bytes(2)+raw
    structural=walk(ctx.arm,isolated)
    assert structural['error'] is None and structural['rows']==prior['rows'] and structural['opaque_effect_bridges']==prior['opaque_effect_bridges']
    env=dict(end_case.__globals__)
    exec(compile(control['source_owned_seeded_end_adapter'],__file__+'::source-owned-seeded-end','exec'),env)
    end=spec['complete_end_map'][0]['target_offset']
    assert end==1220 and block[end:]==bytes(4)
    ends=[env['end_case'](ctx.arm,block,end,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]
    assert len(cases)==14 and not ctx.machines
    assert all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    save(ROOT/'all14_final_dispatches_A00025_normal_seeded_ends_four_relatives_one_menu.json',dict(
        candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),target_block_sha256=sha(block),
        relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),dispatch_cases=cases,
        all14_complete_preambles_voices_and_zero_macro_bodies_bound=True,zero_original_or_invented_FI_FA_FO=True,
        source_A000=prior,relocated_A000=structural,normal_terminal_seed_cases=ends,
        normal_state0_retains_existing_value_word_in_all25_cases=True,
        original_choice_residual0_and1_are_not_flagged_end_controls=True,
        four_relative_sites20_native_target_cases_reused_by_exact_plan_hash=True,
        typed_menu_proof=str(CHOICES),typed_menu_proof_sha256=sha(CHOICES.read_bytes()),
        all21_commands_no_predicate_C200_style_letter_picture_or6329_assumptions=True,
        opaque_A000_effects_bridged_not_fully_explained=True,
        current_native_snapshot_and_exact_same_ARM9_COMMON_for_SC2_only_research=True,
        English_page_buttons_and_visible_choice_association_still_require_actual_capture=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,CONTROL,PLAN,CHOICES,Path(__file__)]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('14 final bodies/voices,A000 and25 normal residual ends pass. Four relatives/menu separately bound;actual English pending.')
