"""Archive bounded source-flow and actual encounter evidence, keeping all graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_encounter_contexts_v619 import ROM, ROOT, RUN
from scripts.verify_village_wrap_v608 import read, save

FLOW = Path('work/analysis/owner_flow_v619')
DOC = Path('docs/owner_flow_and_encounter_v619_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V619 Owner flow and encounter')
KEY = 'expanded_owner_flow_and_current_encounter_ship_state_v619'


def main():
    flow, encounter = read(FLOW / 'flow_followup_proof.json'), read(ROOT / 'encounter_proof.json')
    digest = sha(ROM.read_bytes())
    assert flow['candidate_sha256'] == encounter['candidate_sha256'] == digest
    assert flow['script_sha256'] == sha(Path('scripts/verify_owner_flow_v619.py').read_bytes())
    assert encounter['script_sha256'] == sha(Path('scripts/verify_encounter_contexts_v619.py').read_bytes())
    assert flow['flow_proof_sha256'] == sha((FLOW / 'flow_candidates.json').read_bytes())
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, FLOW / 'flow_followup_proof.json', FLOW / 'flow_candidates.json', ROOT / 'encounter_proof.json',
             ROOT / 'normal_encounter_prefix.json', ROOT / 'source_encounter_replay.json',
             ROOT / 'actual_fleet_position_census.json', ROOT / 'read_only_original_ship_stat_getters.json',
             RUN / 'capture_report.json', RUN / 'navigation_command_journal.json',
             Path('scripts/scan_owner_flow_v619.py'), Path('scripts/verify_owner_flow_v619.py'),
             Path('scripts/verify_encounter_contexts_v619.py'), Path(__file__)]
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    report = read(RUN / 'capture_report.json')
    shots = {r['frame']: r for r in report['frames_captured']}
    rows = []
    for frame in (19800, 20000, 20400, 20800, 21200, 21600, 22000, 22500, 23700, 24500):
        row = shots[frame]
        target = ARCHIVE / f'Encounter_{frame:06d}_UNMODIFIED_NATIVE.png'
        checked_copy(row['path'], target)
        rows.append({'path': str(target), 'sha256': row['PNG_sha256'], 'frame': frame,
                     'ROM_sha256': digest, 'isolated_source_DSV_used': True, 'no_new_RAM_fixture': True,
                     'unmodified_capture': True, 'battle_victory_reward_or_guide_credit': False})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': digest, 'screenshots': rows,
         'ROM_patch_donors_and_registry_unchanged': True, 'publication_approved': False, 'full_goal_complete': False,
         'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'source_flow_proof': str(FLOW / 'flow_followup_proof.json'),
             'source_flow_proof_sha256': sha((FLOW / 'flow_followup_proof.json').read_bytes()),
             'actual_encounter_proof': str(ROOT / 'encounter_proof.json'),
             'actual_encounter_proof_sha256': sha((ROOT / 'encounter_proof.json').read_bytes()),
             'candidate_sha256': digest, 'status': 'bounded_source_flow_and_ordinary_encounter_no_new_graphics_clearance',
             'cross_branch_call_preservation_indexed_table_and_final_join_candidates_checked': True,
             '12_independent_native_control_witnesses_and315_original_owner_initializers_pass': True,
             'seven_candidates_classified_no_new_ordinary_Confirm_miniature_parent': True,
             'actual_two_complete_fire_notices_and_native_ship_depletion_verified': True,
             'actual_battle_outcome_or_reward_screens_not_proven': True,
             'next_action': encounter['next_action'], 'archive': str(ARCHIVE), 'unmodified_screenshots': len(rows),
             'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
             'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        d = read(path)
        assert d.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert d.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        pointers = {k: v for k, v in d.items() if k in ('candidate', 'candidate_sha256', 'latest_candidate',
                    'latest_candidate_sha256', 'current_verified_release_candidate', 'current_verified_release_candidate_sha256',
                    'latest_graphics_preservation', 'latest_compiled_experimental_candidate_with_inherited_native_gap')}
        d[KEY] = entry
        d['current_goal_turn_classification'] = 'progress'
        save(path, d)
        now = read(path)
        assert all(now[k] == v for k, v in pointers.items())
        assert now.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert now.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V619 research: broader owner flow and actual encounter preparation'
    text = '''

The bounded ARM flow model now follows branches/joins,callee-saved registers
across opaque ARM/interworking calls,and indexed source-table loads. Final-state
candidates and12 independent native ISA witnesses reject stale/clobbered facts.
428841 instruction candidates include the actual runtime pool copy;all7 matches
remain known initializer fields or the source-row216 decoration. Complete315-owner
initialization matches clean source. No new ordinary Confirm/miniature parent or
global non-use conclusion follows;Thumb/runtime/switch/alias paths remain open.

The original Copenhagen/Speyer encounter prefix cold-boots on unchanged V617.
Normal controls continue to24500,including complete gunpowder-fire/extinguished
notices. Native CMobileShip virtual getters verify own Hull48 to47,Crew19 to3;
the sampled enemy stays Hull30/Crew21. The model resolves to Vestaros. No new
cheat,RAM/save/outcome mutation occurs;combat victory and rewards are not proven.
Next establish bounded ship-recovery/proximity fixtures and original engagement
controls. Ten unmodified captures,full schedule/journal and proofs are on E.
ROM/patch/registry/canonical remain exact;all18 plaques incomplete,all22 historical
scopes retained,and full graphics goal active. See
[V619 checkpoint](owner_flow_and_encounter_v619_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print('Archived10 unmodified encounter captures and bounded flow/native proofs;3 audits updated;18/22 scopes exact;V617 unchanged;goal active.')


if __name__ == '__main__':
    main()
