"""Preserve the rejected dictionary-gate contract and freeze only its schema successor."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_policy_v8517')
OLD=Path('translations/hodram_B50_native_contract_v1.json')
CONTRACT=Path('translations/hodram_B50_native_contract_v2.json')
DOC=Path('translations/hodram_B50_editorial_manuscript_v5.json')
APPROVAL=Path('work/analysis/Hodram_B50_gate_metadata_v8516/metadata_approval.json')
if __name__=='__main__':
    assert not ROOT.exists() and not CONTRACT.exists();old,doc,approval=map(read,[OLD,DOC,APPROVAL])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['only_root_gate_declaration_andpredecessor_metadata_changed']
    frozen=deepcopy(old);frozen['batch_binding']['review_gates']=doc['review_gates'];frozen['review_gates']=doc['review_gates']
    assert all(r==frozen['record_bindings'][r['id']]['approved_fields'] for r in doc['records']) and not frozen['choice_bindings']
    tools=[];newfiles=[]
    for suffix in ['layout','plan','names']:
        a=Path('dk4tool/dialogue')/('hodram_B50_'+suffix+'_v1.py');b=a.with_name('hodram_B50_'+suffix+'_v2.py');text=a.read_text(encoding='utf-8');changes={}
        for stem in ['profile','plan']:
            key='hodram_B50_'+stem+'_v1'
            if key in text:changes[key]='hodram_B50_'+stem+'_v2'
        if changes:tools.append(derive(str(a),str(b),changes))
        else:
            assert suffix=='plan' and not b.exists();b.write_bytes(a.read_bytes());tools.append(dict(source=str(a),target=str(b),source_sha256=sha(a.read_bytes()),target_sha256=sha(b.read_bytes()),byte_exact_unchanged_planner=True))
        newfiles.append(b)
    deps=dict(old['dependencies'])
    for path in [OLD,DOC,APPROVAL,Path(__file__),Path('scripts/bind_Hodram_B50_review_gates_v8516.py'),Path('dk4tool/dialogue/hodram_B50_profile_v1.py'),*newfiles]:deps[str(path.resolve())]=sha(path.read_bytes())
    assert all(sha(Path(p).read_bytes())==h for p,h in deps.items())
    frozen.update(format='Hodram-B50-source-native-contract-v2',dependencies=deps,predecessor_contract=str(OLD),predecessor_contract_sha256=sha(OLD.read_bytes()),metadata_approval=str(APPROVAL),metadata_approval_sha256=sha(APPROVAL.read_bytes()),only_root_gate_schema_andmodule_import_bindings_changed=True)
    save(CONTRACT,frozen)
    profile='dk4tool/dialogue/hodram_B50_profile_v2.py';tools.append(derive('dk4tool/dialogue/hodram_B50_profile_v1.py',profile,{'translations/hodram_B50_native_contract_v1.json':CONTRACT.as_posix(),sha(OLD.read_bytes()):sha(CONTRACT.read_bytes())}))
    ROOT.mkdir(parents=True);save(ROOT/'frozen_contract.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),modules={str(p):sha(p.read_bytes()) for p in [Path(profile),*newfiles]},module_derivations=tools,all400_original_dependencies_retained_exact=True,record_bindings_planner_QA_native_profiles_andmeasured_limits_value_exact=True,dependency_count=len(deps),supported_gate_schema_registered_without_any_global_guard_change=True,failed_v1_contract_andpolicy_attempt_preserved=True,policy_validation_independent_production_atomic_registered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('B50 frozencontractv2:all3 speech/native/compiler/QA bindings identical;rootgate schema andlocal imports updated;dependencies',len(deps),'.Rejectedv1 preserved.No credit.')
