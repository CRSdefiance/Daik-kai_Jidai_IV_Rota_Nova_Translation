"""Record the complete 186 clean-first drafts while keeping comparison and credit pending."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A = Path('work/analysis')
DRAFTS = [A / f'Rafael_B161_B180_clean_20261105/B{block}_clean_drafts_v1.json' for block in (166,167)]
REGISTRY = Path('translations/release_stack.json')
PREP = A / 'Rafael1674_registered_extended_resume_v1_20261105/registered_preparation.json'
READY = A / 'Rafael_B161_B165_research_final_v1_20261105/research_completion.json'
PACKAGE = A / 'Weekend_testing_package_Rafael1607_20261105/package_verification.json'
RELEASE = A / 'Rafael1607_extended_release_verified_v1_20261105/registered_release_verification.json'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    docs = list(map(load, DRAFTS))
    prep, ready, package, release = map(load, (PREP, READY, PACKAGE, RELEASE))
    assert digest(REGISTRY) == prep['registry_sha256'] and prep['expected_manifest_entries'] == 684
    assert ready['records'] == 67 and ready['all_individual_five_gates_pass']
    assert package['ROM_sha256'] == release['candidate_sha256']
    assert [(d['complete_blocks'], d['records_count']) for d in docs] == [([166], 136), ([167], 50)]
    assert all(d['all_five_gates_pending'] and d['no_current_English_extracted_for_this_intake_before_drafts'] for d in docs)
    drafts = [dict(path=str(p), sha256=digest(p), records=d['records_count']) for p,d in zip(DRAFTS,docs,strict=True)]
    summary = ('Rafael B166 and B167 have 186 independent clean-first drafts across complete exchanges. '
        'The B166 packet preserves the staged Eirene conversation and Charlotte’s Portuguese letter as specific FE leads. '
        'All current comparisons and draft review gates remain pending. B161–B165 has 67 sealed reviews and a qualified 684-entry registered build in progress. '
        'Integrated count remains 13,452 and the Rafael1607 weekend ZIP is preserved.')
    doc = """# Rafael B166 and B167 clean-first checkpoint

All [136 B166 drafts](../work/analysis/Rafael_B161_B180_clean_20261105/B166_clean_drafts_v1.json) cover the royal audience, Claudio and Eirene’s private conversation, the crew’s reactions and the closing expedition and letter. Charlotte’s deliberately halting Portuguese, its phonetic aid and the separate translated reading are distinct source records. The Eirene name heading, alternating staged dialogue and letter need scoped FE layout checks after current comparison.

The [50 B167 drafts](../work/analysis/Rafael_B161_B180_clean_20261105/B167_clean_drafts_v1.json) cover Al’s dismissal and recruitment, including Claudio and Julio’s alternative advice. Qualify Al’s full name against the established name fields before final review. These drafts grant no approval or editorial credit. The 305 B168–B176 records remain at clean inventory, and all 491 B166–B176 current comparisons remain open.

B161–B165 has [67 complete research reviews](editorial_Rafael_B161_B165_research_ready_20261105.md). The registered append passed ten semantic and ordering rejections and ten resume rejections. An initial v6 build reached the manifest writer and failed on the 265-character Windows path. The versioned retry uses a shorter work directory and preserves the first attempt and original guards. The release, exact patch and own startup must pass before credit. The designated main and weekend ZIP are preserved.
"""
    checkpoint(mutation=A/'Rafael_B166_B167_clean_ledger_20261105',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, independently_drafted_records=436,
            independent_draft_blocks=[161,162,163,164,165,166,167,177,178,179,180],
            remaining_clean_meanings_anddrafts=305, current_comparisons=250, remaining_current_comparisons=491,
            partially_drafted_block_166_records=0, complete_next_clean_drafts=drafts, full_intake_not_complete=True),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0, current_batch=summary,
            next_action='Verify Rafael1674 release and own startup, then compare B166 and B167 in source order.',
            native_job_live=False, registered_build_live=True, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B166_B167_clean_checkpoint_20261105.md',
        document_text=doc, completed=13452, protected={str(REGISTRY):prep['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'], release['candidate']:release['candidate_sha256'],
            package['zip']:package['zip_sha256']})
    print('Recorded 186 complete clean-first drafts. No new credit.')


if __name__ == '__main__':
    main()
