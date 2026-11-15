"""Retain better original wraps and prevent new fragments from overconstrained phrases."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B176_B195_clean_20261110')


def main():
    prior=ROOT/'formatting_v1/page_preferences_v8_phrases.json';out=ROOT/'formatting_v1/page_preferences_v9_phrases.json'
    assert not out.exists();prefs=load(prior);entries=prefs['records'];notes=[]
    for key,reason in {
        'DK4_MES_B184_R0020':'Retain the original readable two-row each/other soft wrap. Joining the phrase produces three rows and a new sparse closing fragment, so it does not improve this complete paragraph.',
        'DK4_MES_B186_R0058':'Retain the original readable Shandong/Peninsula soft wrap. Enforcing the whole name creates an early opening row ending in the; no character or geographic meaning was lost in the original.'
    }.items():
        assert entries[key]['required_pairs'];entries[key]['required_pairs']=[]
        entries[key]['reason']=reason;entries[key]['justified_original_layout_retention']=True
        notes.append(dict(id=key,decision='retain-original-layout',reason=reason))
    key='DK4_MES_B183_R0033'
    entries[key]['reason']='The directly viewed original already keeps ended up together. The proposed pair makes no compiled change; this is a justified retention, not a newly found or fixed defect.'
    notes.append(dict(id=key,decision='already-intact-layout-retention',reason=entries[key]['reason']))
    entries['DK4_MES_B188_R0053']['required_pairs'].append(["king's",'name'])
    entries['DK4_MES_B188_R0053']['reason']+=' Keep the whole demon kings name noun phrase to avoid a sparse name-only row.'
    entries['DK4_MES_B193_R0026']['required_pairs']=[['out','of'],['of','nowhere'],["didn't",'it']]
    entries['DK4_MES_B193_R0026']['reason']='Keep out of nowhere and the short didnt it question tag intact. Relax the larger came-out group so the tag does not split or force an unnecessary page.'
    entries['DK4_MES_B194_R0056']['ordinary_boundaries']=[['he','drove']]
    entries['DK4_MES_B194_R0056']['reason']+=' Allow the ordinary complete-word he/drove boundary so the entire natural paragraph remains three rows while drove back stays together; no glyph, bound or pagination guard is waived.'
    prefs.update(previous_preferences=str(prior),previous_preferences_sha256=digest(prior),
        contextual_layout_retentions=notes,no_prose_native_width_font_orengine_changes=True,
        evidence={str(p):digest(p) for p in [prior,ROOT/'plan_v7/automatic_plans.json',ROOT/'initial_body_visual_review_v1.json',Path(__file__)]})
    save(out,prefs);print('Retained two better original wraps andone already intact phrase; refined two new fragments andone ordinary soft boundary.')


if __name__=='__main__':main()
