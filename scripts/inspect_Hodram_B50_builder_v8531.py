"""Record existing registered stage access and exact guarded builder inverse before extension."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v5 import validate_builder_bytes,STAGE_V5,STAGE_B49_V2
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_builder_inspection_v8531')
BUILDER=Path('scripts/build_integrated_release.py')
REGISTRY=Path('translations/release_stack.json')
if __name__=='__main__':
    assert not ROOT.exists();raw=BUILDER.read_bytes();text=raw.decode('utf-8');tree=ast.parse(text)
    predecessor=Path('translations/hodram_outcomes_native_contract_v1.json');old=read(predecessor)
    digest=old['dependencies'][str(BUILDER.resolve())];proof=validate_builder_bytes(raw,digest)
    assert raw.count(STAGE_V5.encode())==raw.count(STAGE_B49_V2.encode())==1
    inverse=raw.replace(STAGE_V5.encode(),b'',1).replace(STAGE_B49_V2.encode(),b'',1);assert sha(inverse)==digest
    accesses=[];dynamic=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='profile_config' and node.func.attr=='get':
            if node.args and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):accesses.append(dict(key=node.args[0].value,line=node.lineno))
            else:dynamic.append(dict(expression=ast.unparse(node),line=node.lineno))
    profile=read(REGISTRY)['profiles']['all-routes-unified-v8475']
    assert profile['hodram_B49_editorial']=='translations/hodram_B49_editorial_release_v3.json'
    assert any(a['key']=='hodram_outcomes_editorial' for a in accesses) and any(a['key']=='hodram_B49_editorial' for a in accesses)
    boundary=text.index('    # Lexically valid "% o"');assert text.index(STAGE_V5)<text.index(STAGE_B49_V2)<boundary
    ROOT.mkdir(parents=True);(ROOT/'current_builder.before.py').write_bytes(raw);(ROOT/'original_guarded_builder_inverse.py').write_bytes(inverse)
    save(ROOT/'builder_inspection.json',dict(builder=str(BUILDER),builder_sha256=sha(raw),registry=str(REGISTRY),registry_sha256=sha(REGISTRY.read_bytes()),profile='all-routes-unified-v8475',profile_value=profile,original_frozen_dependency_source=str(predecessor),original_frozen_dependency_source_sha256=sha(predecessor.read_bytes()),original_builder_sha256=digest,guarded_current_builder_inverse=proof,all_literal_profile_get_accesses=accesses,dynamic_profile_get_accesses=dynamic,existing_fixed_outcomes_v5_thenB49_v2_stages_before_final_percent_safety=True,no_generic_editorial_extension_key_found_in_recorded_profile_get_accesses=True,new_stage_orhook_andall_predecessor_byte_compatibility_andchanged_builder_negatives_still_required=True,no_builder_registry_ROM_orledger_mutation=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Recorded V8475 fixed stages andall profile.get accesses;current outcomesv5/B49v2 invert towhole frozen original builder exactly.No builder/registry/ROM mutation.')
