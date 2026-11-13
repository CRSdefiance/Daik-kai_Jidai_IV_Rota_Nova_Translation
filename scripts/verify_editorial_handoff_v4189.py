"""Independently verify pending B168 credit, exact source/current bytes and complete native planes."""
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B168_layout_v3 as codec
from dk4tool.dialogue.lil_B168_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_B168_native_v4187 import validate_source_macros
from scripts.checkpoint_lil_B168_v4188 import UNCHANGED
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4189')
CHECKPOINT = Path('work/analysis/lil_B168_checkpoint_v4188')

if __name__ == '__main__':
    assert not ROOT.exists()
    receipt = read(CHECKPOINT / 'staged_receipt.json')
    for path, digest in {**receipt['evidence'], **receipt['preserved_release_files']}.items():
        assert sha(Path(path).read_bytes()) == digest, path
    updated = {}
    for entry in read(CHECKPOINT / 'mutation_plan.json'):
        path = Path(entry['target'])
        assert sha(path.read_bytes()) == entry['planned_sha256']
        updated[str(path)] = entry['planned_sha256']
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    before_path = CHECKPOINT / (lp.name + '.before')
    before = read(before_path)
    prior = read(receipt['prior_verified_handoff'])
    assert sha(before_path.read_bytes()) == prior['ledger_sha256']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5656, 5602, 54)
    keys, integrated, pending = [{historical_key(row) for row in fresh[key]} for key in ['record_keys', 'integrated_record_keys', 'pending_record_keys']]
    assert len(keys) == len(fresh['record_keys']) == 5656
    assert len(integrated) == 5602 and len(pending) == 54 and not integrated & pending
    assert keys == integrated | pending
    completed = [row for family in ledger['completed_editorial_families'] for row in family['records']]
    assert len(completed) == len({historical_key(row) for row in completed}) == 5602
    assert {historical_key(row) for row in completed} == integrated
    assert (ledger['records_with_source_and_prose_pass'], ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'], ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4'],
            ledger['records_editorially_completed'], ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (5659, 3803, 64, 5602, 3567, 2035)
    unit = next(unit for unit in ledger['coverage_units'] if unit['id'] == 'all-route-scenes')
    assert (unit['reviewed_route_records'], unit['completed_route_records']) == (4057, 4003)
    approval_path = Path('work/analysis/lil_B168_native_approval_v4187/approval_receipt.json')
    approval = read(approval_path)
    assert len(approval['manuscripts']) == 1
    for path, digest in approval['manuscripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    doc = read(next(iter(approval['manuscripts'])))
    rows = doc['records']
    assert len(rows) == 54 and {historical_key(row) for row in rows} == pending
    assert Counter(row['kind'] for row in rows) == {'progressive': 51, 'system-FE': 3}
    assert Counter(row['editorial_decision'] for row in rows) == {'revise': 28, 'retain-wording': 26}
    current, clean = NdsImage.open(doc['current_ROM']), NdsImage.open('work/clean.nds')
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256'] == prior['rom_sha256']
    block, jp = [IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[168] for image in [current, clean]]
    arm = current.read_file('/__arm9__.bin')
    font = read(doc['native_font_proof'])
    assert sha(Path(doc['native_font_proof']).read_bytes()) == doc['native_font_proof_sha256']
    fonts = {row['id']: row for row in font['cases']}
    notes = 0
    for row in rows:
        assert all(row['review'].values()) and row['source_meaning'] == row['fresh_source_gloss']
        assert row['full_clean_context_precedes_comparison'] and row['clean_source_complete_exchange_read_before_predecessor_English']
        raw, old = bytes.fromhex(row['source_hex']), bytes.fromhex(row['current_hex'])
        sa, ca = row['source_reference']['offset'], row['current_reference']['offset']
        assert jp[sa:sa + len(raw)] == raw and block[ca:ca + len(old)] == old
        assert jp[sa + len(raw)] == block[ca + len(old)] == 0
        assert raw[0] == old[0] == row['source_selector']
        assert jp[sa - 5:sa + 1] == block[ca - 5:ca + 1] == bytes.fromhex(row['source_complete_preamble_hex'])
        assert raw[1:].decode('cp932') == row['source_Japanese']
        fe = row['kind'] == 'system-FE'
        p = profile_for(arm, block, 'FE-paper' if fe else 'progressive')
        encoded = codec.encode_relocatable_dialogue(raw, row['english'], p)
        c = fonts[row['id']]
        assert encoded.encoded.hex() == row['compiled_hex'] == c['encoded_hex']
        assert c['complete_native_independent_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert c['all_visible_origins_zero_and_native_rows_within4rows']
        assert sum(len(v['cases']) for v in c['current_native_macro_pipelines']) == 8
        assert sha(Path(c['preview']).read_bytes()) == c['preview_sha256']
        if fe:
            assert raw[0] == 254 and c['geometry'] == [228, 64] and c['one_native_page_consumes_complete_target']
            assert (c['logical_row_pitch'], c['physical_row_pitch']) == (12, 16)
        else:
            assert raw[0] in [2, 6, 9, 20, 76, 87, 165, 166] and c['geometry'] == [216, 64]
        report = codec.audit_relocatable_dialogue_record(raw, row['english'], p)
        assert not [issue for issue in report['issues'] if issue['severity'] in ['warning', 'error'] and not
                    (issue['severity'] == 'warning' and issue['code'] == 'line-break-count' and row.get('qa_waiver_reason'))]
        assert row.get('qa_waivers') in [None, ['line-break-count']]
        notes += bool(row.get('qa_waivers'))
        validate_source_macros(raw, row['english'])
        if row['editorial_decision'] == 'retain-wording':
            assert row['fresh_retained_wording_justification']
            assert row['english'].split('}', 1)[1] == row['effective_predecessor_paragraph']
    assert notes == 20 and len(font['cases']) == 54 and font['current_original_macro_alignment_calls'] == 432
    for key, count in [('source_consumer_negative_controls', 26), ('source_macro_preservation_negatives', 3), ('source_bound_formatter_negatives', 14)]:
        assert len(font[key]) == count and all(row['rejected'] for row in font[key])
    assert len(font['review_sheets']) == 7 and all(sheet['viewed_in_full_current_turn'] for sheet in font['review_sheets'])
    for sheet in font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    assert approval['new_emulator_runs'] == approval['new_completed_records'] == 0
    scope = ledger['unfinished_editorial_scope_v4188']
    assert sha(Path(scope['path']).read_bytes()) == scope['sha256']
    assert (scope['incomplete_COMMON'], scope['incomplete_route_source_prose'], scope['remaining_B169_B180_physical_speeches'], scope['remaining_choice_command_leads']) == (3, 54, 267, 0)
    inventory = read(scope['path'])
    old_inventory = read(before['unfinished_editorial_scope_v4164']['path'])
    assert inventory['remaining_B168_B180_unreviewed_uncredited'] == old_inventory['remaining_B168_B180_unreviewed_uncredited']
    assert inventory['remaining_B168_B180_inventory_is_historical_at_V4164']
    for key in UNCHANGED:
        assert ledger[key] == before[key], key
    assert read('translations/release_stack.json')['latest_promoted_build']['profile'] == 'all-routes-unified-v4160'
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    for path in updated:
        if Path(path).suffix == '.md':
            assert '## V4188: 54 B168 contextual/native reviews; integration pending' in Path(path).read_text(encoding='utf-8')
    sealed = {**receipt, 'updated_files': updated, 'independent_audit': str(Path(__file__)),
              'independent_audit_sha256': sha(Path(__file__).read_bytes())}
    save(CHECKPOINT / 'checkpoint_receipt.json', sealed)
    ROOT.mkdir(parents=True)
    candidate = ledger['current_integrated_candidate']
    save(ROOT / 'verified_handoff.json', dict(checkpoint='V4188', ledger_sha256=sha(lp.read_bytes()),
        handoff_receipt=str(CHECKPOINT / 'checkpoint_receipt.json'), handoff_receipt_sha256=sha((CHECKPOINT / 'checkpoint_receipt.json').read_bytes()),
        fresh_reread=5656, integrated=5602, pending=54, source_prose=5659, revised=3567, retained=2035,
        candidate=candidate['path'], candidate_sha256=candidate['sha256'], patch=candidate['patch'], patch_sha256=candidate['patch_sha256'],
        manifest_batches=543, accepted_layers=114, all54_source_current_gloss_context_retention_and_native_references_verified=True,
        progressive_planes=51, FE_planes=3, native_macro_alignment_cases=432, all7_native_sheets_viewed=True,
        promoted_V4160_unchanged=True, all_prior_completions_and_wider_scope_preserved=True,
        new_ROM_registry_emulator_or_completion_credit=False, full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('V4188 independently verified:5656 reread/5602 integrated/54 pending;5659 source/prose. Exact references,retentions,native proofs and wider scope pass.')
