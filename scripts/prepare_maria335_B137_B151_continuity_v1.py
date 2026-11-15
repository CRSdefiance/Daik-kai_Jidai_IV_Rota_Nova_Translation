"""Flag three short paragraphs for full-width one-page trials without shortening prose."""
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'continuity_findings_v1.json';assert not out.exists()
    planpath=ROOT/'plan_initial_v1/automatic_plans.json';plans={r['id']:r for r in load(planpath)['records']}
    reasons={
        'DK4_MES_B141_R0043':'The initial plan strands was worse still on page2. Trial the complete126-character explanation at the validated full width before accepting an extra page.',
        'DK4_MES_B146_R0056':'The initial plan strands and look properly on page2 and splits the search instruction. Trial the complete127-character paragraph on one full-width page.',
        'DK4_MES_B148_R0008':'The initial plan puts command respect alone on page2 and uses a sparse their strength row. Trial the entire106-character paragraph on one full-width page.',
    }
    assert all(plans[i]['expected_native_pages']==2 for i in reasons)
    save(out,dict(records={i:dict(one_page=True,reason=r) for i,r in reasons.items()},
        complete_paragraphs_andall_words_macros_controls_unchanged=True,physical_viewports_unchanged=True,
        automatic_checks_andfresh_native_visual_review_still_required=True,new_credit=0,
        evidence={str(planpath):digest(planpath),__file__:digest(__file__)}))
    print('Prepared3 full-width one-page trials; no prose or geometry change.')


if __name__=='__main__':main()
