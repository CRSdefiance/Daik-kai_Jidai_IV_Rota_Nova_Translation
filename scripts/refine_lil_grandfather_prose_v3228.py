"""Resolve one protected-phrase wrap with a faithful complete-exchange wording."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B111_B119_refinement_v3228')
OLD=Path('translations/lil_B111_B119_editorial_manuscript_v1.json')
NEW=Path('translations/lil_B111_B119_editorial_manuscript_v2.json')
FAILURE=Path('work/analysis/lil_B111_B119_layout_v3227/all150_paragraph_layout_and_QA.json')
PLANNER=Path('scripts/prepare_lil_B111_B119_layout_v3229.py')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,NEW,PLANNER])
    doc=deepcopy(read(OLD));failure=read(FAILURE)
    assert [r['id'] for r in failure['failures']]==['DK4_MES_B112_R0119']
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B112_R0119')
    before=row['english'];assert row['editorial_decision']=='revise'
    row['english']="{SPEAKER:AA}No, no! You saved my grandson! I can't send you away empty-handed. Don't worry; it's no use just sitting here."
    note=("The first native plan split grandson's from life. Saved my grandson naturally conveys the lifesaving rescue already established by the drowning and reunion;no source fact is lost. The refusal to send his saviors away empty-handed,reassurance and lack of use for the keepsake all remain explicit. No weak-boundary or missing-meaning waiver is used.")
    row['prior_prose_before_wrap_refinement']=before;row['localization_note']+=' '+note
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        prose_refinement_failure=str(FAILURE),prose_refinement_failure_sha256=sha(FAILURE.read_bytes()))
    previous=Path('scripts/prepare_lil_B111_B119_layout_v3227.py')
    text=previous.read_text(encoding='utf-8')
    oldinputs="""INPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v1.json'),
        Path('translations/lil_B111_B119_actor_style_manuscript_v1.json')]"""
    newinputs=oldinputs.replace('editorial_manuscript_v1','editorial_manuscript_v2')
    oldoutputs="""OUTPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v2.json'),
         Path('translations/lil_B111_B119_actor_style_manuscript_v2.json')]"""
    newoutputs=oldoutputs.replace('editorial_manuscript_v2','editorial_manuscript_v3')
    assert text.count(oldinputs)==text.count(oldoutputs)==1
    changes={oldinputs:newinputs,oldoutputs:newoutputs,'lil_B111_B119_layout_v3227':'lil_B111_B119_layout_v3229'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    PLANNER.write_text(text,encoding='utf-8')
    ROOT.mkdir(parents=True);save(NEW,doc)
    save(ROOT/'faithful_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),id=row['id'],before=before,after=row['english'],reason=note,
        failure=str(FAILURE),failure_sha256=sha(FAILURE.read_bytes()),
        successor_QA_producer=str(PLANNER),successor_QA_producer_sha256=sha(PLANNER.read_bytes()),
        no_source_control_gloss_or_review_gate_change=True,no_renderer_or_global_formatter_change=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('One faithful grandfather wording successor;all source facts/context retained. Newcomplete150QA required.')
