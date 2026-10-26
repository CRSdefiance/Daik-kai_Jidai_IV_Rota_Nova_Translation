"""Resolve the weak promise break with a complete faithful spoken successor."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B141_promise_v3545');old=Path('translations/lil_B141_editorial_manuscript_v1.json');new=Path('translations/lil_B141_editorial_manuscript_v3.json');assert not root.exists() and not new.exists();doc=deepcopy(read(old));r=next(r for r in doc['records'] if r['source_record_index']==50);before=r['english'];r['english']="{SPEAKER:02}I'll do more than wish you well! I'll have the money soon. Trust me and give me a little time!";r['localization_note']+=' The automatic preview stranded just in the longer first clause. The direct I will do more sentence naturally supplies her correction to the student,while retaining the contrast between good intentions and action,the promise of money soon,and the request for trust and a little time. No source fact is cut and no manual break or warning exemption is introduced.';doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()));save(new,doc);pairs=[]
    for a,b,changes in [
        ('scripts/plan_lil_B141_layout_v3543.py','scripts/plan_lil_B141_layout_v3545.py',[('lil_B141_layout_v3543','lil_B141_layout_v3545'),('editorial_manuscript_v1.json','editorial_manuscript_v3.json'),('editorial_manuscript_v2.json','editorial_manuscript_v4.json')]),
        ('scripts/verify_lil_B141_fonts_v3544.py','scripts/verify_lil_B141_fonts_v3546.py',[('lil_B141_fonts_v3544','lil_B141_fonts_v3546'),('editorial_manuscript_v2.json','editorial_manuscript_v4.json')])]:
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    root.mkdir(parents=True);save(root/'finding_and_faithful_successors.json',dict(manuscript=str(new),manuscript_sha256=sha(new.read_bytes()),id=r['id'],source_Japanese=r['source_Japanese'],before=before,after=r['english'],reason=r['localization_note'],tools=pairs,all_prior_artifacts_preserved=True,no_ROM_registry_ledger_review_or_completion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
