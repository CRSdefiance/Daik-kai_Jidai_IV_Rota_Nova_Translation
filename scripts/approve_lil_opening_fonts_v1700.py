"""Approve49 inspected native font layouts;relocation/build/scene gates stay open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_review_v1700')
OUT=Path('translations/lil_opening_editorial_manuscript_v2.json')
FONTS=Path('work/analysis/lil_opening_fonts_v1699b/native_font_proof.json')
MACRO=Path('work/analysis/lil_opening_macro_v1698d/original_story_macro_proof.json')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_context_v1697_1676')


if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    fonts,macro=read(FONTS),read(MACRO);doc=deepcopy(read('translations/lil_opening_editorial_manuscript_v1.json'))
    assert len(fonts['cases'])==49 and fonts['native_macro_alignment_cases']==196
    assert len(macro['all196_paragraph_alignment_cases'])==196
    assert fonts['all_continuation_visible_origins_equal_first_row_zero']
    assert len(fonts['review_sheets'])==7
    for sheet in fonts['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    report_path=CAP/'capture_report.json';report=read(report_path)
    assert report['frames']==6000 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']==fonts['ROM_sha256']==macro['ROM_sha256']
    assert not report.get('battery_save_preloaded') and not any(k.startswith('synthetic_') and v for k,v in report.items())
    assert read('work/analysis/lil_opening_context_v1697/terminal.json')['terminal']
    for row in report['frames_captured']:assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        assert len(Path(row['path']).read_bytes())==row['bytes']==0x400000 and sha(Path(row['path']).read_bytes())==row['sha256']
    ROOT.mkdir(parents=True)
    review={'ROM_sha256':fonts['ROM_sha256'],'source_manuscript':'translations/lil_opening_editorial_manuscript_v1.json',
        'native_font_proof':str(FONTS),'native_font_proof_sha256':sha(FONTS.read_bytes()),
        'native_macro_proof':str(MACRO),'native_macro_proof_sha256':sha(MACRO.read_bytes()),
        'all7_sheets_and49_panels_actually_viewed':True,'full_source_and_dialogue_sequence_reread':True,
        'approved_visible_line_breaks_full_first_last_letters_bounds_and_zero_origins':True,
        'all43_revisions_and6_retentions_keep_prose_exact_to_reviewed_V1694_draft':True,
        'no_English_shortening_or_manual_breaks_to_fit_old_allocations':True,
        'all15_line_break_count_warnings_are_automatic_English_vs_Japanese_line_counts':True,
        'new_native_profile_only_runtime_bound_post_layer_playable_delivery_supported':True,
        'source_cursor_calibration':'Existing modal_cursor_guard.buffered_helper matches actual runtime;one LF guard space is compensated to x0. The rejected V1699 assumption of6px visible indent is retained.',
        'existing_V1676_opening_context_capture':{'report':str(report_path),'sha256':sha(report_path.read_bytes()),'frames':6000,
            'ordinary_no_save_New_Game':True,'stable_opening_captures_actually_viewed':[6000],
            'not_gameplay_verification_of_the_revised_draft':True},
        'remaining_gates':['complete source-bound external/interior reference map for resized B22',
            'registered cumulative post-layer with exact runtime and source locks','exact clean-input patch reconstruction',
            'fixture-free startup regression','actual full49-line revised opening,speakers,pagination,scene transitions and Bruges handoff'],
        'no_new_completed_entries':True,'full_goal_complete':False,'producer_sha256':sha(Path(__file__).read_bytes())}
    save(ROOT/'visual_and_native_review.json',review)
    doc.update(encoder='dialogue-relocatable-v1',dialogue_profile=fonts['profile'],formatting_review_pending=False,
        status='49-source-prose-native-font-approved;relocation-registered-integration-and-actual-pending',
        native_macro_proof=str(MACRO),native_macro_proof_sha256=sha(MACRO.read_bytes()),
        native_font_proof=str(FONTS),native_font_proof_sha256=sha(FONTS.read_bytes()),
        visual_review=str(ROOT/'visual_and_native_review.json'),visual_review_sha256=sha((ROOT/'visual_and_native_review.json').read_bytes()),
        required_runtime_ARM9_sha256=fonts['ARM9_sha256'],no_playable_release_without_runtime_binding=True)
    doc.pop('strict_build_validation_rejects_draft_until_formatting_review')
    by_id={r['id']:r for r in fonts['cases']}
    for row in doc['records']:
        case=by_id[row['id']]
        assert case['complete_native_and_independent216x64_font_planes_equal']
        assert case['complete_leading_trailing_letters_bounds_and_blank_paper_verified']
        row['english']=row['english'].replace('{PAD}','')
        row['review']['formatting']=True
        row['compiled_hex']=case['encoded_hex'];row['formatted_markup']=case['formatted_markup']
        row['formatting_evidence']=str(ROOT/'visual_and_native_review.json')
        warnings=[d for d in case['diagnostics'] if d['severity']=='warning']
        assert all(d['code']=='line-break-count' for d in warnings)
        if warnings:
            row['qa_waivers']=['line-break-count']
            row['qa_waiver_reason']='Automatic English word wrapping intentionally replaces Japanese line divisions. Complete native/independent font planes and this whole panel were reviewed;no authored breaks,missing letters,or extra pages.'
        check=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],get_dialogue_profile(doc['dialogue_profile']))
        assert check.encoded.hex()==row['compiled_hex']
    validate_natural_dialogue_batch(doc)
    save(OUT,doc)
    save(ROOT/'approval_receipt.json',{'approved_manuscript':str(OUT),'sha256':sha(OUT.read_bytes()),
        'all49_prose_native_font_and_visual_review_gates_approved':True,'revised_draft_not_integrated_or_completed':True,
        'runtime_required_sha256':fonts['ARM9_sha256'],'formatting_errors_remaining':0,'original_allocation_does_not_limit_new_prose':True,
        'full_goal_complete':False})
    print('49 current-native/independent font layouts and all7 sheets approved;v2 keeps complete prose. Relocation,registered ROM/patch and full revised gameplay remain pending.')
