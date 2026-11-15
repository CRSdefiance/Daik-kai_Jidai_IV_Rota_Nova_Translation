"""Register the reviewed early Lil dialogue and its reproducible patch."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_final_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_lil_opening_wraps_20261114 as replay
from scripts import stage_lil_opening_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-lil-opening-wraps-v1-20261114'
CHECK = 'registered_lil_opening_wraps_and_complete_parent_inverse'
ROOT = Path('out/lil_opening_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Lil_Opening_Wrap_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_lil_opening_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_lil_opening_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v18.json')
VIEWED = (
    '51ef29ee69d88135b3ebf13aa87f3f58069682e4dac1da3fef25b9e6b1881620',
    '05fa540c6816e657b525b1e9bc55347c84989ff3f29fbdf7c98a30184413c1d0',
    'dc338f34d9483e5f14d9de84c8ffaadf140d87a9d6e65aa8a2b5e8752680997f',
    'e6625412d358ec3c67f816fa3630a554834e57c8caeaa140e1784eadf7dbc74b',
    '64519f6d1e4715eab43d09b44df9022acdb9ed3b90857b95521fe24c945a188d',
    '14a4e736f2a0a95483b7928b72de6dd3f22329d84a67091ce832b1600f824a38',
    '4c03f77dcc93361dfc366fba46317871214bf9b2e6d0d8ecac67266af68dffd7',
    '5963109a88ae0881e382f553163dec929fbca66b5e22bf34116b47f186210828',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Lil_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 4 and live['verified_following_pages'] == 3",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 27 and len(draft['unchanged_leads']) == 1",
        "{'revision': 3, 'retention': 2}": "{'revision': 23, 'retention': 4}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 57 and proof['checked_original_processor_alignments'] == 224",
        "runtime['captain'] == 0": "runtime['captain'] == 2",
        "b'Rafael Castor'.hex()": "b'Lil Argot Argot Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 28 and triage['pending_heuristic_bodies'] == 347",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Lil-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, _, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert proof['fresh_processor_alignments'] == 4 and proof['reused_processor_alignments'] == 220
    assert all(base.digest(p) == h for p, h in proof['exact_render_reuse_dependencies'].items())
    dandy, = draft['unchanged_leads']
    assert dandy['id'] == 'DK4_MES_B12_R0163' and dandy['current_hex'] == dandy['target_hex']
    rows = {r['id']: r for r in draft['records']}
    assert b'Argot Co. because' in bytes.fromhex(rows['DK4_MES_B12_R0060']['after_native']['expanded_hex'])
    assert b'This is bad, Lil!' in bytes.fromhex(rows['DK4_MES_B26_R0072']['after_native']['expanded_hex'])
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Lil opening dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes the early Lil review and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Lil’s early battles, negotiations, and trade exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 28 flagged lines across 18 blocks. It revises 23 lines, reflows four with their wording intact, and keeps Dandy’s two-million-coin offer byte for byte. The conversation keeps Lil’s one-million counteroffer distinct. Aziza’s account preserves both her ambition to be more like her father and her realization that the sword mattered as a keepsake. Snake’s accusation keeps the company-name substitution and fixes the doubled period. Lil’s Calicut question now fits on one page.

All 57 before-and-after pages were visually checked. The 224 line-specific native alignments and 27 changed command boundaries passed. The final page adjustment ran four fresh alignments and reused 220 exact cases with the same initialized game state, renderer and inputs. Focused replay used original commands at Lil’s initialized entry. It observed four revised and three neighboring pages, including both sides of Aziza’s interrupted thought, the company-name substitution, and the one-page Calicut question. Both replays returned to Amsterdam. The other lines received offline checks. The original event triggers and hardware remain unvisited. A separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve earlier work and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 347 leads left, including 180 for Lil and 167 for Maria. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'hodram_final_wraps.pending.json': 'lil_opening_wraps.pending.json',
        'release_stack_before_hodram_final_wraps.json': 'release_stack_before_lil_opening_wraps.json',
        "len(manifest['batches']) == 798 and len(manifest['checks']) == 133":
            "len(manifest['batches']) == 799 and len(manifest['checks']) == 134",
        "len(manifest['batches']) == 799 and len(manifest['checks']) == 134":
            "len(manifest['batches']) == 800 and len(manifest['checks']) == 135",
        'registered_manifest_entries=799, passing_release_checks=134': 'registered_manifest_entries=800, passing_release_checks=135',
        'verified_hodram_rumor_wraps_predecessor=predecessor, hodram_final_wraps_release=str(REVIEW)':
            'verified_hodram_final_wraps_predecessor=predecessor, lil_opening_wraps_release=str(REVIEW)',
        'Hodram’s remaining flagged wraps.': 'Lil’s early battles, negotiations, and trade exchanges.',
        'hodram_final_wraps_registered_successor_pipeline': 'lil_opening_wraps_registered_successor_pipeline',
        'prose_revisions=66, justified_retentions=2': 'prose_revisions=23, justified_retentions=5',
        'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=4, following_original_pages=3, surrounding_identical_frames=3,',
        'representative_excerpts_initialized_at_Hodram_entry=True': 'representative_excerpts_initialized_at_Lil_entry=True',
        'Hodram’s remaining flagged wrap decisions are registered.': 'Lil’s early dialogue and wrap review is registered.',
        'hodram_final_wraps_retrospective_20261114': 'lil_opening_wraps_retrospective_20261114',
        'existing_credit_preserved=68, prose_revisions=66, wrap_only_changes=2, exact_retentions=0':
            'existing_credit_preserved=28, prose_revisions=23, wrap_only_changes=4, exact_retentions=1',
        'Preserve the Hodram wrap review release and verification.': 'Preserve the Lil opening dialogue release and verification.',
        '799 entries, 114 accepted layers, 134 checks': '800 entries, 114 accepted layers, 135 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
