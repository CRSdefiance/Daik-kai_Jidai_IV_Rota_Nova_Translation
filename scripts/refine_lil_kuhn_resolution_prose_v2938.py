"""Two complete-paragraph refinements after preserved2937 findings."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_Kuhn_Resolution_refinement_v2938')
OLD=Path('translations/lil_kuhn_resolution_editorial_manuscript_v1.json')
DOC=Path('translations/lil_kuhn_resolution_editorial_manuscript_v2.json')
CHANGES={
'DK4_MES_B61_R0055':("I want all the Proofs of Supremacy you've collected. Hand them over, and I guarantee your companion's life.",'Use the direct I want request for Japanese handing-over desire while preserving all collected Proofs and the explicit conditional life guarantee. The immediately preceding pains-me-to-ask line carries Clifford false courtesy. This lets the automatic planner keep the complete proper term intact without deleting a proposition or forcing manual layout.'),
'DK4_MES_B62_R0110':('A sheath...? Could this also be connected to a Proof of Supremacy?','Connected to is a natural concise expression of source relationship, and also preserves the source mo without an isolated final too. Keep the identification and possible Proof connection as questions; no object identity or certainty is added.')}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));changes=[]
    for row in doc['records']:
        if row['id'] not in CHANGES:continue
        text,note=CHANGES[row['id']];before=row['english'];row['english']='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+text
        assert row['editorial_decision']=='revise' and before!=row['english']
        row['localization_note']+=' '+note;changes.append(dict(id=row['id'],before=before,after=row['english'],source_meaning=row['source_meaning'],reason=note))
    assert len(changes)==2
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=changes)
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,
        all_other_English_source_controls_and_retention_decisions_unchanged=True,no_manual_layout_or_new_waiver=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Two faithful whole-paragraph refinements;failed2937 plan andall earlier prose preserved. Zero ledger credit.')
