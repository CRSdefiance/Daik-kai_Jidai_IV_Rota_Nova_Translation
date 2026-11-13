"""Seal separate captions after verifying the already-created exact body subset;do notrepeat it."""
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    doc_path = ROOT/'formatting_FE_v1/physical_manuscript.json'
    plan_path = ROOT/'plan_continuity_v2/automatic_plans.json'
    out = ROOT/'native_inputs_v1'
    receipt = out/'separate_choice_scope.json'
    assert not receipt.exists()
    doc, plan, subset, selected = map(load,[doc_path,plan_path,out/'manuscript.json',out/'plans.json'])
    speech = [r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    choices = [r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert subset['records'] == speech and len(speech) == len(selected['records']) == 314 and len(choices) == 15
    assert selected['records'] == plan['records'] and selected['manuscript_sha256'] == digest(out/'manuscript.json')
    save(receipt,dict(records=choices,choice_captions=15,choice_commands=5,source_editorial_objects=328,
        physical_body_candidates=314,one_source_riddle_has_two_native_children=True,
        unchanged_typed_objects_not_rendered_as_speech=True,all_fifth_gates_pending=True,new_credit=0,
        existing_successful_body_subset_preserved_not_recreated=True,
        evidence={str(p):digest(p) for p in [doc_path,plan_path,out/'manuscript.json',out/'plans.json',Path(__file__)]}))
    print('Sealed15 separate captions;existing314-body subset is exact andunchanged.')


if __name__ == '__main__':
    main()
