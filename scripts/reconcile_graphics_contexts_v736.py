"""Reconcile current graphics obligations without changing historical evidence."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_condition_fixtures_v520 import HEALTH, MOOD
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/context_reconciliation_v736')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
OWNERS = {
    1: ['original-comic-playback-and-restoration'],
    2: ['legacy-and-embedded-consumers'],
    3: [],
    4: ['village-and-environment-contexts'],
    5: [],
    6: ['original-comic-playback-and-restoration', 'normal-small-controls',
        'village-and-environment-contexts', 'legacy-and-embedded-consumers'],
    7: ['final-integrated-release-and-acceptance'],
    8: [],
    9: ['legacy-and-embedded-consumers'],
    10: ['legacy-and-embedded-consumers'],
    11: ['original-comic-playback-and-restoration'],
    12: ['original-comic-playback-and-restoration'],
    13: ['original-comic-playback-and-restoration'],
    14: ['original-comic-playback-and-restoration'],
    15: ['original-comic-playback-and-restoration'],
    16: [],
    17: [],
    18: ['final-integrated-release-and-acceptance'],
    19: ['final-integrated-release-and-acceptance'],
    20: [],
    21: ['final-integrated-release-and-acceptance'],
    22: ['legacy-and-embedded-consumers'],
}


def reference(path):
    path = Path(path)
    return {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    assert not (ROOT / 'proof.json').exists()
    ROOT.mkdir(parents=True, exist_ok=True)
    matrix, ledger = read(MATRIX), read(LEDGER)
    pre = read('work/analysis/village_request_sweep_v735/preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(ledger['active_remaining_tasks']) == 6
    assert len(ledger['completed_work_carried_forward']) == 26
    for live, filename in ((MATRIX, 'requirements_before_v736.json'),
                           (LEDGER, 'work_before_v736.json')):
        (ROOT / filename).write_bytes(live.read_bytes())
    historical = []
    for row in matrix['historical22_current_reconciliation']:
        refs = []
        for ref in row['evidence']:
            assert reference(ref['path'])['sha256'] == ref['sha256'], ref
            refs.append(ref)
        index = row['historical_item']
        historical.append({'historical_item': index,
                           'unchanged_original_requirement': row['original_requirement'],
                           'checked_evidence': refs, 'remaining_work_owners': OWNERS[index],
                           'completed_source_and_tested_scopes_carried': row['completed_subscopes'],
                           'remaining_or_scope_limit': row['remaining_scope_or_verification_limit'],
                           'scope_disposition': 'remaining-assigned-to-specific-work' if OWNERS[index]
                           else 'tested-requirement-complete-limits-retained'})
    assert {r['historical_item'] for r in historical} == set(range(1, 23))
    rom = NdsImage.open(ROM)
    assets = []
    for row in matrix['original26_confirmed_entries_current_implementation_links']:
        digest = sha(rom.read_file(row['path']))
        assert digest == row['current_whole_file_sha256'], row['path']
        assert row['matching_registered_file_batches']
        assets.append({'path': row['path'], 'texture_index': row['texture_index'],
                       'current_whole_file_sha256': digest,
                       'registered_batches': [reference(p) for p in row['matching_registered_file_batches']],
                       'not_new_native_display_or_complete_record_coverage_claim': True})
    assert len(assets) == 26
    acceptance = read('work/analysis/plaque_acceptance_v715/acceptance.json')
    assert acceptance['plaque_material_gate'] == 'closed-user-accepted'
    assert acceptance['all18_overall_audit_entries_remain_incomplete']
    for path, digest in acceptance['accepted_static_asset_sha256'].items():
        assert sha(rom.read_file(path)) == digest
    for ref in acceptance['accepted_comparison_sheets']:
        assert reference(ref['path'])['sha256'] == ref['sha256']
    material = read('work/analysis/plaque_review_v714/current_plaque_review_proof.json')
    terms = read('work/analysis/plaque_review_v714/terminology_review.json')
    original = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    objects = next(iter(original.values()))['ongoing_plaque_inventory']
    assert len(objects) == len(material['all18_current_native_review_entries']) == 18
    assert len(material['all17_independent_complete_font_masks']) == 17
    entries = []
    for old, observed, term in zip(objects, material['all18_current_native_review_entries'],
                                    terms['all18_source_context_and_natural_English_decisions'], strict=True):
        assert not old['fully_completed'] and not term['translation_revision_required']
        assert old['english'] == observed['English'] == term['English']
        assert old['bounds'] == observed['bounds']
        assert term['original'] == observed['Japanese']
        if 'id' in old:
            assert old['id'] == term['id'] == observed['id']
        for field in ('source', 'current'):
            crop = Path(observed[field + '_crop'])
            assert sha(crop.read_bytes()) == observed[field + '_crop_sha256']
            full = observed[field + '_PNG']
            assert sha(Path(full['path']).read_bytes()) == full['PNG_sha256']
            native = Image.open(full['path']).convert('RGB').crop(observed['bounds'])
            assert native.tobytes() == Image.open(crop).convert('RGB').tobytes()
        entries.append({'id': observed['id'], 'English': old['english'], 'Japanese': term['original'],
                        'screen': old['screen'], 'bounds': old['bounds'],
                        'material_and_borders': 'accepted-by-user-V715-current-bytes-exact',
                        'translation': 'reviewed-natural-faithful-English-no-revision-required',
                        'native_base_lettering_crop': 'complete-current-V712-proof-and-source-crops-rechecked',
                        'specific_additional_context_evidence': (
                            ['V657 all3 allocation policies and five selected ship rows'] if old['screen'] == 'Assign Sailors'
                            else ['V637 two actors/all84 condition combinations', 'V728 current0/100 stats and restoration',
                                  'V730 current longest equipment hints and occupied/empty slots']),
                        'final_audit_owner': 'final-integrated-release-and-acceptance',
                        'remaining': 'Final combined-release review/sign-off; reopen display checks only for changed dependencies or contradictory evidence.',
                        'all_actor_fleet_acquisition_hardware_combinations_not_claimed': True,
                        'fully_completed': False})
    arm = rom.read_file('/__arm9__.bin')
    crew = read('work/analysis/crew_policy_matrix_v657/proof.json')
    previous = NdsImage.open(crew['candidate']).read_file('/__arm9__.bin')
    assert GameAsciiFont.from_arm9(arm).glyphs == GameAsciiFont.from_arm9(previous).glyphs
    crew_spans = []
    for span in crew['original_native_clean_current_code_spans']:
        lo, hi = span['start'] - BASE, span['end'] - BASE
        assert sha(arm[lo:hi]) == span['sha256']
        assert arm[lo:hi] == previous[lo:hi]
        crew_spans.append(span)
    condition = read('work/analysis/condition_matrix_v637/current_condition_matrix_proof.json')
    older = NdsImage.open(condition['candidate']).read_file('/__arm9__.bin')
    assert GameAsciiFont.from_arm9(arm).glyphs == GameAsciiFont.from_arm9(older).glyphs
    skill_table = struct.unpack_from('<I', arm, 0x80A74)[0] - BASE
    assert skill_table == struct.unpack_from('<I', older, 0x80A74)[0] - BASE
    condition_spans = []
    for lo, hi in ((0x7D000, 0x7EF00), (0x8091C, 0x80988),
                   (skill_table, skill_table + 23 * 28)):
        assert arm[lo:hi] == older[lo:hi]
        condition_spans.append({'start': BASE + lo, 'end': BASE + hi, 'sha256': sha(arm[lo:hi])})
    # Re-execute current selector methods on a guarded actor-layout input.
    # They read bytes6/7 from an actor pointer, rather than taking a state enum.
    # Use current exported RAM for the original already-loaded string pool.
    hints = read('work/analysis/long_hints_v730/proof.json')
    report = read(hints['report'])
    snapshot = report['read_only_RAM_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256'] and report['ROM_sha256'] == matrix['candidate_sha256']
    u = machine(arm)
    u.mem_write(BASE, raw)
    assert bytes(u.mem_read(BASE + 0x7E070, 0x98)) == arm[0x7E070:0x7E108]
    actor = 0x023FF000
    assert bytes(u.mem_read(actor - 16, 48)) == raw[actor - BASE - 16:actor - BASE + 32]
    u.mem_write(actor - 16, b'\xA5' * 48)
    selected = []
    for kind, states, method, field in (('Health', HEALTH, 0x7E0BC, 6), ('Mood', MOOD, 0x7E070, 7)):
        for state, text in enumerate(states):
            u.mem_write(actor + field, bytes([state]))
            before = bytes(u.mem_read(BASE, 0x400000))
            executed = call(u, method, (actor,))
            assert bytes(u.mem_read(BASE, 0x400000)) == before
            assert all(bytes(u.mem_read(pc, 4)) == arm[pc - BASE:pc - BASE + 4] for pc in executed)
            pointer = u.reg_read(UC_ARM_REG_R0)
            actual = bytes(u.mem_read(pointer, 40)).split(b'\0')[0].decode('ascii')
            assert actual == text
            selected.append({'field': kind, 'state': state, 'English': text, 'current_native_pointer': pointer,
                             'actor_layout_input': actor, 'read_byte_offset': field,
                             'complete4MiB_RAM_and_ABI_unchanged_by_selector': True})
    proof = {'candidate': reference(ROM), 'matrix_before': reference(ROOT / 'requirements_before_v736.json'),
             'ledger_before': reference(ROOT / 'work_before_v736.json'),
             'all22_historical_requirements_explicitly_owned_or_tested_complete': historical,
             'all26_confirmed_asset_hashes_and_registered_batches_checked': assets,
             'all18_current_plaque_audit_rows': entries,
             'material_user_acceptance': reference('work/analysis/plaque_acceptance_v715/acceptance.json'),
             'V657_crew_dependency_spans_current_exact': crew_spans,
             'V637_condition_dependency_spans_current_exact': condition_spans,
             'all13_current_native_condition_selectors': selected,
             'current_RAM_for_existing_loaded_string_pool': snapshot,
             'prototype_enum_argument_corrected_to_source_actor_pointer_no_ROM_change': True,
             'historical_condition_and_policy_runs_not_relabelled_as_new_emulator_tests': True,
             'no_original18_or22_historical_object_edits_or_full_completion_claim': True,
             'reconciliation_group_complete_substantive_consumer_work_and_final_review_still_open': True,
             'release_hashes_unchanged': pre['release_hashes'],
             'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT / 'proof.json', proof)
    print('V736:22 requirements assigned,26 asset entries checked,18 current plaque rows reconciled; overall sign-off pending.', flush=True)


if __name__ == '__main__':
    main()
