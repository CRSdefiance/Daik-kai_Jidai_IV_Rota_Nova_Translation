"""One natural gift sentence and one concrete lucky-charm boundary successor."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('translations/lil_crew_items_editorial_manuscript_v2.json')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v3.json')
PARENT=Path('dk4tool/dialogue/lil_crew_items_layout_v1.py')
LAYOUT=Path('dk4tool/dialogue/lil_crew_items_layout_v2.py')
FAILURE=Path('work/analysis/lil_Crew_Items_layout_v3125/all198_layout_and_QA.json')
ROOT=Path('work/analysis/lil_Crew_Items_refine_v3126')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,LAYOUT]);failure=read(FAILURE)
    assert [r['id'] for r in failure['failures']]==['DK4_MES_B82_R0075']
    doc=deepcopy(read(OLD));row=next(r for r in doc['records'] if r['id']=='DK4_MES_B82_R0075');previous=row['english']
    row['english']="{SPEAKER:98}Yes. I'd like someone like you to have my lucky charm. I'm no longer physically able to sail."
    note='Combine the personal offer and his own lucky charm into a natural sentence;past ownership is already implicit in my lucky charm andtheoffer tohand iton. Preserve the intended kindofrecipient andexplicitphysical inability without addinga cause. This resolves the concrete weak-have boundary. Keep the idiomatic lucky charm together under a newbatch-local phrase rule;no manual spaces,layout commands,runtime orglobalhelper change.'
    row['localization_note']+=' '+note
    assert row['editorial_decision']=='revise' and not row['review']['formatting']
    planner=PARENT.read_text(encoding='utf-8');anchor='PROTECTED_BOUNDARIES=frozenset({';assert planner.count(anchor)==1
    planner=planner.replace(anchor,anchor+"('lucky','charm'),")
    planner=planner.replace('# Source0D is actor13, not generic CR whitespace. Bind each source prefix\n    # to this exact consumer before the shared encoder interprets controls.','# Bind every source prefix to this exact consumer before the shared\n    # encoder interprets executable presentation controls.')
    compile(planner,str(LAYOUT),'exec');LAYOUT.write_text(planner,encoding='utf-8')
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),layout_failure=str(FAILURE),layout_failure_sha256=sha(FAILURE.read_bytes()))
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'final_sailor_phrase_refinement.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),id=row['id'],source_Japanese=row['source_Japanese'],source_meaning=row['source_meaning'],previous=previous,english=row['english'],reason=note,
        previous_formatter=str(PARENT),previous_formatter_sha256=sha(PARENT.read_bytes()),formatter=str(LAYOUT),formatter_sha256=sha(LAYOUT.read_bytes()),previous_drafts_plans_and_formatter_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),native_QA_font_reference_release_still_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('One faithful sailor successor andbatch-local lucky-charm rule;allprevious drafts/failedplans preserved.')
