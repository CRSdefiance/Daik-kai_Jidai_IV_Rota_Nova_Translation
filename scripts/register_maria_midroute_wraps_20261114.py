"""Register the contextual wrap review for Maria's discipline, recruitment, and trade scenes."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_maria_opening_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_maria_midroute_wraps_20261114 as replay
from scripts import refine_maria_midroute_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-maria-midroute-wraps-v1-20261114'
CHECK = 'registered_maria_midroute_wraps_and_complete_parent_inverse'
ROOT = Path('out/maria_midroute_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Maria_Midroute_Wrap_Review_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_maria_midroute_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.PRIOR_ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_maria_midroute_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v23.json')
VIEWED = (
    'a4ffd6aadffaf083e204faf959467bcc691d54ff9fcd3ed41a9a8f929efa1fd0',
    '2df10a37d42779cb33c733833cf841ee9f6ef32ed7cd2ac37eaf07f2c3df43a9',
    '998b1a906f03059a78ec7372e3ed1fae0e6a694b4f4cc9a50c27a068eda22560',
    '8116804ada9af4df5dda3e1eb034b4da748ca3d7305c9d9205809cd0642b89ef',
    '012e3275fa4e27456f013f2e29f36d47ce6396e64724f5ffe57614119ba4d6a2',
    '41415fd6a1cd654843b5b31bad2527ccdd59698b3eb5b3b5684c9bd0d3ffd046',
    '303236e26e2516316440388b322d6fbf2c92d0d885085d1d199746399e6f988b',
    '1d54dbe3173cc0efec63774298ade6d8cdafa7fc5961bbb7aae04b2dd3779294',
    'c8b5e2b96d787cc60518a77e2654a19c36a4e95349f2bd4af4923bef3ccc9d15',
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
            "(live['verified_revised_pages'], live['verified_following_pages']) == (4, 5)",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 32 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 31, 'retention': 1}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 65 and proof['checked_original_processor_alignments'] == 256",
        "runtime['captain'] == 0": "runtime['captain'] == 3",
        "b'Rafael Castor'.hex()": "b'Maria Li Li Clan'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 32 and triage['pending_heuristic_bodies'] == 82",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Maria-midroute-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, live, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert proof['fresh_processor_alignments'] == 20 and proof['reused_processor_alignments'] == 236
    assert all(base.digest(path) == digest for path, digest in proof['exact_render_reuse_dependencies'].items())
    assert live['earned_unlock_verified'] is False
    groups = {group['block']: group for group in draft['complete_exchange_references']}
    assert groups[116]['existing_extra_FE_commands'] == [630, 1026]
    before, after = (stage.IlnkContainer.parse(base.NdsImage.open(path).read_file(stage.FILE))
                     for path in (parent.ROM, replay.ROM))
    ian, = [row for row in draft['records'] if row['block'] == 116]
    assert ian['id'] == 'DK4_MES_B116_R0024'
    assert len(ian['before_native']['pages']) == 2 and len(ian['after_native']['pages']) == 1
    offset = ian['current_reference']['offset']
    end = offset + len(bytes.fromhex(ian['target_hex']))
    left, right = before.blocks[116], after.blocks[116]
    assert left[:offset] == right[:offset] and left[end:] == right[end:]
    assert live['observed_Ian_pages_before_after'] == [2, 1]
    queue = base.load(TRIAGE)
    assert {row['file_path'] for row in queue['records']} == {stage.FILE}
    assert min(row['block'] for row in queue['records']) >= 150
    return result


def package_notes(sha, release):
    return f'''# Maria midroute wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes Maria’s next dialogue and wrap batch and the cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. Hardware testing and acceptance for main are pending.
'''


def checkpoint_notes():
    return f'''# Maria’s discipline, recruitment, and trade scenes

The [registered review](../{REVIEW.as_posix()}) resolves 32 flagged lines in 21 story blocks. It revises 31 lines and reflows one with its wording intact. Ian’s account of Maria’s judgment fits on one page. Both original continuation panels in the story he tells remain byte-identical. Cesare’s tutorial ties adding ships to how much the player can buy with a higher market share. Mikhail’s initial peppercorn claim still sets up his correction.

All 65 before-and-after pages received visual review. The 256 processor alignments include 20 fresh checks for five refinements. All 32 changed command boundaries and 56 targeted tests passed. The emulator replay checked four revised utterances, five neighboring utterances, the two-to-one page change and the return to Hangzhou. The baseline needed one more A press to reach the same return screens. The replay used the existing system-only unlock and selected source commands at Maria’s initialized entry. Original conditions and hardware remain unvisited. The cumulative cold boot verified six frame holds and 24 protected name getters.

The [cumulative ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the earlier releases and ASCII right bound. The [wrap queue](../{TRIAGE.as_posix()}) contains 82 remaining Maria leads, beginning with B150–B199. The 279 shared records, remaining UI and name review, and representative town and random-scene coverage stay open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'maria_opening_wraps.pending.json': 'maria_midroute_wraps.pending.json',
        'release_stack_before_maria_opening_wraps.json': 'release_stack_before_maria_midroute_wraps.json',
        "len(manifest['batches']) == 803 and len(manifest['checks']) == 138":
            "len(manifest['batches']) == 804 and len(manifest['checks']) == 139",
        "len(manifest['batches']) == 804 and len(manifest['checks']) == 139":
            "len(manifest['batches']) == 805 and len(manifest['checks']) == 140",
        'registered_manifest_entries=804, passing_release_checks=139': 'registered_manifest_entries=805, passing_release_checks=140',
        'verified_lil_final_wraps_predecessor=predecessor, maria_opening_wraps_release=str(REVIEW)':
            'verified_maria_opening_wraps_predecessor=predecessor, maria_midroute_wraps_release=str(REVIEW)',
        'Maria’s early wrap review.': 'Maria’s discipline, recruitment, and trade scenes.',
        'maria_opening_wraps_registered_successor_pipeline': 'maria_midroute_wraps_registered_successor_pipeline',
        'prose_revisions=41, justified_retentions=12': 'prose_revisions=31, justified_retentions=1',
        'revised_complete_pages=3, following_original_pages=4': 'revised_complete_pages=4, following_original_pages=5',
        'Maria’s early dialogue and wrap review is registered.': 'Maria’s discipline, recruitment, and trade scenes are registered.',
        'maria_opening_wraps_retrospective_20261114': 'maria_midroute_wraps_retrospective_20261114',
        'existing_credit_preserved=53, prose_revisions=41, wrap_only_changes=5, exact_retentions=7':
            'existing_credit_preserved=32, prose_revisions=31, wrap_only_changes=1, exact_retentions=0',
        'Preserve the Maria opening wrap release and verification.': 'Preserve the Maria midroute wrap release and verification.',
        '804 entries, 114 accepted layers, 139 checks': '805 entries, 114 accepted layers, 140 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

