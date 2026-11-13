"""Use recorded paired RAM frames and compare ordinary paid actions to their reference."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original = Path('scripts/verify_tavern_actual_v2193.py')
source = original.read_text()
changes = {
    "work/analysis/tavern_actual_verification_v2193'": "work/analysis/tavern_actual_verification_v2193d'",
    '(3200, 5000, 7000, 8200, 9201)': '(3200, 5000, 7000, 8200, 9200)',
    '(3200, 5000, 6001)': '(3200, 5000, 6000)',
    "        previous = read(plan['prior_report'])": "        previous = read(plan['prior_report'])\n        assert sha(Path(plan['prior_report']).read_bytes()) == plan['prior_report_sha256']",
    "            model_controls.append(dict(frame=f, models=models(arm, raw)))": "            new_models, old_models = models(arm, raw), models(old_arm, old_raw)\n            assert new_models == old_models, (mode, f, new_models, old_models)\n            model_controls.append(dict(frame=f, models=new_models, reference_models=old_models, exact_to_historical_same_ordinary_inputs=True))",
    "        assert all(r['models'] == model_controls[0]['models'] for r in model_controls)": "        stable = lambda r: {k:v for k,v in r['models'].items() if k != 'company'}\n        assert all(stable(r) == stable(model_controls[0]) for r in model_controls)",
    'unchanged_current_ship_models=model_controls': 'paired_native_company_fleet_ship_controls=model_controls',
    'ordinary_drink_cash_changes_exact_to_historical_source_inputs': 'ordinary_Tavern_cash_changes_exact_to_historical_source_inputs',
}
for before, after in changes.items():
    assert source.count(before) == 1
    source = source.replace(before, after)
namespace = {'__name__': '__main__', '__file__': __file__}
exec(compile(source, __file__, 'exec'), namespace)
save(namespace['ROOT']/'snapshot_and_model_scope_correction.json', dict(original_verifier=str(original), original_verifier_sha256=sha(original.read_bytes()), effective_source_sha256=sha(source.encode()), successor_sha256=sha(Path(__file__).read_bytes()), paired_direct_state_frames=[3200,5000,7000,8200,9200], paired_price_state_frames=[3200,5000,6000], old_final_RAM_snapshots_absent=True, new_final_RAM_dumps_preserved_without_invented_old_reference=True, company_model_hash_includes_cash_and_changes_during_paid_actions=True, full_company_fleet_ship_models_equal_historical_same_input_at_all8_frames=True, fleet_and_ship_fields_unchanged_within_both_runs=True, direct_cash_sequence=[8371,8366,8356,8351,8351], price_cancellation_cash_unchanged=8371, earlier2193_2193b_2193c_failed_assumptions_preserved=True, no_ROM_capture_or_gameplay_change=True))
