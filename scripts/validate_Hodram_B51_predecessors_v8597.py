"""Reproduce complete registeredV8543 through all three compatible stages in memory."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_outcomes_editorial_v7 as outcomes
from dk4tool.patch import hodram_B49_editorial_v4 as B49
from dk4tool.patch import hodram_B50_editorial_v2 as B50
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prepare_Hodram_B51_builder_support_v8596 import SPECS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_predecessor_positive_v8597')
SUPPORT = Path('work/analysis/Hodram_B51_builder_support_v8596/source_equivalence.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    support = read(SUPPORT)
    for spec, result in zip(SPECS, support['namespace_only_outcomes_derivations'], strict=True):
        a, b = Path(result['previous']), Path(result['successor'])
        assert sha(a.read_bytes()) == result['previous_sha256'] and sha(b.read_bytes()) == result['successor_sha256']
        assert checked_text(a.read_text('utf-8'), spec[-1]) == b.read_text('utf-8')
    for key in ['B49_guard_import_only_derivation', 'B50_guard_import_only_derivation']:
        result = support[key]
        a, b = Path(result['previous']), Path(result['successor'])
        assert checked_text(a.read_text('utf-8'), {'hodram_outcomes_builder_guard_v6': 'hodram_outcomes_builder_guard_v7'}) == b.read_text('utf-8')
    for key in ['outcomes_configuration', 'B49_configuration', 'B50_configuration']:
        binding = support[key]
        old, new = read(binding['old_configuration']), read(binding['new_configuration'])
        assert {k: v for k, v in old.items() if k != 'dependencies'} == {k: v for k, v in new.items() if k != 'dependencies'}
        assert all(new['dependencies'][p] == digest for p, digest in old['dependencies'].items())
    for p, digest in support['unchanged_frozen_native_contracts'].items():
        assert sha(Path(p).read_bytes()) == digest
    parent = NdsImage.open(outcomes.PARENT)
    image = NdsImage(outcomes.CANONICAL, deepcopy(parent.rom))
    baseline = NdsImage.open(outcomes.CANONICAL)
    results = []
    for label, module, config, expected in [
        ('outcomes', outcomes, 'translations/hodram_outcomes_editorial_release_v7.json', outcomes.ROM),
        ('B49', B49, 'translations/hodram_B49_editorial_release_v5.json', B49.ROM),
        ('B50', B50, 'translations/hodram_B50_editorial_release_v2.json', B50.ROM),
    ]:
        original = image.rom
        before, files = bytes(original.save()), list(original.files)
        components = {p: value for p, value in image.iter_components()}
        calls, commit = [], module.commit_image
        def trapped(target, planned):
            assert target is image and target.rom is original and bytes(original.save()) == before
            assert original.files == files and {p: value for p, value in target.iter_components()} == components
            assert planned is not original and bytes(planned.save()) == expected.read_bytes()
            calls.append('one-complete-NDS')
            commit(target, planned)
        module.commit_image = trapped
        try:
            report = module.apply_release(image, baseline, config=config)
        finally:
            module.commit_image = commit
        assert calls == ['one-complete-NDS'] and bytes(original.save()) == before and bytes(image.rom.save()) == expected.read_bytes()
        results.append(dict(stage=label, config=config, config_sha256=sha(Path(config).read_bytes()), before_sha256=sha(before),
            after_sha256=sha(bytes(image.rom.save())), changed_records=len(report['changed_records']), one_complete_NDS_commit=True,
            original_object_files_components_serialized_bytes_exact_until_commit=True, original_object_still_exact_after_commit=True))
        print('PASS compatible predecessor', label, results[-1]['after_sha256'], flush=True)
    current = Path('out/all_routes_combined_v8543_candidate.nds')
    assert bytes(image.rom.save()) == current.read_bytes() and [r['changed_records'] for r in results] == [6, 16, 3]
    assert outcomes.resolve_config(outcomes.PRESERVED_CONFIG) == outcomes.CONFIG
    ROOT.mkdir(parents=True)
    save(ROOT / 'whole_V8543_byte_exact.json', dict(stages=results, whole_registered_V8543_ROM_byte_exact=True,
        current_V8543_path=str(current), current_V8543_sha256=sha(current.read_bytes()), canonical_source_withfull_predecessor_memory=True,
        all_native_semantic_production_gates_enabled=True, all_original535_outcomes675_B49_and756_B50_dependency_entries_preserved=True,
        all_prior_frozen_native_contracts_byte_exact=True, registered_old_v3_outcomes_alias_still_exact=True,
        no_live_builder_registry_disk_ROM_orcredit_change=True, new_credit=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [Path(__file__), Path(outcomes.__file__), Path(B49.__file__), Path(B50.__file__), SUPPORT]}))
    print('Compatible outcomesv7/B49v4/B50v2 reproduce complete registeredV8543 byte-for-byte with all guards active andthree whole-object commits. No disk ROM/replay/credit.')
