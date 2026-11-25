"""Register the five verified early Rafael name-substitution layouts."""

from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import register_rafael_charlotte_wraps_20261114 as parent
from scripts import replay_rafael_name_wraps_20261114 as replay
from scripts import stage_rafael_name_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-name-wraps-v1-20261114'
CHECK = 'registered_rafael_name_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_name_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Name_Wraps_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_name_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_name_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v5.json')
VIEWED = (
    'e17e9847f650f51745fac5fbb7f54c5a78a8e82910105f005ea7110d64b7153d',
    'a893ff4ec6b5d2750db96c6bc74906706a316fc9c6a08675bf3512a782bb975e',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, vars(parent) | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.previous.scan),
})


def verify_inputs():
    old, proof, setup, live, startup, draft, commands = map(base.load,
        (parent.RELEASE, stage.PROOF, replay.SETUP, replay.LIVE, replay.STARTUP, stage.REVIEW, replay.PROOF))
    assert base.digest(stage.REVIEW) == proof['review_sha256'] and base.digest(stage.PROOF) == setup['proof_sha256']
    assert base.digest(stage.CLEAN) == old['clean_input_sha256']
    assert base.digest(parent.MANIFEST) == old['manifest_sha256']
    assert base.digest(parent.ROM) == old['candidate_sha256'] == proof['candidate_sha256'] == live['parent_sha256']
    assert proof['candidate_sha256'] == commands['parent_sha256'] == setup['parent_sha256']
    assert base.digest(replay.ROM) == setup['candidate_sha256'] == live['candidate_sha256']
    assert live['candidate_sha256'] == startup['candidate_sha256'] == commands['candidate_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['original_protected_name_getters']) == 24 and len(startup['exact_matching_frames']) == 6
    assert live['initialized_excerpts_at_Rafael_entry'] and live['source_commands_preserved']
    assert live['verified_revised_pages'] == live['verified_following_pages'] == 5
    assert all(tuple(observed) == replay.PLAY_ORDER for observed in live['observed'].values())
    assert len(live['outside_exact_frames']) == 3
    assert len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']
    assert Counter(row['decision'] for row in draft['records']) == {'revision': 3, 'retention': 2}
    assert commands['all_command_extents_offsets_branches_and_preambles_exact']
    assert commands['original_catalogue_helper_route_masks_and_entries_verified']
    assert proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40
    runtime = proof['native_runtime']
    assert runtime['captain'] == 0 and runtime['candidate_sha256'] == old['candidate_sha256']
    assert base.digest(runtime['startup_proof']) == runtime['startup_proof_sha256']
    assert base.digest(runtime['snapshot']['path']) == runtime['snapshot']['sha256']
    assert base.digest(stage.CAPTURE) == base.load(stage.RUNTIME)['capture_report_sha256']
    defaults = proof['verified_default_name_expansion']['cases']
    assert len(defaults) == 4 and {case['output_hex'] for case in defaults} == {b'Rafael Castor'.hex()}
    assert tuple(base.digest(row['path']) for row in proof['sheets']) == tuple(row['sha256'] for row in proof['sheets']) == VIEWED
    for dependencies in (live['evidence'], startup['evidence'], commands['dependencies']):
        assert all(base.digest(path) == digest for path, digest in dependencies.items())
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    tests = sum(int(row.get('tests', 0)) for row in suites)
    assert tests == 56 and not any(int(row.get(key, 0)) for row in suites for key in ('errors', 'failures', 'skipped'))
    if not TRIAGE.exists():
        refresh_triage(draft, setup)
    triage = base.load(TRIAGE)
    assert triage['candidate_sha256'] == setup['candidate_sha256']
    assert triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786
    return old, proof, live, draft, tests


def reconstruct(old, proof, draft):
    old_reconstruct = parent.previous.precedent.reconstruct
    env = old_reconstruct.__globals__ | dict(parent=parent, stage=stage, replay=replay)
    FunctionType(old_reconstruct.__code__, env)(old, proof, draft)
    art = parent.parent.stage.ART
    before, after = (base.NdsImage.open(path).read_file(art) for path in (parent.ROM, replay.ROM))
    assert before == after and stage.sha(after) == old['target_PersonInfo_PXL_sha256']


def package_notes(sha, release):
    return f'''# Rafael name-substitution wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the five name-substitution updates and the previous cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s five name-substitution lines

The [registered review](../{REVIEW.as_posix()}) resolves the five lines deferred from the previous batch. It revises three lines and rewraps two with their existing prose. Eirene’s apology, Claudio’s half-finished accusation and Charlotte’s thanks keep their original personal address. Rafael’s given and family names appear together when he introduces himself to Xien.

The current parent cold-booted into Rafael’s route. All 40 line-specific native processor cases and four default controls preserved the original substitutions and produced complete glyphs for the default Rafael Castor name. All ten before-and-after pages were inspected. Both scoped emulator runs showed all five lines and their following replies with complete native pixel masks. These runs placed original speech commands in Rafael’s initialized opening. Hardware, natural triggers and custom-name behavior were outside this check. All five source extents and controls, the cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Sailor Info and Market fixes and the ASCII right bound. The [updated wrap scan](../{TRIAGE.as_posix()}) leaves 786 leads, and the ledger still credits 27,697 reviews. The 279 shared records and the remaining UI, speaker-name, glyph, town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_charlotte_wraps.pending.json': 'rafael_name_wraps.pending.json',
        'release_stack_before_rafael_charlotte_wraps.json': 'release_stack_before_rafael_name_wraps.json',
        "len(manifest['batches']) == 785 and len(manifest['checks']) == 120":
            "len(manifest['batches']) == 786 and len(manifest['checks']) == 121",
        "len(manifest['batches']) == 786 and len(manifest['checks']) == 121":
            "len(manifest['batches']) == 787 and len(manifest['checks']) == 122",
        'registered_manifest_entries=786, passing_release_checks=121': 'registered_manifest_entries=787, passing_release_checks=122',
        'verified_sailor_stat_labels_predecessor=predecessor, rafael_charlotte_wraps_release=str(REVIEW)':
            'verified_rafael_charlotte_wraps_predecessor=predecessor, rafael_name_wraps_release=str(REVIEW)',
        'Rafael and Charlotte early exchange review.': 'Rafael’s five early name-substitution lines.',
        'rafael_charlotte_wraps_registered_successor_pipeline': 'rafael_name_wraps_registered_successor_pipeline',
        'prose_revisions=15, justified_retentions=2': 'prose_revisions=3, justified_retentions=2',
        'revised_complete_pages=3, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=5, following_original_pages=5, surrounding_identical_frames=3,',
        'representative_excerpts_initialized_at_Lil_entry=True': 'representative_excerpts_initialized_at_Rafael_entry=True',
        'Rafael and Charlotte’s early wrap review is registered.': 'Rafael’s five name-substitution lines are registered.',
        'rafael_charlotte_wraps_retrospective_20261114': 'rafael_name_wraps_retrospective_20261114',
        'existing_credit_preserved=17, prose_revisions=15, wrap_only_changes=1, exact_retentions=1, pending_name_substitutions=5':
            'existing_credit_preserved=5, prose_revisions=3, wrap_only_changes=2, exact_retentions=0',
        'Preserve the Rafael and Charlotte wrap release and verification.': 'Preserve the Rafael name-wrap release and verification.',
        '786 entries, 114 accepted layers, 121 checks': '787 entries, 114 accepted layers, 122 checks',
    })


def main():
    precedent = parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

