"""Independently verify B166 pending credit and exact source/current/native references."""
from collections import Counter
import gzip
from pathlib import Path

from dk4tool.dialogue import lil_B166_layout_v4 as codec
from dk4tool.dialogue.lil_B166_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4091')
CHECKPOINT = Path('work/analysis/lil_B166_checkpoint_v4090')

if __name__ == '__main__':
    assert not ROOT.exists()
    receipt = read(CHECKPOINT / 'checkpoint_receipt.json')
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = read(CHECKPOINT / (ledger_path.name + '.before'))
    for path, digest in {**receipt['evidence'], **receipt['updated_files']}.items():
        assert sha(Path(path).read_bytes()) == digest, path
    prior = read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT / (ledger_path.name + '.before')).read_bytes()) == prior['ledger_sha256']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'],
            fresh['fresh_pass_records_pending_native_actual_release']) == (5573, 5529, 44)
    keys, integrated, pending = [{historical_key(r) for r in fresh[k]}
                                for k in ['record_keys', 'integrated_record_keys', 'pending_record_keys']]
    assert len(keys) == len(fresh['record_keys']) == 5573 and len(integrated) == 5529 and len(pending) == 44
    assert not integrated & pending and keys == integrated | pending
    completed = [r for family in ledger['completed_editorial_families'] for r in family['records']]
    assert len(completed) == len({historical_key(r) for r in completed}) == 5529
    assert {historical_key(r) for r in completed} == integrated
    assert (ledger['records_with_source_and_prose_pass'], ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'],
            ledger['records_editorially_completed'], ledger['records_revised_and_integrated'],
            ledger['retained_wordings_editorially_completed']) == (5576, 3720, 5529, 3527, 2002)
    unit = next(u for u in ledger['coverage_units'] if u['id'] == 'all-route-scenes')
    assert (unit['reviewed_route_records'], unit['completed_route_records']) == (3974, 3930)
    approval = read('work/analysis/lil_B166_native_approval_v4082/approval_receipt.json')
    documents = [read(p) for p in approval['manuscripts']]
    rows = [r for d in documents for r in d['records']]
    assert len(rows) == 44 and {historical_key(r) for r in rows} == pending
    assert Counter(r['editorial_decision'] for r in rows) == {'revise': 24, 'retain-wording': 20}
    assert Counter(r['kind'] for r in rows) == {'progressive': 42, 'typed-choice-label': 2}
    for path, digest in approval['manuscripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    doc = next(d for d in documents if len(d['records']) == 42)
    image = NdsImage.open(doc['current_ROM'])
    clean = NdsImage.open('work/clean.nds')
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    block, jp = [IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[166] for im in [image, clean]]
    profile = profile_for(image.read_file('/__arm9__.bin'), block)
    font = read(doc['native_font_proof'])
    assert sha(Path(doc['native_font_proof']).read_bytes()) == doc['native_font_proof_sha256']
    fonts = {r['id']: r for r in font['cases']}
    notes = 0
    for row in rows:
        assert all(row['review'].values()) and row['source_meaning'] == row['fresh_source_gloss']
        assert row['full_clean_context_precedes_comparison'] and row['clean_source_complete_exchange_read_before_predecessor_English']
        raw, old = bytes.fromhex(row['source_hex']), bytes.fromhex(row['current_hex'])
        sa, ca = row['source_reference']['offset'], row['current_reference']['offset']
        assert jp[sa:sa + len(raw)] == raw and block[ca:ca + len(old)] == old
        assert jp[sa + len(raw)] == block[ca + len(old)] == 0
        if row['kind'] == 'progressive':
            assert raw[0] == old[0] == row['source_selector'] in [2, 9, 20, 23]
            assert jp[sa-5:sa+1] == block[ca-5:ca+1] == bytes.fromhex(row['source_complete_preamble_hex'])
            assert raw[1:].decode('cp932') == row['source_Japanese']
            encoded = codec.encode_relocatable_dialogue(raw, row['english'], profile)
            case = fonts[row['id']]
            assert encoded.encoded.hex() == row['compiled_hex'] == case['encoded_hex']
            assert case['complete_native_independent216x64_plane_equal']
            assert case['all_first_final_internal_glyphs_in_order_and_unique_cells']
            assert case['all_visible_origins_zero_and16px_rows_within4rows']
            assert sum(len(p['cases']) for p in case['current_native_macro_pipelines']) == 8
            qa = codec.audit_relocatable_dialogue_record(raw, row['english'], profile)
            assert not [i for i in qa['issues'] if i['severity'] in ['error', 'warning'] and not
                        (i['severity'] == 'warning' and i['code'] == 'line-break-count' and row.get('qa_waiver_reason'))]
            assert row.get('qa_waivers') in [None, ['line-break-count']]
            notes += bool(row.get('qa_waivers'))
            for macro in ['FI', 'FA', 'FO']:
                assert raw.count(macro.encode()) == row['english'].count('{MACRO:' + macro + '}')
        else:
            assert raw.decode('cp932') == row['source_Japanese']
            assert row['english'] == ['Please do', 'Decline'][row['option_index']]
        if row['editorial_decision'] == 'retain-wording':
            assert row['fresh_retained_wording_justification']
            assert (row['english'].split('}', 1)[1] if row['kind'] == 'progressive' else row['english']) == row['effective_predecessor_paragraph']
    assert notes == 15 and len(font['cases']) == 42
    assert approval['actual_menu_only_cold_boot_runs'] == 3 and approval['actual_B166_speech_or_choice_return_coverage_added'] == 0
    scope = ledger['unfinished_editorial_scope_v4090']
    assert sha(Path(scope['path']).read_bytes()) == scope['sha256']
    assert scope['incomplete_route_source_prose'] == 44 and scope['remaining_B167_B180_physical_speeches'] == 348
    candidate = ledger['current_integrated_candidate']
    assert sha(Path(candidate['path']).read_bytes()) == candidate['sha256']
    assert sha(Path(candidate['patch']).read_bytes()) == candidate['patch_sha256']
    frozen = __import__('json').loads(gzip.decompress(Path('releases/all_routes_unified_v4046/build_release_stack.json.gz').read_bytes()))
    registry = read('translations/release_stack.json')
    assert {k: v for k, v in frozen.items() if k != 'latest_promoted_build'} == {k: v for k, v in registry.items() if k != 'latest_promoted_build'}
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4046'
    for key in ['completed_editorial_families', 'current_integrated_candidate', 'reviewed_but_incomplete_COMMON_IDs',
                'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal',
                'native_source_universe_inventory_v2701c', 'Proof_terminology_consistency_lead_v3286',
                'lil_B157_provenance_amendment_v3784', 'promoted_main_build_v4083']:
        assert ledger[key] == before[key], key
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True)
    save(ROOT / 'verified_handoff.json', dict(checkpoint='V4090', ledger_sha256=sha(ledger_path.read_bytes()),
        fresh_reread=5573, integrated=5529, pending=44, source_prose=5576, revised=3527, retained=2002,
        candidate=candidate['path'], candidate_sha256=candidate['sha256'], patch=candidate['patch'],
        patch_sha256=candidate['patch_sha256'], manifest_batches=539, accepted_layers=114,
        all44_exact_source_current_gloss_context_and_native_references_verified=True,
        new_ROM_registry_emulator_or_completion_credit=False, full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('V4090 independently verified:5573 reread/5529 integrated/44 pending;5576 source/prose;V4046 main unchanged.')
