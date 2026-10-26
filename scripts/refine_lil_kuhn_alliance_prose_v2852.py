"""Resolve2851 weak boundary with source-faithful conversational wording."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/lil_kuhn_alliance_editorial_manuscript_v1.json')
DOC=Path('translations/lil_kuhn_alliance_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/lil_Kuhn_Alliance_refinement_v2852')
if __name__=='__main__':
    assert not DOC.exists() and not ROOT.exists();doc=deepcopy(read(OLD));r=next(r for r in doc['records'] if r['id']=='DK4_MES_B48_R0067');before=r['english']
    assert 'He hopes to drive Pereira out of these waters' in before
    r['english']=before.replace('He hopes to drive Pereira out of these waters','He wants Pereira out of these waters')
    note='The2851 automatic plan leaves of at a row end. Wants Pereira out expresses the same desired expulsion naturally without repeated drive-out-of wording; concern, too, region, rather-difficult qualification and the deliberate lead-in all remain. No manual break or weak-ending waiver is allowed.'
    r['localization_note']+=' '+note;changes=[dict(id=r['id'],before=before,after=r['english'],reason=note)]
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=changes)
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,credit_added=0,full_goal_complete=False));print('One source-faithful conversational refinement; original draft and failed plan preserved.')
