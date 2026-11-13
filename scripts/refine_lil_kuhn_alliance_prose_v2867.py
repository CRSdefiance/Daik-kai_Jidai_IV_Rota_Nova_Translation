"""Complete source-faithful business understatement after boundary preflight with source-faithful conversational wording."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/lil_kuhn_alliance_editorial_manuscript_v4.json')
DOC=Path('translations/lil_kuhn_alliance_editorial_manuscript_v5.json')
ROOT=Path('work/analysis/lil_Kuhn_Alliance_refinement_v2867')
if __name__=='__main__':
    assert not DOC.exists() and not ROOT.exists();doc=deepcopy(read(OLD));r=next(r for r in doc['records'] if r['id']=='DK4_MES_B48_R0067');before=r['english']
    assert "it's been rather difficult" in before
    r['english']="{SPEAKER:38}Mr. Kuhn is concerned, too. He wants to drive Pereira from these waters, but it's no easy task. And so..."
    note='Fresh clean-source rereading confirms the formal admission of difficulty is an understatement, not a measured degree or a failed expulsion. No easy task conveys that naturally while preserving concern/too, planned expulsion, these waters and the deliberate And so lead-in. Source-owned automatic wrapping passes with no question/negation, weak-ending or other waiver; all prior drafts and failed2856/2856b/2862 plans remain preserved.'
    r['localization_note']+=' '+note;changes=[dict(id=r['id'],before=before,after=r['english'],reason=note)]
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=doc.get('phrase_flow_refinements',[])+changes)
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,credit_added=0,full_goal_complete=False));print('One source-faithful conversational refinement; original draft and failed plan preserved.')
