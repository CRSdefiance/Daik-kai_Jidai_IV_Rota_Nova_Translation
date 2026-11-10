"""Correct explanatory character counts; preserve the passing plans and all prose."""
from copy import deepcopy
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'continuity_findings_v2.json';assert not out.exists()
    priorpath=ROOT/'continuity_findings_v1.json';prior=load(priorpath)
    planpath=ROOT/'plan_initial_v1/automatic_plans.json';plans={r['id']:r for r in load(planpath)['records']}
    updated=deepcopy(prior);fixes=[]
    for ident,old in [('DK4_MES_B141_R0043',126),('DK4_MES_B146_R0056',127),('DK4_MES_B148_R0008',106)]:
        new=len(plans[ident]['logical_English']);text=updated['records'][ident]['reason']
        assert text.count(f'{old}-character')==1
        updated['records'][ident]['reason']=text.replace(f'{old}-character',f'{new}-character')
        fixes.append(dict(id=ident,earlier_explanatory_count=old,exact_logical_character_count=new))
    updated.update(explanatory_count_corrections=fixes,compiler_input_prose_controls_andrequested_layout_unchanged=True,
        evidence={str(p):digest(p) for p in [priorpath,planpath,__file__]})
    save(out,updated);print('Corrected3 explanatory counts only;one-page preferences andall prose remain unchanged.')


if __name__=='__main__':main()
