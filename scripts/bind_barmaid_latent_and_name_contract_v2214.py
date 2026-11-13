"""Current caller census and unchanged source bindings for latent996/name capacity."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import close_barmaid_latent_context_v779 as original
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/barmaid_context_v2213')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
CLASSIFIED=Path('work/analysis/barmaid_integration_v780/classified_source_windows.json')
NAME=Path('work/analysis/barmaid_editorial_v779/captain_first_name_bound.json')

if __name__=='__main__':
    assert not (ROOT/'latent996_caller_closure.json').exists()
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    c=read(CLASSIFIED);n=read(NAME)
    spans=[(0xE5784,0xE579C),(0x82F3C,0x82F4C),(0x12A510,0x12E510),(0x6DB38,0x6DB54)]
    spans.extend(tuple(s)for s in n['source_current_spans'])
    spans.extend([(0x59E00,0x59E10),(0xB65E4,0xB6650),(0x34674,0x34688)])
    assert all(arm[a:b]==clean[a:b]for a,b in spans)
    assert sha(arm[0x12A510:0x12E510])==c['numeric_table']['sha256']
    assert n['capacity']==16 and n['serialized_bytes']==17 and len(n['cases'])==24
    program=inspect.getsource(original.main)
    old="assert not any(refs[hex(a)][k] for k in ('absolute', 'ADR', 'Thumb_BL_BLX')), (hex(a), refs[hex(a)])"
    new="assert not any(r for k in ('absolute','ADR','Thumb_BL_BLX') for r in refs[hex(a)][k] if [k,*r] not in exclusions),(hex(a),refs[hex(a)])"
    assert program.count(old)==1
    program=program.replace(old,new)
    env={**original.__dict__,'ROOT':ROOT,'CURRENT':ROM,'exclusions':c['exact_classified_references'],'__file__':__file__}
    exec(compile(program,__file__,'exec'),env)
    env['main']()
    refs=read(ROOT/'latent996_reference_leads.json')
    found=sorted([kind,*r]for group in refs.values()for kind,rows in group.items()for r in rows if kind!='ARM_branch')
    assert found==sorted(c['exact_classified_references'])
    save(ROOT/'current_latent996_and_first_name_contract_binding.json',dict(current_ROM=str(ROM),current_ROM_sha256=sha(ROM.read_bytes()),current_ARM9_sha256=sha(arm),all_source_spans_current_clean_exact=[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],fresh_current_whole_unit_caller_reference_census=str(ROOT/'latent996_caller_closure.json'),only_original_two_private_caller_chains=True,only_three_exact_typed_source_scan_coincidences=True,inherited_classification=str(CLASSIFIED),inherited_classification_sha256=sha(CLASSIFIED.read_bytes()),four_instruction_and4096_numeric_loader_cases_inherited_not_freshly_rerun=True,inherited_114_town_guard_proof='work/analysis/barmaid_integration_v780/latent996_caller_closure.json',inherited_114_guard_proof_sha256=sha(Path('work/analysis/barmaid_integration_v780/latent996_caller_closure.json').read_bytes()),unchanged_source_catalog58_null_and_no_normal996_activation_claim=True,name_editor_contract=str(NAME),name_editor_contract_sha256=sha(NAME.read_bytes()),first_name_capacity_bytes=16,serialized_bytes_including_NUL=17,original_24_editor_setter_getter_IO_contract_cases_inherited_not_new_keyboard_or_physical_IO=True,no_ROM_dispatch_catalog_name_or_prose_changes=True,effective_census_sha256=sha(program.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current_caller_chains=2,typed_scan_hits=3,inherited_first_name_capacity=16,latent996_normal_activation=False),flush=True)
