"""One natural spoken construction refined after viewing all28 current native sheets."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_Kuhn_China_refinement_v2902')
OLD=Path('translations/lil_kuhn_china_editorial_manuscript_v3.json')
DOC=Path('translations/lil_kuhn_china_editorial_manuscript_v4.json')
CHANGES={
'DK4_MES_B54_R0031':("If the disguised fleet wins, we can attack the Li family on the pretext of avenging our ally, {MACRO:FO}...",'Replace the awkward claim to avenge construction with on the pretext of avenging. This directly preserves the clean conditional victory, bogus vengeance for the allied company and resulting justification to attack the Li family, without asserting genuine grief or an achieved attack.')
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));changes=[]
    for r in doc['records']:
        if r['id'] not in CHANGES:continue
        en,note=CHANGES[r['id']];prefix='{SPEAKER:'+r['source_presentation_prefix_hex'].upper()+'}';before=r['english'];r['english']=prefix+en
        assert r['editorial_decision']=='revise' and r['english']!=before
        r['localization_note']+=' '+note;changes.append(dict(id=r['id'],before=before,after=r['english'],source_meaning=r['source_meaning'],reason=note))
    assert len(changes)==1
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=doc.get('phrase_flow_refinements',[])+changes)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,all_other_English_source_controls_and_retention_decisions_unchanged=True,no_manual_layout_or_waiver=True,source_prose_orcompletion_credit_added=0,full_goal_complete=False))
    print('One source-faithful natural construction refined; all drafts and prior proofs preserved. Zero editorial credit.')
