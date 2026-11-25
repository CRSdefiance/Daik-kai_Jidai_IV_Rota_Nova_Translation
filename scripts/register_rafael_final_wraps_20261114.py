"""Register the last group of currently flagged Rafael story wraps."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import register_rafael_quest_wraps_20261114 as parent
from scripts import replay_rafael_final_wraps_20261114 as replay
from scripts import stage_rafael_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-rafael-final-wraps-v1-20261114'
CHECK = 'registered_rafael_final_wraps_and_complete_parent_inverse'
ROOT = Path('out/rafael_final_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Rafael_Wrap_Review_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_rafael_final_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_rafael_final_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v14.json')
VIEWED = (
    '67e1f33de4d3dd5f8e22e46301214041cfc4f5157920daf644f883dbc15b1d5a',
    '64de5be15920cb3fda00234c832dd5914f688932684ee19011e892d285556f44',
    '15d8e54f54434e4a86a36c139a47994c69ac1024ddaf75608a779528fe8fcfd4',
    '3eefba2e8f2a418a2177f6164582fed866574c5a4899ca43b9a38f21a13427e5',
    'ba63910e6f1ebcd6b3b59a9f0f4c3a3c20f810e78c4879d145dd6a9023bf9301',
    '511a3d834b4fc2794a146f680706f8d2d12467f5a719f8f6809e896b976f1c08',
    '1a4ebe097dc6fd810dae32b321f27e28b1e4ca8eee552b481db9fb20730b8c28',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 3 and live['verified_following_pages'] == 5",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 26 and len(draft['unchanged_leads']) == 2",
        "{'revision': 3, 'retention': 2}": "{'revision': 26}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 56 and proof['checked_original_processor_alignments'] == 224",
        "b'Rafael Castor'.hex()": "b'Rafael Castor Castor Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 28 and triage['pending_heuristic_bodies'] == 539",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    triage = base.load(TRIAGE)
    assert all(row['file_path'] != stage.FILE for row in triage['records'])
    retained = result[3]['unchanged_leads']
    assert {row['id'] for row in retained} == {'DK4_MES_B235_R0048', 'DK4_MES_B318_R0151'}
    assert all(row['source_Japanese'] and row['current_hex'] == row['target_hex'] for row in retained)
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Rafael wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the final set of flagged Rafael wrap decisions and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Rafael’s remaining flagged wraps

The [registered review](../{REVIEW.as_posix()}) resolves 28 leads across 19 blocks. It revises 26 speeches and retains two records byte for byte. Ian’s letter keeps the sign-off on its own indented line, following the Japanese presentation. The reading keeps Scheherazade’s formal address and preserves Al’s unfinished invocation to Allah. Rafael’s promise to Sakura still depends on his next wine purchase. The Tlaloc Knife exchange keeps the sword test before the object is named.

All 56 before-and-after pages were visually checked. All 224 native processor alignments and 26 changed speech boundaries passed. The scoped replay in Rafael’s initialized opening matched three revised pages and five unchanged pages, including Ian’s signature and Scheherazade’s address. The remaining pages received offline checks. The original scene triggers and hardware remain unvisited. Cumulative cold boot and 56 targeted tests passed.

The apparent Sailor and Retainer mismatch identified in B266 follows the Japanese getters. Actor 154 has 水夫 above dialogue and 配下 in the full catalog. Jean’s subordinate role in B266 is consistent with those labels. The same distinction was already documented for actors 151–159. The catalog result still covers the getter output. [Role-label verification](editorial_shared_nameplates_chooser_checkpoint_20261111.md)

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and Sailor Info fixes and the ASCII right bound. Rafael has no pending leads in the [current wrap scan](../{TRIAGE.as_posix()}). The other routes have 539 flagged bodies. The ledger holds 27,697 credited reviews, and the 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_quest_wraps.pending.json': 'rafael_final_wraps.pending.json',
        'release_stack_before_rafael_quest_wraps.json': 'release_stack_before_rafael_final_wraps.json',
        "len(manifest['batches']) == 794 and len(manifest['checks']) == 129":
            "len(manifest['batches']) == 795 and len(manifest['checks']) == 130",
        "len(manifest['batches']) == 795 and len(manifest['checks']) == 130":
            "len(manifest['batches']) == 796 and len(manifest['checks']) == 131",
        'registered_manifest_entries=795, passing_release_checks=130': 'registered_manifest_entries=796, passing_release_checks=131',
        'verified_rafael_history_wraps_predecessor=predecessor, rafael_quest_wraps_release=str(REVIEW)':
            'verified_rafael_quest_wraps_predecessor=predecessor, rafael_final_wraps_release=str(REVIEW)',
        'Rafael’s quest and village exchanges.': 'Rafael’s remaining flagged wraps.',
        'rafael_quest_wraps_registered_successor_pipeline': 'rafael_final_wraps_registered_successor_pipeline',
        'prose_revisions=34, justified_retentions=1': 'prose_revisions=26, justified_retentions=2',
        'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=3, following_original_pages=5, surrounding_identical_frames=3,',
        'Rafael’s quest and village wrap review is registered.': 'Rafael’s remaining flagged wrap decisions are registered.',
        'rafael_quest_wraps_retrospective_20261114': 'rafael_final_wraps_retrospective_20261114',
        'existing_credit_preserved=35, prose_revisions=34, wrap_only_changes=1, exact_retentions=0':
            'existing_credit_preserved=28, prose_revisions=26, wrap_only_changes=0, exact_retentions=2',
        'Preserve the Rafael quest and village release and verification.': 'Preserve the Rafael wrap review release and verification.',
        '795 entries, 114 accepted layers, 130 checks': '796 entries, 114 accepted layers, 131 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
