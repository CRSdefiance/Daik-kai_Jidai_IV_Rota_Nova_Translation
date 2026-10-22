"""Check the combined candidate, previous prose and all changed-block copies."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.giveaway_editorial import IDS, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/giveaway_editorial_v746')
ROM = Path('out/all_routes_combined_v746_candidate.nds')


def rejected(action):
    try:
        action()
    except (ValueError, AssertionError):
        return True
    raise AssertionError('Invalid giveaway editorial input accepted')


def main():
    old, new = (NdsImage.open(p) for p in ('out/all_routes_combined_v745_candidate.nds', ROM))
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v746'
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == []
    assert all(manifest['checks'].values()) and sha(ROM.read_bytes()) == manifest['candidate_sha256']
    registry = read('translations/release_stack.json')
    before_registry = read(ROOT / 'release_stack_before_V746.json')
    assert len(registry['accepted_layers']) == 114
    assert registry['accepted_layers'] == before_registry['accepted_layers']
    assert registry['canonical_baseline'] == before_registry['canonical_baseline']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    changed = [p for _, p, raw in old.iter_files() if raw != new.read_file(p)]
    if old.read_file('/__arm9__.bin') != new.read_file('/__arm9__.bin'):
        changed.append('/__arm9__.bin')
    assert set(changed) == {'/COMMON/MESFILE.DK4', '/__arm9__.bin'}
    assert old.rom.arm7 == new.rom.arm7
    assert old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    assert common == (ROOT / 'research_COMMON.bin').read_bytes()
    assert arm == (ROOT / 'research_ARM9.bin').read_bytes()
    source_common, source_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    before = common_message_entries(source_common, source_arm, clean=False)
    after = common_message_entries(common, arm, clean=False)
    assert [a.message_id for a, b in zip(before, after, strict=True) if a.text.rstrip() != b.text.rstrip()] == list(IDS)
    assert all(before[i].text.rstrip() == after[i].text.rstrip() for i in (657, 658, 682, 683, 684, 686, 687))
    selected = [e for e in after if e.block == 8]
    ids = [selected[0].message_id - 1, *(e.message_id for e in selected), selected[-1].message_id + 1]
    cases = []
    old_factory = loader.machine_for
    loader.machine_for = arm946_machine
    try:
        for i in ids:
            copies = [loader.warm_copy(arm, common, i, after[i].text, cold_cache=cold) for cold in (False, True)]
            cases.append({'message_id': i, 'expected_text_sha256': sha(after[i].text),
                          'complete_warm_and_cold_native_copies': True,
                          'warm_copy_bytes': copies[0]['copied_bytes'], 'cold_reads': copies[1]['host_file_contract_reads']})
    finally:
        loader.machine_for = old_factory
    manuscript = read('translations/giveaway_editorial_manuscript_v1.json')
    wrong_policy = deepcopy(manuscript)
    wrong_policy['translation_policy'] = 'natural-dialogue-v1'
    wrong_source = deepcopy(manuscript)
    wrong_source['records'][0]['source_hex'] = '41'
    missing_variant = deepcopy(manuscript)
    missing_variant['records'] = [r for r in missing_variant['records'] if r['message_id'] != 665]
    controls = {
        'legacy_policy_rejected': rejected(lambda: transform(source_common, source_arm, wrong_policy)),
        'wrong_Japanese_source_rejected': rejected(lambda: transform(source_common, source_arm, wrong_source)),
        'missing_reviewed_variant_rejected': rejected(lambda: transform(source_common, source_arm, missing_variant)),
        'authored_linebreak_rejected': rejected(lambda: compile_paragraph('Two\nlines.{PAD}')),
        'unsafe_literal_macro_pair_rejected': rejected(lambda: compile_paragraph('FIRE{PAD}')),
    }
    save(ROOT / 'registered_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'all470_batches114_accepted_baked_layers_and_registered_checks_pass': True,
        'only_two_changed_components': changed,
        'all675_graphics_and_all_other_internal_files_exact_V745': True,
        'all3668_native_IDs_and_prior7_revisions_preserved': True,
        'native_warm_cold_copies': cases, 'complete_copy_case_count': len(cases) * 2,
        'native_file_IO_bridged_to_exact_input_not_actual_GPU_evidence': True,
        'meaningful_rejection_controls': controls, 'live_parent_verification_pending': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'V746: {len(cases) * 2} complete native copies; five rejection controls; prior prose/graphics exact.', flush=True)


if __name__ == '__main__':
    main()
