"""Register the Rafael homecoming, tavern and recruitment review."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_alliance_wraps_20261114 as parent
from scripts import replay_rafael_homecoming_wraps_20261114 as replay
from scripts import stage_rafael_homecoming_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-homecoming-wraps-v1-20261114'
CHECK = 'registered_rafael_homecoming_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_homecoming_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Homecoming_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_homecoming_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_homecoming_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v9.json')
VIEWED = (
    '6c336fe579c7ac146fbf26c359600ca681a37ef022556af6a0e3c64858798b46',
    'f017cfa6be207ad944ccb61c44de51761346b3e599409009daed076e1b18dbb3',
    'af422a6b5d72d169d6c30289f6ee3c3fa39b7ac8a4f96724c4c1836517c40a31',
    '945570449f8e02e9ad48e1cf67917f7e12647b062e31af15ca1f819cabb1c08a',
    'f59ad93ebeb3bcf04a3d24ca941f27c82bd72a1f85bf9136e412523d088e62fe',
    '82a52b8210a58708c7045efe648883792f2262070c06279b1cd0a530ba7f0e5d',
    'e889a8b38bdd4a372394261b93ebc3e3651a6b935e35f1d64957e5d5b12e7442',
    '31a83bca2d1dd1ac49f903ee9ee1dff5552b70e956a0c33ffc10668b9e9ad7e7',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = parent.name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 5 and live['verified_following_pages'] == 3",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 27 and len(draft['unchanged_leads']) == 1",
        "{'revision': 3, 'retention': 2}": "{'revision': 25, 'retention': 2}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 60 and proof['checked_original_processor_alignments'] == 224",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 28 and triage['pending_heuristic_bodies'] == 688",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Rafael homecoming wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the homecoming, recruitment and tavern revisions and the previous cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s homecoming and recruitment exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 28 flagged lines across eight source blocks. Twenty-five revise the wording, two reflow their retained prose and one keeps its exact stored layout. The royal audiences distinguish petitioning the Pope from the report of his support. The appointment keeps the viceroy title and the extent of the Estado. The crew’s reactions to Charlotte’s Portuguese letter and the tavern and recruitment replies were reviewed with their surrounding turns.

All 60 before-and-after pages were inspected. All 224 alignments and 27 changed command boundaries passed. Scoped emulator replay verified five revised pages and three following replies using original commands in Rafael’s initialized opening. Natural scene triggers and hardware remain unvisited. The remaining pages received offline checks. Separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 688 open leads. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_alliance_wraps.pending.json': 'rafael_homecoming_wraps.pending.json',
        'release_stack_before_rafael_alliance_wraps.json': 'release_stack_before_rafael_homecoming_wraps.json',
        "len(manifest['batches']) == 789 and len(manifest['checks']) == 124":
            "len(manifest['batches']) == 790 and len(manifest['checks']) == 125",
        "len(manifest['batches']) == 790 and len(manifest['checks']) == 125":
            "len(manifest['batches']) == 791 and len(manifest['checks']) == 126",
        'registered_manifest_entries=790, passing_release_checks=125': 'registered_manifest_entries=791, passing_release_checks=126',
        'verified_rafael_voyage_wraps_predecessor=predecessor, rafael_alliance_wraps_release=str(REVIEW)':
            'verified_rafael_alliance_wraps_predecessor=predecessor, rafael_homecoming_wraps_release=str(REVIEW)',
        'Rafael’s diplomacy, crew and artifact exchanges.': 'Rafael’s homecoming and recruitment exchanges.',
        'rafael_alliance_wraps_registered_successor_pipeline': 'rafael_homecoming_wraps_registered_successor_pipeline',
        'prose_revisions=17, justified_retentions=1': 'prose_revisions=25, justified_retentions=3',
        'revised_complete_pages=3, following_original_pages=3, surrounding_identical_frames=1, later_tutorial_holds_differ_by_one_page=True,':
            'revised_complete_pages=5, following_original_pages=3, surrounding_identical_frames=3,',
        'Rafael’s diplomacy and artifact wrap review is registered.': 'Rafael’s homecoming and recruitment wrap review is registered.',
        'rafael_alliance_wraps_retrospective_20261114': 'rafael_homecoming_wraps_retrospective_20261114',
        'existing_credit_preserved=18, prose_revisions=17, wrap_only_changes=1, exact_retentions=0':
            'existing_credit_preserved=28, prose_revisions=25, wrap_only_changes=2, exact_retentions=1',
        'Preserve the Rafael alliance wrap release and verification.': 'Preserve the Rafael homecoming wrap release and verification.',
        '790 entries, 114 accepted layers, 125 checks': '791 entries, 114 accepted layers, 126 checks',
    })


def main():
    precedent = parent.name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

