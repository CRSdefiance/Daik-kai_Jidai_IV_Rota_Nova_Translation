"""Register the reviewed Rafael voyage exchanges and tutorial layouts."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_crew_wraps_20261114 as parent
from scripts import replay_rafael_voyage_wraps_20261114 as replay
from scripts import stage_rafael_voyage_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-voyage-wraps-v1-20261114'
CHECK = 'registered_rafael_voyage_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_voyage_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Voyage_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_voyage_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_voyage_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v7.json')
VIEWED = (
    'd99c58085bcb3be8615d9d8ca925ac8a31971b6dee86f06d6b20d35c1f9cfaef',
    '6c2768aa9adc4431e18f77d3e3083562a7b9a5d83ab2248fc46c62b4d420b78e',
    'efdb333f411859b2c4fdd59491f9354105be8f617da5c58e3bc1520290bee667',
    '8f2713d9fac9e6d28cd06cde5f4f35a6f50a27ae32547fddd8477b772dfe5e35',
    'e67b8a41e8d3e4382d577830d4809e47ed4dece13fdfc215d6cf1a110c78bac6',
    'b0f132d00f35c0df72ce522bbee1f658319ed7864f75a9c08397dd65566a05dc',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    source = checked_text(getsource(parent.parent.verify_inputs), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 5 and live['verified_following_pages'] == 3",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 21 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 17, 'retention': 4}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 44 and proof['checked_original_processor_alignments'] == 168",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 21 and triage['pending_heuristic_bodies'] == 734",
    })
    env = vars(parent.parent) | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    return env['verify_inputs']()


def reconstruct(old, proof, draft):
    old_reconstruct = parent.parent.parent.previous.precedent.reconstruct
    env = old_reconstruct.__globals__ | dict(parent=parent, stage=stage, replay=replay)
    FunctionType(old_reconstruct.__code__, env)(old, proof, draft)
    art = parent.parent.parent.parent.stage.ART
    before, after = (base.NdsImage.open(path).read_file(art) for path in (parent.ROM, replay.ROM))
    assert before == after and stage.sha(after) == old['target_PersonInfo_PXL_sha256']


def package_notes(sha, release):
    return f'''# Rafael voyage and tutorial wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the voyage and tutorial review and the previous cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s voyage, trade and naval exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 21 flagged lines across 12 story blocks. Seventeen revise the prose and four keep the wording with revised breaks. The trade advice keeps the link between low investment in Verde and its goods and uses the game’s market-share term. Silveira’s wartime tutorial separates the mechanics into two complete sentences on separate pages. Claudio’s question tag and Rafael’s name in the formal introduction each stay with their phrase.

All 44 before-and-after pages were visually checked. All 168 record-specific native processor alignments and 21 changed speech boundaries passed. Four default name and company controls used the current candidate’s ordinary Rafael startup state. Focused emulator replay at the initialized Rafael opening matched the rescue plea, two trade turns, both naval tutorial pages and three following replies. Natural triggers and hardware remain unvisited. The other changed records received offline display checks. A separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 734 open leads. The ledger holds 27,697 credited reviews. The 279 shared records, remaining UI and names, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_crew_wraps.pending.json': 'rafael_voyage_wraps.pending.json',
        'release_stack_before_rafael_crew_wraps.json': 'release_stack_before_rafael_voyage_wraps.json',
        "len(manifest['batches']) == 787 and len(manifest['checks']) == 122":
            "len(manifest['batches']) == 788 and len(manifest['checks']) == 123",
        "len(manifest['batches']) == 788 and len(manifest['checks']) == 123":
            "len(manifest['batches']) == 789 and len(manifest['checks']) == 124",
        'registered_manifest_entries=788, passing_release_checks=123': 'registered_manifest_entries=789, passing_release_checks=124',
        'verified_rafael_name_wraps_predecessor=predecessor, rafael_crew_wraps_release=str(REVIEW)':
            'verified_rafael_crew_wraps_predecessor=predecessor, rafael_voyage_wraps_release=str(REVIEW)',
        'Rafael’s recruitment, training and crew exchanges.': 'Rafael’s voyage and tutorial exchanges.',
        'rafael_crew_wraps_registered_successor_pipeline': 'rafael_voyage_wraps_registered_successor_pipeline',
        'prose_revisions=23, justified_retentions=8': 'prose_revisions=17, justified_retentions=4',
        'Rafael’s recruitment, training and crew wrap review is registered.': 'Rafael’s voyage and tutorial wrap review is registered.',
        'rafael_crew_wraps_retrospective_20261114': 'rafael_voyage_wraps_retrospective_20261114',
        'existing_credit_preserved=31, prose_revisions=23, wrap_only_changes=6, exact_retentions=2':
            'existing_credit_preserved=21, prose_revisions=17, wrap_only_changes=4, exact_retentions=0',
        'Preserve the Rafael crew wrap release and verification.': 'Preserve the Rafael voyage wrap release and verification.',
        '788 entries, 114 accepted layers, 123 checks': '789 entries, 114 accepted layers, 124 checks',
    })


def main():
    precedent = parent.parent.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

