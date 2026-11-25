"""Persist completed research gates and the specific live registered build handle."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v1 import checkpoint

ROOT = Path('work/analysis/Hodram_B171_B190_checked_20261104')
PREP = Path('work/analysis/Hodram_B171_B190_release_20261104/registered_preparation.json')
QUAL = Path('work/analysis/Hodram_B171_B190_release_qualification_20261104/qualification.json')


if __name__ == '__main__':
    checked, prepared, qualification = map(load, [ROOT / 'formatting_checkpoint.json', PREP, QUAL])
    assert checked['all_individual_five_gates_pass_in_research'] and checked['prose_reviews'] == 435
    assert qualification['direct_andshared_scene_targets_equal'] and len(qualification['semantic_rejections']) == 6
    summary = ('B171–B190: all435 individual five-gate research reviews pass (195 revisions/240 retentions), with49 scoped name/term retentions,439 pages and15 layout corrections. '
        'Five initialized English coldboots/85005frames,413 complete body planes,27 headers,both menu highlights/branches andeight final QA sheets pass. '
        'All130 town and30 pirate body calls match their ordered source-command sequences. Six new production rejection cases pass;all114 accepted layers/six prior final stages preserved. '
        'Registered cumulative build42463 started;manifest/clean patch/own startup/once-only credit remain.9498 complete;main unchanged. Full scope/allROMs/evidence preserved;no guide photos.')
    text = '''# Hodram B171–B190: five research gates pass; registered build started

All 435 individual five-gate research reviews pass: 195 proposed revisions and 240 justified retentions. The 49 scoped name/term decisions remain retentions. All 439 stored/native/visually approved pages, both menu captions, 31 name strings, 390 relative cases and 325 archive loads remain checked. Fifteen layout corrections preserve the prose. Reuse these completed checks.

Five initialized English coldboots total 85005 frames. They bind 413 complete body capture planes, 27 name headers and both complete menu highlights to native output. All eight final QA sheets were directly viewed or reused through identical image hashes (first five); the final three were directly viewed. The B171 runs observe both menu choices and distinct responses, normal First/F rendering, complete names/portraits, both pages of all three refined page transitions and the complete one-page question. B179 retains all original commands/transitions/effects/cleanup and observes all 30 copied source body calls, all 13 FE panels, the R47 terminal-space case and the following port return. The town run observes all 130 copied body calls across all eleven complete exchanges.

The default menu highlight was partial at the initial two sampled frames. A focused 5001-frame run changes only screenshot density, with no ROM/input change, and observes the complete default highlight at frame 4498. The refusal highlight at 4680 also matches every caption glyph, blank guard and turquoise/gray background. No engine, font or ROM correction was needed for this sampling issue.

The earlier equivalence-only analysis and its town first/last contact labels are historical. Final source attribution also checks the complete ordered native body-call sequence against byte-exact sequential source commands; a repeated Yeah, yeah cannot be assigned to a different town exchange just because its pixels match. No emulator replay was needed for this correction. Final evidence: `work/analysis/Hodram_B171_B190_actual_pixels_v2_20261104/focused_actual_pixels.json`.

These are initialized content tests. B171/B179 keep their complete original scene commands; their outer natural activation is excluded. The town fixture keeps whole exchanges in original internal order but excludes nontext town conditions and market effects. It does not verify original town layout/control effects, natural conditional activation or economic outcomes. B172–B178, other B171 conditional branches, full catalogues and individual item/city/sail widgets remain offline-only. Later opening/port/sailing frames add no target editorial coverage. No complete natural route or hardware verification is claimed. No guide photos.

Final reviews are `translations/hodram_B171_B190_contextual_final_review_v1.json` and `translations/hodram_B171_B190_scoped_names_final_v1.json`. Research gate/actual evidence is under `work/analysis/Hodram_B171_B190_checked_20261104/`. Registration preparation is `work/analysis/Hodram_B171_B190_release_20261104/registered_preparation.json`; production qualification is `work/analysis/Hodram_B171_B190_release_qualification_20261104/qualification.json`.

The new `dk4tool.patch.reviewed_scene_batch_v8` derives from the unchanged generic complete-scene module, qualifies ordinary two-choice coverage and the exact B179 owned zero-ink events, and introduces no B156 cinematic assumptions. Direct/shared production plans agree. Six invalid new cases are rejected: failed fifth gate, altered encoded layout, nonspace terminal event, wrong choice index, stale parent and missing highlight index. Unchanged final-stage negative qualifications are reused; the final static-data stage passes on its new complete predecessor. All prior profiles and all 114 accepted layers are preserved, along with ASCII right bounds and the five later name/static stages.

Registered build session **42463** has started with `scripts/build_integrated_release_with_static_text.py`, profile `all-routes-hodram-b171-b190-static-text-20261104`, work folder `work/analysis/Hodram_B171_B190_registered_build_20261104` and target `out/all_routes_combined_hodram_b171_b190_static_text_20261104_candidate.nds`. The canonical driver reported all original guards enabled. Poll that handle or inspect authoritative process/terminal state; elapsed time or an output-file absence does not mean it failed. Do not restart it solely for an observation timeout. Previous comparable cumulative builds required roughly 22–27 minutes.

After the build succeeds, verify its complete manifest/profile/stack, exact clean-input patch, target byte identity and candidate-own ordinary startup. The expected full target SHA256 is `d14c24ba6aefd312099970423b8e1a9611a5913bc85f87feeb70fae00b0fe19a`, equal to the pinned full-scene research reference; that equality alone is not a registered handoff. Only then credit all 435 records once and update the current handoff. Main remains unchanged and needs user acceptance before promotion.

Coverage stays 9498 completed (5809 revisions/3689 retentions); historical source/prose/draft counters stay 9501. Full editorial scope, every earlier translation/retention/ROM/evidence artifact, graphics separation and the later older-record technical re-audit remain intact. No promotion, commit/push, pruning or guide photos.
'''
    checkpoint(mutation=ROOT / 'build_started_ledger_mutation_v1', batch_key='Hodram_B171_B190_clean_next_20261102',
        batch_updates=dict(five_gate_research_reviews=435, all_individual_fifth_gates_still_false=False,
            representative_gameplay_pending=False, actual_new_batch_gameplay=True, actual_runs=5, actual_frames=85005,
            actual_complete_body_planes=413, actual_name_headers=27, actual_menu_highlights=2, actual_review_sheets=8,
            actual_all130_town_and30_pirate_body_calls_ordered_source_exact=True,
            final_review=checked['final_review'], final_review_sha256=checked['final_review_sha256'],
            research_checkpoint=str(ROOT / 'formatting_checkpoint.json'), research_checkpoint_sha256=sha((ROOT / 'formatting_checkpoint.json').read_bytes()),
            production_qualification=str(QUAL), production_qualification_sha256=sha(QUAL.read_bytes()),
            prepared_profile=prepared['profile'], registry_preparation=str(PREP), registry_preparation_sha256=sha(PREP.read_bytes()),
            registered_build=dict(session=42463, started=True, terminal=False, authoritative_last_output='Canonical builder reconstruction started; all original guards enabled.'),
            no_live_job=False, registered_release_pending=True, new_credit=0, full_goal_complete=False, guide_photos=False),
        summary=summary, document='docs/editorial_hodram_B171_B190_checked_20261104.md', document_text=text, completed=9498,
        protected={'translations/release_stack.json': prepared['registry_sha256'],
            'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            'out/all_routes_combined_hodram_b151_b170_static_text_20261102_candidate.nds': '7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399'})
    print('Saved completed research/qualification checkpoint and live build42463;9498 prior completions preserved;full goal active.')
