"""Persist five-gate330 progress without granting integration credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    final=Path('translations/rafael_B81_B84_contextual_final_review_v1.json');doc=load(final)
    proof=Path('work/analysis/Rafael330_checked_20261105/formatting_checkpoint.json');p=load(proof)
    assert p['all_five_individual_gates_pass_in_research'] and p['final_review_sha256']==sha(final.read_bytes())
    manuscript=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v3.json')
    summary=('Rafael/tutorial priority continues.330 contextual decisions nowpassallfive research gates(174 revisions/156 retentions).'
        'All336 native/stored/viewed body pages,five typedcaptions and16 scoped names pass;source-owned FE continuations solvebothlong tutorials.'
        '18 layout-only refinements fixseven page turns/11 phrase wraps;four Latin artifacts fixed. Two food-exchange prose lines wereimproved '
        'after contextual actual review,withfresh single-record formatting/storage andshort9-speech initialized tests;335 exact pages reused eachtime.'
        'Current-wording gameplay coverage75 source speeches/86 pages plusfive captions;250 speeches offline-only. Six runs/72406 frames retained;'
        'no fullroute/hardware/reward-stat/originalmenu-outcome claim. Registered330 integration and97 new Help articles plusCoerce33 amendment remain.'
        '11418 integrated,experimental81511dde/main unchanged;no live jobs,no newcredit,no guide photos,all scope/ROMs/evidence preserved.')
    text='''# Rafael330 research ready — November 5, 2026

Rafael’s early story and all tutorials remain first. Continue the complete editorial objective with every earlier translation, route, shared town/shop conversation, random scene, name and text-display issue retained. No guide photos, promotion, pruning or commit/push. Reuse [the preceding integrated Help59 checkpoint](editorial_help59_integrated_Rafael330_actual_20261105.md); its release verification remains current.

`translations/rafael_B81_B84_contextual_final_review_v1.json` now passes **all five individual research gates for 330 objects: 174 revisions/156 justified retentions**. This is 325 source speeches and five choice labels across the complete Emilio/bullfight, Cristina/Mivor, rescue and Gerhard/combat-training exchanges. The two long FE paragraphs retain every word through four native panels with repeated exact source controls; virtual commands add no editorial credit. Other255 source speeches in the B81–100 packet still need drafts/comparisons.

Final manuscript is `translations/rafael_B81_B84_contextual_editorial_manuscript_v3.json`. The complete food exchange prompted two actual prose improvements: R220’s food-driven acceptance and R216’s formerly stiff “There must be!” Rafael now says, “That's right! There must be all kinds of food out there!” Both preserve clean Japanese intent and characterization. R216 was already a revision, so counts remain174/156. Fresh native pages were individually viewed. Both incremental iterations reused326 exact stored records/335 pages, refreshed all140 branch cases and catalogue selection, and updated archive loads/two changed parent modes. No full-scene rerun for these single paragraphs.

Current reconstruction: `work/analysis/Rafael_B81_B84_rebuilt_v3_20261105/reconstruction.json`. Consumer proofs: `work/analysis/Rafael330_stored_consumer_inputs_v3_20261105/`, `Rafael330_stored_native_v3_20261105/`, `Rafael330_stored_catalogue_v3_20261105/` and `Rafael330_loaders_v3_20261105/`. All327 native speech commands/336 complete body pages pass source/current controls, substitutions, complete glyphs, bounds, storage, allocation, pagination, branch and archive checks. `work/analysis/Rafael330_checked_20261105/` seals exact per-source final references, visual approval, release plans and actual/offline scope. Final names/roles: `translations/rafael_B81_B84_scoped_names_actual_final_v1.json` (16 contextual retentions/native and actual headers; full catalogue UI remains unvisited).

Current actual coverage is75 source speeches/77 native commands/86 body pages plus allfive captions,80 editorial objects;250 source speeches are offline-only. Six initialized runs total72406 frames, withfive current-compatible runs/65205 frames. Earlier food-v2 captures are preserved and never relabelled as the changed R216 wording. Final nine-speech/7201-frame food/recruitment run: `work/analysis/Rafael_food_run_v3_20261105/terminal.json`; complete body/header pixel proof: `Rafael_food_actual_pixels_v3_20261105/focused_actual_pixels.json`; allnine final pages were directly viewed on `Rafael_food_actual_sheets_v3_20261105/actual_dialogue_1.png`.

Reuse the qualified full101-command B81 scene,49/51 visited speeches, withtwo conditional asides separately seen in the focused sequence. Static Emilio CG doesnot determine who throws whom; retain faithful implicit wording. All16 headers,allnine two-page cases/seven refined page turns,four FE panels/continuations,three FI notice texts,all two-/three-choice cursor positions andA returns are observed. Numeric return registers, original story outcome branches/cancellation, actual training-stat effects, natural event activation, fullroute and hardware remain unvisited. Targeted initialized emulator fixtures and offline native checks are distinct evidence.

Next integrate330 with the97 remaining new Help articles (30 new pluszero-credit Coerce33 correction,then67) as one ordered cumulative successor where practical, preserving all114 accepted layers/eight final stages/ASCII bounds. The Help31 parent resource is already exactly current675 (`71a0d5bb`),and Help67 follows its compiled target (`01cd9dbd`); avoid repeating completed research or gameplay. Source-owned FE pagination requires the registered scene compiler to reconstruct its two extra commands rather than treating them as new source records.

Integrated completions remain **11418 =6645 revisions+4773 retentions**. Verified experimental candidate remains `out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds`,SHA-256 `81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635`; exact clean patch andown startup/name checks remainpassed. Registry `82a17be4` andoriginal core `27ce0796` unchanged. Main stays `out/raphael_natural_v2_accepted_base.nds`,SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. No live build/emulator. No330 credit until registered integration. Graphics artwork andthe laterolder-record technical re-audit remainseparate. Fullgoalactive.
'''
    protected={
        'translations/release_stack.json':'82a17be4f7610abef225fa39c2059cd4180511af5683f519aec8171de3df5f4e',
        'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
        'out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds':'81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        str(final):sha(final.read_bytes()),str(proof):sha(proof.read_bytes())}
    checkpoint(mutation='work/analysis/Rafael330_research_ready_checkpoint_20261105',completed=11418,protected=protected,
        batch_key='Rafael_SC0_B81_B100_clean_20261105',summary=summary,
        document='docs/editorial_Rafael330_research_ready_20261105.md',document_text=text,
        batch_updates=dict(new_credit=0,manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
            final_review=str(final),final_review_sha256=sha(final.read_bytes()),all_fifth_gates_pending=False,five_gate_passes=330,
            all_registered_integration_pending=True,new_Emilio_stored_andactual_pending=False,
            all330_native_stored_catalogue_branches_loaders_andrepresentative_actual_checks_pass=True,
            latest_wording_compatible_actual_source_speeches=75,latest_wording_compatible_actual_body_pages=86,
            offline_only_source_speeches=250,native_body_records=327,native_body_pages=336,
            final_body_proof='work/analysis/Rafael330_stored_consumer_inputs_v3_20261105/native_consumer_planes.json',
            final_body_proof_sha256=sha(Path('work/analysis/Rafael330_stored_consumer_inputs_v3_20261105/native_consumer_planes.json').read_bytes()),
            new_gameplay_runs=6,total_frames=72406,current_qualifying_runs=5,current_qualifying_frames=65205,
            formal_research_checkpoint=str(proof),formal_research_checkpoint_sha256=sha(proof.read_bytes())),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current330_five_gate_research_ready=True,current330_native_body_pages=336,
            current330_actual_source_speeches=75,current330_offline_source_speeches=250,
            registered_cumulative_integration_next=True,
            next_focus='Register one ordered97-Help-plus330-Rafael successor,preserving all eight stages;thenremaining255 Rafael drafts/comparisons.')})
    print('Saved330 five-gate research checkpoint;11418 integrated unchanged;no new credit orpromotion.')
