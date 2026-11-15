"""Register the verified question-wrap batch on all four routes."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from scripts import register_historical_story_wraps_20261111 as prior
from scripts import replay_story_question_wraps_20261111 as replay
from scripts import stage_story_question_wraps_20261111 as stage
from scripts import verify_story_question_wraps_20261111 as storage
from scripts.source_locked_derivation_v5118 import checked_text


base=stage.base
parent=SimpleNamespace(ROM=prior.ROM,MANIFEST=prior.MANIFEST,RELEASE=prior.RELEASE,CLEAN=stage.CLEAN)
PROFILE='all-routes-story-question-wraps-v1-20261111'
CHECK='registered_story_question_wraps_and_complete_parent_inverse'
ROOT=Path('out/story_question_wraps_registered_20261111_v1')
ROM=ROOT/'Translation_DS_All_Routes_Question_Wraps_20261111_candidate.nds'
MANIFEST=ROM.with_suffix('.manifest.json')
PACKAGE=Path('releases/all_routes_editorial_20261111_story_question_wraps_candidate')
PATCH,VERIFICATION=PACKAGE/'translation.xdelta',PACKAGE/'verification'
REVIEW,RELEASE=(VERIFICATION/name for name in ('registered_review.json','registered_release_verification.json'))
QA=stage.ROOT/'repository_qa.xml'
DOC=Path('docs/editorial_story_question_wraps_registered_20261111.md')
VIEWED = (
    '2ed032184522968e44d6b053ebe3349b0ef8adb448a3e5bfe8bf99822e8df36a',
    '2c51a6379169eae693f4d5fbfc2b11b4020b53bfa3ef2a8738cd5957bc358f1a',
    '94b815490e6b1b8c6eadadea442f55aab365892c5b1e0a926bb2d496d3ad22cf',
)


def verify_inputs():
    old,proof,setup,live,startup,draft,commands,triage=map(base.load,
        (parent.RELEASE,stage.PROOF,replay.SETUP,replay.LIVE,replay.STARTUP,stage.REVIEW,storage.PROOF,storage.TRIAGE))
    assert base.digest(stage.REVIEW)==proof['review_sha256'] and base.digest(stage.PROOF)==setup['proof_sha256']
    assert base.digest(parent.CLEAN)==old['clean_input_sha256'] and base.digest(parent.MANIFEST)==old['manifest_sha256']
    assert base.digest(parent.ROM)==old['candidate_sha256']==proof['candidate_sha256']==live['parent_sha256']==commands['parent_sha256']
    assert base.digest(replay.ROM)==setup['candidate_sha256']==live['candidate_sha256']==startup['candidate_sha256']==commands['candidate_sha256']==triage['candidate_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and len(startup['original_protected_name_getters'])==24
    assert len(startup['exact_matching_frames'])==6 and startup['complete_deployed_payload_exact']
    assert live['initialized_excerpts_at_Lil_entry'] and live['original_body_plane_only']
    assert set(live['observed'])=={'DK4_MES_B26_R0083','DK4_MES_B103_R0053'}
    assert sum(map(len,live['unchanged_sampled_frames'].values()))==6
    assert len(commands['owned_records'])==10 and commands['all_command_extents_offsets_branches_and_preambles_exact']
    assert commands['original_catalogue_helper_route_masks_and_entries_verified']
    assert proof['checked_complete_native_pages']==20 and proof['checked_original_processor_alignments']==80
    assert tuple(base.digest(row['path']) for row in proof['sheets'])==tuple(row['sha256'] for row in proof['sheets'])==VIEWED
    assert len(triage['records'])==833 and not triage['findings_by_kind'].get('possible_split_question_tag')
    for dependencies in (live['evidence'],startup['evidence'],commands['dependencies']):
        assert all(base.digest(path)==digest for path,digest in dependencies.items())
    suites=list(ElementTree.parse(QA).iter('testsuite'))
    tests=sum(int(row.get('tests',0)) for row in suites)
    assert tests==56 and not any(int(row.get(key,0)) for row in suites for key in ('errors','failures','skipped'))
    return old,proof,live,draft,tests


def reconstruct(old,proof,draft):
    image=base.NdsImage.open(parent.ROM)
    before=prior.prior.files(image)
    for path,raw in stage.prior.transform(image,draft['records']):
        record=proof['archives'][path]
        assert stage.sha(raw)==record['sha256'] and stage.sha(before[path])==record['source_sha256']
        assert raw==Path(record['path']).read_bytes()
        image.replace_file(path,raw)
    after=prior.prior.files(image)
    assert after.keys()==before.keys() and {name for name in after if before[name]!=after[name]}==set(proof['archives'])
    assert bytes(image.rom.save())==replay.ROM.read_bytes()
    prior.prior.verify_runtime(after[stage.ARM],old)
    for path in proof['archives']:
        image.replace_file(path,before[path])
    assert bytes(image.rom.save())==parent.ROM.read_bytes()


def package_notes(sha,release):
    return f'''# Question wraps candidate

The [local ROM](../../{ROM.as_posix()}) contains ten question-wrap corrections across the four story routes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Original speaker selectors, terminators and control flow are preserved. Two emulator excerpts, a separate cold boot and 56 targeted tests passed.
'''


def checkpoint_notes():
    return f'''# Ten story questions reflowed

The [registered review](../{REVIEW.as_posix()}) covers all ten question-break leads from the broader scan. Seven keep the original English and change the wrapping. Three also revise wording, including Lil’s London question and rumor about Clifford. One lead was a true question tag. Nine broke between a negative auxiliary and its subject. Margrete’s unflagged Hodram version already keeps its question together and is retained.

All 20 before-and-after native pages and 80 processor alignment cases passed. All ten revised pages were visually checked. Paired excerpts staged at Lil’s entry verified the complete glyph masks for the London tag and Rafael’s question with selector `00`. Six surrounding frames matched exactly. Eight changes were checked offline this pass. Natural activation of the two tested events and hardware remain unvisited. Separate cumulative cold boot and all 56 targeted tests passed.

The [local ROM and byte-exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the prior layers. The updated [wrap triage](../{storage.TRIAGE.as_posix()}) flags 833 other possible wraps. The same scan flags zero further question-tag splits in its ASCII progressive scope. The dialogue ledger still credits 27,697 reviews. The 279 shared-text keys, other text and name review, and remaining representative gameplay are open. Artwork and the older-record technical re-audit remain separate.
'''


def derive():
    return checked_text(prior.derive(),{
        'release_stack.story_wraps.pending.json':'release_stack.question_wraps.pending.json',
        'editorial_review_current.story_wraps.pending.json':'editorial_review_current.question_wraps.pending.json',
        "== 781 and len(manifest['checks']) == 116":"== 782 and len(manifest['checks']) == 117",
        '(stage.PROOF, storage.PROOF, replay.LIVE, replay.STARTUP, QA)':'(stage.PROOF, storage.PROOF, storage.TRIAGE, replay.LIVE, replay.STARTUP, QA)',
        'release_stack_before_story_wraps.json':'release_stack_before_question_wraps.json',
        'verified_lil_ceramics_predecessor=predecessor, historical_story_wraps_release=str(REVIEW)':'verified_historical_story_wraps_predecessor=predecessor, story_question_wraps_release=str(REVIEW)',
        'Twelve scoped dialogue revisions and reflows across the four routes.':'Ten question-wrap revisions and reflows across the four routes.',
        "manifest['historical_story_wraps_registered_successor_pipeline']":"manifest['story_question_wraps_registered_successor_pipeline']",
        "== 782 and len(manifest['checks']) == 117\n":"== 783 and len(manifest['checks']) == 118\n",
        'registered_manifest_entries=782, passing_release_checks=117':'registered_manifest_entries=783, passing_release_checks=118',
        'prose_revisions=3, justified_retentions=9':'prose_revisions=3, justified_retentions=7',
        'revised_complete_pages=4, surrounding_identical_frames=8,\n                                       natural_Lil_New_Game=True, representative_Carlo_initialized_at_entry=True':
            'revised_complete_pages=2, surrounding_identical_frames=6,\n                                       representative_excerpts_initialized_at_Lil_entry=True',
        'The twelve historical story wraps are registered.':'The ten story question wraps are registered.',
        'historical_story_wraps_retrospective_20261111':'story_question_wraps_retrospective_20261111',
        'existing_credit_preserved=12, prose_revisions=3, wrap_only_changes=9':'existing_credit_preserved=10, prose_revisions=3, wrap_only_changes=7',
        "['carlo_ROMs']":"['fixture_ROMs']",
        'Preserve the historical story wrap release and verification.':'Preserve the question-wrap release and verification.',
        '782 entries, 114 accepted layers, 117 checks':'783 entries, 114 accepted layers, 118 checks',
    })


def main():
    env=vars(prior.prior)|vars(prior)|globals()
    exec(compile(derive(),__file__+'::same-cumulative-publication-contract','exec'),env)
    env['main']()


if __name__=='__main__':
    main()
