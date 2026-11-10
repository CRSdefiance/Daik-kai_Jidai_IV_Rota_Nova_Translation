"""Record the verified Rafael1674 integration and exact next comparison inputs."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A = Path('work/analysis')
ROOT = A / 'Rafael1674_extended_release_verified_v1_20261105'
RELEASE = ROOT / 'registered_release_verification.json'
COMPLETION = ROOT / 'completion_checkpoint.json'
STARTUP = ROOT / 'own_registered_startup_verification.json'
GETTERS = ROOT / 'own_Fernan_name_getter_verification.json'
DRAFTS = A / 'Rafael_B161_B180_clean_20261105/B166_B167_clean_first_v1/current_binding_meanings.json'
CURRENT = A / 'Rafael_B166_B167_current1674_20261105/current_effective.json'
PACKAGE = A / 'Weekend_testing_package_Rafael1607_20261105/package_verification.json'
REGISTRY = Path('translations/release_stack.json')


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    release, credit, startup, getters, drafts, current, package = map(load, (RELEASE, COMPLETION, STARTUP, GETTERS, DRAFTS, CURRENT, PACKAGE))
    assert credit['new_credit'] == 67 and credit['counts'] == dict(completed=13519, revised=7702, retained=5817)
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (684, 114, 26)
    assert release['clean_input_patch_byte_exact'] and release['all_eight_registered_final_stages_preserved']
    assert not release['own_registered_startup_pending']
    assert startup['frames'] == 4001 and startup['actual_captain_getter'] == startup['actual_route_word'] == 0
    assert getters['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
    assert package['ROM_sha256'] == release['parent_sha256']
    assert current['current_ROM_sha256'] == release['candidate_sha256']
    assert current['original_current_catalogue_lookups'] == drafts['meanings'] == 186
    assert [g['block'] for g in current['groups']] == [166,167]
    assert digest(REGISTRY) == release['registry_sha256']
    summary = ('Rafael B161–B165 is registered and credited once, with 51 revisions and 16 justified retentions. '
        'Experimental d06bc3d5 passed all 684 stack entries, 114 accepted layers, eight final stages, 26 release checks, '
        'the exact clean-input patch and its own Rafael startup. Integrated total is 13,519. '
        'All 186 B166–B167 clean-first drafts are bound to current English for the next contextual pass. '
        'Main and the Rafael1607 weekend ZIP are preserved.')
    doc = f"""# Registered Rafael1674 checkpoint

The registered experimental [candidate](../{Path(release['candidate']).as_posix()}) has SHA-256 `{release['candidate_sha256']}`. The [clean-input patch](../{Path(release['patch']).as_posix()}) reconstructed it byte for byte. The manifest retains 684 entries, all 114 accepted layers and all eight final stages including ASCII right bounds. All 26 release checks passed. Only SC0 B161–B165 differ from the previous registered ROM. [Release proof](../{RELEASE.as_posix()}).

The [integrated individual reviews](../translations/rafael_B161_B165_integrated_final_review_v1.json) add 51 revisions and 16 justified retentions once. The ledger now records 13,519 integrated reviews, comprising 7,702 revisions and 5,817 retentions. The candidate's own 4,001-frame cold boot reached Rafael's opening and both original Fernan getters passed. The initialized scene fixture displayed 55 speeches and 56 pages with eight nameplates. The other 12 speeches passed offline checks. Original scene activation, natural story chronology and hardware remain unvisited for this batch. [Research scope](editorial_Rafael_B161_B165_research_ready_20261105.md).

The [B166 and B167 drafts](editorial_Rafael_B166_B167_clean_checkpoint_20261105.md) cover 136 and 50 speeches respectively. The [current-English packet](../{CURRENT.as_posix()}) binds all 186 exact stored and effective bodies. Contextual decisions and fresh display gates are pending. Prioritize the staged Eirene scene and Charlotte's Portuguese, phonetic guide and separate player reading. Another 305 B168–B176 speeches remain at clean inventory. Preserve all other storylines, shared dialogue, names and remaining player-facing prose in scope.

The original Windows build-path failure and the successful shorter-path retry are preserved. The Rafael1607 weekend ZIP still contains the earlier registered candidate. The designated main, accepted layers, artwork deferral, later older-record technical re-audit and all older evidence are preserved.
"""
    paths = [RELEASE,COMPLETION,STARTUP,GETTERS,DRAFTS,CURRENT,Path(__file__)]
    checkpoint(mutation=ROOT/'documentation_checkpoint', batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, integrated_subbatch_credit=250,
            integrated_blocks=[161,162,163,164,165,177,178,179,180],
            full_intake_not_complete=True, remaining_current_comparisons=491, remaining_clean_meanings_anddrafts=305,
            current_binding_records=186, next_current_binding=str(CURRENT), next_current_binding_sha256=digest(CURRENT),
            subset_registered_release=str(RELEASE), subset_registered_release_sha256=digest(RELEASE),
            evidence={str(p):digest(p) for p in paths}),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael B166–B167: 186 clean-first drafts bound to current stored and effective English.',
            next_action='Review the complete B166 audience, private talk and letter, then B167 recruitment against the exact current candidate.',
            current_batch_not_yet_integrated=True, prior_B161_B165_integrated_and_credited_once=True,
            native_job_live=False, registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael1674_registered_checkpoint_v1_20261105.md',
        document_text=doc, completed=13519, protected={str(REGISTRY):release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']:release['canonical_sha256'], release['candidate']:release['candidate_sha256'],
            release['parent']:release['parent_sha256'], package['zip']:package['zip_sha256']})
    print('Saved Rafael1674 registered checkpoint and exact B166–B167 current handoff.')


if __name__ == '__main__':
    main()
