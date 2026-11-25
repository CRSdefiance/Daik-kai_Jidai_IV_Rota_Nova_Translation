"""Review one ordinary complete-word boundary without changing prose or native metrics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B197_layout_review_v5667b')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B197_editorial_manuscript_v1.json');row=next(r for r in doc['records'] if r['source_record_index']==74)
    prior=Path('work/analysis/lil_B197_layout_v5667/all21_paragraph_layout_QA.json');qa=read(prior)
    assert len(qa['failures'])==1 and qa['failures'][0]['id']==row['id']
    expected=["I'd like to buy it, but I don't",'have that kind of money.']
    item=next(r for r in qa['records'] if r['id']==row['id'])
    assert item['qa']['visible_lines']==expected
    assert [i['code'] for i in item['qa']['issues']]==['weak-line-ending']
    # This is a complete-word soft wrap,not an authored pause after the auxiliary.
    # Alternatives after I/but also strand dependencies;after the comma clause
    # uses a much shorter first row. Preserve the native ordinary two-row plan.
    reason=("Exact B197 R74 only:the complete53-character personal explanation wraps into two readable rows,29 and23 visible characters,at the ordinary don't/have word boundary. A soft wrap is not a spoken pause. The full negative verb remains adjacent across the row transition;both rows start/end with complete glyphs and keep all words. Breaking earlier after I or but merely moves the dependency;after the comma leaves a much shorter first row. Do not narrow the viewport,shorten the sentence or add a dramatic break to satisfy a weak-word preference. This waives only this warning at these exact two rows;all native glyph,phase,bounds,pagination,source-control and consumer checks remain required.")
    assert len(' '.join(expected))==53 and list(map(len,expected))==[29,23]
    anchor="        issues=[i for i in qa['issues']"
    insertion="""        if r['id']=='DK4_MES_B197_R0074':
            assert raw.hex()==SOURCE_LITERAL and r['english']==ENGLISH_LITERAL
            assert qa['visible_lines']==ROWS_LITERAL
            assert [i['code'] for i in qa['issues']]==['weak-line-ending']
            r.update(qa_waivers=['weak-line-ending'],qa_waiver_reason=REASON_LITERAL,
                exact_reviewed_soft_wrap_rows=ROWS_LITERAL,exact_reviewed_soft_wrap_source_hex=SOURCE_LITERAL)
            notes.append(dict(id=r['id'],reason=REASON_LITERAL,exact_rows=ROWS_LITERAL))
"""
    for a,b in {'SOURCE_LITERAL':repr(row['source_hex']),'ENGLISH_LITERAL':repr(row['english']),'ROWS_LITERAL':repr(expected),'REASON_LITERAL':repr(reason)}.items():insertion=insertion.replace(a,b)
    result=derive('scripts/plan_lil_B197_layout_v5667.py','scripts/plan_lil_B197_layout_v5667b.py',{
        "ROOT=Path('work/analysis/lil_B197_layout_v5667')":"ROOT=Path('work/analysis/lil_B197_layout_v5667b')",
        anchor:insertion+anchor})
    ROOT.mkdir(parents=True);save(ROOT/'one_exact_R74_boundary_review_and_unchanged_planner.json',dict(previous_failed_plan=str(prior),previous_failed_plan_sha256=sha(prior.read_bytes()),
        exact_record=row['id'],source_hex=row['source_hex'],english=row['english'],visible_rows=expected,reason=reason,tool=result,
        formatter_font_width_phase_guard_and_all_prose_bytes_unchanged=True,no_global_weak_word_waiver=True,
        all21_boundaries_reviewed_in_complete_exchange=True,
        other_boundaries_notes={'R14':'Book offer and exact price each form a coherent segment;no tiny price/currency fragment.',
            'R21':'Three complete-word rows retain the full Indian classic description and final invitation.',
            'R49':'Hope followed by with a celestial maiden,too is readable on two rows.',
            'R68':'Sell/it is an ordinary verb-object word boundary,with both complete sentences retained;no extra top break or page.',
            'R93':'The soft laugh/next-time beat,the wish,and its object fit three rows without authored pauses.',
            'R101':'The complete-word celestial/maiden boundary preserves the cultural term across adjacent rows;the doubtful question and self-dismissal remain complete on one page.'},
        native_font_glyph_plane_and_actual_English_scene_checks_still_pending=True,new_review_credit=0,full_goal_complete=False))
