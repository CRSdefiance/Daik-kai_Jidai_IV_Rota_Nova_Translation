"""Preserve belief qualification and re-express the complete Crown counterfactual."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Clifford_North_New_World_refinement_v2975')
OLD=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v1.json')
DOC=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v2.json')
CHANGES={
 'DK4_MES_B68_R0045':("{SPEAKER:02}I believed in you... I thought you were one of us...",'Use thought rather than knew to preserve Lil past belief as her personal perspective, not independently proven knowledge. Her second-person trust and emotional pause remain intact.'),
 'DK4_MES_B68_R0067':("{SPEAKER:09}Without his ties to the English Crown, this wouldn't have happened... I think he wanted to be friends with us...",'Re-express the complete counterfactual naturally with this matching source konna koto, retaining unwanted Crown ties, the unreal past consequence and explicitly qualified desire for friendship with us. No historical detail or relationship is omitted; the prior weak-ending layout remains preserved as a failed plan.')
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));changes=[]
    for row in doc['records']:
        if row['id'] not in CHANGES:continue
        english,note=CHANGES[row['id']];assert row['editorial_decision']=='revise'
        changes.append(dict(id=row['id'],previous_English=row['english'],reviewed_English=english,reason=note))
        row['english']=english;row['localization_note']+=' '+note
    assert len(changes)==2
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=changes,formatting_review_pending=True)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,all_other_English_source_controls_and_decisions_unchanged=True,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Two revised paragraphs clarified;all55retentions andsourcecontrols unchanged. QA/native/release pending;zero credit.')
