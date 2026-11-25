"""Preserve the initial draft; use a complete source-faithful appositive in the armor image."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_appositive_v7046b')
OLD=Path('translations/lil_B222_editorial_manuscript_v1.json')
NEW=Path('translations/lil_B222_editorial_manuscript_v2.json')
FAILED=Path('work/analysis/lil_B222_layout_v7046/sixteen_whole_paragraph_plans_no_macros_no_prose_changes.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists();before=read(OLD);after=deepcopy(before)
    failures=read(FAILED)['failures'];assert [r['id'] for r in failures]==['DK4_MES_B222_R0037']
    row=next(r for r in after['records'] if r['source_record_index']==37);prior=row['english']
    assert prior.count('the strait with an enemy soldier under each arm')==1
    revised=prior.replace('the strait with an enemy soldier under each arm','the strait, an enemy soldier under each arm')
    assert len(revised)==len(prior)-4 and len(revised.split('}',1)[1])>len(bytes.fromhex(row['source_hex']))-1
    row['historical_first_draft_English']=prior;row['english']=revised
    row['localization_note']+=' Natural-dialogue polish: use an absolute appositive image after the strait instead of the with-an prepositional chain. Only the connector with becomes punctuation;exhaustion,the complete hearsay,bottom of the strait,two enemy soldiers(one under each arm),gleaming armor and the trailing coda remain. The paragraph still exceeds the original source allocation and requires relocation;no source fact,descriptive word or report marker is removed to avoid that work.'
    row['editorial_finding']=row['localization_note']
    after.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        source_complete_appositive_polish_v7046b=True,all_original16_source_meanings_and_twelve_revision_four_retention_decisions_unchanged=True)
    ROOT.mkdir(parents=True);save(NEW,after)
    tool=derive('scripts/plan_lil_B222_layout_v7046.py','scripts/plan_lil_B222_layout_v7046b.py',{
        'editorial_manuscript_v1.json':'editorial_manuscript_v2.json','layout_v7046':'layout_v7046b'})
    save(ROOT/'complete_source_image_appositive_and_preserved_first_draft.json',dict(first_manuscript=str(OLD),first_manuscript_sha256=sha(OLD.read_bytes()),
        revised_manuscript=str(NEW),revised_manuscript_sha256=sha(NEW.read_bytes()),before=prior,after=revised,
        failed_first_single_page_plan=str(FAILED),failed_plan_sha256=sha(FAILED.read_bytes()),source_allocation_still_exceeded_relocation_required=True,
        only_with_connector_recast_all_facts_qualifiers_and_descriptive_words_retained=True,source_locked_layout_successor=tool,
        all_native_viewport_pair_phase_guard_and_bare_I_constraints_unchanged=True,new_review_credit=0,full_goal_complete=False))
