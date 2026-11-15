"""Register the Rafael seamanship, tavern and recruitment review."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_homecoming_wraps_20261114 as parent
from scripts import replay_rafael_seamanship_wraps_20261114 as replay
from scripts import stage_rafael_seamanship_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-seamanship-wraps-v1-20261114'
CHECK = 'registered_rafael_seamanship_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_seamanship_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Seamanship_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_seamanship_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_seamanship_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v10.json')
VIEWED = (
    '49b6141901909ce1790787b20d348c25fa0811120f490c811a8b4ff9362dd2bc',
    '40a31dc94f81ee7beb38745eb8f6685e5f967cd6abade9269b1705b7e6ae6390',
    '1f3e610b53635e78146e8380fbffd476f654228aa14227a75a6f62e96fedba7e',
    'e7d0b635b87f7c20595b51aa79578402261c4f65c045aaed4fbef19a5fab04e7',
    '01eb8c262285fe273e891e6567ba32f143e103bb6d13e9795564b7c618f40ce2',
    '2c524800af79059f225907396f4a517a1d7e6e0d67aefd1fd409e400c12a372a',
    'a9766a81135b7ee39c1d6d6cd1a301923d2c04bd698b9ee3265c43750b9542da',
    '5310ea773158f393be7e9d8a1b3e5ae21ebfe2c2af62a65e578c2ecfd5e5e30e',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = parent.parent.name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 6 and live['verified_following_pages'] == 4",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 25 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 25}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 60 and proof['checked_original_processor_alignments'] == 200",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 25 and triage['pending_heuristic_bodies'] == 663",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Rafael seamanship wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the ship tutorials and crew dialogue revisions and the previous cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s seamanship and crew exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 25 flagged lines across 11 story blocks. The new wording preserves the market-share threshold for buying a ship, the Lumber Room and shipyard repair distinction, and the square-sail and lateen context. Rafael’s gambling explanation keeps the arithmetic and turn order. The Silla Gold Crown and Sanghyeon retain their established names.

All 60 before-and-after pages were visually checked. All 200 native processor alignments and 25 changed speech boundaries passed. The focused emulator replay verified six revised tutorial pages and four following pages using original commands in Rafael’s initialized opening. The rest of the changed pages received offline checks. Natural scene triggers and hardware remain unvisited. Separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 663 open leads. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_homecoming_wraps.pending.json': 'rafael_seamanship_wraps.pending.json',
        'release_stack_before_rafael_homecoming_wraps.json': 'release_stack_before_rafael_seamanship_wraps.json',
        "len(manifest['batches']) == 790 and len(manifest['checks']) == 125":
            "len(manifest['batches']) == 791 and len(manifest['checks']) == 126",
        "len(manifest['batches']) == 791 and len(manifest['checks']) == 126":
            "len(manifest['batches']) == 792 and len(manifest['checks']) == 127",
        'registered_manifest_entries=791, passing_release_checks=126': 'registered_manifest_entries=792, passing_release_checks=127',
        'verified_rafael_alliance_wraps_predecessor=predecessor, rafael_homecoming_wraps_release=str(REVIEW)':
            'verified_rafael_homecoming_wraps_predecessor=predecessor, rafael_seamanship_wraps_release=str(REVIEW)',
        'Rafael’s homecoming and recruitment exchanges.': 'Rafael’s seamanship and crew exchanges.',
        'rafael_homecoming_wraps_registered_successor_pipeline': 'rafael_seamanship_wraps_registered_successor_pipeline',
        'prose_revisions=25, justified_retentions=3': 'prose_revisions=25, justified_retentions=0',
        'revised_complete_pages=5, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=6, following_original_pages=4, surrounding_identical_frames=3,',
        'Rafael’s homecoming and recruitment wrap review is registered.': 'Rafael’s seamanship and crew wrap review is registered.',
        'rafael_homecoming_wraps_retrospective_20261114': 'rafael_seamanship_wraps_retrospective_20261114',
        'existing_credit_preserved=28, prose_revisions=25, wrap_only_changes=2, exact_retentions=1':
            'existing_credit_preserved=25, prose_revisions=25, wrap_only_changes=0, exact_retentions=0',
        'Preserve the Rafael homecoming wrap release and verification.': 'Preserve the Rafael seamanship wrap release and verification.',
        '791 entries, 114 accepted layers, 126 checks': '792 entries, 114 accepted layers, 127 checks',
    })


def main():
    precedent = parent.parent.name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
