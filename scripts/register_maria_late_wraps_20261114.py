"""Register Maria's shop, bargaining, and letter scenes."""

import re
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace
from unicodedata import normalize

from scripts import register_maria_midroute_wraps_20261114 as parent
from scripts import register_rafael_charlotte_wraps_20261114 as queue_driver
from scripts import register_rafael_name_wraps_20261114 as name_release
from scripts import replay_maria_late_wraps_20261114 as replay
from scripts import refine_maria_late_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROFILE = 'all-routes-maria-late-wraps-v1-20261114'
CHECK = 'registered_maria_late_wraps_and_complete_parent_inverse'
ROOT = Path('out/maria_late_wraps_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Maria_Late_Wrap_Review_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_maria_late_wraps_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW = VERIFICATION / 'registered_review.json'
RELEASE = VERIFICATION / 'registered_release_verification.json'
QA = stage.PRIOR_ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_maria_late_wraps_registered_20261114.md')
TRIAGE = parent.TRIAGE.with_name('current_progressive_wrap_triage_v24.json')
VIEWED = (
    '39e41c937dd513586f818218ad191b145165ad6f14184b2779821fb18b1f891c',
    '75d0289907ca07118e869082de2d0927e9e152eb58acabecf1411b38640345ce',
    '9f385ceac77e3fac413b65ee61b83580fb1e4254845d081e359d7d1dd3a97e4e',
    'e6c6b60502ac46136fdaa4c03954145b0fccfebd66ea81f874b60ddf27f34f96',
    '51736c80a319535a16d32cb7ae41492ec37e8716f1be0dc11101d44b1ba997e7',
    '68fb126d7fa91d931413cf53e0ce86bee95cd283464a8804d3c49d7b1150ff56',
    '5732751049088899a37aa86849938b6afa70eb7955f2434327bf6f6eb2c07811',
    '838882db19549d5b96a577d3dc59e15122dd85b0f74aed481932fcec5ad4689b',
    'c965cb7b265538269fecb3217a43c96c743b309c65dd8d2b0959a14e47c595cc',
    '3cb2bf261c303aec07dd9578420cc1bcf5d1db73eed6016972638b91940b8588',
    '523915bd7d201903b80abcc127ee9d44941d10fba5cf1e9420a84586077920de',
)

triage_source = checked_text(getsource(queue_driver.refresh_triage), {
    'this_pass_leads_resolved=len(decisions), pending_heuristic_bodies=len(entries),':
        """this_pass_leads_resolved=len(decisions.keys() & keys(old['records'])),
        this_pass_linked_corrections=len(decisions.keys() - keys(old['records'])), pending_heuristic_bodies=len(entries),""",
})
env = queue_driver.refresh_triage.__globals__ | globals() | {
    'previous': SimpleNamespace(TRIAGE=parent.TRIAGE, scan=parent.refresh_triage.__globals__['previous'].scan),
}
exec(compile(triage_source, __file__ + '::exact-queue-membership-and-linked-corrections', 'exec'), env)
refresh_triage = env['refresh_triage']
reconstruct = FunctionType(parent.reconstruct.__code__, parent.reconstruct.__globals__ | globals())


def verify_inputs():
    original = name_release.verify_inputs
    source = checked_text(getsource(original), {
        "live['initialized_excerpts_at_Rafael_entry']": "live['initialized_excerpts_at_Maria_entry']",
        "live['verified_revised_pages'] == live['verified_following_pages'] == 5":
            "(live['verified_revised_pages'], live['verified_following_pages']) == (7, 4)",
        "len(commands['owned_records']) == len(draft['records']) == 5 and not draft['unchanged_leads']":
            "len(commands['owned_records']) == len(draft['records']) == 42 and not draft['unchanged_leads']",
        "{'revision': 3, 'retention': 2}": "{'revision': 41, 'retention': 1}",
        "proof['checked_complete_native_pages'] == 10 and proof['checked_original_processor_alignments'] == 40":
            "proof['checked_complete_native_pages'] == 86 and proof['checked_original_processor_alignments'] == 336",
        "runtime['captain'] == 0": "runtime['captain'] == 3",
        "b'Rafael Castor'.hex()": "b'Maria Li Li Clan'.hex()",
        "triage['this_pass_leads_resolved'] == 5 and triage['pending_heuristic_bodies'] == 786":
            "triage['this_pass_leads_resolved'] == 33 and triage['pending_heuristic_bodies'] == 49",
    })
    env = original.__globals__ | globals()
    exec(compile(source, __file__ + '::registered-Maria-bargaining-and-letter-checks', 'exec'), env)
    result = env['verify_inputs']()
    _, proof, live, draft, _ = result
    assert set(proof['archives']) == {stage.FILE}
    assert proof['fresh_processor_alignments'] == 16 and proof['reused_processor_alignments'] == 320
    assert all(base.digest(path) == digest for path, digest in proof['exact_render_reuse_dependencies'].items())
    assert live['earned_unlock_verified'] is False and live['verified_revised_utterances'] == 6
    records = {row['id']: row for row in draft['records']}
    for ident, signature in (
        ('DK4_MES_B182_R0032', '-- Yukihisa Genjo Shiraki'),
        ('DK4_MES_B187_R0067', '-- Janus Pasar'),
    ):
        assert records[ident]['automatic_layout']['lines'][-1] == signature
    letter = records['DK4_MES_B182_R0026']
    assert len(letter['before_native']['pages']) == len(letter['after_native']['pages']) == 2
    assert letter['automatic_layout']['lines'][3].endswith('ruler of Japan.')
    assert live['observed_Muramasa_pages_before_after'] == [2, 2]
    checked_prices = 0
    for row in records.values():
        if row['block'] not in {169, 174, 179}:
            continue
        clean_numbers = re.findall(r'[0-9]+', normalize('NFKC', row['source_Japanese']))
        if not clean_numbers:
            continue
        stored_numbers = re.findall(r'[0-9][0-9,]*', row['current_English'])
        updated = re.findall(r'[0-9][0-9,]*', row['english'].split('}', 1)[1])
        assert clean_numbers == [value.replace(',', '') for value in stored_numbers]
        assert updated == [format(int(value), ',d') for value in clean_numbers]
        checked_prices += len(clean_numbers)
    assert checked_prices == 12
    queue = base.load(TRIAGE)
    assert queue['this_pass_linked_corrections'] == 9
    assert {row['file_path'] for row in queue['records']} == {stage.FILE}
    assert min(row['block'] for row in queue['records']) >= 200
    return result


def package_notes(sha, release):
    return f'''# Maria bargaining and letters candidate

The [local ROM](../../{ROM.as_posix()}) includes Maria’s bargaining and letter review and the prior cumulative work. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release["clean_input_sha256"]}`. Hardware testing and acceptance for main are pending.
'''


def checkpoint_notes():
    return f'''# Maria’s shop, bargaining, and letter scenes

The [registered review](../{REVIEW.as_posix()}) covers 42 utterances in 22 blocks. It resolves 33 flagged wraps and nine linked fixes. Forty-one lines change wording or punctuation. The earring seller keeps his original wording and pauses after his chuckle. The 12 revised gold amounts use consistent thousands separators and match the clean Japanese. Yukihisa and Janus sign on separate lines. Yukihisa’s Muramasa letter now turns the page after a complete sentence.

All 86 before-and-after pages received visual review. All 336 processor alignments, 42 changed command boundaries and 56 targeted tests passed. The focused emulator replay checked seven revised pages and four neighboring pages, including two grouped prices, the Muramasa page turn, both signatures and the return to Hangzhou. The replay used selected source commands at Maria’s initialized entry with the existing system-only unlock. Original event conditions and hardware remain unvisited. The cumulative cold boot matched six frame holds and 24 protected name getters.

The [cumulative ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the earlier releases and ASCII right bound. The [wrap queue](../{TRIAGE.as_posix()}) contains 49 remaining Maria leads, starting at B200. The 279 shared records, remaining UI and name review, and representative town and random-scene coverage stay open. The ledger holds 27,697 credited reviews.
'''


def derive():
    return checked_text(parent.derive(), {
        'maria_midroute_wraps.pending.json': 'maria_late_wraps.pending.json',
        'release_stack_before_maria_midroute_wraps.json': 'release_stack_before_maria_late_wraps.json',
        "len(manifest['batches']) == 804 and len(manifest['checks']) == 139":
            "len(manifest['batches']) == 805 and len(manifest['checks']) == 140",
        "len(manifest['batches']) == 805 and len(manifest['checks']) == 140":
            "len(manifest['batches']) == 806 and len(manifest['checks']) == 141",
        'registered_manifest_entries=805, passing_release_checks=140': 'registered_manifest_entries=806, passing_release_checks=141',
        'verified_maria_opening_wraps_predecessor=predecessor, maria_midroute_wraps_release=str(REVIEW)':
            'verified_maria_midroute_wraps_predecessor=predecessor, maria_late_wraps_release=str(REVIEW)',
        'Maria’s discipline, recruitment, and trade scenes.': 'Maria’s shop, bargaining, and letter scenes.',
        'maria_midroute_wraps_registered_successor_pipeline': 'maria_late_wraps_registered_successor_pipeline',
        'prose_revisions=31, justified_retentions=1': 'prose_revisions=41, justified_retentions=1',
        'revised_complete_pages=4, following_original_pages=5': 'revised_complete_pages=7, following_original_pages=4',
        'Maria’s discipline, recruitment, and trade scenes are registered.': 'Maria’s shop, bargaining, and letter scenes are registered.',
        'maria_midroute_wraps_retrospective_20261114': 'maria_late_wraps_retrospective_20261114',
        'existing_credit_preserved=32, prose_revisions=31, wrap_only_changes=1, exact_retentions=0':
            'existing_credit_preserved=42, prose_revisions=41, wrap_only_changes=1, exact_retentions=0',
        'Preserve the Maria midroute wrap release and verification.': 'Preserve the Maria bargaining and letter release and verification.',
        '805 entries, 114 accepted layers, 140 checks': '806 entries, 114 accepted layers, 141 checks',
    })


def main():
    precedent = name_release.parent.previous.precedent
    env = vars(precedent.prior.prior) | vars(precedent.prior) | vars(precedent) | globals()
    exec(compile(derive(), __file__ + '::existing-cumulative-publication-contract', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

