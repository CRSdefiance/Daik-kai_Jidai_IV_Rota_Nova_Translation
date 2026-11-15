"""Register Maria's final flagged story wraps."""

import re
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace
from unicodedata import normalize

from scripts import register_maria_late_wraps_20261114 as parent
from scripts import register_rafael_charlotte_wraps_20261114 as queue_driver
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_maria_final_wraps_20261114 as replay
from scripts import refine_maria_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-maria-final-wraps-v1-20261114'
CHECK = 'registered_maria_final_wraps_and_complete_parent_inverse'
ROOT = Path('out/maria_final_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Maria_Final_Wrap_Review_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_maria_final_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.PRIOR_ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_maria_final_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v25.json')
VIEWED = (
    'c29f364395d3317a14eeead59c9b1bc4bccfa4aedf045c698ce3eb83dcf82a7f',
    '09ff3dd52ff8b4ed4c94de3f1b25963b8e24ae3a023e854d1e6bfe6445585463',
    'aecaf857c4848ef12aa6b4e249cca868e9ed534ecef9f18714c86ff90402bcf0',
    'e5a408ef98d28bdd2b634148b83cd241f0130de708837a7855d344bd706b5838',
    'eafd14da494f3b9ba6e4357fb539438084b2f7cf2fd3579e3e2f41d74de90273',
    'c79632e3352877bf70e74383b921f4d28f5aa43fd4f08d78b9b7b72257acd348',
    'c14135e50227c81afc971ee051bebef0cc398ba3992bd4ac285324803e3a8265',
    '4935c86aa4513ebfade9abb3f4794fb1763e3f71610be53310e4bad5d1e7d18a',
    '583a58452aa53cf63fd07baa658e268b1eb6d08449da7700cab85efd36409586',
    '4d2be6748775f56da5c5c69aee1f2cbc38f950b689d825fd2145fe346acd931f',
    'c136b4de73b52aea574b2808126e008875759c49897f84b85e06bebe80cea4d1',
    '9c36d5807d2e5ea5bd0e591c0a58db4a4b728c55f2c32e249f0306b7ae7fd655',
    '49f1231be5b495670f0335e38ee8547ff75e9700d7538909223aed0c51af7a6d',
    'eabd38e7a9267cf4d9cf0bf7888e820c33102d302ca07d14167c31b3531c6b88',
)

triage_source = checked_text(getsource(queue_driver.refresh_triage), {
    'this_pass_leads_resolved=len(decisions), pending_heuristic_bodies=len(entries),':
        """this_pass_leads_resolved=len(decisions.keys() & keys(old['records'])),
        this_pass_linked_corrections=len(decisions.keys() - keys(old['records'])), pending_heuristic_bodies=len(entries),""",
})
env = queue_driver.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
}
exec(compile(triage_source, __file__ + '::exact-queue-membership-and-linked-corrections', 'exec'), env)
refresh_triage = env['refresh_triage']
reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Maria_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "(live['verified_revised_pages'], live['verified_following_pages']) == (11, 4)",
        "assert len(live['outside_exact_frames']) == 3":
            "assert live['outside_exact_frames'] == [3900, 11450] and live['port_focus_frame']['frame'] == 11700",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 51 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 50, 'retention': 1}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 109 and proof['checked_original_processor_alignments'] == 408",
        "runtime['captain'] == 0": "runtime['captain'] == 3",
        "b'Rafael Castor'.hex()": "b'Maria Li Li Clan'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 49 and triage['pending_heuristic_bodies'] == 0",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Maria-final-wrap-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, live, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert proof['fresh_processor_alignments'] == 12 and proof['reused_processor_alignments'] == 396
    assert all(base.digest(path) == digest for path, digest in proof['exact_render_reuse_dependencies'].items())
    assert live['earned_unlock_verified'] is False and live['verified_revised_utterances'] == 8
    records = {row['id']: row for row in draft['records']}
    assert records['DK4_MES_B209_R0048']['automatic_layout']['lines'][-1] == '-- Jam Jack Ludwyan'
    assert 'the thief might be' in records['DK4_MES_B212_R0105']['english']
    for ident in replay.PAGED_IDS:
        row = records[ident]
        assert len(row['before_native']['pages']) == len(row['after_native']['pages']) == 2
        assert row['automatic_layout']['lines'][3].endswith('.')
    reclaimed = records[replay.RECLAIMED_PAGE_ID]
    assert len(reclaimed['before_native']['pages']) == 2 and len(reclaimed['after_native']['pages']) == 1
    assert live['observed_two_page_records'] == sorted(replay.PAGED_IDS)
    assert live['observed_reclaimed_page'] == replay.RECLAIMED_PAGE_ID
    assert live['port_focus_frame']['port_focus_bounds'] == [208, 242, 252, 258]
    assert live['port_focus_frame']['equal_pixels_outside_focus']
    queue = base.load(TRIAGE)
    assert queue['this_pass_linked_corrections'] == 2 and not queue['records']
    assert set(queue['scanned']) == {f'/data/SC{route}.DK4' for route in range(4)}
    return result


def package_notes(sha, release):
    return f'''# Maria final wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the final flagged story wrap batch and all prior cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. Hardware testing and acceptance for main are pending.
'''


def checkpoint_notes():
    return f'''# Maria’s final flagged story wraps

The [registered review](../{REVIEW.as_posix()}) covers 51 decisions in 39 blocks. It resolves 49 flagged wraps and two related corrections. Fifty lines change wording or punctuation. The villager’s frank explanation in the Ancient City Map exchange keeps its wording with a new wrap. Jam signs on a separate line. Maria’s suspicion about the thief in the New World remains tentative. Yifa’s training advice and the two treasure clues now turn the page after complete sentences. The conversation about the missionaries needs one fewer page.

All 109 before-and-after pages received visual review. The 408 processor alignments, 51 changed command boundaries and 56 targeted tests passed. The emulator replay checked 11 revised pages and four neighboring pages in the new build, including three two-page speeches, the reclaimed page and the return to Hangzhou. The baseline took one more A press. The return screen matched exactly at frame 11450. A later sample differed only in the Port focus indicator. The replay used selected source commands at Maria’s initialized entry with the existing system-only unlock. Original event conditions and hardware remain unvisited. The cumulative cold boot matched six frame holds and 24 protected name getters.

The [cumulative ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the prior releases and ASCII right bound. The [current scan](../{TRIAGE.as_posix()}) has no unreviewed leads in its ASCII progressive story scope across the four routes. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and name review, and representative town and random-scene coverage stay open. Deferred artwork and the older-record technical re-audit remain separate.
'''


def derive():
    return checked_text(parent.derive(), {
        'maria_late_wraps.pending.json': 'maria_final_wraps.pending.json',
        'release_stack_before_maria_late_wraps.json': 'release_stack_before_maria_final_wraps.json',
        "len(manifest['batches']) == 805 and len(manifest['checks']) == 140":
            "len(manifest['batches']) == 806 and len(manifest['checks']) == 141",
        "len(manifest['batches']) == 806 and len(manifest['checks']) == 141":
            "len(manifest['batches']) == 807 and len(manifest['checks']) == 142",
        'registered_manifest_entries=806, passing_release_checks=141': 'registered_manifest_entries=807, passing_release_checks=142',
        'verified_maria_midroute_wraps_predecessor=predecessor, maria_late_wraps_release=str(REVIEW)':
            'verified_maria_late_wraps_predecessor=predecessor, maria_final_wraps_release=str(REVIEW)',
        'Maria’s shop, bargaining, and letter scenes.': 'Maria’s final flagged story wraps.',
        'maria_late_wraps_registered_successor_pipeline': 'maria_final_wraps_registered_successor_pipeline',
        'prose_revisions=41, justified_retentions=1': 'prose_revisions=50, justified_retentions=1',
        'revised_complete_pages=7, following_original_pages=4': 'revised_complete_pages=11, following_original_pages=4',
        'surrounding_identical_frames=3,': 'surrounding_identical_frames=2, additional_return_focus_check=True,',
        'Maria’s shop, bargaining, and letter scenes are registered.': 'Maria’s final flagged story wraps are registered.',
        'maria_late_wraps_retrospective_20261114': 'maria_final_wraps_retrospective_20261114',
        'existing_credit_preserved=42, prose_revisions=41, wrap_only_changes=1, exact_retentions=0':
            'existing_credit_preserved=51, prose_revisions=50, wrap_only_changes=1, exact_retentions=0',
        'Preserve the Maria bargaining and letter release and verification.': 'Preserve the final Maria wrap release and verification.',
        '806 entries, 114 accepted layers, 141 checks': '807 entries, 114 accepted layers, 142 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

