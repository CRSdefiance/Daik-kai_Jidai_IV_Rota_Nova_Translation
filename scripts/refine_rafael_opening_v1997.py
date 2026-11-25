"""Explicit successor restores FO/FI/FA command order without weakening meaning."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('translations/rafael_opening_contextual_editorial_manuscript_v1.json')
TARGET=Path('translations/rafael_opening_contextual_editorial_manuscript_v2.json')

if __name__=='__main__':
    assert not TARGET.exists()
    doc=read(SOURCE)
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B44_R0316')
    row['previous_editorial_english']=row['english']
    row['english']="{SPEAKER:06}You're the leader of {MACRO:FO}, {MACRO:FI} {MACRO:FA}. I'm lending you this money because I trust you. You're responsible.{PAD}"
    row['localization_note']+=' The successor also keeps the source executable substitution order FO, FI, FA exactly; no personal-trust clause is omitted.'
    row['finding']=row['localization_note']
    doc['supersedes']=str(SOURCE);doc['superseded_manuscript_sha256']=sha(SOURCE.read_bytes())
    doc['successor_reason']='Restore original FO/FI/FA order in R0316; personal loan, trust and responsibility remain explicit. Measured Rafael runtime FI is six ASCII bytes; the legacy seven-byte profile is pending a source-bound successor.'
    save(TARGET,doc)
    print(dict(successor=str(TARGET),records=len(doc['records']),formatting=False))
