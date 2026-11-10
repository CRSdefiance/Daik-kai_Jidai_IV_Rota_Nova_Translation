"""Keep original FO/FA order in natural English; preserve the rejected first plan."""
from copy import deepcopy
from pathlib import Path
import re
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    prior=Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v1.json')
    target=Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v2.json')
    input_path=ROOT/'formatting_input_v2.json'
    assert not target.exists() and not input_path.exists()
    doc=deepcopy(load(prior))
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B70_R0029')
    assert row['decision']=='revision'
    previous=row['english']
    english="Excuse me. If I'm not mistaken, you lead {MACRO:FO}, Mr. {MACRO:FA}."
    reason='Keep the source FO-then-FA runtime substitution order while naturally identifying the faction leader; no rank or relationship is invented.'
    row.update(english=english,logical_English=english,
        planned_English_markup='{SPEAKER:0A}'+english,
        contextual_refinement=dict(previous_proposal=previous,reason=reason),
        finding=row['finding']+' '+reason,localization_note=reason)
    bindings=[]
    for row in doc['records']:
        original=re.findall(r'FI|FA|FO|FU',row['source_Japanese'])
        final=re.findall(r'\{MACRO:(FI|FA|FO|FU)\}',row['english'])
        assert Counter(original)==Counter(row['source_macros'])
        assert original==final,(row['id'],original,final)
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        bindings.append(dict(id=row['id'],source_macro_sequence=original,target_macro_sequence=final))
    assert len(bindings)==539
    doc.update(previous_manuscript=str(prior),previous_manuscript_sha256=sha(prior.read_bytes()),
        source_macro_order_refinement_record='DK4_MES_B70_R0029',
        all539_source_macro_sequences_exact=bindings,
        rejected_first_plan_preserved=str(ROOT/'automatic_v1/automatic_plans.json'),
        rejected_first_plan_failed_only_one_macro_order_guard=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(target,doc)
    save(input_path,dict(**doc,source_full_manuscript=str(target),source_full_manuscript_sha256=sha(target.read_bytes())))
    print('539 source/target macro sequences verified;one natural FO-before-FA refinement;old manuscript/failed plan preserved. No source/control guard relaxed.',flush=True)
