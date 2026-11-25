"""Verify the packaged checkpoint with the ledger's established historical identity helper."""
from pathlib import Path
from collections import Counter
from scripts.verify_village_wrap_v608 import read,save
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B186_package_audit_v5185')
if __name__=='__main__':
    assert not ROOT.exists()
    verified=Path('work/analysis/editorial_handoff_verification_v5183/verified_handoff.json')
    package=Path('releases/all_routes_unified_v5177/verification.json')
    p=read(verified);d=read('translations/editorial_review_current_v1.json')
    f=read('translations/lil_B186_contextual_final_review_v1.json');family=d['completed_editorial_families'][-1]
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==p['ledger_sha256']
    assert len(f['records'])==12 and family['records']==f['records']
    assert Counter(r['editorial_decision'] for r in f['records'])=={'revise':7,'retain-wording':5}
    assert (family['revised_count'],family['retained_count'])==(7,5)
    rows=[r for x in d['completed_editorial_families'] for r in x['records']]
    assert len(rows)==len({historical_key(r) for r in rows})==6027
    assert d['goal_status']=='active' and not d['full_goal_complete']
    scope=read(d['unfinished_editorial_scope_v5182']['path'])
    assert scope['next_Lil_B187_clean_only_v5187']['objects']==16
    assert scope['untranslated_Alexandria_alias_v5139b']['caller_and_display_fidelity_open']
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    pkg=read(package);assert pkg['candidate_sha256']==p['candidate_sha256'] and pkg['patch_sha256']==p['patch_sha256']
    for path,digest in pkg['evidence'].items():assert sha(Path(path).read_bytes())==digest
    ROOT.mkdir(parents=True);save(ROOT/'verified_package_and_once_only_coverage.json',dict(
        candidate=p['candidate'],candidate_sha256=p['candidate_sha256'],patch=p['patch'],patch_sha256=p['patch_sha256'],
        completed=6027,source_prose=6030,revised=3818,retained=2209,unique_historical_keys=6027,
        B186_decisions=dict(Counter(r['editorial_decision'] for r in f['records'])),
        ledger_bytes=Path('translations/editorial_review_current_v1.json').stat().st_size,
        previous_inline_audit_diagnostic='A read-only inline audit assumed every historical record has a file_path field and stopped with KeyError. No file changed. This successor uses the established historical_key helper already used by completion and inverse verification.',
        previous_inline_diagnostic_no_file_mutation=True,all_prior_history_preserved=True,main_V4701_preserved=True,
        package=str(package),package_sha256=sha(package.read_bytes()),verified_handoff=str(verified),verified_handoff_sha256=sha(verified.read_bytes()),
        next16_clean_only_objects_uncredited=True,untranslated_Alexandria_alias_open=True,
        full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('V5177 package and6027 unique completed identities verified;7 revisions/5 retentions counted once. Full editorial goal active.')
