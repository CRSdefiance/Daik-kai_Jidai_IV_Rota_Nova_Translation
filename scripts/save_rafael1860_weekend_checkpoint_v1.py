"""Record the exact verified weekend package and the next Rafael editorial batch."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


ANALYSIS = Path('work/analysis')
ROOT = ANALYSIS / 'Rafael1860_extended_release_verified_v1_20261105'
RELEASE = ROOT / 'registered_release_verification.json'
CREDIT = ROOT / 'completion_checkpoint.json'
PACKAGE = ANALYSIS / 'Weekend_testing_package_Rafael1860_20261105/package_verification.json'
PREVIOUS = ANALYSIS / 'Weekend_testing_package_Rafael1607_20261105/package_verification.json'
RESEARCH = ANALYSIS / 'Rafael_B166_B167_research_final_v1_20261105/research_completion.json'
B168 = Path('translations/rafael_B168_contextual_review_v1.json')
B168_PLAN = ANALYSIS / 'Rafael_B168_current1674_20261105/ordinary_plans_v3/automatic_plans.json'
B169 = ANALYSIS / 'Rafael_B161_B180_clean_20261105/B169_clean_drafts_v1.json'
REGISTRY = Path('translations/release_stack.json')


def digest(path):
    return sha(Path(path).read_bytes())


def link(label, path):
    return f'[{label}](../{Path(path).as_posix()})'


def main():
    release, credit, package, previous, research, review, plan, drafts = map(
        load, (RELEASE, CREDIT, PACKAGE, PREVIOUS, RESEARCH, B168, B168_PLAN, B169)
    )
    assert credit['new_credit'] == 186
    assert credit['counts'] == dict(completed=13705, revised=7848, retained=5857)
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (685, 114, 26)
    assert release['only_owned_SC0_blocks_changed'] == [166, 167]
    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']
    assert release['clean_input_patch_byte_exact'] and release['all_eight_registered_final_stages_preserved']
    assert not release['own_registered_startup_pending']
    assert research['all_individual_five_gates_pass']
    assert (research['records'], research['revisions'], research['retentions'], research['body_pages']) == (186, 146, 40, 187)
    assert (research['actual_source_variants'], research['actual_pages'], research['offline_only_source_variants']) == (101, 102, 85)
    assert review['current_ROM_sha256'] == release['parent_sha256']
    assert len(review['records']) == len(plan['records']) == 47 and not plan['failures']
    assert review['all_individual_four_prose_gates_pass'] and review['all_fifth_formatting_gates_pending']
    assert drafts['records_count'] == 68 and drafts['all_five_gates_pending']
    assert package['ROM_sha256'] == release['candidate_sha256'] == package['reconstructed_sha256']
    assert package['ZIP_CRCs_and_member_hashes_pass'] and package['experimental_not_promoted']
    assert digest(package['zip']) == package['zip_sha256'] and digest(previous['zip']) == previous['zip_sha256']
    assert digest(REGISTRY) == release['registry_sha256']
    summary = (
        f"Rafael B166–B167 is registered and credited once (146 revisions, 40 justified retentions). "
        f"Experimental b68173a5 passed 685 stack entries, all 114 accepted layers, eight final stages, 26 release checks, "
        f"byte-for-byte clean-input reconstruction and its own Rafael startup. The {link('Rafael1860 weekend ZIP', package['zip'])} "
        f"adds 253 reviewed records since Rafael1607. Integrated total is 13,705. Next are B168 native display checks "
        f"and the B169 contextual comparison. Earlier packages and the designated main are preserved."
    )
    doc = f"""# Rafael1860 registered checkpoint and weekend package

{link('Download the Rafael1860 weekend ZIP', package['zip'])} for registered combined ROM `{release['candidate_sha256']}`. The ZIP includes the ROM, clean-input patch, manifest, checksums and a Rafael-first testing checklist. It adds 253 contextual reviews since Rafael1607 across B161–B167, with 197 revisions and 56 justified retentions. Package member hashes, the baseline and menu checks and byte-for-byte clean-input patch reconstruction passed. The registered build retains all 114 accepted layers and eight final stages including the ASCII right-bound correction. The candidate's own ordinary cold boot reached Rafael's opening. Physical hardware testing and a full playthrough remain open. {link('Package verification', PACKAGE)}. {link('Release proof', RELEASE)}.

B166–B167 adds 186 records once, with 146 revisions and 40 justified retentions. All 187 pages and 24 public nameplates passed offline and direct visual review. Focused initialized emulator sequences showed 101 speeches, 102 body pages, all 24 headers and all 29 modal pages. The other 85 speeches passed offline checks. The clean Japanese fixture and English checks preserve Arcadius's public nameplate and Eirene's staged name distinction. The original conditional activations remain unvisited. {link('Review and scope', RESEARCH)}.

The B161–B180 intake now has 551 independent clean-first drafts, 483 current-English comparisons and 436 integrated records. Of the 741 inventoried records, 258 current comparisons and 190 clean drafts remain. B168 has 47 contextual decisions (38 revisions and nine retentions) and a 49-page formatter plan. Bind it to the verified successor before fresh native pixels, direct visual, stored, and focused gameplay checks. B169 has 68 clean-first drafts ready for contextual comparison. {link('B168 review', B168)}. {link('B168 formatter plan', B168_PLAN)}. {link('B169 drafts', B169)}.

The designated main and all earlier packages, ROMs and editorial evidence are preserved. The Rafael and tutorial priority continues with the remaining editorial scope, deferred graphics artwork and later technical re-audit tracked separately.
"""
    intake_evidence = [RELEASE, CREDIT, PACKAGE, RESEARCH, B168, B168_PLAN, B169, Path(__file__)]
    checkpoint(
        mutation=ROOT / 'weekend_documentation_checkpoint',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(
            new_credit=0, independently_drafted_records=551, independent_draft_blocks=[*range(161, 170), *range(177, 181)],
            integrated_subbatch_credit=436, integrated_blocks=[*range(161, 168), *range(177, 181)],
            full_intake_not_complete=True, remaining_current_comparisons=258, remaining_clean_meanings_anddrafts=190,
            contextual_comparison_records=483, current_binding_records=47,
            next_current_binding=review['current_ROM'], next_current_binding_sha256=release['parent_sha256'],
            B168_contextual_review=str(B168), B168_formatter_plan=str(B168_PLAN), B169_clean_first_drafts=str(B169),
            subset_registered_release=str(RELEASE), subset_registered_release_sha256=digest(RELEASE),
            evidence={str(path): digest(path) for path in intake_evidence},
        ),
        additional_updates={'editorial_execution_priority_20261104': dict(
            new_credit=0, current_batch='Rafael B168 display gates and B169 contextual comparison.',
            next_action='Bind B168 to Rafael1860, run fresh native and visual checks, then stored and focused display tests. Compare B169 with current English.',
            current_batch_not_yet_integrated=True, prior_B166_B167_integrated_and_credited_once=True,
            native_job_live=False, registered_build_live=False, guide_photos=False,
        )},
        new_entries={'weekend_testing_package_Rafael1860_20261105': dict(
            new_credit=0, package=package['zip'], package_sha256=package['zip_sha256'],
            verification=str(PACKAGE), verification_sha256=digest(PACKAGE), candidate=release['candidate'],
            candidate_sha256=release['candidate_sha256'], previous_package=previous['zip'],
            additional_reviewed_records_since_previous_package=253, main_unchanged=True,
        )},
        summary=summary, document='docs/editorial_Rafael1860_registered_checkpoint_v1_20261105.md',
        document_text=doc, completed=13705,
        protected={
            str(REGISTRY): release['registry_sha256'],
            'dk4tool/rom/nds.py': '27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'],
            release['parent']: release['parent_sha256'],
            package['zip']: package['zip_sha256'],
            previous['zip']: previous['zip_sha256'],
        },
    )
    print('Saved verified Rafael1860 weekend package and editorial handoff.')


if __name__ == '__main__':
    main()