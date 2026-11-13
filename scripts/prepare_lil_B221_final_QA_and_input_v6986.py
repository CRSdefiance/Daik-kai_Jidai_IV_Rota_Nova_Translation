"""Bind the final wrap and correct a harness input spelling without changing gameplay."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save,read
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B221_final_QA_input_tools_v6986')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/probe_lil_B221_paragraph_QA_v6982.py','scripts/probe_lil_B221_paragraph_QA_v6982b.py',{
        'base_QA_v6982':'base_QA_v6982b','layout_v6976b/':'layout_v6976c/','native_pages_v6980b/':'native_pages_v6980c/'}),
        ('scripts/run_lil_B221_source_v6979b.py','scripts/run_lil_B221_source_v6979c.py',{
            'source_run_v6979b':'source_run_v6979c',"source_v6979b'":"source_v6979c'",
            "buttons=['Down']":"buttons=['DOWN']"})]
    for source,target,changes in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf-8'),changes)
    rows=[derive(source,target,changes) for source,target,changes in jobs]
    ROOT.mkdir(parents=True)
    failed=Path('work/analysis/lil_B221_source_run_v6979b')
    assert not (failed/'terminal.json').exists()
    save(ROOT/'final_wrap_QA_and_preserved_failed_harness_input.json',dict(derivations=rows,
        preserved_failed_runner='scripts/run_lil_B221_source_v6979b.py',
        preserved_partial_run=str(failed),partial_run_is_not_complete_capture_or_selection_evidence=True,
        failure="Harness KeyError: Down; the documented ordinary controller button is uppercase DOWN.",
        correction_changes_only_input_button_spelling_same_requested_frame3700_duration5=True,
        source_fixture_ROM_conditions_results_RNG_and_all_A_inputs_unchanged=True,
        original_exception_path_runs_observer_close_in_finally_not_a_terminal_capture_proof=True,
        failed_inputs_sha256=sha((failed/'inputs.json').read_bytes()),
        no_new_ROM_or_editorial_credit=True,full_goal_complete=False))
