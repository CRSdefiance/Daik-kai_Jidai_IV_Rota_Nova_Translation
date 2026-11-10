"""Join complete individual comparisons andmapped speakers withoutsilently approving held gates."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['source','identity','out']:
        parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--comparisons',type=Path,nargs='+',required=True)
    args = parser.parse_args(); assert not args.out.exists()
    source, identity = map(load,[args.source,args.identity])
    expected = {r['id']:r for r in source['records']};rows = {}
    public = {r['actor_ID']:next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in identity['name_bindings']}
    roles = {r['source_selector']:r for r in identity['dynamic_roles']}
    parents = []
    for path in args.comparisons:
        doc = load(path);parents.append(doc)
        assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
        assert doc['current_ROM_sha256'] == identity['runtime']['candidate_sha256']
        for row in doc['records']:
            key = row['id'];assert key not in rows and key in expected
            assert all(row[k] == expected[key][k] for k in ['source_hex','source_reference','source_Japanese','independent_English_draft'])
            assert row['review']['source'] and row['review']['context'] and row['review']['naturalness'] and not row['review']['formatting']
            assert row['finding'].strip() and row['localization_note'].strip()
            assert row['decision'] in ['revision','retention'] and ((row['english'] == row['current_English']) == (row['decision']=='retention'))
            assert row['english'].isascii() and not any(s in row['english'] for s in ['\n','\r','{LB','{PAD}','{ALIGN'])
            for macro,count in row.get('source_macros',{}).items(): assert row['english'].count(macro) == count
            value = deepcopy(row);selector = row.get('source_selector')
            if selector is None:
                assert row['kind'] == 'typed-choice-label';value['speaker'] = 'Player choice'
            elif selector == 254:
                value['speaker'] = 'System'
            elif selector < 207:
                value['speaker'] = public[selector]
            else:
                role = roles[selector];value['speaker'] = f"Runtime role{role['role_index']} companion"
                value['native_dynamic_role'] = deepcopy(role)
                value['own_startup_role_binding_does_not_assign_original_conditional_speaker'] = True
            value['native_scoped_identity_proof'] = str(args.identity)
            value['native_scoped_identity_proof_sha256'] = sha(args.identity.read_bytes())
            value['source_name_term_control_binding_pending'] = not row['review']['localization']
            rows[key] = value
    assert set(rows) == set(expected) and len(rows) == source['source_objects']
    assert len({d['current_archive_sha256'] for d in parents}) == 1
    ordered = [rows[r['id']] for r in source['records']]
    save(args.out,dict(format='dk4-natural-dialogue-v2-editorial-manuscript',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=source['file_path'],blocks=sorted({r['block'] for r in ordered}|{130,131}),records=ordered,
        current_ROM=parents[0]['current_ROM'],current_ROM_sha256=parents[0]['current_ROM_sha256'],current_archive_sha256=parents[0]['current_archive_sha256'],
        source_objects=len(ordered),source_speeches=sum(r['kind']!='typed-choice-label' for r in ordered),
        ordinary_speeches=sum(r['kind']!='typed-choice-label' and r.get('native_object_kind')!='4100-style-alternative' for r in ordered),
        physical_style_variants=sum(r.get('native_object_kind')=='4100-style-alternative' for r in ordered),
        typed_choice_labels=sum(r['kind']=='typed-choice-label' for r in ordered),
        contextual_comparisons=len(ordered),proposed_revisions=sum(r['decision']=='revision' for r in ordered),
        justified_retentions=sum(r['decision']=='retention' for r in ordered),
        four_gate_passes=sum(all(r['review'][g] for g in ['source','context','localization','naturalness']) for r in ordered),
        pending_name_term_IDs=[r['id'] for r in ordered if not r['review']['localization']],
        remaining_current_comparisons=0,all_contextual_findings_wording_andindividual_gate_values_exact_preserved=True,
        all_fifth_formatting_gates_pending=True,all_scoped_name_planes_andtwo_full_name_particle_fixes_pending=True,
        scoped_name_review=identity['scoped_name_review'],scoped_name_review_sha256=identity['scoped_name_review_sha256'],
        source_context_localization_formatting_gates_pending=True,new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [args.source,args.identity,*args.comparisons,Path(__file__)]}))
    d=load(args.out);print(dict(comparisons=len(ordered),revisions=d['proposed_revisions'],retentions=d['justified_retentions'],
        four_gate_passes=d['four_gate_passes'],remaining_name_term_holds=len(d['pending_name_term_IDs']),remaining_comparisons=0,new_credit=0))


if __name__ == '__main__': main()
