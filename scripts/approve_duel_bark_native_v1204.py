"""Approve native formatting after exact-font visual review; gameplay stays open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_native_review_v1204')
OUT=Path('translations/duel_bark_editorial_manuscript_v2.json')


def main():
    assert not ROOT.exists() and not OUT.exists()
    source=Path('translations/duel_bark_editorial_manuscript_v1.json');doc=deepcopy(read(source))
    native_path=Path('work/analysis/duel_bark_native_v1202/native_font_scope_verification.json')
    copies_path=Path('work/analysis/duel_bark_copies_v1203/changed_block_copy_verification.json')
    escape_path=Path('work/analysis/duel_bark_escape_regression_v1203/original_direct_pipeline.json')
    native,copies,escape=map(read,(native_path,copies_path,escape_path))
    assert len(native['cases'])==36 and len(native['direct_numeric_exclusion_cases'])==36
    assert len(copies['complete_native_copies'])==92 and len(escape['all13_direct_pipeline_cases'])==13
    assert native['ARM9_sha256']==copies['ARM9_sha256']==escape['ARM9_sha256']
    assert native['COMMON_sha256']==copies['COMMON_sha256']==escape['COMMON_sha256']
    ROOT.mkdir(parents=True)
    visual=ROOT/'visual_review.json'
    save(visual,{'sheet':native['review_sheet'],'sheet_sha256':native['review_sheet_sha256'],
        'all16_new_reactions_visually_inspected':True,
        'natural_reading_complete_first_last_letters_uniform_margins_and_source_crops_accepted':True,
        'no_authored_alignment_or_manual_breaks':True,
        'compiler_selected_short_opening_exclamations_are_deliberate_complete_utterances':True,
        'no_weak_function_word_row_end_or_orphaned_final_word_observed':True,
        'single_line_vertical_centering_and_two_three_line_origin_follow_original_duel_contract':True,
        'actual_gameplay_still_pending':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    for row in doc['records']:
        case=next(c for c in native['cases'] if c['message_ID']==row['message_id'])
        row['review']['formatting']=True
        row.update(status='native-source-prose-and-format-approved;original-gameplay-pending',
            formatted_lines=case['lines'],native_font_proof=str(native_path),native_font_proof_sha256=sha(native_path.read_bytes()))
    doc.update(formatting_review_pending=False,status='native-approved;experimental-integration-and-gameplay-pending',
        supersedes_manuscript=str(source),supersedes_manuscript_sha256=sha(source.read_bytes()),
        native_font_proof=str(native_path),native_font_proof_sha256=sha(native_path.read_bytes()),
        native_copy_proof=str(copies_path),native_copy_proof_sha256=sha(copies_path.read_bytes()),
        escape_regression_proof=str(escape_path),escape_regression_proof_sha256=sha(escape_path.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()),
        target_COMMON_sha256=native['COMMON_sha256'],target_ARM9_sha256=native['ARM9_sha256'])
    validate_natural_dialogue_batch(doc)
    save(OUT,doc)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_with_source_and_prose_pass']==1283 and ledger['records_editorially_completed']==1229
    drafts=ledger['active_source_prose_drafts'];key=str(source)
    assert key in drafts['manuscripts']
    drafts['manuscripts']=[str(OUT) if s==key else s for s in drafts['manuscripts']]
    subset=drafts['manuscript_record_subsets_pending'].pop(key);drafts['manuscript_record_subsets_pending'][str(OUT)]=subset
    ledger['duel_bark_prose_v1200'].update(manuscript=str(OUT),native_font_proof=str(native_path),
        native_copy_proof=str(copies_path),escape_regression_proof=str(escape_path),visual_review=str(visual),
        formatting_and_actual_pending=False,native_formatting_pass=True,actual_gameplay_pending=True,completed_entries=0)
    save(ledger_path,ledger)
    print('All16 native formatting gates approved;1283 prose-reviewed/1229 complete unchanged;actual gameplay open.',flush=True)


if __name__=='__main__':main()
