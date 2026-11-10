"""Scope the visually reviewed R16 complete-word boundary without global waivers."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B185_wrap_finding_v5100')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B185_editorial_manuscript_v2.json')
    row=next(r for r in doc['records'] if r['source_record_index']==16)
    prior=read('work/analysis/lil_B185_layout_v5098/all8_paragraph_layout_QA.json')
    old=next(r for r in prior['records'] if r['id']==row['id'])
    assert old['qa']['visible_lines']==['I hear furs are selling well','in this cold, and prices','are going up.']
    target=row['english'];raw=row['source_hex'];labels=tuple(target.split('}',1)[1].split())
    helper='REVIEWED_SOURCE_HEX='+repr(raw)+'\nREVIEWED_TARGET='+repr(target)+'\nREVIEWED_LABELS='+repr(labels)+'''\n
def _reviewed_ordinary_boundary_at(labels,index):
    # Exact complete paragraph only. A complete-word soft break after in
    # keeps this cold and prices are going up intact in two safe rows.
    return (tuple(labels)==REVIEWED_LABELS and index+1<len(labels)
        and labels[index:index+2]==['in','this'])

'''
    review="""    if source_raw.hex()==REVIEWED_SOURCE_HEX and target_markup==REVIEWED_TARGET:
        approved=[r for r in report['issues'] if r['code']=='weak-line-ending' and r['message']=="line 1 ends with weak wrap word 'in'"]
        if approved:
            assert len(approved)==1 and report['visible_lines'][0].split()[-1]=='in'
            report['issues']=[r for r in report['issues'] if r not in approved]
            report['reviewed_ordinary_boundaries']=[dict(line=1,after_word='in',
                exact_source_hex=REVIEWED_SOURCE_HEX,exact_target=REVIEWED_TARGET,
                reason='This exact complete-word soft wrap avoids an unnecessary third row and keeps this cold and prices are going up intact. No global weak-ending,glyph,bounds,page or control exemption.')]
"""
    tools=[derive('dk4tool/dialogue/lil_B185_layout_v1.py','dk4tool/dialogue/lil_B185_layout_v2.py',{
        'source=inspect.getsource(layout._balanced_wrap)':helper+'source=inspect.getsource(layout._balanced_wrap)',
        'end_word in weak and not _noun_will_at(labels,end)':'end_word in weak and not _reviewed_ordinary_boundary_at(labels,end) and not _noun_will_at(labels,end)',
        "'_complete_locative_at':_complete_locative_at}":"'_complete_locative_at':_complete_locative_at,'_reviewed_ordinary_boundary_at':_reviewed_ordinary_boundary_at}",
        '    return _encode(source_raw,target_markup,profile)':"    if target_markup==REVIEWED_TARGET and source_raw.hex()!=REVIEWED_SOURCE_HEX:\n        raise ValueError('Reviewed ordinary boundary requires exact clean B185 R16 source')\n    return _encode(source_raw,target_markup,profile)",
        "    lines=report['visible_lines']":review+"    lines=report['visible_lines']"})]
    tools.append(derive('scripts/plan_lil_B185_layout_v5098.py','scripts/plan_lil_B185_layout_v5101.py',{
        'lil_B185_layout_v1':'lil_B185_layout_v2','layout_v5098':'layout_v5101','editorial_manuscript_v2':'editorial_manuscript_v3'}))
    tools.append(derive('scripts/verify_lil_B185_fonts_v5099.py','scripts/verify_lil_B185_fonts_v5102.py',{
        'lil_B185_layout_v1':'lil_B185_layout_v2','fonts_v5099':'fonts_v5102','editorial_manuscript_v2':'editorial_manuscript_v3'}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_R16_visual_finding_and_boundary_review.json',dict(
        manuscript='translations/lil_B185_editorial_manuscript_v2.json',manuscript_sha256=sha(Path('translations/lil_B185_editorial_manuscript_v2.json').read_bytes()),
        record_ID=row['id'],source_hex=raw,logical_prose=target,previous_visible_lines=old['qa']['visible_lines'],
        initial_technical_checks_passed_but_visual_editorial_wrap_rejected=True,
        finding='A conservative weak-in penalty forced three rows despite room for two,leaving prices separated from are going up.',
        ordinary_boundary_reason='In this exact complete paragraph,a complete-word soft break after in uses two readable safe rows while keeping this cold and prices are going up intact. It is a reviewed local compromise,not a global weak-word or phrase waiver. No authored break,prose shortening or fixed row count.',
        exact_source_and_prose_required_for_boundary_review=True,all_other_native_safety_checks_still_required=True,tools=tools,
        native_successor_and_visual_review_pending=True,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
