"""Register the reviewed Rafael quest assignments and village exchanges."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_history_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_rafael_quest_wraps_20261114 as replay
from scripts import stage_rafael_quest_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-quest-wraps-v1-20261114'
CHECK = 'registered_rafael_quest_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_quest_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Quests_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_quest_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_quest_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v13.json')
VIEWED = (
    '4a89d1564b0037e3483b580a0348e19a8ebf7f0192074cf1b17558ff382dd051',
    'b967a8cef35127319b160852f588c628c666c7702eb65d348880befc4e159410',
    '400ff78f13cefa7acf9a0434160adbc5c1d58e1c002c4fac127d394f74a654f4',
    'd311297bfb1be0204b25f1e4e993b2335746041f8adcee553e65cf2f9da45f9a',
    'cb835bdab6f97a1c44ec4c1e4cfa2fd9db2c10161ddbcf9eae394e74cbf9332d',
    '94afa78e428fede454bf0ee9197171b145b2802d7cb22f48c993060ed394d398',
    'f60e386aaf090cbf177c2c0deec1b7b69e963516710cc8d979f8f95d8f680be5',
    'bc796c29b814c671b960e3f938a67b84956294556fd8e1dd2d964de9a6063fff',
    '9892b1ab1c52765cae0f2c064f7e05a8c5d67a86fd53be93fed889a9a1550e43',
    '05acafbe9073dde5ce1f3b786bf3a01a29c82acb7e67d57f6aa26d20726ff9f2',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 6 and live['verified_following_pages'] == 3",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 35 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 34, 'retention': 1}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 74 and proof['checked_original_processor_alignments'] == 280",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 35 and triage['pending_heuristic_bodies'] == 567",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Rafael quest and village dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised dialogue and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s quest and village exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 35 flagged lines across 24 story blocks. Thirty-four receive prose revisions and one retains the wording with new breaks. The guildmasters’ reports distinguish rumors and assignments, and the parallel recovery scenes in B306 and B308 now use identical English. In B309 the second page starts with the map clue after the first page explains the cliff and village. In B286 the second page retains the guildmaster’s closing appeal as a complete sentence after the warning.

All 74 before-and-after pages, 280 native processor alignments, and 35 changed speech boundaries were checked. Scoped replay in Rafael’s initialized opening matched six revised pages and three neighboring pages from the Sofala escort, the boy’s recovery, and the cliff directions. The remaining pages received offline checks. The original quest triggers and hardware remain unvisited. Cumulative cold boot and 56 targeted tests passed.

The B266 exchange surfaced a role-label inconsistency for actor 154. The clean table has 配下, and R0008, R0045 and R0049 establish that the speaker takes Jean Ramusio’s orders. The progressive nameplate is “Sailor” and the full-catalogue label is “Retainer.” The other entries in the 151–159 group share those outputs and need contextual comparison before any role change. The [actor inventory](../translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json) binds the exact strings and getter references.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 567 open leads, including 28 from Rafael. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_history_wraps.pending.json': 'rafael_quest_wraps.pending.json',
        'release_stack_before_rafael_history_wraps.json': 'release_stack_before_rafael_quest_wraps.json',
        "len(manifest['batches']) == 793 and len(manifest['checks']) == 128":
            "len(manifest['batches']) == 794 and len(manifest['checks']) == 129",
        "len(manifest['batches']) == 794 and len(manifest['checks']) == 129":
            "len(manifest['batches']) == 795 and len(manifest['checks']) == 130",
        'registered_manifest_entries=794, passing_release_checks=129': 'registered_manifest_entries=795, passing_release_checks=130',
        'verified_rafael_port_wraps_predecessor=predecessor, rafael_history_wraps_release=str(REVIEW)':
            'verified_rafael_history_wraps_predecessor=predecessor, rafael_quest_wraps_release=str(REVIEW)',
        'Rafael’s confrontations and artifact conversations.': 'Rafael’s quest and village exchanges.',
        'rafael_history_wraps_registered_successor_pipeline': 'rafael_quest_wraps_registered_successor_pipeline',
        'prose_revisions=23, justified_retentions=8': 'prose_revisions=34, justified_retentions=1',
        'revised_complete_pages=5, following_original_pages=4, surrounding_identical_frames=3,':
            'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,',
        'Rafael’s confrontation and artifact wrap review is registered.': 'Rafael’s quest and village wrap review is registered.',
        'rafael_history_wraps_retrospective_20261114': 'rafael_quest_wraps_retrospective_20261114',
        'existing_credit_preserved=31, prose_revisions=23, wrap_only_changes=6, exact_retentions=2':
            'existing_credit_preserved=35, prose_revisions=34, wrap_only_changes=1, exact_retentions=0',
        'Preserve the Rafael confrontation and artifact release and verification.': 'Preserve the Rafael quest and village release and verification.',
        '794 entries, 114 accepted layers, 129 checks': '795 entries, 114 accepted layers, 130 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
