"""Check the registered ROM and every selection in the repacked COMMON block."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shop_business_editorial import IDS, compile_paragraph, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shop_business_v745')
ROM = Path('out/all_routes_combined_v745_candidate.nds')


def rejected(function):
    try:
        function()
    except (AssertionError, ValueError):
        return True
    raise AssertionError('Invalid editorial input unexpectedly accepted')


def main():
    old = NdsImage.open('out/all_routes_combined_v712_candidate.nds')
    new = NdsImage.open(ROM)
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v745'
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == []
    assert all(manifest['checks'].values()) and sha(ROM.read_bytes()) == manifest['candidate_sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    changed = [p for _, p, data in old.iter_files() if data != new.read_file(p)]
    # iter_files covers FNT files; ARM9 is a separately exposed ROM component.
    if old.read_file('/__arm9__.bin') != new.read_file('/__arm9__.bin'):
        changed.append('/__arm9__.bin')
    assert set(changed) == {'/__arm9__.bin', '/COMMON/MESFILE.DK4'}
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    assert common == (ROOT / 'research_COMMON.bin').read_bytes()
    assert arm == (ROOT / 'research_ARM9.bin').read_bytes()
    before = common_message_entries(old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin'), clean=False)
    after = common_message_entries(common, arm, clean=False)
    assert [a.message_id for a, b in zip(before, after) if a.text.rstrip() != b.text.rstrip()] == list(IDS)
    selected = [e for e in after if e.block == 8]
    ids = [selected[0].message_id - 1, *(e.message_id for e in selected), selected[-1].message_id + 1]
    reports = []
    old_factory = loader.machine_for
    loader.machine_for = arm946_machine
    try:
        for i in ids:
            cases = [loader.warm_copy(arm, common, i, after[i].text, cold_cache=cold) for cold in (False, True)]
            reports.append({'message_id': i, 'whole_expected_text_sha256': sha(after[i].text),
                            'complete_native_warm_and_cold_copies_pass': True,
                            'warm_copy_bytes': cases[0]['copied_bytes'],
                            'cold_reads': cases[1]['host_file_contract_reads']})
    finally:
        loader.machine_for = old_factory
    manuscript = read('translations/shop_business_editorial_manuscript_v1.json')
    old_common, old_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    controls = {}
    invalid = deepcopy(manuscript)
    invalid['translation_policy'] = 'natural-dialogue-v1'
    controls['legacy_policy_rejected'] = rejected(lambda: transform(old_common, old_arm, invalid))
    stale = deepcopy(manuscript)
    stale['records'][0]['source_hex'] = '41'
    controls['stale_Japanese_source_rejected'] = rejected(lambda: transform(old_common, old_arm, stale))
    missing = deepcopy(manuscript)
    missing['records'] = [r for r in missing['records'] if r['message_id'] != 658]
    controls['missing_packed_business_sibling_rejected'] = rejected(lambda: transform(old_common, old_arm, missing))
    controls['authored_linebreak_rejected'] = rejected(lambda: compile_paragraph('Altered\nline.{PAD}'))
    controls['unsafe_literal_macro_pair_rejected'] = rejected(lambda: compile_paragraph('FIRE{PAD}'))
    save(ROOT / 'registered_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'registered470_batch_rebuild_all_original_checks_pass': True,
        'all_other_ROM_internal_files_including675_graphics_exact_V712': True,
        'only_two_changed_internal_files': changed,
        'all3668_unselected_visible_texts_preserved_except7_reviewed_IDs': True,
        'complete_native_changed_block_and_neighbor_warm_cold_copies': reports,
        'native_copy_case_count': len(reports) * 2,
        'SDK_file_read_contracts_bridged_not_actual_emulator_loads': True,
        'meaningful_rejection_controls': controls,
        'live_gameplay_verification_pending': True, 'full_goal_complete': False,
        'prototype_FNT_iteration_assumption_corrected_to_check_ARM9_component_separately': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()),
    })
    print(f'V745 registered ROM passes: {len(reports) * 2} complete warm/cold copies; five rejection controls.', flush=True)


if __name__ == '__main__':
    main()
