"""Exercise final B210 stored dispatches against the separately booted exact corrected-name runtime."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.Al_Ferid_name_release_v1 import SOURCE,TARGET
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/B210_Ferid_compatibility_v6536')
SOURCE_PACKET=Path('work/analysis/lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json')
CURRENT=Path('work/analysis/lil_B210_current_consumers_v6499/ten_effective_bodies20_dispatches_two_names_four_getters_and_exact_source_fields.json')
if __name__=='__main__':
    assert not ROOT.exists();current=read(CURRENT);mapping=read('translations/lil_B210_editorial_relocation_map_v1.json');name=read('translations/Al_Ferid_name_editorial_manuscript_v1.json');input_path=Path('work/analysis/Al_Ferid_target_proof_v6521/current_native_input.json');image=NdsImage.open(name['approved_target_research_ROM']);assert sha(image.read_file('/__arm9__.bin'))==TARGET
    target=IlnkContainer.parse(NdsImage.open('out/lil_B210_reference_v6515_RESEARCH_ONLY.nds').read_file('/data/SC2.DK4')).blocks[210]
    ns={**inherited.__dict__,'SOURCE':SOURCE_PACKET,'CATALOG_LOOKUP':{}};adapters=dict(current['source_owned_dispatch_adapters']);old=adapters['bind_current_catalog'];assert old.count(SOURCE)==1;adapters['bind_current_catalog']=old.replace(SOURCE,TARGET);assert adapters['bind_current_catalog'].replace(TARGET,SOURCE)==old
    for key,text in adapters.items():exec(compile(text,__file__+'::exact-target-'+key,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image);ROOT.mkdir(parents=True);ctx=CurrentContext(input_path,'unused-no-historical-ROM',ROOT/'current_context');cases=[];prior=read('work/analysis/lil_B210_relocated_controls_v6528/ten_target_dispatches_one_original_A000_and_five_guarded_ends.json')['relocated_dispatch_cases']
    for ref,before in zip(mapping['blocks'][0]['text_records'],prior,strict=True):
        value=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert target[at:at+len(value)+1]==value+b'\0';result=ctx.execute(ns['dispatch'],value[0],value[1:]);ctx.machines.pop();assert result=={k:v for k,v in before.items() if k not in ['id','new_offset','target_hex']};cases.append(dict(id=ref['id'],new_offset=at,target_hex=value.hex(),dispatch=result,entire_dispatch_result_exact_to_pre_name_proof=True))
    assert len(cases)==10 and not ctx.machines
    save(ROOT/'ten_final_B210_dispatches_exact_after_name_typography.json',dict(cases=cases,exact_corrected_name_ARM9_sha256=TARGET,own_target_native_input=str(input_path),own_target_native_input_sha256=sha(input_path.read_bytes()),only_adapter_hash_guard_updated_no_address_or_instruction_change=True,all10_entire_dispatch_results_identical=True,all467_catalogue_rows_and_native_calls_bound=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),not_new_gameplay_or_full_catalogue_UI=True,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,SOURCE_PACKET,input_path,Path(__file__),Path('scripts/Al_Ferid_exact_native_context_v6520.py')]},full_goal_complete=False));print('All ten B210 final dispatch results remain exact after the isolated name correction; original catalogue/calls and own target snapshot retained.')
