"""Avoid a stranded admiral and premature control/of wrap without changing any prose."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')
def main():
    out=ROOT/'preferences_v2.json';assert not out.exists()
    prefs=load(ROOT/'preferences_v1.json')
    row=prefs['records']['DK4_MES_B50_R0057']
    row['ordinary_boundaries']=[['you','was']]
    row['QA_line_ending_retention']=dict(exact_line='admiral like you',line_index=1,
        reason='Like you completes beautiful admiral in this mocking farewell. End the full noun phrase at you and continue immediately with its predicate was quite a pleasure. This source-bound clause boundary is natural continuous prose and avoids the isolated admiral row;no punctuation,page,extra input hold or word changes. Retain only this exact grammatical boundary,with all native glyph/bounds checks.')
    row['reason']='Keep the complete admiral like you phrase together and allow its ordinary clause boundary before was. Preserve the full mocking farewell.'
    doc=load(ROOT/'physical17_manuscript.json');target=next(r for r in doc['records'] if r['id']=='DK4_MES_B50_R0076')
    from dk4tool.patch.grand_race_menu_release import sha
    prefs['records'][target['id']].update(ordinary_boundaries=[['control','of']],
        reason='Permit the ordinary control/of boundary so the whole mainland-Ming trading-rights report uses three substantial rows instead of sparse opening rows. No prose,term,font,viewport orguard changes.')
    prefs.update(previous_preferences=str(ROOT/'preferences_v1.json'),previous_preferences_sha256=digest(ROOT/'preferences_v1.json'),no_prose_changes=True)
    save(out,prefs)
if __name__=='__main__':main()
