"""Maintain an active graphics queue that carries completed evidence forward."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/graphics_current_work_v1.json')
ROOT = Path('work/analysis/graphics_remaining_v716')
KEY = 'current_remaining_graphics_queue_completed_work_carried_forward_v716'


def main():
    ROOT.mkdir(exist_ok=True)
    assert not LEDGER.exists()
    completed = [
        {'id': 'plaque-material', 'task': 'Wood texture and borders of the18 reviewed plaque/hint entries',
         'evidence': 'work/analysis/plaque_acceptance_v715/acceptance.json',
         'scope': 'Explicit user acceptance of the current17 static plaques and equipment backing.'},
        {'id': 'plaque-terminology-and-base-views', 'task': 'All18 plaque meanings and current base-screen lettering/crops',
         'evidence': 'work/analysis/plaque_review_v714/terminology_review.json',
         'scope': 'All18 source/context meanings,17 glyph masks,three hints and four complete current screens; overall18 audit objects remain open.'},
        {'id': 'refit-help-layout', 'task': 'Natural Refit paragraphs and shared clipping/word-wrap correction',
         'evidence': 'work/analysis/refit_help_v712/display_proof.json',
         'scope': 'All31 native font tests,23 actual displays covering13 IDs,59 whole Yard models and49 New Game pairs.'},
        {'id': 'refit-bitmap-lifetime', 'task': 'Actual Refit bitmap allocation and cleanup',
         'evidence': 'work/analysis/refit_help_v713/heap_proof.json',
         'scope': 'One ordinary native allocation/free and59 complete matching RGB/RAM pairs; repeated-entry stress is not claimed.'},
        {'id': 'event-scenes-gallery', 'task': 'All164 Event Scenes gallery positions and their captions',
         'evidence': 'work/analysis/file_requests_v681/proof.json',
         'scope': 'Complete original carousel/display/loading evidence; ordinary original comic playback is a separate task.'},
        {'id': 'character-gallery', 'task': 'All42 Characters gallery labels and portraits',
         'evidence': 'docs/characters_gallery_v525_checkpoint.md',
         'scope': 'Complete gallery family and carousel verification; this is not all story appearances.'},
        {'id': 'naming-decisions', 'task': 'Chosen Rafael,Joakim,Maria and Camille spellings',
         'evidence': 'docs/characters_gallery_v525_checkpoint.md',
         'scope': 'The spelling decisions and this verified family do not need to be reconsidered without a new inconsistency.'},
    ]
    for row in completed:
        p = Path(row['evidence'])
        assert p.exists()
        row['evidence_sha256'] = sha(p.read_bytes())
        row['queue_status'] = 'complete-not-in-active-queue'
    remaining = [
        {'id': 'original-comic-playback-and-restoration',
         'task': 'Finish original comic viewer/loading,geometry,readability and covered-background review.',
         'remaining_scope': '21 raw frames,18 translated caption regions and the related recruitment/chase/creature/decorative/reaction restoration cases; retain approved brown marks.'},
        {'id': 'normal-small-controls',
         'task': 'Resolve ordinary parents,palettes and selection states for six small controls.',
         'remaining_scope': 'Confirm,Pick Cargo,Pick Ship,Done,Rank,Cancel. Existing original loader/widget/crop fixture proofs carry forward.'},
        {'id': 'village-and-environment-contexts',
         'task': 'Finish unverified ordinary village-card and remaining environmental caption contexts.',
         'remaining_scope': 'Eight village cards,including preserved image207 fragment; reuse completed town/icon/map evidence.'},
        {'id': 'legacy-and-embedded-consumers',
         'task': 'Resolve remaining legacy/embedded graphic classifications and ordinary source/crop uses.',
         'remaining_scope': 'Standalone/Porto Estado titles,legacy/sepia resources,copyright and ship texture consumers,and unresolved aliases. Preserve completed source/tile/native tests.'},
        {'id': 'remaining-context-audit',
         'task': 'Reconcile the remaining historical context requirements against their latest evidence.',
         'remaining_scope': 'Close only the verified scopes; separate actual display risks from standalone diagnostic-model limitations. Keep the18 overall audit objects open until final reconciliation.'},
        {'id': 'final-integrated-release-and-acceptance',
         'task': 'Complete final combined-build regression,exact patch/progress audit and user acceptance.',
         'remaining_scope': 'Use the registered integrated builder if further changes are needed; retain all existing layers and complete source/visual gates. Current V712 patch reconstruction already passes.'},
    ]
    data = {'format': 'dk4-current-graphics-work-v1',
        'user_direction': 'The copied goal preserves the pre-limit scope. Completed tasks may be removed from remaining work.',
        'active_goal_status': 'active', 'active_remaining_tasks': remaining,
        'completed_work_carried_forward': completed,
        'retest_policy': 'Reopen a completed scope only when relevant assets/code/dependencies change,required final integration checks apply,or new contradictory evidence appears.',
        'scope_exclusions': {'four_low_resolution_Online_bodies':
            {'status': 'excluded-by-user-reconfirmed', 'evidence': 'work/analysis/plaque_acceptance_v715/acceptance.json'}},
        'after_goal_followup': 'Revisit older record-based checks as requested; keep this note after completion.',
        'historical22_requirements_and_original18_objects_preserved_for_provenance': True,
        'full_goal_complete': False}
    save(LEDGER, data)
    scope = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in scope}
    save(ROOT / 'audits_before.json', before)
    entry = {'ledger': str(LEDGER), 'ledger_sha256': sha(LEDGER.read_bytes()),
        'six_active_remaining_task_groups': [r['id'] for r in remaining],
        'seven_completed_scopes_carried_forward_out_of_active_queue': [r['id'] for r in completed],
        'copied_goal_not_a_request_to_repeat_completed_work': True,
        'original_scope_preserved_with_reconfirmed_Online_exception': True,
        'full_goal_complete': False}
    for name, frozen in scope.items():
        p = Path('translations') / name
        current = read(p)
        assert current == before[name]
        assert current.get('historical_pending_items_retained') == frozen['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == frozen['ongoing_plaque_inventory']
        current[KEY] = entry
        save(p, current)
    heading = '## V716: completed scopes removed from the active graphics queue'
    text = ('The user clarifies that the goal was copied from before the usage limit and permits '
        'removing completed work. The new current-work ledger carries seven completed scopes forward '
        'with exact evidence hashes and keeps six unresolved groups active. Plaque material approval, '
        'base plaque terminology/display,Refit layout/lifetime and verified Gallery families are not '
        'routine repeat work. Reopen them only for relevant changes,new defects or required final '
        'integration checks. Four Online bodies remain excluded. Original18 overall audit objects '
        'and22 historical requirements stay exact; the full objective and later older-record note '
        'are preserved. See [remaining work](graphics_remaining_work.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        p = Path('docs') / name
        content = p.read_text(encoding='utf-8')
        assert heading not in content
        p.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + text, encoding='utf-8')
    save(ROOT / 'record.json', entry)
    for name in scope:
        current = read(Path('translations') / name)
        current.pop(KEY)
        assert current == before[name]
    print('V716 current queue:6 unresolved groups;7 completed scopes carried forward without routine retesting.', flush=True)


if __name__ == '__main__':
    main()
