"""Register the remaining flagged Hodram dialogue decisions."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_rumor_wraps_20261114 as parent
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_hodram_final_wraps_20261114 as replay
from scripts import stage_hodram_final_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-hodram-final-wraps-v1-20261114'
CHECK = 'registered_hodram_final_wraps_and_complete_parent_inverse'
ROOT = Path('out/hodram_final_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Hodram_Wrap_Review_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_hodram_final_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa_padded_2.xml'
DOC = Path('docs/editorial_hodram_final_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v17.json')
VIEWED = (
    '59aedf1076ea008cc06fd0b72cdbb9bc1a9b377454e635ef0573f640dd975dd9',
    '2ed58ef2f00563d48688a62c385b69fc6411774cd6051bd796f46b899916f00b',
    '45636fd5fb3eb1eeb8319f62ece08e46440472711279f432b5d17e01e7d742f1',
    'b70af441a1f982b3600a9fae56d5d12b3ee7a0524099cb1971fbd8936eefb8d6',
    'a0acec6bb38c475ce135dd68eff1995d635cedca8d5fb35b9c7e83d202569f87',
    'cb318495f38ec1de99629f98719d17f8ffee86f13e3801c0850c67484c752415',
    'ed744f2a0d8718cafbeac7f8fcd518f4cf0b96fc8daa173f781e437d92b11162',
    '8d4be04cc3aeb80938329961de8015491da9f340a7a63fbccc92ac1058539421',
    'cd011cba64530409453dcd6ec3256a411183e18c455f97cf52fc88e05dd91781',
    'cfec07c5558046db19a2a893c12b80a65e78ef968fe1644e3873287dafd9f18d',
    '104d1c70f55a630d0e206d4e0ebd47a79fac0a6e1f94f103f69b19358fa852b2',
    '90ddfad7f79fee5bb320023b28d44ab0dd42c5ab2a9fdff7ca02f317181dec1b',
    '00bdd6c70f69c8f4a308e5c9641cdcc0b0e85aa13dcf47e638be4dc20865146a',
    '08274ca7c883b6329c84370ff14052ff76e8e477a7c202d760f8cdab52e2fa22',
    'c0d93e879f473c1fffad3b1627315a780483805af97d0af55a7b672cd9902f17',
    '1a4bf46206b1fa11ea73c01403e1e80380bfb9a2985ceea8519554c7b89d87fc',
    '0be2d87db545b1d4f6ba11e4e9d0295e5f339e90780a5b0e469a00c114a254ce',
    'e6b7539ced704e128026116923efadd0c6a8b4e0f408adb034f556793bf3e7d7',
)
refresh_triage = FunctionType(parent.refresh_triage.__code__, parent.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
})


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Hodram_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "live['verified_revised_pages'] == 6 and live['verified_following_pages'] == 3",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 68 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 66, 'retention': 2}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 139 and proof['checked_original_processor_alignments'] == 544",
        "runtime['captain'] == 0": "runtime['captain'] == 1",
        "b'Rafael Castor'.hex()": "b'Hodram Bergstrom Bergstrom Fleet'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 68 and triage['pending_heuristic_bodies'] == 375",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-input-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, _, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    records = {row['id']: row for row in draft['records']}
    assert b'Mr. Bergstrom, right?' in bytes.fromhex(records['DK4_MES_B257_R0006']['after_native']['expanded_hex'])
    assert b'Say, Hodram' in bytes.fromhex(records['DK4_MES_B314_R0010']['after_native']['expanded_hex'])
    assert all(row['file_path'] != stage.FILE for row in base.load(TRIAGE)['records'])
    return result


reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def package_notes(sha, release):
    return f'''# Hodram wrap review candidate

The [local ROM](../../{ROM.as_posix()}) includes the final set of flagged Hodram wrap decisions and earlier cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. This candidate awaits hardware testing and acceptance for main.
'''


def checkpoint_notes():
    return f'''# Hodram’s remaining flagged wraps

The [registered review](../{REVIEW.as_posix()}) resolves 68 flagged lines across 51 blocks. It revises 66 speeches and reflows two with their wording intact. The Muramasa letter starts its second page with the effort to destroy the blades. The village account restores the epidemic detail and fits on one page. The Goryeo Incense Burner rumor preserves its material, location clue, and the speaker’s uncertainty. Storage padding uses the expanded name width to keep the rumor on one page.

All 139 before-and-after pages were visually checked. The 544 native processor alignments and 68 changed speech boundaries passed. Scoped replay in Hodram’s initialized opening matched six revised pages and three neighboring pages from the letter, town lead, artifact rumor, and village account. The replay exercised native first-name and family-name substitutions and the return to the original departure flow. Optional scene triggers and hardware remain unvisited. The remaining pages received offline checks. Cumulative cold boot and 56 targeted tests passed.

The [cumulative ROM and byte-exact patch](../{PACKAGE.as_posix()}/README.md) preserve earlier work and the ASCII right bound. The [wrap scan](../{TRIAGE.as_posix()}) has 375 leads left across Lil and Maria. The 279 shared records, remaining UI and name coverage, and representative town and random-scene coverage remain open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'hodram_rumor_wraps.pending.json': 'hodram_final_wraps.pending.json',
        'release_stack_before_hodram_rumor_wraps.json': 'release_stack_before_hodram_final_wraps.json',
        "len(manifest['batches']) == 797 and len(manifest['checks']) == 132":
            "len(manifest['batches']) == 798 and len(manifest['checks']) == 133",
        "len(manifest['batches']) == 798 and len(manifest['checks']) == 133":
            "len(manifest['batches']) == 799 and len(manifest['checks']) == 134",
        'registered_manifest_entries=798, passing_release_checks=133': 'registered_manifest_entries=799, passing_release_checks=134',
        'verified_hodram_opening_wraps_predecessor=predecessor, hodram_rumor_wraps_release=str(REVIEW)':
            'verified_hodram_rumor_wraps_predecessor=predecessor, hodram_final_wraps_release=str(REVIEW)',
        'Hodram’s artifact, diplomacy, and crew exchanges.': 'Hodram’s remaining flagged wraps.',
        'hodram_rumor_wraps_registered_successor_pipeline': 'hodram_final_wraps_registered_successor_pipeline',
        'prose_revisions=55, justified_retentions=3': 'prose_revisions=66, justified_retentions=2',
        'revised_complete_pages=7, following_original_pages=2, surrounding_identical_frames=3,':
            'revised_complete_pages=6, following_original_pages=3, surrounding_identical_frames=3,',
        'Hodram’s artifact, diplomacy, and crew wrap review is registered.':
            'Hodram’s remaining flagged wrap decisions are registered.',
        'hodram_rumor_wraps_retrospective_20261114': 'hodram_final_wraps_retrospective_20261114',
        'existing_credit_preserved=58, prose_revisions=55, wrap_only_changes=3, exact_retentions=0':
            'existing_credit_preserved=68, prose_revisions=66, wrap_only_changes=2, exact_retentions=0',
        'Preserve the Hodram artifact and dialogue wrap release and verification.':
            'Preserve the Hodram wrap review release and verification.',
        '798 entries, 114 accepted layers, 133 checks': '799 entries, 114 accepted layers, 134 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
