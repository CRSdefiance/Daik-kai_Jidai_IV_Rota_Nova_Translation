"""Cold boot Lil using ordinary inputs and the qualified read-only modal observer."""
from scripts.run_maria359_display_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

start = previous.index("    prior=load('work/Maria_current_context_20261109_v1/run_plan.json')")
end = previous.index('    old=harness.ct;', start)
source = checked_text(previous, {
    previous[start:end]: '',
    'existing_system_only_unlock_not_earned=True': 'existing_system_only_unlock_not_earned=False',
    "    sys.argv.extend(['--battery-save',str(donor),'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(unlock_path)])\n": '',
    " and report.get('battery_save_preloaded')": " and not report.get('battery_save_preloaded')",
    "    assert sha(donor.read_bytes())==prior['donor_sha256']\n": '',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-readonly-observer-normal-inputs-no-battery', 'exec'), globals())
