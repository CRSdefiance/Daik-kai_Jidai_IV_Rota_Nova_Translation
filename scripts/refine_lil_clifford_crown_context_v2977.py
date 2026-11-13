"""Use the established Crown referent in the complete B68 exchange."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Clifford_North_New_World_refinement_v2977')
OLD=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v2.json')
DOC=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));r=next(r for r in doc['records'] if r['id']=='DK4_MES_B68_R0067')
    earlier=next(r for r in doc['records'] if r['id']=='DK4_MES_B68_R0012');assert 'English Crown' in earlier['english']
    old=r['english'];r['english']="{SPEAKER:09}If he weren't tied to the Crown, none of this would've happened... I think he wanted to be our friend..."
    reason='The complete exchange already names the English Crown in Lil opening. Camille natural anaphoric the Crown preserves that exact referent and unwanted obligations without redundant naming. The unreal counterfactual, complete none-of-this consequence, explicit I think and personal friendship inference all remain. This is contextual prose, with no invented royal order or actual forgiveness.'
    r['localization_note']+=' '+reason
    change=dict(id=r['id'],previous_English=old,reviewed_English=r['english'],reason=reason)
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=doc['phrase_flow_refinements']+[change])
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),change=change,all143_source_controls_and88_revision55_retention_decisions_unchanged=True,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Established English Crown referent preserved in natural anaphoric prose;full counterfactual/qualified intent retained. Zero credit.')
