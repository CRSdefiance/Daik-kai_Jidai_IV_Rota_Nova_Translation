"""Register the source-reviewed Rafael confrontations and artifact conversations."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import register_rafael_port_wraps_20261114 as parent
from scripts import replay_rafael_history_wraps_20261114 as replay
from scripts import stage_rafael_history_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-history-wraps-v1-20261114'
CHECK = 'registered_rafael_history_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_history_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_History_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_history_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_history_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v12.json')
VIEWED = (
    '06f13970492de07d28ec2c2e7ac041e1ecb8da9e833a45ca69cf4aa7fcfaf0ff',
    '605551d260a98b34c676881013a875fbdff07cf735a31967f4468f5f1793388f',
    '8542e208db63084d71336827fdaa6fbde0afd9a26eeb6df12d446c6b1f960b49',
    '73bf7e87b2ea732bb2091c43e6eac2877c2dc3c7da19411ce529258b4273417c',
    '8c9108b523276a4a8e347f2d3a8c255e19b470bcd45d5c24bdbfc6d7d0f1abef',
    '189ad42c5dc18ca497ed3327dbfb60bba75336fd804ff88d4bffe6d05b4b6a5a',
    '9657bab97b14dd554159c0a9f18b3859940fb01828499ff3ad42cd5243dd410e',
    '4fabbaa187ffbf159ebfd417094693f6e2a0fe77f0ee50cde7f393a66d0c4290',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 5 and live['verified_following_pages'] == 4",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 29 and len(draft['unchanged_leads']) == 2",
        "{'revision': 3, 'retention': 2}": "{'revision': 23, 'retention': 6}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 64 and proof['checked_original_processor_alignments'] == 248",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 31 and triage['pending_heuristic_bodies'] == 602",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Rafael confrontation and artifact dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised dialogue and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s confrontations and artifact conversations

The [registered review](../{REVIEW.as_posix()}) resolves 31 flagged lines in 22 story blocks. Twenty-three receive prose revisions, six retain their wording with new breaks, and two retain the whole record with an individual reason. Clau’s cabin joke fits on one line, Aziza’s decision to leave piracy keeps its original wording, and two of Gerhard’s anecdotes now finish on the first page. The signed letter at B235 R0048 remains in the queue for the letter layout review.

All 64 before-and-after pages were visually checked. All 248 native processor alignments and 29 changed speech boundaries passed. Scoped emulator replay matched five revised pages and four following pages using original speech commands in Rafael’s initialized opening. It verified that Gerhard’s one-page revision proceeds to the same response as the former two-page version. The other changed pages received offline checks. Ordinary event triggers and hardware remain unvisited. Separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 602 open leads. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_port_wraps.pending.json': 'rafael_history_wraps.pending.json',
        'release_stack_before_rafael_port_wraps.json': 'release_stack_before_rafael_history_wraps.json',
        "len(manifest['batches']) == 792 and len(manifest['checks']) == 127":
            "len(manifest['batches']) == 793 and len(manifest['checks']) == 128",
        "len(manifest['batches']) == 793 and len(manifest['checks']) == 128":
            "len(manifest['batches']) == 794 and len(manifest['checks']) == 129",
        'registered_manifest_entries=793, passing_release_checks=128': 'registered_manifest_entries=794, passing_release_checks=129',
        'verified_rafael_seamanship_wraps_predecessor=predecessor, rafael_port_wraps_release=str(REVIEW)':
            'verified_rafael_port_wraps_predecessor=predecessor, rafael_history_wraps_release=str(REVIEW)',
        'Rafael’s port and artifact exchanges.': 'Rafael’s confrontations and artifact conversations.',
        'rafael_port_wraps_registered_successor_pipeline': 'rafael_history_wraps_registered_successor_pipeline',
        'prose_revisions=27, justified_retentions=3': 'prose_revisions=23, justified_retentions=8',
        'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=5, following_original_pages=4, surrounding_identical_frames=3,',
        'Rafael’s port and artifact wrap review is registered.': 'Rafael’s confrontation and artifact wrap review is registered.',
        'rafael_port_wraps_retrospective_20261114': 'rafael_history_wraps_retrospective_20261114',
        'existing_credit_preserved=30, prose_revisions=27, wrap_only_changes=3, exact_retentions=0':
            'existing_credit_preserved=31, prose_revisions=23, wrap_only_changes=6, exact_retentions=2',
        'Preserve the Rafael port wrap release and verification.': 'Preserve the Rafael confrontation and artifact release and verification.',
        '793 entries, 114 accepted layers, 128 checks': '794 entries, 114 accepted layers, 129 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
