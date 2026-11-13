"""Balance the complete farewell phrases after its first native wrap refinement."""
from copy import deepcopy
from scripts.refine_maria390_native_layout_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    source=ROOT/'continuity_preferences_v2.json';out=ROOT/'continuity_preferences_v3.json'
    note=ROOT/'native_layout_findings_v2.json'
    assert not out.exists() and not note.exists()
    proofpath=ROOT/'native_pages_v2/complete_DK4_MES_B170_R0092.json'
    proof=load(proofpath)
    assert proof['four_native_alignment_cases_pass']
    row=proof['record'];assert row['id']=='DK4_MES_B170_R0092'
    display=row['complete_native_English_display'];page=display['pages'][0]
    assert digest(page['preview'])==page['preview_sha256']
    pref=deepcopy(load(source));entry=pref['records'][row['id']]
    entry['required_pairs']=[['i\'d','like'],['like','to'],['to','fall'],['fall','in'],['in','love'],
        ['with','a'],['a','man'],['man','like'],['like','you']]
    entry['reason']='The directly viewed first refinement keeps fall in love together but leaves like you as a nine-character third row. Keep the full longing verb phrase and with a man like you complement coherent in balanced native rows. The native continuation guard makes a36-character second row too wide; preserve216px width and every word rather than shorten the farewell.'
    pref.update(previous_preferences=str(source),previous_preferences_sha256=digest(source),new_credit=0)
    save(out,pref)
    save(note,dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
        previous_compiled_hex=row['compiled_hex'],previous_preview=page['preview'],previous_preview_sha256=page['preview_sha256'],
        reason=entry['reason'],original_prose_width_font_controls_andall_other_preferences_unchanged=True,
        fresh_native_anddirect_visual_checks_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [source,proofpath,__file__]}))
    print('Prepared one farewell phrase-balance successor;no prose orwidth changes.')


if __name__=='__main__':main()
