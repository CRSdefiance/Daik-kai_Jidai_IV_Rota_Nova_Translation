"""Register the early Rafael wrap and prose review on its verified predecessor."""

from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import register_story_question_wraps_20261111 as precedent
from scripts import replay_rafael_early_wraps_20261111 as replay
from scripts import scan_current_progressive_wrap_leads_20261111 as scan
from scripts import stage_rafael_early_wraps_20261111 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
parent = SimpleNamespace(ROM=precedent.ROM, MANIFEST=precedent.MANIFEST, RELEASE=precedent.RELEASE, CLEAN=stage.CLEAN)
PROFILE = 'all-routes-rafael-early-wraps-v1-20261111'
CHECK = 'registered_rafael_early_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_early_wraps_registered_20261111_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Early_Wraps_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261111_rafael_early_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_early_wraps_registered_20261111.md')
TRIAGE = scan.OUTPUT.with_name('current_progressive_wrap_triage_v3.json')
storage = SimpleNamespace(PROOF=replay.PROOF, TRIAGE=TRIAGE)
VIEWED = (
    'aa551abebe1292c8eefc73967de66bcfdcb313c2c1f8981e7529438c9880bcbd',
    '2fdb35e199609fed6043305e8ea5f84d9f1e01026c84be77986d0661c2df40a6',
    '5449124ed047405af38064cf4268db0290b0c22564911ec161f65cffd43ceda2',
    '95160a94ab7bab952f8f3b91d6ac7a67c7012af4adb48bec8637d4cb6b4d7a69',
    '25690549f8e74a631427fc25340cb54bdc0ab6172c38714ca88df903fff75c5e',
    'f3873e4f4444c857080674d5b3bca55ff02cdacfa12049d22a99c5d5bf9e0f10',
    'abe84d63a360e3bada9d4d439d361e6ce28ea1d0d36d2855edf297272d660849',
)


def refresh_triage(draft, setup):
    assert not TRIAGE.exists()
    image = base.NdsImage.open(replay.ROM)
    decisions = {(row['file_path'], row['block'], row['current_reference']['offset']): row
                 for row in draft['records'] + draft['unchanged_leads']}
    entries, decided, totals = [], [], {}
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        raw = image.read_file(path)
        counts, rows = scan.scan(path, raw)
        totals[path] = dict(counts, flagged_bodies=len(rows), archive_sha256=stage.sha(raw))
        for row in rows:
            key = path, row['block'], row['offset']
            if key in decisions:
                decision = decisions[key]
                assert row['stored_body_hex'] == decision['target_hex'][2:]
                decided.append(row | dict(registered_review_id=decision['id'],
                                          decision=decision['decision']))
            else:
                entries.append(row)
    by_kind = Counter(reason['kind'] for row in entries for reason in row['findings'])
    base.save(TRIAGE, dict(candidate_sha256=setup['candidate_sha256'], scanned=totals,
        records=entries, findings_by_kind=dict(by_kind), reviewed_current_heuristic_hits=decided,
        this_pass_leads_resolved=len(decisions), pending_heuristic_bodies=len(entries),
        scope='ASCII progressive story dialogue only. Exact registered decisions are removed from the pending lead list.',
        new_editorial_credit=0, full_goal_complete=False))
    return len(entries)


def verify_inputs():
    old, proof, setup, live, startup, draft, commands = map(base.load,
        (parent.RELEASE, stage.PROOF, replay.SETUP, replay.LIVE, replay.STARTUP, stage.REVIEW, replay.PROOF))
    assert base.digest(stage.REVIEW) == proof['review_sha256'] and base.digest(stage.PROOF) == setup['proof_sha256']
    assert base.digest(parent.CLEAN) == old['clean_input_sha256']
    assert base.digest(parent.MANIFEST) == old['manifest_sha256']
    assert base.digest(parent.ROM) == old['candidate_sha256'] == proof['candidate_sha256']
    assert proof['candidate_sha256'] == live['parent_sha256'] == commands['parent_sha256']
    assert base.digest(replay.ROM) == setup['candidate_sha256'] == live['candidate_sha256']
    assert live['candidate_sha256'] == startup['candidate_sha256'] == commands['candidate_sha256']
    assert startup['cold_boot'] and not startup['savestate']
    assert len(startup['original_protected_name_getters']) == 24
    assert len(startup['exact_matching_frames']) == 6 and startup['complete_deployed_payload_exact']
    assert live['initialized_excerpts_at_Lil_entry'] and live['source_commands_preserved']
    assert live['verified_albuquerque_pages'] == [2, 1] and live['verified_pereira_pages'] == [2, 2]
    assert set(live['observed']['after']) == set(replay.PLAY_ORDER)
    assert set(live['outside_exact_frames']) == {'before', 'after'}
    assert all(len(frames) == 3 for frames in live['outside_exact_frames'].values())
    assert len(commands['owned_records']) == len(draft['records']) == 22
    assert len(draft['unchanged_leads']) == 3
    assert commands['all_command_extents_offsets_branches_and_preambles_exact']
    assert commands['original_catalogue_helper_route_masks_and_entries_verified']
    assert proof['checked_complete_native_pages'] == 53 and proof['checked_original_processor_alignments'] == 200
    assert tuple(base.digest(row['path']) for row in proof['sheets']) == tuple(row['sha256'] for row in proof['sheets']) == VIEWED
    for dependencies in (live['evidence'], startup['evidence'], commands['dependencies']):
        assert all(base.digest(path) == digest for path, digest in dependencies.items())
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    tests = sum(int(row.get('tests', 0)) for row in suites)
    assert tests == 56 and not any(int(row.get(key, 0)) for row in suites for key in ('errors','failures','skipped'))
    if TRIAGE.exists():
        triage = base.load(TRIAGE)
        assert triage['candidate_sha256'] == setup['candidate_sha256'] and triage['this_pass_leads_resolved'] == 25
    else:
        refresh_triage(draft, setup)
    return old, proof, live, draft, tests


reconstruct = FunctionType(precedent.reconstruct.__code__, vars(precedent) | globals())


def package_notes(sha, release):
    return f'''# Rafael early wrap review candidate

The [local ROM](../../{ROM.as_posix()}) carries the early Rafael review and the full previous cumulative build. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. Original command extents, speaker controls and source branches are preserved. Emulator pagination, cold boot and 56 targeted tests passed.
'''


def checkpoint_notes():
    triage = base.load(TRIAGE)
    return f'''# Rafael’s early exchanges reflowed

The [registered review](../{REVIEW.as_posix()}) adjudicates 25 flagged lines across thirteen complete early Rafael exchanges. Six preserve the prose and adjust the breaks. Sixteen also revise the wording, including Claudio’s comeback in the departure tutorial and the port worker’s relay of Albuquerque’s request. Three retain their exact stored text because the existing break keeps the following phrase intact. Each decision is bound to the original Japanese and the previous English.

All 53 before-and-after native pages were viewed. All 200 processor alignments and 22 exact command-boundary and catalogue checks passed. The port worker’s message goes from two pages to one. The allocator distributes eight of its required storage blanks in pairs before an existing break, preserving its original terminator and producing the same pixels as the unpadded text. Pereira’s trade warning still takes two pages and advances after a complete sentence.

Paired emulator replays at Lil’s initialized entry displayed both changed tutorial lines and both pagination cases. Both following replies matched the native masks. The B60 excerpt is from inside a branch in the source. Its original event trigger and hardware remain unvisited. The rest of the revised lines received offline display checks. A separate cumulative cold boot and 56 targeted tests passed.

The [local ROM and byte-exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the previously registered layers. The [updated scan](../{TRIAGE.as_posix()}) leaves {triage["pending_heuristic_bodies"]} unadjudicated heuristic wrap leads. The ledger still credits 27,697 reviews. The 279 shared keys, other UI text, additional name and glyph contexts, and representative town and random-scene coverage remain open. Artwork and the older-record technical re-audit stay separate.
'''


def derive():
    return checked_text(precedent.derive(), {
        'release_stack.question_wraps.pending.json': 'release_stack.rafael_early_wraps.pending.json',
        'editorial_review_current.question_wraps.pending.json': 'editorial_review_current.rafael_early_wraps.pending.json',
        "== 782 and len(manifest['checks']) == 117": "== 783 and len(manifest['checks']) == 118",
        "== 783 and len(manifest['checks']) == 118\n": "== 784 and len(manifest['checks']) == 119\n",
        'release_stack_before_question_wraps.json': 'release_stack_before_rafael_early_wraps.json',
        'for row in draft[\'records\'])': "for row in draft['records'] + draft['unchanged_leads'])",
        '    review = draft | dict(records=records, registered_candidate_sha256=sha,':
            "    retained = [row | dict(review=row['review'] | {'formatting': True}) for row in draft['unchanged_leads']]\n"
            '    review = draft | dict(records=records, unchanged_leads=retained, registered_candidate_sha256=sha,',
        'verified_historical_story_wraps_predecessor=predecessor, story_question_wraps_release=str(REVIEW)':
            'verified_story_question_wraps_predecessor=predecessor, rafael_early_wraps_release=str(REVIEW)',
        'Ten question-wrap revisions and reflows across the four routes.': 'Early Rafael dialogue and pagination review.',
        "manifest['story_question_wraps_registered_successor_pipeline']":
            "manifest['rafael_early_wraps_registered_successor_pipeline']",
        'registered_manifest_entries=783, passing_release_checks=118':
            'registered_manifest_entries=784, passing_release_checks=119',
        'prose_revisions=3, justified_retentions=7': 'prose_revisions=16, justified_retentions=9',
        'revised_complete_pages=2, surrounding_identical_frames=6,':
            'revised_complete_pages=5, surrounding_identical_frames=3,',
        'The ten story question wraps are registered.': 'Rafael’s early wrap review is registered.',
        'story_question_wraps_retrospective_20261111': 'rafael_early_wraps_retrospective_20261111',
        'existing_credit_preserved=10, prose_revisions=3, wrap_only_changes=7':
            'existing_credit_preserved=25, prose_revisions=16, wrap_only_changes=6, exact_retentions=3',
        'Preserve the question-wrap release and verification.':
            'Preserve the Rafael early wrap release and verification.',
        '783 entries, 114 accepted layers, 118 checks': '784 entries, 114 accepted layers, 119 checks',
    })


def main():
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::same-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
