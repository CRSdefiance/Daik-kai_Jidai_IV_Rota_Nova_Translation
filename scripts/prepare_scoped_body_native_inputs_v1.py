"""Select all exact planned bodies, keeping typed captions out of the speech renderer."""
import argparse
import runpy
import sys
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['manuscript', 'plan', 'out']:
        parser.add_argument('--'+key, type=Path, required=True)
    args = parser.parse_args()
    doc, plan = map(load, [args.manuscript, args.plan])
    assert not args.out.exists() and plan['manuscript_sha256'] == digest(args.manuscript)
    speech = [r for r in doc['records'] if r['kind'] in ['progressive', 'system-FE']]
    captions = [r for r in doc['records'] if r['kind'] == 'typed-choice-label']
    assert len(speech) + len(captions) == len(doc['records'])
    assert len(speech) == doc['physical_speech_objects'] == len(plan['records'])
    assert len(captions) == doc['typed_choice_objects'] and not plan['failures']
    assert {r['id'] for r in speech} == {r['id'] for r in plan['records']}
    assert not any(i['severity'] in ['error', 'warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    sys.argv = ['prepare_editorial_native_subset_v2', '--manuscript', str(args.manuscript),
        '--plan', str(args.plan), '--out', str(args.out), '--ids', *[r['id'] for r in speech]]
    runpy.run_module('scripts.prepare_editorial_native_subset_v2', run_name='__main__')
    subset, selected = map(load, [args.out/'manuscript.json', args.out/'plans.json'])
    assert subset['records'] == speech and selected['records'] == plan['records']
    assert selected['manuscript_sha256'] == digest(args.out/'manuscript.json')
    save(args.out/'separate_choice_scope.json', dict(records=captions,
        choice_captions=len(captions), choice_commands=doc['typed_choice_commands'],
        physical_body_candidates=len(speech), source_editorial_objects=len(doc['records']),
        unchanged_typed_objects_not_rendered_as_speech=True, all_fifth_gates_pending=True,
        new_credit=0, evidence={str(p): digest(p) for p in [args.manuscript, args.plan,
            args.out/'manuscript.json', args.out/'plans.json', Path(__file__)]}))
    print(f'Selected all {len(speech)} exact body plans; {len(captions)} captions remain separate; no display approval or credit.')


if __name__ == '__main__':
    main()
