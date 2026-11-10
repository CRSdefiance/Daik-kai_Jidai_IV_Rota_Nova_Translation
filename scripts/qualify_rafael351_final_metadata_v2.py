"""Clear superseded intake holds using sealed proofs; preserve all prose and ROMs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    root = Path('work/analysis/Rafael351_final_metadata_v2_20261105')
    old_main = Path('translations/rafael_B121_B140_contextual_final_review_v1.json')
    old_names = Path('translations/rafael_B121_B140_scoped_names_final_v1.json')
    old_combined = Path('translations/rafael_B121_B140_cumulative867_refs_v1.json')
    new_main = old_main.with_name('rafael_B121_B140_contextual_final_review_v2.json')
    new_names = old_names.with_name('rafael_B121_B140_scoped_names_final_v2.json')
    new_combined = old_combined.with_name('rafael_B121_B140_cumulative867_refs_v2.json')
    assert not any(p.exists() for p in [root, new_main, new_names, new_combined])
    completed_path = Path('work/analysis/Rafael351_checked_v1_20261105/research_completion.json')
    combined_path = Path('work/analysis/Rafael867_combined_research_v1_20261105/reconstruction.json')
    completed, combined = map(load, [completed_path, combined_path])
    for path, digest in completed['evidence'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    before, names, cumulative = map(load, [old_main, old_names, old_combined])
    assert before['scoped_names_andterms_bound_for_prose']
    assert not before['pending_name_term_IDs'] and not before['remaining_current_comparisons']
    for key in ['scoped_identity_proof', 'scoped_term_proof']:
        assert sha(Path(before[key]).read_bytes()) == before[key + '_sha256']
    assert all(all(r['review'].values()) and len(r['review']) == 5 for r in before['records'] + names['records'])
    assert names['all22_individual_five_gates_pass_for_public_nameplanes']
    assert names['all22_name_formatting_gates_pending']
    identity = load(before['scoped_identity_proof'])
    assert len(identity['actors']) == 22
    assert combined['manuscript_sha256'] == sha(old_combined.read_bytes())
    assert combined['research_ROM_sha256'] == '3bf3239736982e6398eda1f837f4c249b93e541128985013fbde02466bcbaa9c'
    assert sha(Path(combined['research_ROM']).read_bytes()) == combined['research_ROM_sha256']
    names = deepcopy(names)
    names['all22_name_formatting_gates_pending'] = False
    names['superseded_intake_metadata'] = str(old_names)
    names['superseded_intake_metadata_sha256'] = sha(old_names.read_bytes())
    validate_natural_dialogue_batch(names)
    root.mkdir(parents=True)
    save(new_names, names)
    cleared = []
    allowed = {'scoped_name_role_oritem_binding_pending',
               'town_name_spelling_pending_approved_label_binding',
               'treasure_label_andsource_uncertainty_binding_pending'}
    for original, document, destination in [(before, deepcopy(before), new_main),
                                            (cumulative, deepcopy(cumulative), new_combined)]:
        for old, row in zip(original['records'], document['records'], strict=True):
            for key in allowed:
                if row.get(key):
                    row[key] = False
                    if destination == new_main:
                        cleared.append({'id': row['id'], 'superseded_hold': key})
            assert all(row[k] == v for k, v in old.items() if k not in allowed)
            assert row['registered_release_andcompletion_credit_pending'] and row['new_credit'] == 0
        document.update(scoped_name_review=str(new_names), scoped_name_review_sha256=sha(new_names.read_bytes()),
                        superseded_intake_metadata=str(old_main if destination == new_main else old_combined),
                        superseded_intake_metadata_sha256=sha((old_main if destination == new_main else old_combined).read_bytes()),
                        resolved_intake_flags_aligned_with_existing_sealed_proofs=True)
        validate_natural_dialogue_batch(document)
        save(destination, document)
    plans = load('work/analysis/Rafael351_checked_v1_20261105/release_plans.json')
    plans.update(manuscript=str(new_main), manuscript_sha256=sha(new_main.read_bytes()))
    save(root / 'release_plans.json', plans)
    cumulative_plans = load(combined['plan'])
    cumulative_plans.update(manuscript=str(new_combined), manuscript_sha256=sha(new_combined.read_bytes()))
    save(root / 'cumulative_release_plans.json', cumulative_plans)
    view = deepcopy(combined)
    view.update(manuscript=str(new_combined), manuscript_sha256=sha(new_combined.read_bytes()),
                plan=str(root / 'cumulative_release_plans.json'),
                plan_sha256=sha((root / 'cumulative_release_plans.json').read_bytes()),
                stored_native_pages_gameplay_andregistered_release_pending=False,
                registered_release_andcompletion_credit_pending=True,
                original_reconstruction=str(combined_path), original_reconstruction_sha256=sha(combined_path.read_bytes()),
                metadata_only_no_new_ROM_or_display_execution=True)
    save(root / 'cumulative_reconstruction.json', view)
    result = deepcopy(completed)
    result.update(manuscript=str(new_main), manuscript_sha256=sha(new_main.read_bytes()),
                  original_completion=str(completed_path), original_completion_sha256=sha(completed_path.read_bytes()),
                  resolved_intake_flags_aligned_with_existing_sealed_proofs=True,
                  evidence={str(p): sha(p.read_bytes()) for p in [new_main, new_names, new_combined, completed_path,
                      combined_path, root / 'release_plans.json', root / 'cumulative_release_plans.json',
                      root / 'cumulative_reconstruction.json', Path(before['scoped_identity_proof']),
                      Path(before['scoped_term_proof']), Path(__file__)]})
    save(root / 'research_completion.json', result)
    save(root / 'qualification.json', dict(cleared_intake_flags=cleared, public_name_formatting_pending_cleared=True,
        all_source_current_references_wording_decisions_findings_controls_five_gates_andstored_bytes_unchanged=True,
        all_ROMs_andoriginal_proofs_unchanged=True, full_catalogue_particles_andglobal_name_review_still_pending=True,
        registered_integration_pending=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [old_main, old_names, old_combined,
            root / 'research_completion.json', new_main, new_names, new_combined]}))
    print(f'Aligned {len(cleared)} superseded per-record intake flags and22 name-formatting flags; prose, controls, five gates, stored bytes andROMs preserved. No credit orpromotion.')


if __name__ == '__main__':
    main()
