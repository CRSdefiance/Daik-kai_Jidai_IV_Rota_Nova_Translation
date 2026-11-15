"""Record direct native body review without approving storage, actual scenes or typed-menu formatting."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_native_review_v8397')
OLD=Path('translations/hodram_B49_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_B49_editorial_manuscript_v2.json')
PLAN=Path('work/analysis/Hodram_B49_layout_v8394/automatic_plans.json')
PAGES=Path('work/analysis/Hodram_B49_pages_v8395/compiled_native_pages.json')
GUARDS=Path('work/analysis/Hodram_B49_layout_guards_v8396/focused_guard_rejections.json')
REASONS={
6:'One complete greeting fits one native row;keep the natural excited exclamation.',
10:'Three readable rows retain the full Proof of Supremacy term together andthe last sentence whole;the first-row possessive continues naturally into the named object. No prose orwidth change.',
15:'The sole source-bound ellipsis renders as its complete original native glyph withno extra ink,page orspoken text.',
19:'Two rows keep I\'d trade it for together andavoid a tiny final it for fragment. The full usable width remains available;no words shortened.',
22:'Two full rows keep Heavenly Wristband together andthe informal name qualifier/cute reaction intact;source row-count info isretained.',
33:'The automatic complete-word New/World boundary gives three balanced32/33/32-cell rows,withallwords/capitals andthe exact New World geography intact. The fourth uneven row isgone. This one exact source/approved paragraph has a scoped ordinary boundary;noglobal pair/weak/width rule ischanged andbaseQA isrecomputed,not filtered.',
40:'One native row keeps the surprised question andeager request together withoutan early break.',
43:'Two full rows retain the delighted reaction,request andbow offer. The ordinary give/it soft wrap preservescompletewords andavoids extra short rows;no global verb-object prohibition isneeded.',
58:'One full native row carries allthree buoyant exclamations andcompletefinalpunctuation.',
64:'The complete Proof question fitsone row without splitting the tagorlosing the question mark.',
67:'The exact clean-source-bound leading ellipsis andfollowing ASCII It\'s rendercompletely onone row. Independent glyphs/byteconsumption/firstorigin andallfour alignments pass;no broad Unicode allowance.',
71:'Two rows nowend at thefirst sentence andkeep Now give me the wristband intact,without added rows orchangedwording.',
74:'The short celebratory farewell fitsone row andstays distinctfromthe earlierrequest/offer.',
81:'The original FE consumer gives two complete rows,keeping the established itemname together andthe outgoingaction clear. Actual FE palette/transition isnot newlyobserved bythis offline preview.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,plan,pages,guards=map(read,[OLD,PLAN,PAGES,GUARDS]);assert plan['manuscript_sha256']==pages['manuscript_sha256']==sha(OLD.read_bytes()) and pages['plan_sha256']==sha(PLAN.read_bytes()) and guards['negative_count']==14
    assert len(old['records'])==len(plan['records'])==len(pages['records'])==14 and pages['fresh_compiled_alignment_cases']==56 and not plan['failures'];sheet=pages['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    infos=[i for p in plan['records'] for i in p['base_QA']['issues']];assert len(infos)==7 and all(i['severity']=='info' and i['code']=='line-break-count' for i in infos)
    doc=deepcopy(old)
    for row,p,native in zip(doc['records'],plan['records'],pages['records'],strict=True):
        assert row['id']==p['id']==native['id'] and row['english']==p['logical_English']==native['logical_English'] and p['encoded_hex']==native['compiled_hex'] and len(native['pages'])==1
        for page in native['pages']:
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            if 'physical_plane' in page:assert sha(Path(page['physical_plane']).read_bytes())==page['physical_plane_sha256']
        row.update(compiled_hex=p['encoded_hex'],compiled_bytes=len(bytes.fromhex(p['encoded_hex'])),planned_English_markup=p['planning_record']['english'],formatted_markup=p['formatted_markup'],generated_lines=p['lines'],expected_native_pages=1,qa_waivers=[],qa_waiver_scope=[],all_original_QA_issues=p['base_QA']['issues'],native_body_review_reason=REASONS[row['source_record_index']],compiled_native_body_review=native,native_body_review_proof=str(PAGES),native_body_review_proof_sha256=sha(PAGES.read_bytes()),compiled_body_directly_viewed_andapproved_offline=True,formatting_stored_actual_choice_UI_policy_andregistered_release_pending=True)
        assert row['review']['formatting'] is False
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),compiled_body_plan=str(PLAN),compiled_body_plan_sha256=sha(PLAN.read_bytes()),native_body_proof=str(PAGES),native_body_proof_sha256=sha(PAGES.read_bytes()),all14_compiled_single_body_pages_directly_viewed=True,original_QA_line_count_infos=7,original_QA_warnings=0,qa_waivers_used=0,typed_choice_UI_fullglyphs_geometry_backing_selection_stored_andactual_tests_pending=True,all16_formatting_gates_remain_false=True,new_credit=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'native_body_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),directly_viewed_native_sheet=sheet,reviewed_body_pages=14,fresh_compiled_alignment_cases=56,source_bound_standalone_andmixed_ellipsis_complete=True,R33_fullwidth_three_balanced_rows_complete_word_boundary_reason=REASONS[33],all_original_QA_infos=7,warnings=0,waivers=0,focused_new_guard_rejections=14,typed_choice_font_geometry_backing_selection_actual_andstored_release_still_pending=True,all16_formatting_gates_remain_false=True,no_prose_word_source_control_runtime_substitution_font_orviewport_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,PLAN,PAGES,GUARDS,Path(__file__)]}))
    print('Direct review14native bodypages/56alignments:bothsourceellipsis forms complete;R33threebalancedrows,7linecountinfos/0warnings/0waivers. Unchangedprose;all16formatgates remainfalse.PendingtypedUI/stored/actual/release;zero credit.')
