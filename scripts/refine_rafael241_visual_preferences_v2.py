"""Bind observed wrap/page andone native FE spill finding without changing prose orgeometry."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v3.json')
OUT=Path('translations/rafael_B101_B120_visual_preferences_v2.json')
DATA={
'DK4_MES_B101_R0049':dict(line_phrases=["old man's worry"],reason='Keep the grandfatherly noun phrase together instead of old/man\'s worry.'),
'DK4_MES_B101_R0068':dict(page_clause='I never seriously looked for it, but...',line_phrases=['around there'],
    reason='Keep around there onone page andstart the second page withJulio\'s complete admission instead ofa dangling location word.'),
'DK4_MES_B101_R0071':dict(line_phrases=['find it'],reason='Keep the phrasalverb object together instead offind/it.'),
'DK4_MES_B102_R0014':dict(line_phrases=['like to see one'],reason='Review anintact invitation phrase rather thanlike/to see one onan isolated final row.'),
'DK4_MES_B103_R0014':dict(line_phrases=['look for'],ordinary_boundaries=[['jaguar',"god's"]],
    reason='Avoid the sparse Let\'s look opening andkeep look for together. A normal word boundary within the complete multiword item title ispreferable tobreaking the phrasalverb; no word isremoved.'),
'DK4_MES_B103_R0042':dict(page_clause="Oh, of course I'll tell you if I happen to hear any more rumors.",
    reason='Keep the complete rumor offer onpage2 instead ofending page1 withif I happen andstranding to hear onpage2.'),
'DK4_MES_B104_R0014':dict(page_clause="They say it even showed the moon's uneven surface in clear detail.",line_phrases=['uneven surface'],
    reason='Keep the reported lunar-surface description together rather thanuneven/surface across a page turn.'),
'DK4_MES_B113_R0037':dict(FE_planning_cells=36,
    reason='Concrete native row failure: the final period ofthe37-character one-row plan spills to row12 despite nominal228px viewport. Reserve onlythis observed FE record to36 planning cells; preserve the physical viewport,font,checker andwords.'),
'DK4_MES_B115_R0056':dict(page_clause='who dare defy the divine!',
    reason='Keep the complete relative clause onpage2 rather thanstranding the divine alone afterthe turn.'),
'DK4_MES_B120_R0056':dict(page_clause='far, far to the northeast, so the story goes.',
    reason='Keep the reported destination andhearsay together onpage2 rather thanan isolated so the story goes tail.')
}

if __name__=='__main__':
    assert not OUT.exists()
    doc=load(DOC);by={r['id']:r for r in doc['records']};records={}
    for key,data in DATA.items():
        row=by[key]
        records[key]={**data,'bindings':{k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']}}
    save(OUT,dict(records=records,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        visual_wrap_findings=9,native_FE_row_failure_findings=1,all_words_andnative_geometry_unchanged=True,
        original_FE_row_checker_not_relaxed=True,
        native_failure_diagnostic='work/analysis/Rafael241_FE_all22_row_audit_v1_20261105.json',
        failed_native_session=95959,partial_complete_blocks=list(range(101,113)),
        all_remaining_body_visual_native_stored_actual_andregistered_checks_pending=True,new_credit=0))
    print('Bound9 wrap/page refinements andone concrete FE row spill;no prose orgeometry changes.')
