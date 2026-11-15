"""Register the Rafael port and artifact review."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import register_rafael_seamanship_wraps_20261114 as parent
from scripts import replay_rafael_port_wraps_20261114 as replay
from scripts import stage_rafael_port_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-port-wraps-v1-20261114'
CHECK = 'registered_rafael_port_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_port_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Port_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_port_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_port_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v11.json')
VIEWED = (
    '83830c627a145b7e7d63548924a512a2ab4bd6596fd95d220428ccce447ad367',
    '30a0304d641936409d2d952e4df5149bb95df3c51fbb03b12ae360acdd99604e',
    '27529051e4fc7f5ff5ad3f616064ef337f2c1e9dd983c0a5e64663125ac21b86',
    'a6c857cf94a3deb771b7be7700db7050add48f64d09bcd590167a6633c4a3a47',
    'db721db66fdece5a393d7e029c575081c681e74e2832e53b4e142acaf1e41a3c',
    '5abf89fdb68ef46ed1099821bfc2ad53cf79a837a55e167b94be3ebb77973e43',
    '9a28d019157dce2a4a92a0960c00bcaa96b35af2de6229d528aa5eb864f9c8c9',
    'c75a949bb9833b1d616a1df912280745975742c3f8d932a4adf1c686bc917b37',
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
            "len(commands['owned_records']) == len(draft['records']) == 30 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 27, 'retention': 3}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 62 and proof['checked_original_processor_alignments'] == 240",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 30 and triage['pending_heuristic_bodies'] == 633",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Rafael port wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the port and artifact dialogue revisions and the previous cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s port and artifact exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 30 flagged lines across 20 story blocks. Twenty-seven receive prose revisions and three retain their wording with new breaks. The shop exchanges preserve the bargain and its 9,000-coin price. Yukihisa’s letter keeps the Muramasa report as hearsay, the guard’s address preserves the family-name substitution, and the guildmaster’s question keeps Romance of the Three Kingdoms on one line.

All 62 before-and-after pages were visually checked. The 240 native processor alignments and 30 changed speech boundaries passed. Scoped emulator replay matched six revised pages and three following pages from the artifact letter, the guard and Ian’s exchange using original speech commands in Rafael’s initialized opening. The other changed pages received offline checks. Natural triggers and hardware remain unvisited. Separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 633 open leads. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_seamanship_wraps.pending.json': 'rafael_port_wraps.pending.json',
        'release_stack_before_rafael_seamanship_wraps.json': 'release_stack_before_rafael_port_wraps.json',
        "len(manifest['batches']) == 791 and len(manifest['checks']) == 126":
            "len(manifest['batches']) == 792 and len(manifest['checks']) == 127",
        "len(manifest['batches']) == 792 and len(manifest['checks']) == 127":
            "len(manifest['batches']) == 793 and len(manifest['checks']) == 128",
        'registered_manifest_entries=792, passing_release_checks=127': 'registered_manifest_entries=793, passing_release_checks=128',
        'verified_rafael_homecoming_wraps_predecessor=predecessor, rafael_seamanship_wraps_release=str(REVIEW)':
            'verified_rafael_seamanship_wraps_predecessor=predecessor, rafael_port_wraps_release=str(REVIEW)',
        'Rafael’s seamanship and crew exchanges.': 'Rafael’s port and artifact exchanges.',
        'rafael_seamanship_wraps_registered_successor_pipeline': 'rafael_port_wraps_registered_successor_pipeline',
        'prose_revisions=25, justified_retentions=0': 'prose_revisions=27, justified_retentions=3',
        'revised_complete_pages=6, following_original_pages=4, surrounding_identical_frames=3,':
            'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,',
        'Rafael’s seamanship and crew wrap review is registered.': 'Rafael’s port and artifact wrap review is registered.',
        'rafael_seamanship_wraps_retrospective_20261114': 'rafael_port_wraps_retrospective_20261114',
        'existing_credit_preserved=25, prose_revisions=25, wrap_only_changes=0, exact_retentions=0':
            'existing_credit_preserved=30, prose_revisions=27, wrap_only_changes=3, exact_retentions=0',
        'Preserve the Rafael seamanship wrap release and verification.': 'Preserve the Rafael port wrap release and verification.',
        '792 entries, 114 accepted layers, 127 checks': '793 entries, 114 accepted layers, 128 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
