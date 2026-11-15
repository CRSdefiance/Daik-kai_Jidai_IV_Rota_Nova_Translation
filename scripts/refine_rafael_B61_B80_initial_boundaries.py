"""Record eight concrete planned-page boundary findings without changing prose."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
PREFERENCES={
'DK4_MES_B65_R0035':dict(one_page=True,line_phrases=["wouldn't it?"],
    reason='The127-character paragraph should not strand has their hands full on a second page; keep the short question tag together within validated width.'),
'DK4_MES_B65_R0046':dict(page_clause='the profits from trading would keep it going.',line_phrases=['keep it going.'],
    reason='The147-character paragraph needs pagination. Start the next page with the complete profits/main clause rather than only it going.'),
'DK4_MES_B70_R0193':dict(one_page=True,
    reason='The129-character paragraph should use available width instead of stranding catch them on a second page.'),
'DK4_MES_B70_R0211':dict(one_page=True,
    reason='The127-character paragraph should not leave of various types isolated on a second page.'),
'DK4_MES_B73_R0036':dict(page_clause='I thought I had to handle everything on my own...',line_phrases=['on my own...'],
    reason='The148-character paragraph needs pagination. Keep the main-clause I thought and its complete handle-everything statement on the next page.'),
'DK4_MES_B75_R0238':dict(one_page=True,
    reason='The133-character boast may fit a full native page; test this rather than create a separate page for the final contempt sentence.'),
'DK4_MES_B78_R0005':dict(page_clause='and our support for restoring the Portuguese royal house!',
    reason='Keep the entire parallel object and restoration phrase together at the next page instead of isolating the Portuguese royal house.'),
'DK4_MES_B79_R0022':dict(one_page=True,line_phrases=['some kind of crown...'],
    reason='The125-character inference should use the native width without stranding kind of crown on another page.'),
}

if __name__=='__main__':
    output=ROOT/'planned_boundary_preferences_v2.json'
    assert not output.exists()
    manuscript_path=ROOT/'formatting_input_v2.json';plan_path=ROOT/'automatic_v2/automatic_plans.json'
    doc,plan=map(load,[manuscript_path,plan_path]);rows={r['id']:r for r in doc['records']};plans={r['id']:r for r in plan['records']}
    assert not plan['failures'] and len(plans)==539
    preferences={}
    for key,values in PREFERENCES.items():
        row,layout=rows[key],plans[key]
        assert layout['expected_native_pages']==2
        preferences[key]=dict(**values,bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
            previous_lines=layout['lines'],finding_from_planned_line_andpage_boundaries=True,
            native_visual_review_pending=True)
    save(output,dict(records=preferences,manuscript=str(manuscript_path),manuscript_sha256=sha(manuscript_path.read_bytes()),
        previous_plan=str(plan_path),previous_plan_sha256=sha(plan_path.read_bytes()),
        all539_English_paragraphs_unchanged=True,only_record_scoped_layout_preferences=True,
        native_widths_controls_font_phase_rules_andglobal_QA_unchanged=True,
        no_visual_ornew_gameplay_claim=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved eight exact planned-boundary findings;five one-page candidates/three coherent page-clause candidates. Prose/native geometry unchanged.',flush=True)
