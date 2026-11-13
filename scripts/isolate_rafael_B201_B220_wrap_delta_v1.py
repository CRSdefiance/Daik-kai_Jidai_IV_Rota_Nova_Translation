"""Isolate newly encoded B201–B220 speech for fresh native verification."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest
from scripts.refine_rafael_B201_B220_wraps_v2 import OUT as MANUSCRIPT, EDIT, PHRASES


OLD = ROOT/'ordinary_plans_v2/automatic_plans.json'
NEW = ROOT/'ordinary_plans_v3/automatic_plans.json'
DELTA_DOC = ROOT/'ordinary_delta_manuscript_v1.json'
DELTA_PLAN = ROOT/'ordinary_delta_plan_v1.json'


def main():
    assert not DELTA_DOC.exists() and not DELTA_PLAN.exists()
    doc,old,new = map(load,(MANUSCRIPT,OLD,NEW))
    assert len(old['records']) == len(new['records']) == 381
    assert new['manuscript_sha256'] == digest(MANUSCRIPT)
    assert not new['failures']
    assert not any(i['severity'] in ('warning','error') for row in new['records'] for i in row['base_QA']['issues'])
    changed = []
    for before,after in zip(old['records'],new['records'],strict=True):
        assert before['id'] == after['id']
        if before['encoded_hex'] == after['encoded_hex']:
            assert before['lines'] == after['lines'] and before['logical_English'] == after['logical_English']
            continue
        assert after['id'].removeprefix('DK4_MES_') in EDIT.keys() | PHRASES.keys()
        changed.append(after)
        print(after['id'],after['lines'])
    ids = {r['id'] for r in changed}
    assert len(ids) >= len(EDIT)
    save(DELTA_DOC,{**doc,'records':[r for r in doc['records'] if r['id'] in ids],
        'physical_speech_objects':len(ids),'ordinary_speech_objects':len(ids),
        'typed_choice_objects':0,'typed_choice_commands':0})
    save(DELTA_PLAN,{**new,'records':changed,'manuscript':str(DELTA_DOC),
        'manuscript_sha256':digest(DELTA_DOC),'complete_plan_sha256':digest(NEW)})
    print(len(ids),'fresh native records',381-len(ids),'exact reused encodings.')


if __name__ == '__main__':
    main()

