"""Four source-faithful conversational refinements after the preserved2897 plan."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_Kuhn_China_refinement_v2898')
OLD=Path('translations/lil_kuhn_china_editorial_manuscript_v1.json')
DOC=Path('translations/lil_kuhn_china_editorial_manuscript_v2.json')
CHANGES={
'DK4_MES_B146_R0140':("When you're worried, don't shut yourself away. Keeping busy distracts you. Once you're calmer, you can find a solution.",'Keep the complete withdrawal/activity/distraction/calmer-solution sequence while saying distracts you directly; this removes an awkward weak boundary without deleting an idea or inventing a diagnosis.'),
'DK4_MES_B147_R0186':("I can't believe it! You did that, and now you're playing innocent?!",'Preserve disbelief, the accusation and current feigned innocence in natural clause order, avoiding an isolated innocent final row. This remains Christina allegation, not narrator proof.'),
'DK4_MES_B147_R0269':("Listen. He starts by making a show of working with people like you to build his influence. Then...",'Listen and he starts already introduce the method; remove the redundant second setup while retaining first-step facade/cooperation, people like Lil, expanded influence and the deliberate Then lead-in.'),
'DK4_MES_B147_R0273':("Once he's done with his partners, he gets rid of them when it suits him... Only his expanded territory remains.",'Done with his partners is the natural idiom for their use being over. Preserve opportunistic timing, disposal and only the enlarged domain remaining; do not specify a universal killing method.')
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));changes=[]
    for r in doc['records']:
        if r['id'] not in CHANGES:continue
        en,note=CHANGES[r['id']];prefix='{SPEAKER:'+r['source_presentation_prefix_hex'].upper()+'}';before=r['english'];r['english']=prefix+en
        assert r['editorial_decision']=='revise' and r['english']!=before
        r['localization_note']+=' '+note;changes.append(dict(id=r['id'],before=before,after=r['english'],source_meaning=r['source_meaning'],reason=note))
    assert len(changes)==4
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=changes)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,all_other_English_source_controls_and_retention_decisions_unchanged=True,no_manual_layout_or_waiver=True,source_prose_orcompletion_credit_added=0,full_goal_complete=False))
    print('Four faithful conversational refinements; original draft and failed2897 plan preserved. Zero editorial credit.')
