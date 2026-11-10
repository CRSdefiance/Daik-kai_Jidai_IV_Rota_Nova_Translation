"""Record a visual wrapping defect and scope its ordinary-boundary correction."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B184_wrap_finding_v5052')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B184_editorial_manuscript_v2.json')
    row=next(r for r in doc['records'] if r['source_record_index']==14)
    prior=read('work/analysis/lil_B184_layout_v5050/all9_paragraph_layout_QA.json')
    old=next(r for r in prior['records'] if r['id']==row['id'])
    assert old['qa']['visible_lines']==["It's strange that something","this delicious didn't catch","on sooner."]
    target=row['english'];raw=row['source_hex'];labels=tuple(target.split('}',1)[1].split())
    helper='REVIEWED_SOURCE_HEX='+repr(raw)+'\nREVIEWED_TARGET='+repr(target)+'\nREVIEWED_LABELS='+repr(labels)+'''\n
def _reviewed_ordinary_boundary_at(labels,index):
    # This exact paragraph can use two safe rows. A complete-word soft break
    # after this is preferable to an extra row that splits catch on.
    return (tuple(labels)==REVIEWED_LABELS and index+1<len(labels)
        and labels[index:index+2]==['this','delicious'])

'''
    old_predicate='end_word in weak and not _noun_will_at(labels,end)'
    new_predicate='end_word in weak and not _reviewed_ordinary_boundary_at(labels,end) and not _noun_will_at(labels,end)'
    audit_old='if end in STRONG_ENDINGS and end not in qa.WEAK_LINE_ENDINGS'
    audit_new="if not (source_raw.hex()==REVIEWED_SOURCE_HEX and target_markup==REVIEWED_TARGET and end=='this' and index==1) and end in STRONG_ENDINGS and end not in qa.WEAK_LINE_ENDINGS"
    tools=[derive('dk4tool/dialogue/lil_B184_layout_v1.py','dk4tool/dialogue/lil_B184_layout_v2.py',{
        'source=inspect.getsource(layout._balanced_wrap)':helper+'source=inspect.getsource(layout._balanced_wrap)',
        old_predicate:new_predicate,
        "'_complete_locative_at':_complete_locative_at}":"'_complete_locative_at':_complete_locative_at,'_reviewed_ordinary_boundary_at':_reviewed_ordinary_boundary_at}",
        '    return _encode(source_raw,target_markup,profile)':
        "    if target_markup==REVIEWED_TARGET and source_raw.hex()!=REVIEWED_SOURCE_HEX:\n        raise ValueError('Reviewed ordinary boundary requires exact clean B184 R14 source')\n    return _encode(source_raw,target_markup,profile)",
        audit_old:audit_new})]
    tools.append(derive('scripts/plan_lil_B184_layout_v5050.py','scripts/plan_lil_B184_layout_v5053.py',{
        'lil_B184_layout_v1':'lil_B184_layout_v2','layout_v5050':'layout_v5053',
        'editorial_manuscript_v2':'editorial_manuscript_v3'}))
    tools.append(derive('scripts/verify_lil_B184_fonts_v5051.py','scripts/verify_lil_B184_fonts_v5054.py',{
        'lil_B184_layout_v1':'lil_B184_layout_v2','fonts_v5051':'fonts_v5054',
        'editorial_manuscript_v2':'editorial_manuscript_v3'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'exact_R14_visual_finding_and_boundary_review.json',dict(
        manuscript='translations/lil_B184_editorial_manuscript_v2.json',
        manuscript_sha256=sha(Path('translations/lil_B184_editorial_manuscript_v2.json').read_bytes()),
        record_ID=row['id'],source_hex=raw,logical_prose=target,previous_visible_lines=old['qa']['visible_lines'],
        initial_technical_checks_passed_but_visual_editorial_wrap_rejected=True,
        finding='Overconservative weak-this penalty forced three rows and split the phrasal verb catch on despite room for two safe rows.',
        ordinary_boundary_reason='For this exact complete paragraph,a complete-word soft break after this keeps catch on sooner intact and uses two readable rows. This is a reviewed local compromise,not a global removal of weak-ending or phrase checks. No authored break,word change or forced row count.',
        complete_words_unchanged_font_width_guard_phase_bounds_and_pagination_still_required=True,
        source_or_prose_mutation_cannot_inherit_reviewed_boundary=True,
        tools=tools,native_successor_and_visual_review_pending=True,new_review_credit=0,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
