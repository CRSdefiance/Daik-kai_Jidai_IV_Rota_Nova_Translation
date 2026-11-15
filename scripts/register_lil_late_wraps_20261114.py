"""Register Lil's B150–B199 edits on the verified cumulative release."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_lil_midroute_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_lil_late_wraps_20261114 as replay
from scripts import stage_lil_late_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-lil-late-wraps-v1-20261114'
CHECK = 'registered_lil_late_wraps_and_complete_parent_inverse'
ROOT = Path('out/lil_late_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Lil_Late_Wrap_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_lil_late_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_lil_late_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v20.json')
PAGE_COUNT = 122
VIEWED = (
    'f344b092147c0c62ee0f49834a45e2fc89e8fbcdea714e5473f294b5fed4141e',
    'ee8540d4e7b67c9db9a263648db143ef71519bdb9ad57bc3b153da8e60c1d521',
    'a382e2769df0bc841449ace70710bac2eeb541e3b18683fac5b8e539adf5a458',
    '02ca1eaa4465da0524b4129aaf0763c77de0a21110298c618f5e23c673a76e74',
    '0c6b34590f54a2d194818b6966d9b65928244e386b54b3558f4ff9321fd3ce66',
    '810420713ba8ebe9041983b5debbf1e181998eda66f82743a0e80be8a71d59c5',
    '5a97325088bbe147ba6563944b3f0fc4f0f00e734bed3869f3f0491c6ab71ab8',
    '4f09224ca4c61e8c141c26087adf2434a187a4212195108403dfaaf1fd766eba',
    '0571d77daa3352488f1765d8ffc2c37336f0e573899d6650f2cfe48a2de573a2',
    'b769b8a7292733079d124c87ace90885d5b1a7fe2e4dc7d8359b7dd29632951f',
    '06e5b6286099d7a06c635e72662916dbbcaafebd47a016800a2b1bd10ab3dbcb',
    '44f0d0a3fadd0df552c768b980af260836653ae1a62c511a8f60548c17bfcf38',
    '1937d65e7ebc0e4df33cf5e6fd90c1d1635f7e69d849aa3715ccb803327eef77',
    '1c1e7785819bbb44501e315b01edc834ca2a182c2800f77c8041da5d9f67ada5',
    '9b53f1f71897b7218c2d6307896fad34747e6e1ea4286d16b3c19a979a3e178c',
    '58e41c334f3e448e5affc80a57fe2dd39d87e160d4c91a010e17b27210dea874',
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
            "len(commands['owned_records']) == len(draft['records']) == 57 and len(draft['unchanged_leads']) == 4",
        "{'revision': 3, 'retention': 2}": "{'revision': 55, 'retention': 2}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == PAGE_COUNT and proof['checked_original_processor_alignments'] == 488",
        "runtime['captain'] == 0": "runtime['captain'] == 2",
        "b'Rafael Castor'.hex()": "b'Lil Argot Argot Co.'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 61 and triage['pending_heuristic_bodies'] == 221",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Lil-late-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, _, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert base.load(TRIAGE)['this_pass_linked_corrections'] == 0
    exact = {r['id'] for r in draft['unchanged_leads']}
    assert exact == {'DK4_MES_B159_R0063', 'DK4_MES_B174_R0110', 'DK4_MES_B188_R0022', 'DK4_MES_B189_R0013'}
    text = {r['id']: bytes.fromhex(r['after_native']['expanded_hex']) for r in draft['records']}
    assert b'Galley and Livestock Room' in text['DK4_MES_B166_R0157']
    assert b'Small ships' in text['DK4_MES_B167_R0095'] and b'spritsail.' in text['DK4_MES_B167_R0095']
    assert b'two or more masts' in text['DK4_MES_B167_R0101']
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Lil shop, crew, and sailing dialogue candidate

The [local ROM](../../{ROM.as_posix()}) includes the Lil B150–B199 review and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Lil’s shop, crew, and sailing exchanges

The [registered review](../{REVIEW.as_posix()}) resolves 61 wrap leads in 29 blocks, revising 55 lines, reflowing two with the original wording, and retaining four exactly. The Malacca shop scene preserves the trader’s switch from accepting Carlo’s advice to addressing the waiting customers. Manuel’s Galley and Livestock Room advice preserves the fleet-wide food and water effect. The shipwright’s tutorial retains the spritsail size limit and the minimum of two masts for the wind lesson.

All {PAGE_COUNT} before-and-after pages received visual review. The batch passed 488 line-specific native alignments and 57 changed command boundaries. Focused emulator replay used eight original commands at Lil’s initialized entry to verify four revised and four neighboring pages from the shop and the tutorial, followed by the original return to Amsterdam. Other lines received offline checks. The original event triggers and hardware remain unvisited. A separate cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve earlier work and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 221 leads left, including 54 for Lil and 167 for Maria. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'lil_midroute_wraps.pending.json': 'lil_late_wraps.pending.json',
        'release_stack_before_lil_midroute_wraps.json': 'release_stack_before_lil_late_wraps.json',
        "len(manifest['batches']) == 800 and len(manifest['checks']) == 135":
            "len(manifest['batches']) == 801 and len(manifest['checks']) == 136",
        "len(manifest['batches']) == 801 and len(manifest['checks']) == 136":
            "len(manifest['batches']) == 802 and len(manifest['checks']) == 137",
        'registered_manifest_entries=801, passing_release_checks=136': 'registered_manifest_entries=802, passing_release_checks=137',
        'verified_lil_opening_wraps_predecessor=predecessor, lil_midroute_wraps_release=str(REVIEW)':
            'verified_lil_midroute_wraps_predecessor=predecessor, lil_late_wraps_release=str(REVIEW)',
        'Lil’s family revelations, confrontations, and adventures.': 'Lil’s shop, crew, and sailing exchanges.',
        'lil_midroute_wraps_registered_successor_pipeline': 'lil_late_wraps_registered_successor_pipeline',
        'prose_revisions=78, justified_retentions=6': 'prose_revisions=55, justified_retentions=6',
        'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,':
            'revised_complete_pages=4, following_original_pages=4, surrounding_identical_frames=3,',
        'Lil’s family, confrontation, and adventure exchanges are registered.': 'Lil’s shop, crew, and sailing exchanges are registered.',
        'lil_midroute_wraps_retrospective_20261114': 'lil_late_wraps_retrospective_20261114',
        'existing_credit_preserved=84, prose_revisions=78, wrap_only_changes=5, exact_retentions=1':
            'existing_credit_preserved=61, prose_revisions=55, wrap_only_changes=2, exact_retentions=4',
        'Preserve the Lil mid-route dialogue release and verification.': 'Preserve the Lil shop, crew, and sailing dialogue release and verification.',
        '801 entries, 114 accepted layers, 136 checks': '802 entries, 114 accepted layers, 137 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
