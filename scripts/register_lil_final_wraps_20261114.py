"""Register the last batch of flagged wraps on Lil's route."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_lil_late_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_lil_final_wraps_20261114 as replay
from scripts import refine_lil_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-lil-final-wraps-v1-20261114'
CHECK = 'registered_lil_final_wraps_and_complete_parent_inverse'
ROOT = Path('out/lil_final_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Lil_Wrap_Review_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_lil_final_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.PRIOR_ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_lil_final_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v21.json')
PAGE_COUNT = 110
VIEWED = (
    '7fb97f264eaa496f12ba014460e7c139eb07efee5d68f7aec03b944168d1a9ce',
    '4656526f6b0983991d2af73db7bb1ee94cb61a8c5b0b168db4aef1ac7a693c75',
    'd157e9f6aeb556db97848d34d8fdac2e5bd960f294d300da371638bc6f2a99a6',
    'e073b6724c3ecd964c4016f33461ee220365e0004f9d799227d7a8de9ab2632f',
    '7c8643c87b461444bee8453f82ca6debec77c4b21854c911767321db91a7625c',
    'fd290b504775d499335a7b56af95975ff39f3bccda77ce6ca12be096cd3699e9',
    '36b8e8edbc135c1a4048c2d573fae494cee6c2508d1cfb559db04f6515c96efa',
    '192457558b576324687363c55933a29240addae0d17515e7c0773cf18699f302',
    '2e4ee878b162e0afba1c9f0b57086ebbd4b66c09dd2192efd33c298e28059b91',
    'fba5088eee7d3a47e8a92eea31dbfa9d5e9a8f5223baa3f125afa8fe25870767',
    '75bb9c1ff33c855b52d91dc6517dd58a1660f4805dc273db1a9439ccc6e4e7e8',
    '96c01a11d07b51fd6cfb5bbcbab76e5192d1dc0f11db00c1f8f5171faab03cb4',
    '153ddec8f4b329b955bba6c15bf77bd52358777010f356f4c19eae7f89a7785d',
    '5256107ce282206384e286dae06ea208aa77e8220b8cdc808c0638dc21a10aff',
)

refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Lil_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == live['verified_following_pages'] == 4",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 54 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 49, 'retention': 5}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == PAGE_COUNT and proof['checked_original_processor_alignments'] == 432",
        "runtime['captain'] == 0": "runtime['captain'] == 2",
        "b'Rafael Castor'.hex()": "b'Lil Argot Argot Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 54 and triage['pending_heuristic_bodies'] == 167",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Lil-final-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, _, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert proof['fresh_processor_alignments'] == 20 and proof['reused_processor_alignments'] == 412
    assert all(base.digest(p) == h for p, h in proof['exact_render_reuse_dependencies'].items())
    queue = base.load(TRIAGE)
    assert queue['this_pass_linked_corrections'] == 0
    assert {r['file_path'] for r in queue['records']} == {'/data/SC3.DK4'}
    records = {r['id']: r for r in draft['records']}
    assert records['DK4_MES_B214_R0068']['automatic_layout']['lines'][-1] == '-- Janus Pasar'
    assert b'Come on, Lil!' in bytes.fromhex(records['DK4_MES_B288_R0069']['after_native']['expanded_hex'])
    for ident in ('DK4_MES_B304_R0051', 'DK4_MES_B319_R0018'):
        row = records[ident]
        assert len(row['before_native']['pages']) == 2 and len(row['after_native']['pages']) == 1
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Lil wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the final Lil wrap batch and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Lil’s final wrap review

The [registered review](../{REVIEW.as_posix()}) resolves the last 54 flagged Lil wrap leads in 41 blocks. It revises 49 lines and reflows five with their original wording. Janus’s letter keeps his signature on a separate line. The spice sourcing tip preserves both regions and the Market Info instruction on one page. The trader’s account of gold and ivory keeps the local specialties, profits and scarcity on one page before he explains why some traders turned to other goods.

All {PAGE_COUNT} before-and-after pages received visual review. The 432 native alignment cases and 54 changed command boundaries passed. The five refinements used 20 fresh alignments and reused 412 cases with identical dependencies. Focused emulator replay used eight original commands at Lil’s initialized entry. It verified four revised and four neighboring pages, both reclaimed page turns and the return to Amsterdam. The other lines received offline checks. Original event triggers and hardware remain unvisited. A separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve the previous releases and the ASCII right bound. All [167 remaining wrap leads](../{TRIAGE.as_posix()}) are on Maria’s route. Match B87 and B116 by their registered command boundaries because their source and current speech counts differ. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'lil_late_wraps.pending.json': 'lil_final_wraps.pending.json',
        'release_stack_before_lil_late_wraps.json': 'release_stack_before_lil_final_wraps.json',
        "len(manifest['batches']) == 801 and len(manifest['checks']) == 136":
            "len(manifest['batches']) == 802 and len(manifest['checks']) == 137",
        "len(manifest['batches']) == 802 and len(manifest['checks']) == 137":
            "len(manifest['batches']) == 803 and len(manifest['checks']) == 138",
        'registered_manifest_entries=802, passing_release_checks=137': 'registered_manifest_entries=803, passing_release_checks=138',
        'verified_lil_midroute_wraps_predecessor=predecessor, lil_late_wraps_release=str(REVIEW)':
            'verified_lil_late_wraps_predecessor=predecessor, lil_final_wraps_release=str(REVIEW)',
        'Lil’s shop, crew, and sailing exchanges.': 'Lil’s final wrap review.',
        'lil_late_wraps_registered_successor_pipeline': 'lil_final_wraps_registered_successor_pipeline',
        'prose_revisions=55, justified_retentions=6': 'prose_revisions=49, justified_retentions=5',
        'Lil’s shop, crew, and sailing exchanges are registered.': 'Lil’s final flagged wrap review is registered.',
        'lil_late_wraps_retrospective_20261114': 'lil_final_wraps_retrospective_20261114',
        'existing_credit_preserved=61, prose_revisions=55, wrap_only_changes=2, exact_retentions=4':
            'existing_credit_preserved=54, prose_revisions=49, wrap_only_changes=5, exact_retentions=0',
        'Preserve the Lil shop, crew, and sailing dialogue release and verification.':
            'Preserve the Lil final wrap release and verification.',
        '802 entries, 114 accepted layers, 137 checks': '803 entries, 114 accepted layers, 138 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
