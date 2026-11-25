"""Preserve the first comparison producer; bind explicit decision-shape and read-aloud refinements."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B275_B285_clean_20261110')

def main():
    before=ROOT/'authored_contextual_v1.json';after=ROOT/'authored_contextual_v2.json';assert not after.exists()
    doc=deepcopy(load(before));byid={r[0]:r for r in doc['records']}
    row=byid['SC3_B281_STYLE_422_186'];assert row[1]=='D' and len(row)==4;row[1]='T'
    fixes={
        'DK4_MES_B275_R0083':('Preserve his initial half-mocking interest and gradual disgust in natural rough dialogue.',"At first, I was there more for a laugh than anything. But the more I listened, the more disgusted I got with the business."),
        'DK4_MES_B278_R0004':('Correct exactly100 to over100 and preserve the claimed Society of Jesus affiliation in two natural sentences.',"More than a hundred of us have just arrived. We were sent by the Society of Jesus."),
        'DK4_MES_B281_R0294':('Restore the complete fatigue notice and apparent departure from the expedition; merely falling behind does not express leaving the party.',"Sailors are tired. Some seem to have left the party."),
        'DK4_MES_B285_R0333':('Retain the existing generic sailor reference while restoring the apparent-injury qualification; the clean Japanese gives no exact count.',"A sailor seems to have been injured."),
    }
    for ident,(reason,text) in fixes.items():
        row=byid[ident];assert row[1]=='D';row[:]=[ident,'T',reason,text]
    row=byid['DK4_MES_B285_R0114'];assert row[1]=='D'
    row[2]='Restore Leave it to me: the clipped Leave it can mean stop rather than entrust this action to Maria.'
    assert len(doc['records'])==349 and [r[0] for r in doc['records']]==[r[0] for r in load(before)['records']]
    doc.update(original_comparisons=str(before),original_comparisons_sha256=digest(before),readaloud_refinements_andexact_mode_correction=True)
    save(after,doc);print('Saved349 explicit contextual decisions with the original comparisons preserved.')

if __name__=='__main__':main()
