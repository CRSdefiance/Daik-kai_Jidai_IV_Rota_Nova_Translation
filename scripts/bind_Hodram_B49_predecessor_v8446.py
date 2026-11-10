"""Bind unchanged prior semantic cases and challenge the exact preserved-config alias."""
from pathlib import Path
from unittest.mock import patch
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prepare_Hodram_B49_predecessor_v8444 import SPECS
from dk4tool.patch import hodram_outcomes_editorial_v4 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_predecessor_binding_v8446')
EQUIVALENCE=Path('work/analysis/Hodram_B49_predecessor_tools_v8444/source_equivalence.json')
PRIOR=Path('work/analysis/Hodram_fixture_binding_v8375b/semantic_binding.json')
POSITIVE=Path('work/analysis/Hodram_outcome_atomic_positive_v8445/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
GUARD=Path('work/analysis/Hodram_B49_builder_v8431b/exact_builder_inverse_cases.json')

if __name__=='__main__':
    assert not ROOT.exists();equivalence,prior,positive,guard=map(read,[EQUIVALENCE,PRIOR,POSITIVE,GUARD]);bindings=[]
    for (area,name,old,new,changes),d in zip(SPECS,equivalence['derivations'],strict=True):
        source,target=Path(d['previous']),Path(d['successor']);a,b=source.read_text('utf8'),target.read_text('utf8')
        assert sha(source.read_bytes())==d['previous_sha256'] and sha(target.read_bytes())==d['successor_sha256']
        if name=='editorial':
            start=b.index("\nPRESERVED_CONFIG=");end=b.index('def plan_release(',start)
            without_alias=b[:start]+b[end:];without_alias=without_alias.replace('conf=load(resolve_config(config));check_dependencies(conf)','conf=load(config);check_dependencies(conf)')
            assert checked_text(a,changes)==without_alias
        else:assert checked_text(a,changes)==b
        bindings.append(d)
    assert prior['prior_semantic_cases']==50 and prior['all_protected_files_hash_exact'] and len(prior['new_lifecycle_negatives'])==3
    assert positive['single_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and positive['exact_preserved_registered_v3config_alias_used']
    assert len(guard['positives'])==5 and len(guard['negatives'])==16 and all(n['rejected'] for n in guard['negatives'])
    old=read(owned.PRESERVED_CONFIG);new=read(owned.CONFIG)
    assert len(old['dependencies'])==506 and len(new['dependencies'])==515 and all(new['dependencies'][p]==h for p,h in old['dependencies'].items())
    assert all(old[k]==new[k] for k in old if k!='dependencies')
    assert owned.resolve_config(owned.PRESERVED_CONFIG)==owned.CONFIG and owned.resolve_config(str(Path(owned.PRESERVED_CONFIG).resolve()))==owned.CONFIG and owned.resolve_config(owned.CONFIG)==owned.CONFIG
    original_read=Path.read_bytes;raw=Path(owned.PRESERVED_CONFIG).read_bytes();negatives=[]
    for label,value in [('changed-config-byte',bytes([raw[0]^1])+raw[1:]),('trailing-whitespace',raw+b'\n'),('different-valid-config',Path(owned.CONFIG).read_bytes()),('empty-config',b'')]:
        def replaced(path):return value if path.resolve()==Path(owned.PRESERVED_CONFIG).resolve() else original_read(path)
        with patch.object(Path,'read_bytes',replaced):
            try:owned.resolve_config(owned.PRESERVED_CONFIG)
            except ValueError as exc:
                assert 'exact preserved registered v3 config alias' in str(exc);negatives.append(dict(case=label,rejected=True,error=str(exc),changed_input_sha256=sha(value)))
            else:raise AssertionError('Changed preserved config accepted:'+label)
    assert len(negatives)==4 and Path(owned.PRESERVED_CONFIG).read_bytes()==raw
    ROOT.mkdir(parents=True);save(ROOT/'semantic_binding.json',dict(derivations=bindings,prior_semantic_cases=50,prior_semantic_cases_reused_by_exact_source_equivalence_not_rerun=True,prior_binding=str(PRIOR),prior_binding_sha256=sha(PRIOR.read_bytes()),new_positive=str(POSITIVE),new_positive_sha256=sha(POSITIVE.read_bytes()),new_builder_guard_positive_forms=5,new_builder_guard_rejections=16,new_builder_guard=str(GUARD),new_builder_guard_sha256=sha(GUARD.read_bytes()),exact_oldconfig_alias_positive_forms=3,actual_changed_oldconfig_rejections=negatives,oldconfig_unchanged=True,all506_prior_dependencies_preserved=True,new_dependency_count=515,no_builder_registry_ROM_orcredit_change=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Predecessor compatibility:7exact source bindings/prior50semantic cases retained;full positive byte-exact;5builder forms/16mutations and4changed-config aliases rejected. No emulator replay orcredit.')
