"""Record verified integration and the exact next clean-source intake."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import BINDING, PACKAGE, RESEARCH, link
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


A = Path('work/analysis')
ROOT = A / 'Rafael1975_extended_release_verified_v1_20261105'
RELEASE = ROOT / 'registered_release_verification.json'
CREDIT = ROOT / 'completion_checkpoint.json'
STARTUP = ROOT / 'own_registered_startup_verification.json'
GETTERS = ROOT / 'own_Fernan_name_getter_verification.json'
CURRENT = A / 'Rafael_B170_B176_current1975_20261105/current_effective.json'
REGISTRY = Path('translations/release_stack.json')
INTEGRATED = Path('translations/rafael_B168_B169_integrated_final_review_v1.json')


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    release, credit, startup, getters, package, current = map(load, (RELEASE, CREDIT, STARTUP, GETTERS, PACKAGE, CURRENT))
    assert credit['new_credit'] == 115 and credit['counts'] == dict(completed=13820, revised=7938, retained=5882)
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (686, 114, 26)
    assert release['only_owned_SC0_blocks_changed'] == [168,169] and release['all_eight_registered_final_stages_preserved']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert startup['frames'] == 4001 and startup['actual_captain_getter'] == startup['actual_route_word'] == 0
    assert getters['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    assert package['ROM_sha256'] == release['parent_sha256'] and digest(package['zip']) == package['zip_sha256']
    assert current['current_ROM_sha256'] == release['candidate_sha256'] and current['original_current_catalogue_lookups'] == 190
    assert [g['block'] for g in current['groups']] == list(range(170,177))
    assert digest(REGISTRY) == release['registry_sha256']
    summary = ('Rafael B168–B169 is registered and credited once, with 90 revisions and 25 justified retentions. '
        f"Experimental {release['candidate_sha256'][:8]} passed 686 entries, all 114 accepted layers, eight final stages, "
        '26 release checks, exact clean-input reconstruction and its own Rafael startup. Integrated total is 13,820. '
        'All 190 B170–B176 clean drafts are bound to current English for contextual comparison. '
        'Rafael1860 remains the delivered weekend build.')
    doc = f"""# Rafael1975 registered checkpoint

The {link('registered experimental ROM', release['candidate'])} has SHA-256 `{release['candidate_sha256']}`. The {link('clean-input patch', release['patch'])} reconstructed it byte for byte. The manifest retains 686 entries, 114 accepted layers and all eight final stages, including the ASCII right-bound correction. All 26 release checks and the candidate’s own 4,001-frame cold boot to Rafael’s opening passed. Both original Fernan name getters passed from its own snapshot. Only B168–B169 differ from Rafael1860. {link('Release proof', RELEASE)}.

The {link('integrated individual reviews', INTEGRATED)} credit 90 revisions and 25 retentions once. The ledger now has 13,820 integrated reviews, comprising 7,938 revisions and 5,882 retentions. All 117 pages and ten nameplates passed offline and direct visual checks. The initialized emulator sequence displayed 58 speeches and 60 pages. The other 57 speeches passed offline checks. Original conditions, locations and hardware remain unvisited. {link('Review scope', RESEARCH)}.

The {link('current-English packet', CURRENT)} binds all 190 clean-first B170–B176 drafts to the verified registered candidate. Compare the seven complete blocks and preserve the six source modal presentations, Jam’s explicit spelling, and both departure office follow-up records. All 741 records in this intake have clean drafts, 551 have contextual decisions, and 551 are integrated.

The earlier preparation using the incompatible schema and its generated references are preserved. The successful retry uses the established FU-capable preparation and verified prefix. The designated main, delivered Rafael1860 weekend ZIP, earlier builds and evidence are preserved. Keep artwork and the later technical re-audit separate.
"""
    evidence = {str(p): digest(p) for p in (RELEASE,CREDIT,STARTUP,GETTERS,RESEARCH,BINDING,CURRENT,INTEGRATED,Path(__file__))}
    checkpoint(
        mutation=ROOT / 'documentation_checkpoint',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, integrated_subbatch_credit=551,
            integrated_blocks=[*range(161,170), *range(177,181)],
            current_binding_records=190, next_current_binding=str(CURRENT), next_current_binding_sha256=digest(CURRENT),
            subset_registered_release=str(RELEASE), subset_registered_release_sha256=digest(RELEASE), evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B170–B176 exact clean/current comparison for 190 records.',
            next_action='Compare the complete seven blocks, with particular attention to six modal panels and Jam’s spelling and sayings.',
            current_batch_not_yet_integrated=True, prior_B168_B169_integrated_and_credited_once=True,
            native_job_live=False, registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael1975_registered_checkpoint_v1_20261105.md', document_text=doc,
        completed=13820, protected={
            str(REGISTRY): release['registry_sha256'],
            'dk4tool/rom/nds.py': '27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            release['parent']: release['parent_sha256'], package['zip']: package['zip_sha256'],
        },
    )
    print('Saved registered Rafael1975 integration and the B170–B176 current binding.')


if __name__ == '__main__':
    main()
