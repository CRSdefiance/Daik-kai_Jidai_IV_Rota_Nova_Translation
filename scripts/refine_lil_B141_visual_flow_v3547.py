"""Preserve viewed prose while protecting five spoken phrase boundaries."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B141_visual_flow_v3547');assert not root.exists();fontpath=Path('work/analysis/lil_B141_fonts_v3546/current_macro_QA_and_progressive_font_proof.json');font=read(fontpath);assert len(font['review_sheets'])==2
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    pairs=[]
    def make(a,b,changes):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('dk4tool/dialogue/lil_B141_layout_v1.py','dk4tool/dialogue/lil_B141_layout_v2.py',[
        ('def _word(value):',"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('still',\"don't\"),('gotta','work'),('working','hard'),(\"trading's\",'my'),('my','specialty'),('only','raised')})\n\ndef _word(value):")])
    make('scripts/plan_lil_B141_layout_v3545.py','scripts/plan_lil_B141_layout_v3548.py',[
        ('lil_B141_layout_v1','lil_B141_layout_v2'),('lil_B141_layout_v3545','lil_B141_layout_v3548'),('editorial_manuscript_v3.json','editorial_manuscript_v4.json'),('editorial_manuscript_v4.json','editorial_manuscript_v5.json')])
    # The planner substitutions above intentionally identify INPUT/OUTPUT separately
    # below before execution, so a successor can never read its own output.
    p=Path('scripts/plan_lil_B141_layout_v3548.py');t=p.read_text(encoding='utf-8');assert "INPUT=Path('translations/lil_B141_editorial_manuscript_v5.json')" in t;t=t.replace("INPUT=Path('translations/lil_B141_editorial_manuscript_v5.json')","INPUT=Path('translations/lil_B141_editorial_manuscript_v4.json')");compile(t,str(p),'exec');p.write_text(t,encoding='utf-8');pairs[-1]['successor_sha256']=sha(p.read_bytes())
    make('scripts/verify_lil_B141_fonts_v3546.py','scripts/verify_lil_B141_fonts_v3549.py',[
        ('lil_B141_layout_v1','lil_B141_layout_v2'),('lil_B141_fonts_v3546','lil_B141_fonts_v3549'),('editorial_manuscript_v4','editorial_manuscript_v5')])
    root.mkdir(parents=True);save(root/'both_viewed_sheets_and_phrase_flow_successors.json',dict(font_proof=str(fontpath),font_proof_sha256=sha(fontpath.read_bytes()),both_native_sheets_viewed=True,sheets=font['review_sheets'],findings=[dict(id=i,phrase=p,action='Protect phrase in this scoped automatic formatter;words unchanged.') for i,p in [('DK4_MES_B141_R0015',"still don't"),('DK4_MES_B141_R0041','gotta work'),('DK4_MES_B141_R0058','working hard'),('DK4_MES_B141_R0063',"Trading's my specialty"),('DK4_MES_B141_R0069','only raised')]],tools=pairs,all_prior_artifacts_preserved=True,no_manual_breaks_or_warning_waivers=True,no_prose_or_review_decision_change=True,no_ROM_registry_ledger_review_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
