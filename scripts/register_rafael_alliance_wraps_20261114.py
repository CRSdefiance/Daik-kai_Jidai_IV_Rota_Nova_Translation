"""Register Rafael's diplomacy, crew and artifact wrap fixes."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_voyage_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_rafael_alliance_wraps_20261114 as replay
from scripts import stage_rafael_alliance_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-alliance-wraps-v1-20261114'
CHECK = 'registered_rafael_alliance_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_alliance_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Alliance_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_alliance_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_alliance_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v8.json')
VIEWED = (
    'ae204ae867030e9fd25c15328afad18de25660ee20c9a2d18f7721e808354527',
    '82f0a7fc6267960128f16e0ff531f345f68f1a8e86799aab4509ffe97ad06519',
    '8f384b29f2808b1cf603d8990a9679705f8deec5487659bc4db349e973293194',
    '2fcc3b412a9e31c503a165c376b40730e90ef78ff91727746a1f9f461b2185de',
    'd36edd409f834eb34b79348fb1c611f9b334a1940230aeddc616aac52e3ee916',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    source = checked_text(getsource(name_release.verify_inputs), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == live['verified_following_pages'] == 3 and live['previous_revised_pages'] == 4",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 18 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 17, 'retention': 1}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 37 and proof['checked_original_processor_alignments'] == 144",
        "assert len(live['outside_exact_frames']) == 3":
            "assert live['outside_exact_frames'] == [2200] and live['later_tutorial_frames'] == [8500, 8700]",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 18 and triage['pending_heuristic_bodies'] == 716",
    })
    env = vars(name_release) | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


def reconstruct(old, proof, draft):
    precedent = name_release.parent.previous.precedent
    check = precedent.reconstruct
    env = check.__globals__ | dict(parent=parent, stage=stage, replay=replay)
    FunctionType(check.__code__, env)(old, proof, draft)
    art = name_release.parent.parent.stage.ART
    before, after = (base.NdsImage.open(path).read_file(art) for path in (parent.ROM, replay.ROM))
    assert before == after and stage.sha(after) == old['target_PersonInfo_PXL_sha256']


def package_notes(sha, release):
    return f'''# Rafael alliance wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the eighteen reviewed lines and the previous cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s diplomacy, crew and artifact exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 18 flagged lines across 11 story blocks. Seventeen update the prose and one keeps the wording with a revised break. The Kushan Platter explanation fits on one page. Rafael refers to the Portuguese military absorbed by Spain, and Pereira keeps his title and the reason he must obey the Spanish king. Eirene’s account of Charlotte’s feelings keeps both name substitutions.

All 37 before-and-after pages were visually checked. All 144 record-specific processor alignments and 18 changed speech boundaries passed. The focused emulator replay compared the two-to-one page change, both default name-substitution lines and their three following replies. It used original commands at Rafael’s initialized opening. With the same input schedule, the shorter version reached the next original tutorial instruction one press earlier. Both later holds are recorded. Natural triggers, custom names and hardware were outside this replay. A separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 716 open leads, and the ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and names, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_voyage_wraps.pending.json': 'rafael_alliance_wraps.pending.json',
        'release_stack_before_rafael_voyage_wraps.json': 'release_stack_before_rafael_alliance_wraps.json',
        "len(manifest['batches']) == 788 and len(manifest['checks']) == 123":
            "len(manifest['batches']) == 789 and len(manifest['checks']) == 124",
        "len(manifest['batches']) == 789 and len(manifest['checks']) == 124":
            "len(manifest['batches']) == 790 and len(manifest['checks']) == 125",
        'registered_manifest_entries=789, passing_release_checks=124': 'registered_manifest_entries=790, passing_release_checks=125',
        'verified_rafael_crew_wraps_predecessor=predecessor, rafael_voyage_wraps_release=str(REVIEW)':
            'verified_rafael_voyage_wraps_predecessor=predecessor, rafael_alliance_wraps_release=str(REVIEW)',
        'Rafael’s voyage and tutorial exchanges.': 'Rafael’s diplomacy, crew and artifact exchanges.',
        'rafael_voyage_wraps_registered_successor_pipeline': 'rafael_alliance_wraps_registered_successor_pipeline',
        'prose_revisions=17, justified_retentions=4': 'prose_revisions=17, justified_retentions=1',
        'revised_complete_pages=5, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=3, following_original_pages=3, surrounding_identical_frames=1, later_tutorial_holds_differ_by_one_page=True,',
        'Rafael’s voyage and tutorial wrap review is registered.': 'Rafael’s diplomacy and artifact wrap review is registered.',
        'rafael_voyage_wraps_retrospective_20261114': 'rafael_alliance_wraps_retrospective_20261114',
        'existing_credit_preserved=21, prose_revisions=17, wrap_only_changes=4, exact_retentions=0':
            'existing_credit_preserved=18, prose_revisions=17, wrap_only_changes=1, exact_retentions=0',
        'Preserve the Rafael voyage wrap release and verification.': 'Preserve the Rafael alliance wrap release and verification.',
        '789 entries, 114 accepted layers, 124 checks': '790 entries, 114 accepted layers, 125 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

