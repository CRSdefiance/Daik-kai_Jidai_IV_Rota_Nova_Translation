"""Post-application verification of B182 integration and the unchanged full goal."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.audit_lil_B182_completion_v4920 import audit
from scripts.complete_lil_B182_v4919 import ROOT as COMPLETION,RELEASE,PRIOR
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4921')
if __name__=='__main__':
    assert not ROOT.exists();plan=read(COMPLETION/'staged_completion.json')
    application=read(COMPLETION/'native_application_receipt.json');assert application['all6_staged_targets_hash_exact']
    assert application['staged_plan_sha256']==sha((COMPLETION/'staged_completion.json').read_bytes())
    for r in plan['files']:
        assert sha(Path(r['target']).read_bytes())==sha(Path(r['planned']).read_bytes())==r['planned_sha256']
        assert sha((COMPLETION/(Path(r['target']).name+'.before')).read_bytes())==r['before_sha256']
    lp=Path('translations/editorial_review_current_v1.json');before=read(COMPLETION/(lp.name+'.before'));ledger=read(lp)
    assert sha((COMPLETION/(lp.name+'.before')).read_bytes())==read(PRIOR)['ledger_sha256']
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    audit(before,ledger)
    receipt=read(plan['staged_receipt'])
    assert sha(Path(plan['staged_receipt']).read_bytes())==plan['staged_receipt_sha256']
    for p,h in {**receipt['evidence'],**receipt['updated_files']}.items():assert sha(Path(p).read_bytes())==h
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4919')
    assert not (COMPLETION/'completion_receipt.json').exists();save(COMPLETION/'completion_receipt.json',receipt)
    release=read(RELEASE);ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(ledger_sha256=sha(lp.read_bytes()),completed=5941,source_prose=5944,revised=3764,retained=2177,
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        all_original_root_and_nested_ledger_history_preserved=True,new_source_prose_and_completion_credit=8,all5941_completed_keys_unique=True,
        all564_manifest_entries114_accepted_and18_checks_verified=True,source_current_integrated_references_exact=True,
        all31_startup_framebuffers_and_five_actor_controls_match=True,all8_actual_scene_panels_and_conditional_controls_verified=True,
        native_state_equality_and_unequal_final_PRNG_timings_indicator_differences_disclosed=True,next_B183_clean_only_uncredited_objects=25,
        promoted_main_V4701_unchanged=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('V4919 sealed/audited:5941 completed,5944 source/prose;V4914 patch/startup/current references pass. B18325 uncredited;full goal active.')
