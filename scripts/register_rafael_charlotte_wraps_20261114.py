"""Register the verified Rafael and Charlotte wrap review on the Sailor Info build."""

from collections import Counter
from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from scripts import register_rafael_early_wraps_20261111 as previous
from scripts import replay_rafael_charlotte_wraps_20261114 as replay
from scripts import stage_rafael_charlotte_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
parent = stage.parent
PROFILE = 'all-routes-rafael-charlotte-wraps-v1-20261114'
CHECK = 'registered_rafael_charlotte_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_charlotte_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_and_Charlotte_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_charlotte_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa_pass.xml'
DOC = Path('docs/editorial_rafael_charlotte_wraps_registered_20261114.md')
TRIAGE = previous.TRIAGE.with_name('current_progressive_wrap_triage_v4.json')
VIEWED = (
    '6d64090d3a59993ef4696a1d4aaa11a432c14240aa6f51642c5474de7a583e1f',
    '30443ebd17efdd4e668c857b7f51c250eef46a47711aa481d3f599db14fb1865',
    '10e9e737c927d93e82ee2dea7ee33eb09cba2e567b9e311fa62e1a62ba1e1be0',
    '356b6dd10fa4653f368f2c98a6aefe2399a420352121df8efc063b21e0f3ff2a',
    'b5be1b2a7a5a7782f6dd18931d8195b2a6582bb477f9dc66c3c78141e76c7ab4',
)


def refresh_triage(draft, setup):
    assert not TRIAGE.exists()
    old = base.load(previous.TRIAGE)
    prior_flags = {(row['file_path'], row['block'], row['offset']): row
                   for row in old['reviewed_current_heuristic_hits']}
    decisions = {(row['file_path'], row['block'], row['current_reference']['offset']): row
                 for row in draft['records'] + draft['unchanged_leads']}
    assert prior_flags.keys().isdisjoint(decisions)
    image = base.NdsImage.open(replay.ROM)
    entries, decided, totals = [], [], {}
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        raw = image.read_file(path)
        counts, rows = previous.scan.scan(path, raw)
        totals[path] = dict(counts, flagged_bodies=len(rows), archive_sha256=stage.sha(raw))
        for row in rows:
            key = path, row['block'], row['offset']
            if key in decisions:
                decision = decisions[key]
                assert row['stored_body_hex'] == decision['target_hex'][2:]
                decided.append(row | dict(registered_review_id=decision['id'], decision=decision['decision']))
            elif key in prior_flags:
                inherited = prior_flags[key]
                assert row['stored_body_hex'] == inherited['stored_body_hex']
                assert row['native_preamble_hex'] == inherited['native_preamble_hex']
                decided.append(row | {field: inherited[field] for field in ('registered_review_id', 'decision')})
            else:
                entries.append(row)
    keys = lambda rows: {(row['file_path'], row['block'], row['offset']) for row in rows}
    assert keys(entries) == keys(old['records']) - decisions.keys()
    by_kind = Counter(reason['kind'] for row in entries for reason in row['findings'])
    base.save(TRIAGE, dict(candidate_sha256=setup['candidate_sha256'], scanned=totals, records=entries,
        findings_by_kind=dict(by_kind), reviewed_current_heuristic_hits=decided,
        this_pass_leads_resolved=len(decisions), pending_heuristic_bodies=len(entries),
        scope='ASCII progressive story dialogue only. Exact registered decisions are removed from the pending lead list.',
        new_editorial_credit=0, full_goal_complete=False))


def verify_inputs():
    old, proof, setup, live, startup, draft, commands = map(base.load,
        (parent.RELEASE, stage.PROOF, replay.SETUP, replay.LIVE, replay.STARTUP, stage.REVIEW, replay.PROOF))
    assert base.digest(stage.REVIEW) == proof['review_sha256'] and base.digest(stage.PROOF) == setup['proof_sha256']
    assert base.digest(stage.CLEAN) == old['clean_input_sha256']
    assert base.digest(parent.MANIFEST) == old['manifest_sha256']
    assert base.digest(parent.ROM) == old['candidate_sha256'] == proof['candidate_sha256']
    assert proof['candidate_sha256'] == live['parent_sha256'] == commands['parent_sha256']
    assert base.digest(replay.ROM) == setup['candidate_sha256'] == live['candidate_sha256']
    assert live['candidate_sha256'] == startup['candidate_sha256'] == commands['candidate_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['original_protected_name_getters']) == 24 and len(startup['exact_matching_frames']) == 6
    assert live['initialized_excerpts_at_Lil_entry'] and live['source_commands_preserved']
    assert live['verified_revised_pages'] == live['verified_following_pages'] == 3
    assert all(tuple(observed) == replay.PLAY_ORDER for observed in live['observed'].values())
    assert len(live['outside_exact_frames']) == 3
    assert len(commands['owned_records']) == len(draft['records']) == 16
    assert len(draft['unchanged_leads']) == 1 and len(draft['deferred_macro_leads']) == 5
    assert Counter(row['decision'] for row in draft['records']) == {'revision': 15, 'retention': 1}
    assert commands['all_command_extents_offsets_branches_and_preambles_exact']
    assert commands['original_catalogue_helper_route_masks_and_entries_verified']
    assert proof['checked_complete_native_pages'] == 34 and proof['checked_original_processor_alignments'] == 136
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
    assert triage['this_pass_leads_resolved'] == 17 and triage['pending_heuristic_bodies'] == 791
    return old, proof, live, draft, tests


def reconstruct(old, proof, draft):
    previous_reconstruct = previous.precedent.reconstruct
    env = previous_reconstruct.__globals__ | dict(parent=parent, stage=stage, replay=replay)
    FunctionType(previous_reconstruct.__code__, env)(old, proof, draft)
    before, after = (base.NdsImage.open(path).read_file(parent.stage.ART) for path in (parent.ROM, replay.ROM))
    assert before == after and stage.sha(after) == old['target_PersonInfo_PXL_sha256']


def package_notes(sha, release):
    return f'''# Rafael and Charlotte wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the six reviewed Rafael exchanges and the Sailor Info stat-label fix. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael and Charlotte's early exchanges

The [registered review](../{REVIEW.as_posix()}) covers 17 wrap leads in six exchanges. Fifteen revise the prose, one keeps the prose with improved breaks and one keeps the exact stored line. Charlotte's account preserves the group's agreement to cross the sea and her response to Rafael's assumption that there is a country to return to. Eirene's replies preserve her public identity and the timing of Claudio's reproach. Maria's condition keeps the term *wako*, which Claudio asks Xien to explain.

All 34 before-and-after pages were visually checked. The 136 processor alignments and all 16 changed command boundaries passed. The initialized emulator replay matched three revised speeches and their following replies, along with three identical surrounding frames. Natural event triggers and hardware remain unvisited. The other records received offline display checks. A separate cumulative cold boot and 56 targeted tests passed.

The [candidate and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the Sailor Info fix, registered market format and ASCII right bound. The [updated wrap scan](../{TRIAGE.as_posix()}) leaves 791 unadjudicated leads, including the five name-substitution lines documented in this review. The ledger still credits 27,697 reviews. The 279 shared keys, remaining UI and name/glyph contexts, and representative town and random-scene visits remain open. Artwork and the older-record technical re-audit stay separate.
'''


def derive():
    source = previous.derive()
    return checked_text(source, {
        'rafael_early_wraps.pending.json': 'rafael_charlotte_wraps.pending.json',
        'release_stack_before_rafael_early_wraps.json': 'release_stack_before_rafael_charlotte_wraps.json',
        'len(manifest[\'batches\']) == 783 and len(manifest[\'checks\']) == 118':
            "len(manifest['batches']) == 785 and len(manifest['checks']) == 120",
        'len(manifest[\'batches\']) == 784 and len(manifest[\'checks\']) == 119':
            "len(manifest['batches']) == 786 and len(manifest['checks']) == 121",
        'registered_manifest_entries=784, passing_release_checks=119': 'registered_manifest_entries=786, passing_release_checks=121',
        'make_xdelta(parent.CLEAN,': 'make_xdelta(stage.CLEAN,',
        'apply_xdelta(parent.CLEAN,': 'apply_xdelta(stage.CLEAN,',
        'storage.PROOF, storage.TRIAGE': 'replay.PROOF, TRIAGE',
        'verified_story_question_wraps_predecessor=predecessor, rafael_early_wraps_release=str(REVIEW)':
            'verified_sailor_stat_labels_predecessor=predecessor, rafael_charlotte_wraps_release=str(REVIEW)',
        'Early Rafael dialogue and pagination review.': 'Rafael and Charlotte early exchange review.',
        'rafael_early_wraps_registered_successor_pipeline': 'rafael_charlotte_wraps_registered_successor_pipeline',
        'prose_revisions=16, justified_retentions=9': 'prose_revisions=15, justified_retentions=2',
        'revised_complete_pages=5, surrounding_identical_frames=3,': 'revised_complete_pages=3, following_original_pages=3, surrounding_identical_frames=3,',
        'Rafael’s early wrap review is registered.': 'Rafael and Charlotte’s early wrap review is registered.',
        'rafael_early_wraps_retrospective_20261111': 'rafael_charlotte_wraps_retrospective_20261114',
        'existing_credit_preserved=25, prose_revisions=16, wrap_only_changes=6, exact_retentions=3':
            'existing_credit_preserved=17, prose_revisions=15, wrap_only_changes=1, exact_retentions=1, pending_name_substitutions=5',
        'Preserve the Rafael early wrap release and verification.': 'Preserve the Rafael and Charlotte wrap release and verification.',
        'Current editorial checkpoint - 2026-11-11': 'Current editorial checkpoint - 2026-11-14',
        '784 entries, 114 accepted layers, 119 checks': '786 entries, 114 accepted layers, 121 checks',
    })


def main():
    precedent = previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

