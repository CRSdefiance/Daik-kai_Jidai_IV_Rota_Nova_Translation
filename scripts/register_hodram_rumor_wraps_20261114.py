"""Register Hodram's reviewed artifact, diplomacy, and crew dialogue."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_opening_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_hodram_rumor_wraps_20261114 as replay
from scripts import stage_hodram_rumor_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-hodram-rumor-wraps-v1-20261114'
CHECK = 'registered_hodram_rumor_wraps_and_complete_parent_inverse'
ROOT = Path('out/hodram_rumor_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Hodram_Rumors_Wrap_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_hodram_rumor_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_hodram_rumor_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v16.json')
VIEWED = (
    '50557a2337bc2c9aca58253972b70455600af765424c9ee478cd1c01d52dc08b',
    '8e628a3a0f40d422f1dfd615e7ced356060619ebe784f7fd35eb9a0ed62cf140',
    '7ac1076889bf9b4d159ff3d08f409cc8dd4112cd38efb83f575f3ff89326a041',
    'd5367153d1609142f929ef2734d7e1be6ce2de584f397202dc873826fb9f7e03',
    'ab322fad56fd2ecd45b1d5f5c4c1caa533539c081cea452fa215137fe052153f',
    '496c285388b727f0d210ea539ce7349cf1c277b2f13d4de0c5ccb95cc6ebd579',
    'd4e6ff510e691b9d835bfab72adf7b8deb54696284037f225b448ae262be168c',
    '3da0c7a616e7d7df13471b01f51e94c57dac3011c511364734572bbbe3423503',
    '5d0b0d4493c18bdfd062d6737cc87221ea1c9fefb85e8f11786bab68415847b2',
    '8f8fc822c65c60d87c0a98dca4f54d3941730703756ad2ca055ed9ea16b90f59',
    'be80ff6c60455e6e99ab33c9943d6ddf2c345b366e39d12e98645f8c4930e5a4',
    '48a84bfb56da4159f705d7ddef66c7ca0807e3eb7e7a4e2bf43fd0a03decbe41',
    '6b907ea62fc2926a598b3206663fa1b99bdd627c61070784b645edea2ce7a08e',
    '46f4b36d24deb251781a437ad6b7679a541e180b5dcbf3d66eb9ea72a845235b',
    'f596bce2eac59fc723ad2b614963ed86a2530193c3636515d96b0cedbaac9e02',
    '28dad6c0fcd95b70749316bc4ec9bf4c12992460a8425e1cf63f19bd6ddc61fd',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Hodram_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 7 and live['verified_following_pages'] == 2",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 58 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 55, 'retention': 3}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 121 and proof['checked_original_processor_alignments'] == 464",
        "runtime['captain'] == 0": "runtime['captain'] == 1",
        "b'Rafael Castor'.hex()": "b'Hodram Bergstrom Bergstrom Fleet'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 58 and triage['pending_heuristic_bodies'] == 443",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, _, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert proof['fresh_processor_alignments'] == 32 and proof['reused_processor_alignments'] == 432
    assert all(base.digest(path) == digest for path, digest in proof['exact_render_reuse_dependencies'].items())
    records = {row['id']: row for row in draft['records']}
    assert b"I'm Hodram." in bytes.fromhex(records['DK4_MES_B142_R0233']['after_native']['expanded_hex'])
    assert 'Proof of Conquest' in records['DK4_MES_B154_R0005']['english']
    assert 'Proof of Supremacy' in records['DK4_MES_B154_R0005']['current_English']
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Hodram artifacts and dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes this Hodram batch and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Hodram’s artifact, diplomacy, and crew exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 58 flagged lines across 33 blocks. It revises 55 speeches and reflows three with their wording intact. Maria’s reply keeps her argument about the causes of conflict and the distinction between the perpetrators and Europeans generally. The Patterned Cloth scene uses “Proof of Conquest,” matching the Japanese term used in the other Proof scenes. Carlo’s remark about noticing illness now refers to health. The Ceremonial Knife and Sun-Crest Sheath fit together on one page, and the stern-sail tutorial starts its second page with the restriction to large ships.

All 121 before-and-after pages were visually checked. The 464 native processor alignments and 58 changed speech boundaries passed. The last revision ran 32 fresh alignments and reused 432 exact checks with the same ROM, initialized state, renderer and input bytes. Scoped replay in Hodram’s initialized opening matched seven revised pages and two neighboring pages, including the two revised page transitions and Hodram’s name. The original optional scene triggers and hardware remain unvisited. The other pages received offline checks. Separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve earlier work, including the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 443 open leads, including 68 from Hodram. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'hodram_opening_wraps.pending.json': 'hodram_rumor_wraps.pending.json',
        'release_stack_before_hodram_opening_wraps.json': 'release_stack_before_hodram_rumor_wraps.json',
        "len(manifest['batches']) == 796 and len(manifest['checks']) == 131":
            "len(manifest['batches']) == 797 and len(manifest['checks']) == 132",
        "len(manifest['batches']) == 797 and len(manifest['checks']) == 132":
            "len(manifest['batches']) == 798 and len(manifest['checks']) == 133",
        'registered_manifest_entries=797, passing_release_checks=132': 'registered_manifest_entries=798, passing_release_checks=133',
        'verified_rafael_final_wraps_predecessor=predecessor, hodram_opening_wraps_release=str(REVIEW)':
            'verified_hodram_opening_wraps_predecessor=predecessor, hodram_rumor_wraps_release=str(REVIEW)',
        'Hodram’s early confrontations and recruitment exchanges.': 'Hodram’s artifact, diplomacy, and crew exchanges.',
        'hodram_opening_wraps_registered_successor_pipeline': 'hodram_rumor_wraps_registered_successor_pipeline',
        'prose_revisions=36, justified_retentions=2': 'prose_revisions=55, justified_retentions=3',
        'revised_complete_pages=3, following_original_pages=4, surrounding_identical_frames=3,':
            'revised_complete_pages=7, following_original_pages=2, surrounding_identical_frames=3,',
        'Hodram’s early confrontation and recruitment wrap review is registered.':
            'Hodram’s artifact, diplomacy, and crew wrap review is registered.',
        'hodram_opening_wraps_retrospective_20261114': 'hodram_rumor_wraps_retrospective_20261114',
        'existing_credit_preserved=38, prose_revisions=36, wrap_only_changes=1, exact_retentions=1':
            'existing_credit_preserved=58, prose_revisions=55, wrap_only_changes=3, exact_retentions=0',
        'Preserve the Hodram opening wrap release and verification.': 'Preserve the Hodram artifact and dialogue wrap release and verification.',
        '797 entries, 114 accepted layers, 132 checks': '798 entries, 114 accepted layers, 133 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
