"""Record all642 drafts and42 comparison decisions without adding completion credit."""
import copy
import gzip
import os
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.editorial_ledger_storage_v1 import encode_ledger

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
MANUSCRIPT = Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v1.json')
DOC = Path('docs/editorial_hodram_B151_B170_prose_20261102.md')
SUMMARY = ('B151–B170:all642 clean meanings andEnglish drafts sealed before current-ROM extraction;642 exact current bindings. '
           'First42 whole-exchange comparisons:22 proposed revisions/20 wording retentions,40 complete four-prose-gate passes;'
           'two Abkhaz/Abhaz localization questions open,600 comparisons remain. Two current B153 lines are still Japanese. '
           'Purser/room labels/Venice bound;separate Japanese Elysion code literal andB156 cinematic geometry remain. '
           'All formatting/visual/stored/gameplay/release gates pending;no credit,ROM orimages. '
           '8856 completed/current7fb6f6d7/main unchanged;full scope preserved;no guide photos.')


if __name__ == '__main__':
    target = ROOT / 'source_prose_progress_checkpoint_v2.json'
    assert not target.exists()
    doc = load(MANUSCRIPT)
    drafts = ROOT / 'all642_clean_English_drafts_v1.json'
    original = load(drafts)
    assert original['total_editorial_objects'] == doc['source_andcurrent_exact_reference_bindings'] == len(doc['records']) == 642
    assert (doc['current_comparisons'],doc['proposed_revisions'],doc['wording_retentions'],doc['complete_four_gate_comparisons'],doc['place_name_questions']) == (42,22,20,40,2)
    assert all(r['review']['formatting'] is False for r in doc['records'])
    current = Path('work/analysis/Hodram_B151_B170_current_20261102/current_effective.json')
    objects = Path('work/analysis/Hodram_B151_B170_current_objects_20261102/current_objects.json')
    bound = load(current)
    assert bound['records'] == bound['original_current_catalogue_lookups'] == 634
    assert sum(r['current_catalogue_selected'] for g in bound['groups'] for r in g['records']) == 0
    assert len(load(objects)['choice_records']) == 8
    registry = Path('translations/release_stack.json')
    registry_before = registry.read_bytes()
    assert sha(registry_before) == 'dde90af7920d7562851e16858cb9fef923d25268691c8d9fa1ced156ecd9265a'
    candidate = Path(bound['current_ROM'])
    assert sha(candidate.read_bytes()) == bound['current_ROM_sha256'] == '7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    ledger_path = Path('translations/editorial_review_current_v1.json')
    before = ledger_path.read_bytes()
    ledger = load(ledger_path)
    assert ledger['records_editorially_completed'] == 8856 and ledger['records_revised_and_integrated'] == 5540
    assert ledger['retained_wordings_editorially_completed'] == 3316
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 8859
    prior = dict(ledger)
    backup = ROOT / 'ledger_before_642_drafts_42_comparisons.json.gz'
    if not backup.exists():
        backup.write_bytes(gzip.compress(before,mtime=0))
    assert gzip.decompress(backup.read_bytes()) == before
    key = 'Hodram_B151_B170_clean_next_20261102'
    entry = copy.deepcopy(ledger[key])
    entry.update(logical_English_drafts=642,remaining_localized_drafts=0,current_English_conversation_comparisons=42,
                 remaining_current_English_comparisons=600,proposed_revisions=22,wording_retentions=20,
                 complete_four_gate_comparisons=40,open_localization_record_questions=2,
                 no_current_English_dialogue_exposure=False,no_current_ROM_English_dialogue_extraction=False,
                 current_English_extracted_with642_exact_source_current_bindings=True,
                 all642_drafts_saved_before_current_ROM_extraction=True,
                 complete_source_first_drafts=str(drafts),complete_source_first_drafts_sha256=sha(drafts.read_bytes()),
                 current_speech_bindings=str(current),current_caption_bindings=str(objects),
                 contextual_manuscript=str(MANUSCRIPT),contextual_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
                 source_draft_checkpoint=str(target),previous_source_draft_checkpoint=entry['source_draft_checkpoint'],
                 source_first_draft_prose_gates_not_final_current_comparison=True,
                 separate_Elysion_code_literal_still_Japanese_pending_consumer_scope=True,
                 B156_cinematic_geometry_andall642_formatting_pending=True,
                 scoped_names_andAbkhaz_Abhaz_cross_consumer_localization_pending=True,
                 documentation=str(DOC),prior_latest_checkpoint=ledger['latest_checkpoint'])
    entry['source_first_English_drafts'] = {p:h for p,h in original['evidence'].items() if p.endswith('_clean_English_drafts_v1.json') or p.endswith('eight_clean_caption_English_drafts_v1.json')}
    assert len(entry['source_first_English_drafts']) == 9
    ledger[key] = entry
    ledger['latest_checkpoint'] = SUMMARY
    assert all(ledger[k] == v for k,v in prior.items() if k not in [key,'latest_checkpoint'])
    dependencies = [drafts,MANUSCRIPT,current,objects,DOC,ROOT/'remaining_role_ship_and_Venice_terms_v1.json',
                    ROOT/'four_ship_room_terms_current_bindings.json',Path('translations/hodram_B151_B155_contextual_decisions_v1.json'),Path(__file__)]
    checkpoint = dict(summary=SUMMARY,source_meanings=642,logical_English_drafts=642,remaining_localized_drafts=0,
                      current_source_bindings=642,current_catalogue_lookups=634,typed_caption_bindings=8,
                      contextual_comparisons=42,remaining_current_comparisons=600,proposed_revisions=22,wording_retentions=20,
                      complete_four_gate_comparisons=40,open_localization_record_questions=2,formatting_approvals=0,
                      untranslated_current_Japanese_findings=['DK4_MES_B153_R0009','DK4_MES_B153_R0016'],
                      source_speech_extraction_session=62257,source_speech_extraction_terminal_exit=0,object_binder_terminal_exit=0,
                      no_jobs_left_running_from_this_checkpoint=True,new_ROMs=0,new_emulator_runs=0,new_images=0,
                      native_offline_binding_is_not_gameplay=True,new_editorial_completion_credit=0,completed_records=8856,
                      all_other_ledger_keys_exact=True,ledger_before_sha256=sha(before),ledger_backup=str(backup),
                      registry_unchanged_sha256=sha(registry_before),current_candidate_sha256=sha(candidate.read_bytes()),
                      guide_photo_collection_discontinued=True,no_main_promotion=True,full_goal_complete=False,
                      evidence={str(p):sha(p.read_bytes()) for p in dependencies})
    assert ledger_path.read_bytes() == before
    # Keep the old complete ledger intact until a fully written replacement is ready.
    encoded = encode_ledger(ledger)
    staged = ledger_path.with_name('editorial_review_current_v1.pending_B151_B170_prose.json')
    assert staged.resolve().parent == ledger_path.resolve().parent
    if staged.exists():
        assert staged.read_bytes() == encoded
    else:
        staged.write_bytes(encoded)
    assert staged.read_bytes() == encoded and ledger_path.read_bytes() == before
    os.replace(staged,ledger_path)
    assert load(ledger_path) == ledger and registry.read_bytes() == registry_before
    checkpoint['ledger_after_sha256'] = sha(ledger_path.read_bytes())
    save(target,checkpoint)
    print('Checkpoint:642 drafts/current bindings;42 comparisons,22 revisions/20 retentions,40 four-gate passes/two name questions. All prior credit/releases unchanged.')
