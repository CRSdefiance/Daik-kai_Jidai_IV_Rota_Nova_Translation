"""Record nine viewed sheets and preserve wording while improving phrase flow."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B139_B140_visual_flow_v3473');assert not root.exists()
    fontpath=Path('work/analysis/lil_B139_B140_fonts_v3472/current_macro_QA_and_progressive_font_proof.json');font=read(fontpath)
    assert len(font['review_sheets'])==9
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    findings=[('DK4_MES_B139_R0041','Nice timing'),('DK4_MES_B140_R0075','good land'),('DK4_MES_B140_R0078','poor, too'),('DK4_MES_B140_R0120','call it'),('DK4_MES_B140_R0123','make lives better'),('DK4_MES_B140_R0209','all this'),('DK4_MES_B140_R0231','many countries'),('DK4_MES_B140_R0235','grand house')]
    pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('dk4tool/dialogue/lil_B139_B140_layout_v1.py','dk4tool/dialogue/lil_B139_B140_layout_v2.py',[
      ('def _word(value):',"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('nice','timing'),('good','land'),('poor','too'),('call','it'),('make','lives'),('lives','better'),('all','this'),('many','countries'),('grand','house')})\n\ndef _word(value):")])
    make('scripts/plan_lil_B139_B140_layout_v3471.py','scripts/plan_lil_B139_B140_layout_v3473.py',[
      ('layout_v3471','layout_v3473'),('lil_B139_B140_layout_v1','lil_B139_B140_layout_v2'),('editorial_manuscript_v3','editorial_manuscript_v4'),('editorial_manuscript_v4.json\')]', 'editorial_manuscript_v5.json\')]')])
    # The two manuscript declarations are checked explicitly after the replacements.
    planner=Path('scripts/plan_lil_B139_B140_layout_v3473.py');t=planner.read_text(encoding='utf-8')
    assert "INPUTS=[Path('translations/lil_B139_B140_editorial_manuscript_v5.json')]" in t
    # Correct this new, still unexecuted producer to read v4 and write v5.
    t=t.replace("INPUTS=[Path('translations/lil_B139_B140_editorial_manuscript_v5.json')]","INPUTS=[Path('translations/lil_B139_B140_editorial_manuscript_v4.json')]");planner.write_text(t,encoding='utf-8');pairs[-1]['successor_sha256']=sha(planner.read_bytes())
    make('scripts/verify_lil_B138_fonts_v3437.py','scripts/verify_lil_B139_B140_fonts_v3474.py',[
      ('Current352 macro calls,44 progressive planes and44 full paragraph QA.','Current536 macro calls,67 progressive planes and67 full paragraph QA.'),('lil_B138_profile','lil_B139_B140_profile'),('lil_B138_layout_v2','lil_B139_B140_layout_v2'),('lil_B138_fonts_v3437','lil_B139_B140_fonts_v3474'),('lil_B138_fonts_v3435','lil_B139_B140_fonts_v3472'),('lil_B138_editorial_manuscript_v5','lil_B139_B140_editorial_manuscript_v5'),('len(cases)==44 and len(qa_reports)==44 and macro_calls==352','len(cases)==67 and len(qa_reports)==67 and macro_calls==536'),('blocks[138]','blocks[139]'),('selectors=[2,14,20,21,22,23,92]','selectors=[2,4,9,16,20,21,171]'),('format(14 if selector==2 else 2','format(4 if selector==2 else 2'),('all44','all67'),('current_original_macro_alignment_calls=352','current_original_macro_alignment_calls=536'),('actual_selected_B137_IDs','actual_selected_B139_B140_IDs'),('44complete progressiveplanes,352macro cases,44QAplans','67complete progressiveplanes,536macro cases,67QAplans'),('sixsheets','nine sheets')])
    root.mkdir(parents=True);save(root/'all9_viewed_native_sheets_and_phrase_findings.json',dict(font_proof=str(fontpath),font_proof_sha256=sha(fontpath.read_bytes()),all9_progressive_sheets_viewed=True,sheets=font['review_sheets'],findings=[dict(id=i,phrase=p,action='Scoped formatter phrase boundary; preserve all prose tokens and native rules.') for i,p in findings],three_wordless_ellipses_complete_at_origin_seen=True,all_first_final_glyphs_bounds_and_readable_exchange_reviewed=True,tools=pairs,no_manual_layout_or_warning_waiver=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
