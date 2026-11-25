"""Cold-boot the Maria display fixture with the existing system-only unlock."""
from scripts.run_reviewed_dialogue_fixture_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "    old=harness.ct;harness.ct=Proxy()":
        """    prior=load('work/Maria_current_context_20261109_v1/run_plan.json')
    donor=Path(prior['donor']);assert sha(donor.read_bytes())==prior['donor_sha256']
    unlock=load(prior['fixture_manifest'])
    assert sha(Path(prior['fixture_manifest']).read_bytes())==prior['fixture_manifest_sha256']
    assert unlock['only_system_low_four_bits_and_original_checksum_changed']
    assert unlock['all_six_route_save_slots_and_footer_unchanged'] and not unlock['earned_unlock_verified']
    unlock.update(production_ROM=str(rom),production_ROM_sha256=sha(rom.read_bytes()),
        current_test_scope='Maria301 initialized native-command display QA. Existing system-only unlock is not earned; optional source events are not activated.')
    unlock_path=args.out/'existing_system_unlock_manifest.json';save(unlock_path,unlock)
    saved_plan=load(args.out/'run_plan.json')
    saved_plan.update(existing_isolated_system_unlock_not_earned=True,donor=str(donor),donor_sha256=sha(donor.read_bytes()),
        unlock_manifest=str(unlock_path),unlock_manifest_sha256=sha(unlock_path.read_bytes()))
    save(args.out/'run_plan.json',saved_plan)
    old=harness.ct;harness.ct=Proxy()""",
    'no_savestate_battery_or_emulated_memory_override=True,':
        'no_savestate_or_emulated_memory_override=True, existing_system_only_unlock_not_earned=True,',
    "    try:harness.main()":
        "    sys.argv.extend(['--battery-save',str(donor),'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(unlock_path)])\n    try:harness.main()",
    " and not report.get('battery_save_preloaded')":
        " and report.get('battery_save_preloaded')",
    "    assert len(observers)==1 and not observed['errors']":
        "    assert sha(donor.read_bytes())==prior['donor_sha256']\n    assert len(observers)==1 and not observed['errors']",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-readonly-modal-guards-explicit-existing-Maria-unlock', 'exec'), globals())
