"""Record newly resolved Deck terminology while preserving pending controls and zero credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.save_editorial_progress_checkpoint_v4 import checkpoint
from scripts import checkpoint_HELP_priority_progress_20261104_v1 as previous

COMPARE = 'work/analysis/Shared_HELP_T103_T132_clean_20261104/whole_article_comparisons_v2.json'
BIND = 'work/analysis/Shared_HELP_T103_T132_clean_20261104/native_roles_rooms_andskills_v1.json'
SUMMARY = previous.SUMMARY.replace(
    'Next30 Deck/crew comparisons have7 proposed revisions/23 word-exact retention candidates; native localization bindings and all display gates remain.',
    'Next30 Deck/crew comparisons now have12 revisions/18 exact-body retentions and27 four-gate passes. Sixteen native roles/35 stored labels bind real Health/Social/Tactics mismatches;103/104/106 control bindings and all display gates remain.')

DOCUMENT = '''# Deck tutorial terminology checkpoint

Continue the full Rafael/tutorial-priority checkpoint in [the preserved release and Help batch handoff](editorial_town_integrated_help37_build_sea22_fleet66_20261104.md). Its Town23 verification/credit, live37 build, qualified22 and qualified66 amendment remain current. No new credits or promotion;11359 integrated completions.

The latest30-article comparison is now `work/analysis/Shared_HELP_T103_T132_clean_20261104/whole_article_comparisons_v2.json`:12 revisions/18 exact-body retentions,27 individual four-prose-gate passes. This supersedes the provisional7/23 decisions. All30 source/current references and individual findings are retained. All display gates remain open.

`native_roles_rooms_andskills_v1.json` in the same directory binds16 native roles from the verified Town ROM's own RAM plus35 exact stored source/current room, skill and command labels. Role selector bytes are clean/current/own-RAM exact; source/current pointers and complete label bytes, including retained native trailing phase spaces, are recorded. This is offline source/current label evidence, not individual room/skill UI visits.

Concrete corrections: clean生命力 is current Health, not older Help Vigor; clean説得力 is Social, not Speech; clean謀略術 is Tactics, not Guile. Targeted records116/117/118/121/126 are corrected while preserving each threshold and effect. Workroom hub110 uses recognizable native room names including Lounge, Sickbay, Nursery and Tactics Room. Full Office/Cabin/Room descriptions remain where they naturally explain abbreviated native labels; no global shortening or name replacement. Title-only changes are recorded separately from18 exact-body retentions.

Only103/104/106 localization gates remain open. Bind the current native shared-menu X, map zoom-out Y and Deck auto-assignment access before approving those instructions. The older Choose Auto may be a correct description of a DS menu action; do not label it an error without that consumer evidence. After resolving the controls, format all30 logical articles, review all fresh native pages/contact sheets and use focused navigation/representative behavior checks.

The registered37 build73767/PID104848 was last confirmed running at23:44 November4. Continue polling that job; do not restart it or change its registry until terminal. Verify it once complete, then integrate the qualified Command amendment with the reviewed22 before granting any37 completion credit. See the previous checkpoint for exact paths, hashes, prepared verifiers and scope. All previous ROMs, translations, coverage and evidence are preserved. No guide photos. The rest of the full editorial objective, separate graphics work and later older-record technical re-audit remain active.
'''

if __name__ == '__main__':
    protected = {p:sha(Path(p).read_bytes()) for p in [COMPARE,BIND,previous.FINAL37,previous.FINAL22,previous.FINAL66,previous.TOWN,previous.PREP]}
    protected.update({
        'translations/release_stack.json':'9d4a352f95f67c847a9ae29f7dd7f93a1a209c79720d070d253d5fe202299c35',
        'out/all_routes_combined_town_help23_20261104_candidate.nds':'9c5ca87bce5c4ace721ad4ce33c8409374eb412349acf4098098c927f08e7a9f',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    checkpoint(mutation='work/analysis/Editorial_checkpoint_HELP30_native_labels_20261104',
        batch_key='shared_HELP_T103_T132_contextual_20261104',
        batch_updates=dict(new_credit=0,comparisons=COMPARE,comparisons_sha256=sha(Path(COMPARE).read_bytes()),
            native_binding=BIND,native_binding_sha256=sha(Path(BIND).read_bytes()),proposed_revisions=12,justified_retentions=18,
            word_exact_retention_candidates=18,first_four_gates_passed=27,all_localization_native_binding_gates_pending=False,
            pending_localization_binding_topic_IDs=[103,104,106],all_fifth_gates_pending=True,
            all16_native_roles_and35_room_skill_command_labels_bound=True,real_Health_Social_Tactics_mismatches_corrected=True),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,next30_proposed_revisions=12,
            next30_word_exact_retention_candidates=18,next30_four_gate_passes=27,next30_native_localization_andall_display_gates_pending=False,
            next30_pending_controls=[103,104,106],next30_all_display_gates_pending=True)},
        coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch='shared_HELP_T103_T132_contextual_20261104',
            progress_evidence=COMPARE,progress_evidence_sha256=sha(Path(COMPARE).read_bytes()))},
        summary=SUMMARY,document='docs/editorial_tutorial_labels30_progress_20261104.md',document_text=DOCUMENT,completed=11359,protected=protected)
    print('Deck30 checkpoint updated:12/18,27 four-gate passes;11359 integrated unchanged, no duplicate credit.')
