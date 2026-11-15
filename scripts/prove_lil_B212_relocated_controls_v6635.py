"""Bind final stored speech dispatches and typed labels; reuse the separately proved ends."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B212_consumers_v6595 import choice_getters
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_relocated_controls_v6635')
SOURCE=Path('work/analysis/lil_B212_source_v6594b/all14_clean_current_complete_exchange_with_two_three_choices.json')
CURRENT=Path('work/analysis/lil_B212_consumers_v6595/nine_effective_bodies18_dispatches_actor149_two_name_consumers.json')
PLAN=Path('work/analysis/lil_B212_relocation_v6622/all14_objects10_spans_three_exact_ends_full884_inverse_RESEARCH.json')
ROM=Path('out/lil_B212_reference_v6624_RESEARCH_ONLY.nds')
ENDS=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();source,current,plan=map(read,[SOURCE,CURRENT,PLAN]);image=NdsImage.open(ROM);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[212];spec=plan['blocks'][0];assert sha(block)==spec['research_block_sha256'] and len(block)==980
    ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}}
    for name,text in current['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image);ROOT.mkdir(parents=True);ctx=CurrentContext(source['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context');cases=[]
    for ref in spec['text_records']:
        value=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert value[0]==149 and block[at:at+len(value)+1]==value+b'\0';result=ctx.execute(ns['dispatch'],149,value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==149 and result['source_voice_class']==0 and result['registered_catalog_match'] is None;boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');assert boundary['text_hex']==value[1:].hex();cases.append(dict(id=ref['id'],offset=at,target_hex=value.hex(),**result))
    assert len(cases)==9 and not ctx.machines;menus=[]
    for menu in spec['choice_commands']:
        # Mapped commands carry the exact final bytes, rather than a reconstructed label-only surrogate.
        at=menu['new_offset'];raw=bytes.fromhex(menu['target_hex']);assert block[at:at+len(raw)]==raw;versions=choice_getters(ctx.arm,dict(offset=at,whole_command_hex=raw.hex()))
        for version in versions:
            for label,ref in zip(version['labels'],menu['label_references'],strict=True):assert (label['offset'],label['hex'],label['option_index'])==(ref['new_offset'],ref['target_hex'],ref['option_index'])
        menus.append(dict(offset=at,alignment_cases=versions))
    assert len(menus)==2 and sum(len(v['labels']) for m in menus for v in m['alignment_cases'])==10
    save(ROOT/'nine_final_dispatches_four_count_ten_label_pointer_cases.json',dict(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),target_block_sha256=sha(block),dispatch_cases=cases,choice_getter_cases=menus,nine_static_actor149_voice0_no_catalogue_override=True,four_count_ten_label_pointer_cases=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),separate_150_seeded_terminal_cases=str(ENDS),separate_150_seeded_terminal_cases_sha256=sha(ENDS.read_bytes()),normal_end_keeps_result_word1_flagged_end_sets_state1_value0=True,native_UI_bodies_unexecuted_here=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,PLAN,ENDS,Path(__file__)]},full_goal_complete=False))
    print('Nine final dispatches/four count/ten label-pointer cases pass; 150 seeded terminal cases separately bound.')
