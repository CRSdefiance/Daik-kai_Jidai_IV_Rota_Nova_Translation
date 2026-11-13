"""Advance uncredited source/draft progress without changing completion or release state."""
import copy
import gzip
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
DOC = Path('docs/editorial_hodram_B151_B170_source_drafts_20261102.md')
DRAFTS = [ROOT / f for f in ['B151_B155_42_clean_English_drafts_v1.json', 'B157_B158_73_clean_English_drafts_v1.json', 'B159_61_clean_English_drafts_v1.json']]
SUMMARY = ('B151–B170:all642 clean meanings saved;176 logical English drafts across eight complete exchanges,466 drafts remain. '
           '36 ordinary identities bound (13 fresh/23 reused),four items,two city labels,Mivor andnine Rafael preambles. '
           'Prior-English conversation comparison,formatting,visual/stored/gameplay/release gates remain open;no new credit orROM. '
           '8856 completed/current experimental7fb6f6d7/main unchanged. Full scope preserved;no guide photos.')


if __name__ == '__main__':
    target = ROOT / 'source_draft_progress_checkpoint_v1.json'
    assert not target.exists()
    meanings = load(ROOT / 'complete_clean_meanings_checkpoint.json')
    assert meanings['source_meanings_saved'] == 642 and meanings['remaining_source_meanings'] == 0
    bindings = load(ROOT / 'native_identity_and_item_checkpoint_v1.json')
    assert bindings['ordinary_actor_bindings'] == 36 and bindings['fresh_actors'] == 13 and bindings['reused_actors'] == 23
    docs = [load(p) for p in DRAFTS]
    rows = [r for d in docs for r in d['records']]
    assert len(rows) == len({r['id'] for r in rows}) == 176
    assert sorted({r['block'] for r in rows}) == [151, 152, 153, 154, 155, 157, 158, 159]
    assert all(all(r['review'][g] is True for g in ['source', 'context', 'localization', 'naturalness']) and r['review']['formatting'] is False for r in rows)
    assert sum(bool(r['incidental_legacy_line_exposure']) for r in rows) == 1
    registry = Path('translations/release_stack.json')
    registry_before = registry.read_bytes()
    assert sha(registry_before) == 'dde90af7920d7562851e16858cb9fef923d25268691c8d9fa1ced156ecd9265a'
    candidate = Path(bindings['runtime']['candidate'])
    assert sha(candidate.read_bytes()) == '7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    ledger_path = Path('translations/editorial_review_current_v1.json')
    before = ledger_path.read_bytes()
    ledger = load(ledger_path)
    assert ledger['records_editorially_completed'] == 8856 and ledger['records_revised_and_integrated'] == 5540
    assert ledger['retained_wordings_editorially_completed'] == 3316
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 8859
    previous = dict(ledger)
    backup = ROOT / 'ledger_before_642_meanings_176_drafts.json.gz'
    assert not backup.exists()
    backup.write_bytes(gzip.compress(before, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    key = 'Hodram_B151_B170_clean_next_20261102'
    entry = copy.deepcopy(ledger[key])
    entry.update(source_meanings_saved=642, remaining_ordinary_meanings=0, remaining_caption_meanings=0,
                 complete_meanings_checkpoint=str(ROOT / 'complete_clean_meanings_checkpoint.json'),
                 complete_meanings_checkpoint_sha256=sha((ROOT / 'complete_clean_meanings_checkpoint.json').read_bytes()),
                 logical_English_drafts=176, remaining_localized_drafts=466, current_English_conversation_comparisons=0,
                 no_new_English_drafts_orcontextual_comparisons=False,
                 no_current_ROM_English_dialogue_extraction=True,
                 incidental_legacy_line_exposure=bindings['incidental_legacy_dialogue_exposure'],
                 native_identities=36, fresh_actor_bindings=13, reused_actor_bindings=23,
                 native_identity_terms_anddisplay_gates_pending=True,
                 ordinary_speaker_identities_andfour_items_bound_other_terms_anddisplay_pending=True,
                 documentation=str(DOC), source_draft_checkpoint=str(target), prior_latest_checkpoint=ledger['latest_checkpoint'])
    entry['source_meaning_parts'] = {str(p):sha(p.read_bytes()) for p in [ROOT/'all634_clean_meanings_before_English_v1.json', ROOT/'eight_clean_caption_meanings_before_English.json']}
    entry['source_first_English_drafts'] = {str(p):sha(p.read_bytes()) for p in DRAFTS}
    ledger[key] = entry
    ledger['latest_checkpoint'] = SUMMARY
    assert all(ledger[k] == v for k, v in previous.items() if k not in [key, 'latest_checkpoint'])
    checkpoint = dict(summary=SUMMARY, source_meanings=642, logical_English_drafts=176, remaining_localized_drafts=466,
                      complete_draft_blocks=[151, 152, 153, 154, 155, 157, 158, 159], draft_record_ids=[r['id'] for r in rows],
                      draft_four_prose_gates=176, formatting_approvals=0, prior_English_conversation_comparisons=0,
                      every_draft_is_logical_paragraph_with_exact_source_ID_andmacro_counts=True,
                      draft_checks_not_native_formatting_orstored_integration_approval=True,
                      incidental_legacy_line_exposure=bindings['incidental_legacy_dialogue_exposure'],
                      remaining_terms=['Carlo shipboard role', 'Cesare ship name', 'remaining ship/tutorial terms'],
                      B156_cinematic_FE_geometry_andspeaker_continuity_before_formatting=True,
                      new_editorial_completion_credit=0, completed_records=8856, new_ROMs=0, new_emulator_runs=0,
                      new_images=0, guide_photo_collection_discontinued=True, no_main_promotion=True,
                      all_other_ledger_keys_exact=True, ledger_before_sha256=sha(before), ledger_backup=str(backup),
                      registry_unchanged_sha256=sha(registry_before), current_candidate_sha256=sha(candidate.read_bytes()),
                      full_goal_complete=False,
                      evidence={str(p):sha(p.read_bytes()) for p in [*DRAFTS, ROOT/'complete_clean_meanings_checkpoint.json', ROOT/'native_identity_and_item_checkpoint_v1.json', ROOT/'B151_B155_place_terms.json', DOC, Path(__file__)]})
    assert ledger_path.read_bytes() == before
    ledger_path.write_bytes(encode_ledger(ledger))
    assert load(ledger_path) == ledger and registry.read_bytes() == registry_before
    checkpoint['ledger_after_sha256'] = sha(ledger_path.read_bytes())
    save(target, checkpoint)
    print('Checkpoint:642 clean meanings/176 English drafts;all unrelated ledger keys andrelease state exact;8856 completions unchanged.')
