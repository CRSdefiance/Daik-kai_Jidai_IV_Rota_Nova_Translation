"""Save exact native reuse/display findings and the delivered weekend package without credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael557_display_checkpoint_v1_20261105')
PROSE=Path('translations/rafael_B141_B160_contextual_review_v3.json')
DOC=Path('translations/rafael_B141_B160_formatting_manuscript_v3.json')
PLAN=Path('work/analysis/Rafael557_automatic_plans_v7_20261105/automatic_plans.json')
PREF=Path('translations/rafael_B141_B160_visual_preferences_v7.json')
MACROS=Path('work/analysis/Rafael557_macros_inputs_v1_20261105/qualified_identity_andmacros.json')
REUSE=Path('work/analysis/Rafael557_native_resume_inputs_v1_20261105/exact_reused_native_records.json')
NAMES=Path('work/analysis/Rafael557_name_planes_v1_20261105/native_name_planes.json')
MENUS=Path('work/analysis/Rafael557_two_choice_v1_20261105/complete_choice_objects.json')
STYLES=Path('work/analysis/Rafael557_all_caption_styles_v1_20261105/receipt.json')
FE=Path('work/analysis/Rafael557_FE_diagnostic_v2_20261105/FE_row_diagnostics.json')
PACKAGE=Path('work/analysis/Weekend_testing_package_v1_20261105/package_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan,prefs,macros,reuse,names,menus,styles,fe,package=map(load,[DOC,PLAN,PREF,MACROS,REUSE,NAMES,MENUS,STYLES,FE,PACKAGE])
    assert len(doc['records'])==557 and plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(plan['records'])==549 and sum(r['expected_native_pages'] for r in plan['records'])==558
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert all(not r['review']['formatting'] for r in doc['records'])
    assert reuse['completed_old_records']==221 and reuse['completed_old_pages']==229
    assert reuse['reused_records']==reuse['reused_pages']==208 and len(reuse['retired_due_to_changed_compiled_layouts'])==13
    assert names['scoped_actors']==names['distinct_strings']==20 and names['fresh_name_planes']==11 and names['exact_reused_name_planes']==9
    assert menus['all_checks_pass'] and len(menus['objects'])==4 and styles['planes']==32
    assert not fe['failed_IDs'] and len(fe['records'])==6
    sheets=[Path('work/analysis/Rafael557_native_v1_20261105')/name for name in ['B141_part1.png','B141_part2.png','B142_part1.png',*[f'B143_part{i}.png' for i in range(1,9)]]]
    sheets += [Path(r['path']) for r in names['review_sheets']]
    sheets += [Path(r['review_sheet']['path']) for r in menus['objects']]
    sheets += [Path(styles['sheet']),Path('work/analysis/Rafael557_FE_diagnostic_v1_20261105/FE_diagnostic_sheet.png'),Path(fe['review_sheet'])]
    assert all(p.is_file() for p in sheets)
    ROOT.mkdir(parents=True)
    receipt=ROOT/'direct_visual_review_scope.json'
    save(receipt,dict(directly_viewed_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in sheets],
        baseline_native_blocks_fully_viewed=[141,142,143],baseline_body_records_viewed=110,baseline_body_pages_viewed=117,
        final_layout_exact_reused_body_pages_already_viewed=sum(r['block'] in [141,142,143] for r in reuse['records']),
        retired_changed_layout_previews_do_not_approve_final_pages=True,
        all20_public_name_planes_andall32_caption_style_planes_directly_viewed=True,
        both_six_panel_FE_diagnostic_sheets_viewed=True,no_new_gameplay_orfull_fifth_gate_credit=True,new_credit=0))
    release=load('work/analysis/Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json')
    summary=('Weekend combined candidate packaged atout/Translation_DS_Weekend_Test_2026-11-05.zip: exactregistered3bf3 ROM, '
        'manifest andclean-input patch;fresh baseline/53-file/menu/hash checks andpatch reconstruction pass. Main unchanged;557 newreviews notincluded. '
        'Rafael557 formatting nowpreserves macroorder;549 speechplans/558 pages pass withtwo exact reviewed ordinary-infinitive boundaries. '
        'FU13ASCII/78px qualified;20 nameplanes/eight labels/all32 captionstates checked andviewed. '
        'Initial native runstopped atone FE blank-row mismatch after221 complete records/229 pages;failure preserved. '
        'Exact source-bound guard reserve fixes thatnotice;all six FE row checks pass.208 unchanged native records/pages qualifiedforreuse; '
        '341 records/350 freshpages remain.117 baselinebodypages viewed;changed layouts stillneedfreshviews. '
        'No livejobs,newcredit orpromotion;integrated12712/current3bf3/main3cb8 unchanged. Fullgoal andRafael/tutorial priority preserved.')
    text=f'''# Rafael557 display and weekend handoff — November 5, 2026

The user-requested weekend package is ready: `out/Translation_DS_Weekend_Test_2026-11-05.zip` (35,477,621 bytes). It contains the exact registered **3bf3 combined ROM**, original681-entry manifest, clean-input patch, full contents/checksums and concise testing notes. Fresh verification: `{PACKAGE}`. It includes12712 integrated reviews and all114 accepted layers/eight final stages; it excludes the unfinished557-record batch. No new ROM build or main promotion. The package README identifies baseline, profile, full hashes,53 changed files and the existing4001-frame cold-boot scope. Keep these copies and all originals.

Latest557 prose: `{PROSE}`; formatter input: `{DOC}`; plans: `{PLAN}`; preferences: `{PREF}`. The guard introduction now preserves FO-before-FA macroorder. All549 speeches/558 planned pages pass with no errors or unreviewed warnings. Two exact, source-bound ordinary infinitive continuations are documented to use native width and avoid unnecessary rows/pages; no words are shortened and no ordinary breaks are authored. Four one-page trials failed native planning limits and were replaced with whole-clause page boundaries. Failed plans are preserved.

`{MACROS}` proves FU is13 ASCII characters/78px (Rafael Castor), with12 fresh original-wrapper alignment cases. FI/FA/FO reuse exact ARM9/COMMON/font/actor dependencies. Six FE panels are separately classified. Twenty public-name planes pass (11 fresh/nine exact reuses); four complete two-choice menus/eight labels pass provider, return, geometry and all32 native caption-state planes. All name/menu/style previews were directly viewed. Global full-catalogue UI remains open.

Initial native run **77468 is terminal1**, not live: `work/analysis/Rafael557_native_gc_v1_20261105/completion.json`. It completed B141–B147:221 records/229 pages. B148R121 then emitted an extra native blank row at y12 before the second text row at y24. The fresh diagnostic proves all glyphs remain complete but the planned/native row membership mismatches. Only that exact notice receives a36-cell planning budget; physical FE width remains228px. `{FE}` now proves all six FE row memberships pass, and both diagnostic sheets were viewed. No engine/font change or general narrowing is introduced. Never import unsealed partial B148 results.

`{REUSE}` qualifies **208 exact unchanged native records/pages** from complete blocks, comparing source/current references, words, compiled bytes, four ABI alignments, complete glyph/bounds/page assertions and binary/PNG hashes. Thirteen changed layouts retire their old display proofs. Ready continuation inputs: `work/analysis/Rafael557_native_resume_inputs_v1_20261105/remaining_manuscript.json` and `remaining_plans.json`: **341 records/350 pages**. All jobs are terminal; no duplicate restart is needed. Start this fresh remainder, preserving the exact208 reuse receipt:

```text
python -m scripts.run_checked_script_with_gc_v1 --script scripts/check_rafael_compiled_pages_v3.py --telemetry work/analysis/Rafael557_remaining_native_gc_v1_20261105 -- --manuscript work/analysis/Rafael557_native_resume_inputs_v1_20261105/remaining_manuscript.json --plan work/analysis/Rafael557_native_resume_inputs_v1_20261105/remaining_plans.json --release work/analysis/Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json --startup work/analysis/Rafael867_extended_release_verified_v3_20261105/own_registered_startup_verification.json --out work/analysis/Rafael557_remaining_native_v1_20261105
```

Visual scope is exact in `{receipt}`:11 original body sheets cover110 records/117 baseline pages across B141–B143. Only unchanged compiled pages retain that credit; changed pages need fresh review. B144–B147 previews still require review. Merge the complete native remainder with208 exact reuses, view every remaining/fresh page, and refine concrete findings. Then finish stored/catalogue/loader/allocation checks, representative transitions/menus/FU/pagination tests and registered cumulative integration with an exact patch. All557 fifth gates remainfalse; no new gameplay or integration credit is inferred from offline evidence.

Rafael and all tutorials remain first. Every other route, earlier unfinished contextual pass, shared town/shop/random scene, names and remaining prose remain in scope. Two catalogue de pointer fixes need proper separate ownership. Deferred artwork and later older-record re-audit stay separate. No guide photos, pruning, promotion orcommit/push. Fullgoal active; main/current registry/core unchanged.
'''
    evidence={str(p):sha(p.read_bytes()) for p in [PROSE,DOC,PLAN,PREF,MACROS,REUSE,NAMES,MENUS,STYLES,FE,PACKAGE,receipt,Path(__file__)]}
    checkpoint(mutation='work/analysis/Rafael557_display_andweekend_checkpoint_20261105',
        batch_key='Rafael_SC0_B141_B160_clean_20261105',batch_updates=dict(new_credit=0,
            manuscript=str(PROSE),manuscript_sha256=sha(PROSE.read_bytes()),formatting_manuscript=str(DOC),formatting_manuscript_sha256=sha(DOC.read_bytes()),
            visual_preferences=str(PREF),visual_preferences_sha256=sha(PREF.read_bytes()),automatic_plans=str(PLAN),automatic_plans_sha256=sha(PLAN.read_bytes()),
            planned_speeches=549,planned_pages=558,exact_reviewed_QA_boundary_retentions=2,
            current_FU_expansion_parity_andwidth_qualified=True,current_FU_expansion_parity_width_anddisplay_pending=True,
            scoped_native_name_planes=20,name_planes_directly_viewed=20,typed_caption_records_checked=8,caption_style_planes_checked_andviewed=32,
            completed_initial_native_records=221,completed_initial_native_pages=229,exact_reusable_native_records=208,exact_reusable_native_pages=208,
            remaining_native_records=341,remaining_native_pages=350,old_native_run_terminal=True,old_native_run_success=False,
            exact_native_reuse=str(REUSE),exact_native_reuse_sha256=sha(REUSE.read_bytes()),
            baseline_body_pages_directly_viewed=117,all_fifth_formatting_gates_pending=True,one_exact_FE_blank_row_fixed=True,evidence=evidence),
        new_entries={'weekend_testing_package_20261105':dict(new_credit=0,package=package['zip'],package_sha256=package['zip_sha256'],
            ROM_sha256=package['ROM_sha256'],proof=str(PACKAGE),proof_sha256=sha(PACKAGE.read_bytes()),
            exact_registered_build_copied_not_rebuilt=True,experimental_not_promoted=True,unfinished557_batch_excluded=True)},
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael557:549 plans/558 pages;208 native reuses,341 records/350 pages next. Weekend3bf3 packaged.',
            next_action='Start prepared341-record native remainder;merge exact208 reuses,view remaining/fresh pages,then stored/focused tests andregistered integration.',
            native_job_live=False,guide_photos=False)},summary=summary,
        document='docs/editorial_Rafael557_display_weekend_checkpoint_20261105.md',document_text=text,completed=12712,
        protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256']})
    print('Savednative reuse/display checkpoint andverifiedweekendpackage. No livejobs/newcredit/promotion;fullgoal active.')
