"""Retain the exact good prose, all base diagnostics and two source-bound soft-wrap decisions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_native_review_v7049')
OLD=Path('translations/lil_B222_editorial_manuscript_v2.json')
NEW=Path('translations/lil_B222_editorial_manuscript_v3.json')
PLAN=Path('work/analysis/lil_B222_layout_v7046b/sixteen_whole_paragraph_plans_no_macros_no_prose_changes.json')
FONT=Path('work/analysis/lil_B222_native_pages_v7047/all16_paragraphs16_complete_native_pages128_alignments.json')
QA=Path('work/analysis/lil_B222_base_QA_v7048/all16_base_QA_diagnostics_before_any_scoped_classification.json')
NAMES=Path('work/analysis/lil_B222_name_planes_v7041/two_actors_four_getters_six_name_component_planes48_alignments.json')
SOURCEVIEW=Path('work/analysis/lil_B222_source_view_v7044b/all16_source_speeches_four_source_sheets_and_six_name_planes_viewed.json')
NOTES={
5:'The silent ellipsis is one complete beat, not an audible utterance or an invented gesture.',
9:'The sunset question completes the first row. The following concern remains a complete short question; no copied Japanese staging or narrow global width is needed.',
13:'The in/Japan boundary is an ordinary preposition/object soft wrap after a full34-cell first row. Moving in down would exceed the following guarded row or require an unnecessary fourth row. It/moved is an ordinary subject/predicate continuation. All hearing,Japan,certain man,deep emotion and self-conscious understatement remain in one page. The complete native glyph proof independently passes; this is no permission to drop a glyph or end a row on bare uppercase I.',
17:'The thoughtful recognition question fits one complete row without implying personal acquaintance.',
20:'Who/lived is an ordinary relative-pronoun/predicate continuation. Ago/His separates two complete sentences,keeping the name reveal intact without adding an audible pause.',
23:'The brief interested prompt is one complete natural question.',
27:'Great/glory is a complete-word modifier/noun boundary. Defeat/at and drove/them are ordinary prepositional and verb/object continuations. All unnamed clan membership,former glory,repeated defeats and prospective extinction remain together.',
30:'Down/one and fought/back are ordinary complete-word continuations. The one-by-one progression and brave resistance remain in three rows; no word or source judgment is omitted.',
33:'The first25-cell row ends before the cohesive seven ships phrase. Across/seven and ship/carrying are ordinary preposition/object and noun/modifier continuations. Naval/battle is a complete-word modifier/noun wrap; seven ships and enemy commander stay intact,and the final battle and reported attempt remain together on one page. Filling every row is subordinate to the whole paragraph.',
37:'The complete exhaustion sentence ends the first row. Of/the is a reviewed ordinary preposition/object boundary after33 cells,not a deliberate pause; under/each is another complete-word preposition/object boundary. All137 characters of the reported scene remain on one page:bottom of the strait,two enemy soldiers(one under each arm),and gleaming armor. Narrowing the global width or cutting facts to avoid of is unwarranted. Complete first/internal/final glyphs and guarded bounds pass independently.',
40:'Eastern/nation and glimpse/of are ordinary complete-word modifier/noun and noun/complement boundaries. The complete admiration remains the character\'s dated viewpoint,not narrator endorsement.',
44:'Exceptional/heroes is a complete-word modifier/noun continuation that keeps the short heroes,huh tag together instead of stranding huh on its own row.',
47:'Nation/shouldn\'t is an ordinary subject/predicate continuation of one complete principle; even and the warning remain.',
50:'Spot/for is an ordinary noun/complement continuation. Gerhard/(He separates the spoken teasing from the explicit parenthesized private thought; such/a preserves the complete final pure-heart phrase. The thought is neither spoken to Gerhard nor a new relationship.',
54:'The first row completes the quiet strait echo; the second keeps gleaming armor and all together. No recovery,coordinates or guaranteed find is supplied.',
57:'Like/that is an ordinary complete-word complement boundary. The self-conscious reflection and return to duty remain together; bare uppercase I is safely internal to the second row.'}
ROW_REASONS={
9:'Three brief source-staged questions occupy two complete English rows; the sunset and concern remain distinct natural questions.',
17:'The complete singular recognition question occupies one English row rather than two Japanese rows.',
20:'The complete military-commander account,hundreds of years and Noritsune reveal occupy three English rows rather than two source rows.',
30:'The complete one-by-one decline and sole brave resistance occupy three English rows rather than two source rows.',
33:'The complete reported seven-ship leap,final naval battle and attempt to reach the enemy commander occupy four English rows rather than three Japanese rows.',
50:'All spoken teasing and the complete parenthesized private thought occupy four English rows rather than three source rows; the two planes of speech remain explicit.',
57:'The complete self-conscious conclusion and return to duty occupy two English rows rather than three Japanese staging rows.'}
WAIVERS={13:"line 1 ends with weak wrap word 'in'",37:"line 2 ends with weak wrap word 'of'"}
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    old,plan,font,qa=map(read,[OLD,PLAN,FONT,QA]);doc=deepcopy(old)
    assert font['manuscript_sha256']==plan['manuscript_sha256']==qa['manuscript_sha256']==sha(OLD.read_bytes())
    assert font['layout_plan_sha256']==qa['layout_plan_sha256']==sha(PLAN.read_bytes())
    assert font['complete_native_pages']==16 and font['logical_compiled_input_alignment_cases']==128
    issues=[i for r in qa['records'] for i in r['base_QA']['issues']]
    assert sum(i['severity']=='warning' for i in issues)==2 and sum(i['code']=='line-break-count' for i in issues)==7
    assert not any(i['severity']=='error' for i in issues)
    annotations=[]
    for row in doc['records']:
        index=row['source_record_index'];p=next(r for r in plan['records'] if r['id']==row['id']);q=next(r for r in qa['records'] if r['id']==row['id'])['base_QA']
        assert row['english']==p['English'] and row['source_hex']==p['source_hex']
        assert any(i['code']=='line-break-count' for i in q['issues'])==(index in ROW_REASONS)
        expected=[dict(severity='warning',code='weak-line-ending',message=WAIVERS[index])] if index in WAIVERS else []
        assert [i for i in q['issues'] if i['severity']=='warning']==expected
        row['historical_clean_gloss_predecessor_English_not_read']=row['predecessor_English_not_read']
        row['predecessor_English_not_read']=False
        row['current_English_not_read']=False
        row['predecessor_provenance_note']='The historical flag described the source-first gloss stage. Earlier English was subsequently read for the contextual comparison; source and current reference bytes remain unchanged.'
        row['ordinary_boundary_reasons']=[dict(after_line=i+1,last_word=a.split()[-1],next_first_word=b.split()[0],reason=NOTES[index]) for i,(a,b) in enumerate(zip(p['lines'],p['lines'][1:]))]
        row['row_count_reason']=ROW_REASONS.get(index)
        row['qa_waivers']=['weak-line-ending'] if expected else []
        row['qa_waiver_reason']=NOTES[index] if expected else None
        row['exact_reviewed_base_warnings']=expected
        row['all_original_base_QA_issues']=q['issues']
        row['native_review_note']=NOTES[index]
        row['native_body_formatting_proof']=str(FONT)
        annotations.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],paragraph=row['english'],compiled_hex=p['encoded_hex'],lines=p['lines'],ordinary_boundary_reasons=row['ordinary_boundary_reasons'],row_count_reason=row['row_count_reason'],base_QA=q,exact_reviewed_base_warnings=expected,note=NOTES[index]))
    for spec in font['review_sheets']:assert sha(Path(spec['path']).read_bytes())==spec['sha256']
    assert len(font['review_sheets'])==3
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),metadata_annotation_only_all16_source_English_and_compiled_bytes_unchanged=True,native_review=str(ROOT/'all16_native_pages_and_exact_boundary_decisions.json'),two_exact_record_local_weak_boundary_waivers_no_global_rule_change=True)
    ROOT.mkdir(parents=True);save(NEW,doc)
    save(ROOT/'all16_native_pages_and_exact_boundary_decisions.json',dict(manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),native_prose_manuscript=str(OLD),native_prose_manuscript_sha256=sha(OLD.read_bytes()),paragraph_plan=str(PLAN),font_proof=str(FONT),base_QA=str(QA),name_proof=str(NAMES),source_visual_review=str(SOURCEVIEW),records=annotations,viewed_native_images=font['review_sheets'],all_three_native_sheets_individually_viewed=True,names_and_actual_source_views_bound_separately=True,all16_exact_source_and_English_bytes_unchanged_no_native_rerun_required=True,complete_native_pages=16,logical_compiled_alignment_cases=128,original_errors=0,original_warnings=2,exact_record_local_weak_boundary_waivers=2,unwaived_warnings=0,individual_rowcount_reasons=7,no_base_QA_diagnostic_deleted=True,no_global_weak_word_font_width_guard_pair_phase_or_literal_I_change=True,all16_dialogue_formatting_gates_remain_false=True,English_actual_final_stored_and_registered_release_pending=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,NEW,PLAN,FONT,QA,NAMES,SOURCEVIEW,Path(__file__)]}))
    print('16 pages viewed;7 row-count reasons;2 exact soft-wrap waivers with every original diagnostic retained. No prose change or credit.')
