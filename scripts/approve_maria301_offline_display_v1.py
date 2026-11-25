"""Seal directly viewed final pages andexact in-batch native/style reuse; no fifth-gate credit."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT=Path('work/Maria_B0_B32_clean_20261109')


def pages(row):
    rendered=row['complete_native_English_display']
    return rendered['pages'] if row['kind']=='progressive' else [rendered]


def main():
    out=ROOT/'offline_display_approval_v1.json'
    layout_path=ROOT/'final_layout_decisions_v1.json'
    assert not out.exists() and not layout_path.exists()
    input_path=ROOT/'formatting_v1/formatting_input.json'
    plan_path=ROOT/'refined_plans_v2/automatic_plans.json'
    final_path=ROOT/'refined_native_v2/compiled_native_pages.json'
    initial_path=ROOT/'initial_native_v1/compiled_native_pages.json'
    first_path=ROOT/'refined_native_v1/fresh/compiled_native_pages.json'
    last_path=ROOT/'refined_native_v2/fresh/compiled_native_pages.json'
    doc,plan,final,initial,first,last=map(load,[input_path,plan_path,final_path,initial_path,first_path,last_path])
    assert final['manuscript_sha256']==plan['manuscript_sha256']==digest(input_path)
    assert final['plan_sha256']==digest(plan_path)
    assert len(final['records'])==299 and final['pages']==303
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    reviewed=set();leaf_rows={}
    for receipt,path in [(initial,initial_path),(first,first_path),(last,last_path)]:
        assert receipt['runtime']==final['runtime'] and receipt['font_sha256']==final['font_sha256']
        assert receipt['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert receipt['complete_consumption_andpagination_exact']
        for row in receipt['records']:
            for index,page in enumerate(pages(row),1):
                assert digest(page['preview'])==page['preview_sha256']
                assert digest(page['native_plane'])==page['native_plane_sha256']
                reviewed.add((row['id'],index,page['preview_sha256'],page['native_plane_sha256']))
            leaf_rows[(row['id'],row['compiled_hex'])]=(row,path)
    planned={r['id']:r for r in plan['records']}
    source={r['id']:r for r in doc['records']}
    selected=[]
    for row in final['records']:
        expected=planned[row['id']]
        assert row['compiled_hex']==expected['encoded_hex'] and row['logical_English']==source[row['id']]['english']
        original,path=leaf_rows[(row['id'],row['compiled_hex'])]
        assert original==row
        assert row['source_reference']==source[row['id']]['source_reference'] and row['current_reference']==source[row['id']]['current_reference']
        for index,page in enumerate(pages(row),1):
            assert (row['id'],index,page['preview_sha256'],page['native_plane_sha256']) in reviewed
            selected.append(dict(id=row['id'],page=index,preview=page['preview'],preview_sha256=page['preview_sha256'],
                native_plane_sha256=page['native_plane_sha256'],native_receipt=str(path),native_receipt_sha256=digest(path)))
    assert len(selected)==303
    names_path=ROOT/'name_planes_v1/native_name_planes.json'
    menu_path=ROOT/'menu_planes_v1/menu_provider_and_planes.json'
    names,menu=map(load,[names_path,menu_path])
    assert names['runtime']==menu['runtime']==final['runtime']
    assert names['actors']==36 and names['distinct_current_strings']==44 and len(names['planes'])==44
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert len(menu['records'])==8 and menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert (menu['native_provider_alignments'],menu['bridged_modal_returns'],len(menu['compiler_negatives_rejected']))==(6,18,7)
    sheets=[*initial['review_sheets'],*load(ROOT/'refined_native_v1/global_review_v1/contact_sheet_manifest.json')['review_sheets'],
        *last['review_sheets'],*names['review_sheets'],menu['review_sheet']]
    for sheet in sheets:
        assert digest(sheet['path'])==sheet['sha256']
    # Only B4 changed between these plans; the complete B32 compiler inputs remain exact.
    styles_path=ROOT/'compiled_styles_v1/compiled_style_objects.json'
    styles=load(styles_path);old_style_plan=load(styles['plan'])
    assert digest(styles['plan'])==styles['plan_sha256'] and styles['runtime']==final['runtime']
    old_style_rows={r['id']:r for r in old_style_plan['records'] if r['id'].startswith('SC3_B32_STYLE_')}
    assert len(old_style_rows)==7 and all(planned[key]==value for key,value in old_style_rows.items())
    assert styles['native_target_slot_cases']==8 and styles['physical_alternatives']==7
    assert sum(len(n['rejected']) for n in styles['compiler_negatives'])==9
    for obj in styles['objects']:
        assert digest(obj['target_path'])==obj['target_sha256']
    style_reuse=ROOT/'compiled_styles_v1/final_plan_qualification_v1.json'
    assert not style_reuse.exists()
    save(style_reuse,dict(prior=str(styles_path),prior_sha256=digest(styles_path),final_plan=str(plan_path),final_plan_sha256=digest(plan_path),
        all_seven_complete_style_plan_rows_exact=True,native_context_andall_compiler_inputs_exact=True,
        eight_native_target_slots_andnine_rejections_reused=True,no_style_VM_replay_ornew_actual_assignment=True,new_credit=0))
    prefs_path=ROOT/'formatting_v1/preferences_v6.json';prefs=load(prefs_path)['records']
    initial_plan=load(ROOT/'initial_plans_v2/automatic_plans.json')
    raw_plan=load(ROOT/'initial_plans_v1/automatic_plans.json')
    before={r['id']:r for r in initial_plan['records']};raw={r['id']:r for r in raw_plan['records']}
    changes=[]
    for key,row in planned.items():
        previous=before[key]
        if key=='DK4_MES_B5_R0035':previous=raw[key]
        if previous['encoded_hex']==row['encoded_hex']:continue
        reference=source[key]
        assert key in prefs
        changes.append(dict(id=key,source_reference=reference['source_reference'],current_reference=reference['current_reference'],
            decision='layout-revision',finding=prefs[key]['reason'],logical_English=reference['editorial_logical_English'],
            previous_native_lines=previous['lines'],final_native_lines=row['lines'],
            previous_pages=previous['expected_native_pages'],final_pages=row['expected_native_pages'],
            final_encoded_hex=row['encoded_hex'],no_prose_change=True))
    assert len(changes)==35
    retentions=[]
    for key,reason in [
        ('DK4_MES_B0_R0039','Retain the original three rows: forcing really-is together produced an unacceptable article-at-row-end warning.'),
        ('DK4_MES_B0_R0048','Retain the more balanced original three rows; the candidate left may suggest on a sparse middle row without improving comprehension.')]:
        assert planned[key]['encoded_hex']==before[key]['encoded_hex']
        retentions.append(dict(id=key,source_reference=source[key]['source_reference'],current_reference=source[key]['current_reference'],
            decision='layout-retention',finding=reason,final_native_lines=planned[key]['lines']))
    save(layout_path,dict(records=changes+retentions,wrap_improvements=35,justified_layout_retentions=2,
        old_final_native_pages=304,final_native_pages=303,one_page_reclaimed='DK4_MES_B24_R0011',
        every_changed_layout_fresh_native_checked_anddirectly_viewed=True,no_prose_shortened_orordinary_break_authored=True,new_credit=0))
    glyph_scope=load(ROOT/'all301_contextual_proposals_qualification_v1.json')['glyph_consistency_targets']
    glyphs=[]
    for item in glyph_scope:
        row=source[item['id']];english=row['editorial_logical_English']
        assert english.isascii() and not item['current'].isascii()
        glyphs.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            old_nonASCII_codepoints=sorted({f'U+{ord(c):04X}' for c in item['current'] if not c.isascii()}),
            final_English=english,all_final_native_characters_independently_checked=True))
    assert len(glyphs)==12 and sum('U+FF29' in g['old_nonASCII_codepoints'] for g in glyphs)==1
    save(out,dict(runtime=final['runtime'],body_records=299,final_body_pages=303,caption_records=2,
        selected_final_pages=selected,every_final_page_directly_viewed_in_readable_sheets=True,
        initial_native_records=299,initial_native_pages=304,initial_native_alignments=1196,
        first_refinement_fresh_records=34,first_refinement_fresh_pages=38,first_refinement_alignments=136,
        last_refinement_fresh_records=1,last_refinement_fresh_pages=2,last_refinement_alignments=4,
        final_all299_records_and1196_alignment_cases_bound_once_orby_exact_reuse=True,
        all_native_glyph_consumption_bounds_andpagination_guards_pass=True,
        all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked=True,
        full_catalogue_name_literals_not_actual_catalogue_UI_layout_approval=True,
        menu_native_alignment_cases=6,menu_bridged_returns=18,menu_style_planes=8,menu_compiler_rejections=7,
        one_complete_style_object_seven_bodies_eight_slots_andnine_rejections_pass_or_exactly_reused=True,
        glyph_targets=glyphs,mixed_fullwidth_I_target_corrected_in_planned_text_not_yet_shipped=True,
        remaining_eleven_targets_are_punctuation_consistency_not_eleven_claimed_font_failures=True,
        wrap_improvements=35,layout_retentions=2,one_page_reclaimed_without_shortening=True,
        new_actual_gameplay=False,stored_script_allocation_catalogue_loader_checks_pending=True,
        representative_gameplay_transitions_andregistered_integration_pending=True,
        all_fifth_gates_still_false=True,new_credit=0,full_goal_complete=False,
        reviewed_sheets=sheets,evidence={str(p):digest(p) for p in [input_path,plan_path,final_path,initial_path,first_path,last_path,
            names_path,menu_path,styles_path,style_reuse,layout_path,prefs_path,Path(__file__)]}))
    release=load('work/hodram_residual_release_v1/registered_release_verification.json')
    summary=('Maria301 retains178 prose revisions/123 retentions. All303 final offline body pages,44 name strings '
        'andthe two-choice menu are native-checked anddirectly viewed. Thirty-five wrap improvements,two justified '
        'layout retentions andone reclaimed page preserve every word;the mixed I and11 punctuation targets pass. '
        'Only changed layouts were rerendered;all265 other bodies reuse exact proofs. Stored/allocation checks, '
        'representative gameplay andregistration remain;all fifth gates stillfalse. Integrated19,161/registeredf166991f/main unchanged.')
    text='''# Maria301 offline display checkpoint — November9,2026

The301 contextual decisions remain178 revisions/123 justified retentions; no wording changed during formatting. All **299 speech bodies/303 final native pages**,44 distinct strings from36 scoped name/role identities, andthe two menu captions are visually reviewed. Complete leading/internal/trailing glyphs, independent font pixels, input/output guards, bounds, consumption andpagination pass. No new completion credit orROM is claimed.

`work/Maria_B0_B32_clean_20261109/offline_display_approval_v1.json` binds every final page to the exact directly viewed PNG/native-plane hashes andits original orfresh receipt. Current formatter input is `formatting_v1/formatting_input.json`; final plan is `refined_plans_v2/automatic_plans.json`; final native receipt is `refined_native_v2/compiled_native_pages.json`; preferences are `formatting_v1/preferences_v6.json`. Do not restart source review, native characterization orunchanged page checks.

`final_layout_decisions_v1.json` records35 improvements andtwo justified layout retentions with exact references andbefore/after rows. Phrase constraints keep commands, short questions, source titles/epithets andcommon idioms intact. Four two-page speeches retain coherent clauses instead of isolated tails. The unchanged Havana taunt at B24R11 now fits four native rows, removing its destination-only second page. No prose was shortened andno ordinary authored LB oralignment was introduced. The source laugh, explicit shriek andpoem justify the documented short opening/verse rows in three scoped layouts; these are not global dramatic-break rules.

All304 initial pages were directly viewed. The first native pass checks1,196 alignments. The first refinement rerenders34 changed bodies/38 pages/136 alignment cases andreuses265 exact bodies. One remaining first-page question is then refined alone:one body/two pages/four cases;298 other final bodies reuse exact proofs. All selected303 final pages are covered. The intermediate rejected predicate layouts, four-row capacity trials andshell-quoting failure remain as evidence; no warnings were waived. Two clearer original predicate layouts are retained with reasons.

The measured current Maria macro lengths are FI5,FA2,FO7,FU15. The historical Maria profile’s FA3/five-row assumptions are not used ormodified. The qualified216px/four-row consumer remains unchanged;all21 substitutions preserve their native contract. Twelve glyph targets pass the final native checks:one mixed full-width I correction at B14R5 andeleven reaction/silence punctuation harmonizations. This is not a claim of twelve prior renderer failures. The Julio First/F issue andearlier registered ASCII right-bound correction remain preserved from their completed batches.

`name_planes_v1/native_name_planes.json` covers72 previously bound getters/44 deduplicated native style11 strings; all three name sheets were viewed. Full-name literals are font checks, not actual catalogue UI layout observation. `menu_planes_v1/menu_provider_and_planes.json` passes six provider alignment cases,18 bridged returns,eight style planes andseven rejection checks; its current/reviewed caption sheet was viewed. Actual controller selections remain pending. `compiled_styles_v1/compiled_style_objects.json` passes allseven physical bodies/eight alias slots andnine rejections. `final_plan_qualification_v1.json` qualifies its exact seven unchanged style-plan rows forthe latest plan without replaying the native proof. No actual future lookout assignment is inferred.

Next prepare the source-qualified stored SC3 transaction andcheck every final buffer, allocation, command/control, substitution, archive loader/catalogue result andinverse. Then run representative current-English scenes covering the four distinct two-page speeches, the menu/return andrepresentative names/styles/transitions, with focused follow-up only for concrete risks. These are **offline** font/page checks;the existing opening-to-Hangzhou run is context evidence, not changed-batch gameplay. All301 fifth gates remainfalse until necessary stored/representative/release evidence is complete. Integrate through the registered cumulative workflow andexact clean-input patch;do not promote main without acceptance.

Integrated totals stay19,161=11,532 revisions+7,629 retentions;historical counters retain19,164. Remaining native-story objects stay6,737 until full review/integration;shared/UI scope is separate. Current registered candidate/manifest/patch remainf166991f, main all-routes-unified-v4701. All accepted layers,the ASCII right-bound correction, all ROMs, earlier translations/retentions andfull editorial scope are preserved. No process is live. No guide photos. Deferred artwork andthe later older-record technical re-audit remain separate.
'''
    checkpoint(mutation='work/Maria301_offline_display_checkpoint_20261109',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria301:303 final native/visually reviewed pages;stored andrepresentative tests next.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,
            current_body_pages_native_andvisually_reviewed=303,wrap_improvements=35,
            next_action='Stored source-qualified SC3 buffers/allocation/catalogue/loaders/inverse,thenrepresentative scenes/transitions andregistered integration.',guide_photos=False),
        additional_updates={'Maria_SC3_B0_B32_clean_20261109':dict(new_credit=0,
            offline_display_approval=str(out),offline_display_approval_sha256=digest(out),
            final_formatting_input=str(input_path),final_formatting_input_sha256=digest(input_path),
            final_native_plan=str(plan_path),final_native_plan_sha256=digest(plan_path),
            final_native_pages=str(final_path),final_native_pages_sha256=digest(final_path),
            final_body_pages=303,wrap_improvements=35,justified_layout_retentions=2,
            one_page_reclaimed=True,all12_glyph_targets_native_checked=True,
            all_offline_body_menu_name_visual_checks_pass=True,
            native_display_stored_andrepresentative_gameplay_pending=False,
            stored_andrepresentative_gameplay_pending=True,all_fifth_formatting_gates_pending=True,
            registered_integration_pending=True)},
        summary=summary,document='docs/editorial_Maria301_offline_display_20261109.md',document_text=text,
        completed=19161,protected={'translations/release_stack.json':release['registry_sha256'],
            release['candidate']:release['candidate_sha256'],release['manifest']:release['manifest_sha256'],
            release['patch']:release['patch_sha256'],
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Approved303 offline pages/44 names/menu;35 wrap improvements/two retentions/one reclaimed page. Fifth gates andintegration pending;19161 unchanged.')


if __name__=='__main__':main()
