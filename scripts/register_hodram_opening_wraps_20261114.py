"""Register the source-reviewed Hodram opening and recruitment dialogue."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_final_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_hodram_opening_wraps_20261114 as replay
from scripts import stage_hodram_opening_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-hodram-opening-wraps-v1-20261114'
CHECK = 'registered_hodram_opening_wraps_and_complete_parent_inverse'
ROOT = Path('out/hodram_opening_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Hodram_Opening_Wrap_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_hodram_opening_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_hodram_opening_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v15.json')
VIEWED = (
    'ba2b2c8d84df83a0447545c4bf4a7108af3adcab2f6e5f1f4feeb98a44f03035',
    '01f964a4d7c66adfd9ac5b0ace14000857e057bc066351539b2c1e14ff054829',
    '757e76720591c39e9eb4bd5ad66a868d6e391e173c2ae80c6d279f38ae121dbf',
    '6e13b2dabcb7013ba27b2f423834065a8ad7292ccb7ef9e51f20c9cf7d0f8250',
    '6f5f89243b453a9b91eea5f420d56e74e21b8a8a8243da3ec6b3a093cb78b4be',
    'e93dc07af58ac739012c8439c8c443cd00fe9468becfd215332aea0db6b17ee5',
    '3badf94e51e2bcd3bd44b58e564ada7a14c0b70840561d848e02f3900e3dcb04',
    '03dc0f377a410650b4fb97c710b4cb7d6a77536b4753af61ecca521cca177d9f',
    'da3c347b90f0b9642ba3facbcc0b4f41cc166ae37a8b259deb9d821553e9248a',
    '6bbc33d7c46dbdd96b980ac106a553a1b0efa61de52b2e1dff6ca8526962ef6e',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Hodram_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 3 and live['verified_following_pages'] == 4",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 37 and len(draft['unchanged_leads']) == 1",
        "{'revision': 3, 'retention': 2}": "{'revision': 36, 'retention': 1}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 77 and proof['checked_original_processor_alignments'] == 304",
        "runtime['captain'] == 0": "runtime['captain'] == 1",
        "b'Rafael Castor'.hex()": "b'Hodram Bergstrom Bergstrom Fleet'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 38 and triage['pending_heuristic_bodies'] == 501",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::prior-registration-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    draft = result[3]
    introduction = next(row for row in draft['records'] if row['id'] == 'DK4_MES_B84_R0165')
    assert introduction['file_path'] == stage.FILE and introduction['source_selector'] == 1
    assert b"I'm Hodram Bergstrom." in bytes.fromhex(introduction['after_native']['expanded_hex'])
    assert draft['unchanged_leads'][0]['id'] == 'DK4_MES_B91_R0031'
    assert set(result[1]['archives']) == {stage.FILE}
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Hodram opening dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes the early Hodram review and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Hodram’s early confrontations and recruitment exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 38 flagged lines across 26 blocks. It revises 36 speeches, reflows Lil’s question without changing her words, and keeps Fernando’s objection intact. Aziza’s account of her father’s sword and Julian Vermeer’s retort use the wording from their parallel Rafael scenes. Hodram’s exchange with Maria fits on one page. The introduction to Emilio keeps Hodram’s first and last name together after the native substitutions.

The B17 speaker at R0146 and R0160 takes a price for releasing Aziza. His original nameplate is ダンディー. “Dandy” preserves the nickname in this exchange and agrees with the catalog label. [Actor 185 inventory](../translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json)

All 77 before-and-after pages were visually checked. The 304 native processor alignments and 37 changed speech boundaries passed. Scoped replay in Hodram’s initialized opening matched three revised pages and four neighboring pages and verified the return to the original departure choice after one fewer page. The original optional scene triggers and hardware remain unvisited. The other changed pages received offline checks. Separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve previous work, including the Market and Sailor Info fixes and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 501 open leads, including 126 from Hodram. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'rafael_final_wraps.pending.json': 'hodram_opening_wraps.pending.json',
        'release_stack_before_rafael_final_wraps.json': 'release_stack_before_hodram_opening_wraps.json',
        "len(manifest['batches']) == 795 and len(manifest['checks']) == 130":
            "len(manifest['batches']) == 796 and len(manifest['checks']) == 131",
        "len(manifest['batches']) == 796 and len(manifest['checks']) == 131":
            "len(manifest['batches']) == 797 and len(manifest['checks']) == 132",
        'registered_manifest_entries=796, passing_release_checks=131': 'registered_manifest_entries=797, passing_release_checks=132',
        'verified_rafael_quest_wraps_predecessor=predecessor, rafael_final_wraps_release=str(REVIEW)':
            'verified_rafael_final_wraps_predecessor=predecessor, hodram_opening_wraps_release=str(REVIEW)',
        'Rafael’s remaining flagged wraps.': 'Hodram’s early confrontations and recruitment exchanges.',
        'rafael_final_wraps_registered_successor_pipeline': 'hodram_opening_wraps_registered_successor_pipeline',
        'prose_revisions=26, justified_retentions=2': 'prose_revisions=36, justified_retentions=2',
        'revised_complete_pages=3, following_original_pages=5, surrounding_identical_frames=3,':
            'revised_complete_pages=3, following_original_pages=4, surrounding_identical_frames=3,',
        'representative_excerpts_initialized_at_Rafael_entry=True': 'representative_excerpts_initialized_at_Hodram_entry=True',
        'Rafael’s remaining flagged wrap decisions are registered.': 'Hodram’s early confrontation and recruitment wrap review is registered.',
        'rafael_final_wraps_retrospective_20261114': 'hodram_opening_wraps_retrospective_20261114',
        'existing_credit_preserved=28, prose_revisions=26, wrap_only_changes=0, exact_retentions=2':
            'existing_credit_preserved=38, prose_revisions=36, wrap_only_changes=1, exact_retentions=1',
        'Preserve the Rafael wrap review release and verification.': 'Preserve the Hodram opening wrap release and verification.',
        '796 entries, 114 accepted layers, 131 checks': '797 entries, 114 accepted layers, 132 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
