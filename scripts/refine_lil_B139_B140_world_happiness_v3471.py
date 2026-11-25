"""Preserve Lil's motive while resolving a reviewed phrase split."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B139_B140_world_happiness_v3471');assert not root.exists()
    old=Path('translations/lil_B139_B140_editorial_manuscript_v1.json');new=Path('translations/lil_B139_B140_editorial_manuscript_v3.json');assert not new.exists()
    failure=Path('work/analysis/lil_B139_B140_layout_v3469/all67_paragraph_layout_QA.json');assert [r['id'] for r in read(failure)['failures']]==['DK4_MES_B140_R0258']
    doc=deepcopy(read(old));r=next(r for r in doc['records'] if r['id']=='DK4_MES_B140_R0258');before=r['english']
    r['english']='{SPEAKER:02}I want to help people who are struggling, like everyone back home. I want people all over the world to be happy!'
    r['localization_note']+=' The initial plan split people happy across rows. This spoken successor retains helping struggling people like her home village and her wish for worldwide happiness; no fact, emphasis, manual break or warning exemption is added.'
    r.update(prose_refinement_producer=str(Path(__file__)),prose_refinement_producer_sha256=sha(Path(__file__).read_bytes()))
    doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()));save(new,doc)
    pairs=[]
    for a,b,changes in [
      ('scripts/plan_lil_B139_B140_layout_v3469.py','scripts/plan_lil_B139_B140_layout_v3471.py',[('layout_v3469','layout_v3471'),('editorial_manuscript_v1','editorial_manuscript_v3'),('editorial_manuscript_v2','editorial_manuscript_v4')]),
      ('scripts/verify_lil_B139_B140_fonts_v3470.py','scripts/verify_lil_B139_B140_fonts_v3472.py',[('fonts_v3470','fonts_v3472'),('editorial_manuscript_v2','editorial_manuscript_v4')])]:
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    root.mkdir(parents=True);save(root/'finding_and_successors.json',dict(id=r['id'],source_Japanese=r['source_Japanese'],before=before,after=r['english'],previous_manuscript=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),failure_proof=str(failure),failure_sha256=sha(failure.read_bytes()),tools=pairs,no_meaning_cut_manual_layout_or_warning_waiver=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
