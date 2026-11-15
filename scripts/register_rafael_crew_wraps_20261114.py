"""Register the reviewed recruitment, training and crew layouts."""

from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import register_rafael_name_wraps_20261114 as parent
from scripts import replay_rafael_crew_wraps_20261114 as replay
from scripts import stage_rafael_crew_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-crew-wraps-v1-20261114'
CHECK = 'registered_rafael_crew_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_crew_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Crew_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_crew_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_crew_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v6.json')
VIEWED = (
    '94c66bfd940669b127b3f1d4468d4ebe62573865a2b350d2958fa5b8828b1a62',
    'bfa05430c1cbec2f1d6b5fd8be6073e737f032b8df10b7beb22c8edcbf8c5ef9',
    '98ca84a1510cddba660bceaf138638ddaffe9dff6b5f59a8b34d7038eca68b5a',
    '3f1dbd075b133507ccdcf15cd226739c240aefeaae9eda0b594a3af7f2779ebf',
    '5e5e83edb3ef83be6f2ff83892c2f652330873f7a6468d98aa727158ab2d6cc6',
    '3014be624c5b573ecb989514b00532a3d2230dc8c5b354e4df5f17c49e2751c3',
    'a400eb2fea8a09a8baa6c320a4998e22b763c3a30a06b7a91f526c98a491556b',
    '98d26b9d6f8454d50f25228606887abbc7ce8a900fc093f3f457f129fb7a0fb6',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.parent.previous.scan),
})


def verify_inputs():
    source = checked_text(getsource(parent.verify_inputs), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 5 and live['verified_following_pages'] == 3",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 29 and len(draft['unchanged_leads']) == 2",
        "{'revision': 3, 'retention': 2}": "{'revision': 23, 'retention': 6}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 64 and proof['checked_original_processor_alignments'] == 248",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 31 and triage['pending_heuristic_bodies'] == 755",
    })
    env = globals().copy()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


def reconstruct(old, proof, draft):
    old_reconstruct = parent.parent.previous.precedent.reconstruct
    env = old_reconstruct.__globals__ | dict(parent=parent, stage=stage, replay=replay)
    FunctionType(old_reconstruct.__code__, env)(old, proof, draft)
    art = parent.parent.parent.stage.ART
    before, after = (base.NdsImage.open(path).read_file(art) for path in (parent.ROM, replay.ROM))
    assert before == after and stage.sha(after) == old['target_PersonInfo_PXL_sha256']


def package_notes(sha, release):
    return f'''# Rafael crew and training wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the crew and training dialogue review and the previous cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s recruitment, training and crew exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 31 flagged lines across 14 story blocks. Twenty-three update the prose, six keep the prose with improved breaks and two keep the exact stored line. Mivor’s stammer and Cristina’s interruption retain the comic timing. Claudio’s introduction keeps the rank, both names and his navigator role. Janus’s tag stays with his question. Julio’s shield rumor turns the page after a complete sentence.

All 64 before-and-after pages were visually checked. All 248 record-specific processor alignments and 29 changed speech boundaries passed. Four default name and company controls ran on the current candidate’s ordinary Rafael startup state. The focused emulator replay compared five revised pages and three original replies on each build. The replay used original commands in the initialized Rafael opening. The remaining dialogue received offline review. Natural event triggers, custom names and hardware remain outside this batch’s replay. The cumulative cold boot and 56 targeted tests passed.

The [test ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 755 open leads. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and names, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_name_wraps.pending.json': 'rafael_crew_wraps.pending.json',
        'release_stack_before_rafael_name_wraps.json': 'release_stack_before_rafael_crew_wraps.json',
        "len(manifest['batches']) == 786 and len(manifest['checks']) == 121":
            "len(manifest['batches']) == 787 and len(manifest['checks']) == 122",
        "len(manifest['batches']) == 787 and len(manifest['checks']) == 122":
            "len(manifest['batches']) == 788 and len(manifest['checks']) == 123",
        'registered_manifest_entries=787, passing_release_checks=122': 'registered_manifest_entries=788, passing_release_checks=123',
        'verified_rafael_charlotte_wraps_predecessor=predecessor, rafael_name_wraps_release=str(REVIEW)':
            'verified_rafael_name_wraps_predecessor=predecessor, rafael_crew_wraps_release=str(REVIEW)',
        'Rafael’s five early name-substitution lines.': 'Rafael’s recruitment, training and crew exchanges.',
        'rafael_name_wraps_registered_successor_pipeline': 'rafael_crew_wraps_registered_successor_pipeline',
        'prose_revisions=3, justified_retentions=2': 'prose_revisions=23, justified_retentions=8',
        'revised_complete_pages=5, following_original_pages=5, surrounding_identical_frames=3,':
            'revised_complete_pages=5, following_original_pages=3, surrounding_identical_frames=3,',
        'Rafael’s five name-substitution lines are registered.': 'Rafael’s recruitment, training and crew wrap review is registered.',
        'rafael_name_wraps_retrospective_20261114': 'rafael_crew_wraps_retrospective_20261114',
        'existing_credit_preserved=5, prose_revisions=3, wrap_only_changes=2, exact_retentions=0':
            'existing_credit_preserved=31, prose_revisions=23, wrap_only_changes=6, exact_retentions=2',
        'Preserve the Rafael name-wrap release and verification.': 'Preserve the Rafael crew wrap release and verification.',
        '787 entries, 114 accepted layers, 122 checks': '788 entries, 114 accepted layers, 123 checks',
    })


def main():
    precedent = parent.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

