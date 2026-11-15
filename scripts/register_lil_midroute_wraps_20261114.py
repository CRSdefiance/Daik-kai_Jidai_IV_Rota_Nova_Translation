"""Register Lil's reviewed mid-route exchanges and clean-input patch."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_lil_opening_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_lil_midroute_wraps_20261114 as replay
from scripts import refine_lil_midroute_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-lil-midroute-wraps-v1-20261114'
CHECK = 'registered_lil_midroute_wraps_and_complete_parent_inverse'
ROOT = Path('out/lil_midroute_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Lil_Midroute_Wrap_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_lil_midroute_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.PRIOR_ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_lil_midroute_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v19.json')
PAGE_COUNT = 170
VIEWED = (
    '501b8c97f0c9f25b36168f2ed3843f703cb887a618e603f89d88d5170d7205f9',
    'c89f1c81502f4a049030eb1f0d67f1ab0ccef0c8dd893fb249c313dc8d4cba2c',
    '670fca58c3173210b0484fa918d046ab029bd12f560441b4a244ce98fb7482a1',
    '01aaa3cd2f0203e7332d145f262813ac09b4f330af8c2a5226766bb49703e0ed',
    '4b0422d1709a4cd5ba3feb7afcc8b82eea6df5e2660f4456f2c465a44b8829e1',
    '0c434cbb9c846a84da659760a87ff8bd3ae6f6c53177b055cf8c66907f193750',
    '051e250e38f6588c0c19c1d17b9e1dd53808aab2d3b6328b386cbe4ec778630d',
    '8b09ec5713b0cd85e145dd85daf75f35c7c90ae2adc049bb34e762353b727646',
    '218b1992868318043a6ee2101f610b1a65be85336a13414bc7807a34fed9b387',
    '78b4c39a2686b4d82c632ad5a8d17ad233b29e52c8bfb1e507562e855463a632',
    '44fb4c24ab57fb00d546c820502e250c5c2dfb8e3f41b54a821da899606440d8',
    '238ec83b2a3fcc707e7ef5252d929b3a5259913164c0e13f102e28fbb2325d4e',
    '1e6ad834bd85bf351cccb4e3f958d5c974275e899f9ee698aa9fb9e6ef5e0d99',
    'e0892190de7b9177747e1266062081c177673f1498a4432bd96a7e141900c324',
    '5d087e6919c7d79deb2982e6c524037ba8a613b568e624a554b092944406d0ee',
    'c1d2970adfe8c00e6711b0b2c2c18ebc86daa36b1f779d804206724808f74886',
    '6aaaf3aead49183e0055be6715a0fde9ed1b707fa7c9541e90e36f6000599333',
    'cb37583689a36e2b9bafe91f61e05a0031f9912d7131dc1a98d01c0973898d66',
    '14bccb0243ba334085685a8e2a4c146aa718900ef9fb61aa511003a7d2c7a786',
    '1fa586b43062eae50add3cbf89dd279f33c75bb8a38f64bf8a3457f8d10f9565',
    'cc8331dc2d1ed22d7c20167fe9d114404442adc805488e885c8369914a47c6ac',
    'c2c617f0cb5654f8b361b0ea34270da507b2417f9648bf8efb99e9a5e5d9c6f1',
)

triage_source = checked_text(getsource(parent.refresh_triage), {
    'this_pass_leads_resolved=len(decisions), pending_heuristic_bodies=len(entries),':
        """this_pass_leads_resolved=len(decisions.keys() & keys(old['records'])),
        this_pass_linked_corrections=len(decisions.keys() - keys(old['records'])), pending_heuristic_bodies=len(entries),""",
})
env = parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
}
exec(compile(triage_source, __file__ + '::wrap-queue-and-linked-corrections', 'exec'), env)
refresh_triage = env['refresh_triage']


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Lil_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 6 and live['verified_following_pages'] == 3",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 83 and len(draft['unchanged_leads']) == 1",
        "{'revision': 3, 'retention': 2}": "{'revision': 78, 'retention': 5}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == PAGE_COUNT and proof['checked_original_processor_alignments'] == 672",
        "runtime['captain'] == 0": "runtime['captain'] == 2",
        "b'Rafael Castor'.hex()": "b'Lil Argot Argot Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 65 and triage['pending_heuristic_bodies'] == 282",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Lil-midroute-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, _, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert base.load(TRIAGE)['this_pass_linked_corrections'] == 19
    changed = {row['id']: row for row in draft['records']}
    assert len([row for row in changed.values() if b'Christina' in bytes.fromhex(row['current_hex'])
                and b'Cristina' in bytes.fromhex(row['target_hex'])]) == 20
    assert b"Proof of Supremacy" in bytes.fromhex(changed['DK4_MES_B136_R0022']['current_hex'])
    assert b"Proof of Conquest" in bytes.fromhex(changed['DK4_MES_B136_R0022']['target_hex'])
    assert b'Proofs of Conquest' in bytes.fromhex(changed['DK4_MES_B115_R0128']['after_native']['expanded_hex'])
    assert any(b'Lil' in bytes.fromhex(row['after_native']['expanded_hex']) for row in changed.values()
               if row['block'] == 128)
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Lil mid-route dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes the Lil B61–B149 review and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Lil’s family revelations, confrontations, and adventures

The [registered review](../{REVIEW.as_posix()}) covers 84 dialogue records in 38 blocks. It resolves 65 wrap leads and 19 linked wording or name references, revising 78 lines, reflowing five with their wording intact, and retaining one exactly. Twenty lines now spell Cristina’s name as it appears on her nameplate. Maria’s appeal keeps the Proofs of Conquest together and turns the page when she shifts from the great powers’ plans to what her group is doing. The tablet scene uses Proof of Conquest and retains Emilio’s chart and cheese tart misunderstanding.

All {PAGE_COUNT} before-and-after pages received visual review. The batch passed 672 line-specific native alignments and 83 changed command boundaries. Focused emulator replay used eight original commands at Lil’s initialized entry to verify six revised and three neighboring pages, including Mivor’s reversal, Maria’s page turn, the tablet joke, and the return to Amsterdam. Other lines received offline checks. The original event triggers and hardware remain unvisited. A separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve earlier work and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 282 leads left, including 115 for Lil and 167 for Maria. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'lil_opening_wraps.pending.json': 'lil_midroute_wraps.pending.json',
        'release_stack_before_lil_opening_wraps.json': 'release_stack_before_lil_midroute_wraps.json',
        "len(manifest['batches']) == 799 and len(manifest['checks']) == 134":
            "len(manifest['batches']) == 800 and len(manifest['checks']) == 135",
        "len(manifest['batches']) == 800 and len(manifest['checks']) == 135":
            "len(manifest['batches']) == 801 and len(manifest['checks']) == 136",
        'registered_manifest_entries=800, passing_release_checks=135': 'registered_manifest_entries=801, passing_release_checks=136',
        'verified_hodram_final_wraps_predecessor=predecessor, lil_opening_wraps_release=str(REVIEW)':
            'verified_lil_opening_wraps_predecessor=predecessor, lil_midroute_wraps_release=str(REVIEW)',
        'Lil’s early battles, negotiations, and trade exchanges.': 'Lil’s family revelations, confrontations, and adventures.',
        'lil_opening_wraps_registered_successor_pipeline': 'lil_midroute_wraps_registered_successor_pipeline',
        'prose_revisions=23, justified_retentions=5': 'prose_revisions=78, justified_retentions=6',
        'revised_complete_pages=4, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,',
        'Lil’s early dialogue and wrap review is registered.': 'Lil’s family, confrontation, and adventure exchanges are registered.',
        'lil_opening_wraps_retrospective_20261114': 'lil_midroute_wraps_retrospective_20261114',
        'existing_credit_preserved=28, prose_revisions=23, wrap_only_changes=4, exact_retentions=1':
            'existing_credit_preserved=84, prose_revisions=78, wrap_only_changes=5, exact_retentions=1',
        'Preserve the Lil opening dialogue release and verification.': 'Preserve the Lil mid-route dialogue release and verification.',
        '800 entries, 114 accepted layers, 135 checks': '801 entries, 114 accepted layers, 136 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
