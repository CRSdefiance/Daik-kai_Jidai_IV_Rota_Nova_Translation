"""Save the source-return search boundary without claiming actual control use."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/owner_returns_v658')
DOC = Path('docs/owner_returns_v658_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V658 Owner returns')
KEY = 'source_bound64_pure_ARM_helpers1991_native_return_contexts_no_new_control_parent_v658'


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(proof['all1991_resolved_source_call_return_contexts']) == proof['total_native_context_witnesses'] == 1991
    assert len(proof['candidate_owner_addresses_not_new_ordinary_parents']) == 7
    assert not proof['full_goal_complete']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in (DOC, Path(__file__), *(Path(p) for p in proof['scripts']), *ROOT.glob('*.json')):
        checked_copy(source, ARCHIVE / source.name)
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'all64_complete_pure_helper_bodies_and_PC_literals_clean_exact128_native_cases': True,
        'all1991_resolved_return_contexts_original_callee_ABI_and_no_write_witnesses_pass': True,
        'source_controls_preserve_calculated_return_positive_and_unknown_call_input_negatives': True,
        'seven_existing_owner_candidates_reconciled_original_initializer_and_row216_decoration': True,
        'no_new_miniature_or_Confirm_ordinary_parent_display_or_global_nonuse_credit': True,
        'input_memory_stack_Thumb_switch_indirect_and_other_runtime_readers_remain_open': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V658: native helper-return analysis for unresolved small controls'
    addition = ('A separate V619 flow implementation adds source-bound pure ARM leaf return '
        'expressions. All 64 complete bodies/literals match clean; 128 original native cases '
        'pass. The fixed-point scan resolves 1,991 return contexts, independently checked '
        'through 1,991 complete original native callee executions with ABI/no-write checks. '
        'Controls retain a calculated owner return and uncertainty for unknown arguments '
        'and opaque calls. No additional Frame/Confirm candidate is found: six existing '
        'initializer stores and the known source-row216 decoration are reconciled. '
        'This closes that specific search gap, not ordinary control reachability or global '
        'non-use. Input-memory/stack aliases, non-pure calls, Thumb, switches and indirect '
        'runtime paths remain open. No new ROM, screenshot, GPU, guide or release pointer '
        'changes; all 18 plaques stay incomplete and 22 historical scopes exact. Evidence '
        'archived on E; full goal active. See [V658 checkpoint](owner_returns_v658_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'no_new_screenshot_GPU_ordinary_control_global_nonuse_or_guide_credit': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), *(Path(p) for p in proof['scripts']))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V658 native return evidence archived; three audits/four progress documents updated; graphics goal active.')


if __name__ == '__main__':
    main()
