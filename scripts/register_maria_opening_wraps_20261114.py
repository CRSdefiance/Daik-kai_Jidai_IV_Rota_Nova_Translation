"""Register the contextual wrap review for the early Maria scenes."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_lil_final_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_maria_opening_wraps_20261114 as replay
from scripts import refine_maria_opening_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-maria-opening-wraps-v1-20261114'
CHECK = 'registered_maria_opening_wraps_and_complete_parent_inverse'
ROOT = Path('out/maria_opening_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Maria_Opening_Wrap_Review_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_maria_opening_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.PRIOR_ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_maria_opening_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v22.json')
VIEWED = (
    '13bba4877c29ac36b10ae797ea977a3217dbf3fb428039545b1516f6a6546940',
    '5f9c9c17de0d053a42226ca7c1e152b50bf7732f5634c8788ae47e184391ffd9',
    '9334da4c16ddd8ade6b2eacd87b5e49ded48108596eb364e3c4eb4d17417c66f',
    'ea380696970b3a262b3c2630652461883dad7aa413df6217c36788dc88eab2c5',
    'd2fe4fe6132c4e4b53aa64a8d39e1b5fe03912c24c0cdd1d55edab6e9549bb98',
    '5831227ef3c0b749feb7cc17c98067bed9abc0cb12aba9e058aedbe6aede0f32',
    '4436f6377d3b659fcdf1003ba89fc1e7fae6a85f76d0dae81a2e7f958623db0d',
    '84d490b91f4c9d48c234c8c2a46cf99683ab288275610f6c8b52ed49e487fe16',
    '1d08b6518e19872061e9f83c491077bb36fed6101145edd01146b96e63d5acba',
    '7e2909a2da75f822e02b97b63192b147a5cd223f258e2b826264bb1c4b868826',
    '035c495abab43fba2dca282cf47f20e90fd27def95f1b54e17d6a4e2ccd4c62f',
    '9c0c1ce4308b22e5ff6bac434b9c7144c0d5ecddd4ec93967e53522712058b9f',
    '0fd68bfb0021a1c0f47799aa92b6e3fea512b94932f670a3bfb0ecfa48b73fa0',
    '8fc79fb6deaa34601b8a5837485ad30c6686597d7d813c71c2ce8b38cc179d6b',
)

refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})
reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Maria_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "(live['verified_revised_pages'], live['verified_following_pages']) == (3, 4)",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 46 and len(draft['unchanged_leads']) == 7",
        "{'revision': 3, 'retention': 2}": "{'revision': 41, 'retention': 5}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 106 and proof['checked_original_processor_alignments'] == 424",
        "runtime['captain'] == 0": "runtime['captain'] == 3",
        "b'Rafael Castor'.hex()": "b'Maria Li Li Clan'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 53 and triage['pending_heuristic_bodies'] == 114",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Maria-opening-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, live, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert proof['fresh_processor_alignments'] == 12 and proof['reused_processor_alignments'] == 412
    assert all(base.digest(path) == digest for path, digest in proof['exact_render_reuse_dependencies'].items())
    assert live['earned_unlock_verified'] is False
    groups = {group['block']: group for group in draft['complete_exchange_references']}
    assert groups[87]['existing_extra_FE_commands'] == [712]
    before, after = (stage.IlnkContainer.parse(base.NdsImage.open(path).read_file(stage.FILE))
                     for path in (parent.ROM, replay.ROM))
    assert before.blocks[87] == after.blocks[87]
    queue = base.load(TRIAGE)
    assert {row['file_path'] for row in queue['records']} == {stage.FILE}
    assert min(row['block'] for row in queue['records']) >= 100
    return result


def package_notes(sha, release):
    return f'''# Maria opening wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the early Maria review and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. Hardware testing and acceptance for main are pending.
'''


def checkpoint_notes():
    return f'''# Maria’s opening wrap review

The [registered review](../{REVIEW.as_posix()}) covers 53 flagged lines in 32 story blocks. It revises 41, reflows five with their existing wording and retains seven exactly. Aziza answers Yukihisa’s charge of stooping to piracy in his terms. Janus’s plain account of his ship and repair skills matches his parallel recruitment exchange. Rafael’s compliment and his aside to Claudio each occupy a complete line. Both existing riddle panels and their answer branches remain byte-identical.

All 106 before-and-after pages received visual review. The native checks covered 424 processor alignments including 12 fresh alignments for three refinements. All 46 changed command boundaries and 56 targeted tests passed. Two controlled emulator runs compared seven pages, including the Li Clan substitution and four original replies, and the return to Hangzhou. These runs used original commands in Maria’s initialized opening with the existing system-only unlock. The other lines received offline checks. Original triggers and hardware remain unvisited. The cumulative cold boot verified six matching frames and 24 protected name getters.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the previous releases and the ASCII right bound. The [wrap queue](../{TRIAGE.as_posix()}) has 114 pending Maria leads. Begin with B100–B149, matching B116 by its registered command boundaries. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage stay open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'lil_final_wraps.pending.json': 'maria_opening_wraps.pending.json',
        'release_stack_before_lil_final_wraps.json': 'release_stack_before_maria_opening_wraps.json',
        "len(manifest['batches']) == 802 and len(manifest['checks']) == 137":
            "len(manifest['batches']) == 803 and len(manifest['checks']) == 138",
        "len(manifest['batches']) == 803 and len(manifest['checks']) == 138":
            "len(manifest['batches']) == 804 and len(manifest['checks']) == 139",
        'registered_manifest_entries=803, passing_release_checks=138': 'registered_manifest_entries=804, passing_release_checks=139',
        'verified_lil_late_wraps_predecessor=predecessor, lil_final_wraps_release=str(REVIEW)':
            'verified_lil_final_wraps_predecessor=predecessor, maria_opening_wraps_release=str(REVIEW)',
        'Lil’s final wrap review.': 'Maria’s early wrap review.',
        'lil_final_wraps_registered_successor_pipeline': 'maria_opening_wraps_registered_successor_pipeline',
        'prose_revisions=49, justified_retentions=5': 'prose_revisions=41, justified_retentions=12',
        'revised_complete_pages=4, following_original_pages=4': 'revised_complete_pages=3, following_original_pages=4',
        'representative_excerpts_initialized_at_Lil_entry': 'representative_excerpts_initialized_at_Maria_entry',
        'Lil’s final flagged wrap review is registered.': 'Maria’s early dialogue and wrap review is registered.',
        'lil_final_wraps_retrospective_20261114': 'maria_opening_wraps_retrospective_20261114',
        'existing_credit_preserved=54, prose_revisions=49, wrap_only_changes=5, exact_retentions=0':
            'existing_credit_preserved=53, prose_revisions=41, wrap_only_changes=5, exact_retentions=7',
        'Preserve the Lil final wrap release and verification.': 'Preserve the Maria opening wrap release and verification.',
        '803 entries, 114 accepted layers, 138 checks': '804 entries, 114 accepted layers, 139 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

