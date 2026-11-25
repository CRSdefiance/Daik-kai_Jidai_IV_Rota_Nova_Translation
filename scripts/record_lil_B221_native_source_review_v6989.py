"""Record viewed native/source evidence without approving English gameplay or a name asset."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B221_native_source_view_v6989')
DOC=Path('translations/lil_B221_editorial_manuscript_v1.json')
PLAN=Path('work/analysis/lil_B221_layout_v6976c/fourteen_whole_paragraph_plans_no_macros_no_prose_changes.json')
FONT=Path('work/analysis/lil_B221_native_pages_v6980c/all14_paragraphs16_complete_native_pages112_alignments.json')
NAMES=Path('work/analysis/lil_B221_name_planes_v6981/three_actors_six_getters_nine_name_component_planes36_alignments.json')
MENU=Path('work/analysis/lil_B221_choices_v6977/three_original_choice_decoders_nine_modal_cases_twelve_complete_label_planes.json')
QA=Path('work/analysis/lil_B221_base_QA_v6982b/all14_base_QA_diagnostics_before_any_scoped_classification.json')
ACTUAL=Path('work/analysis/lil_B221_source_actual_v6988/two_source_choices_all14_speeches_all30_commands_complete_bodies_names_and_returns.json')
WRAP=Path('work/analysis/lil_B221_wrap_tools_v6985/one_source_bound_auxiliary_boundary_no_prose_or_page_change.json')

NOTES={
5:'The full-width opening keeps the abrupt call and challenge together, with the complete object our square on the continuation. The ordinary through/our wrap does not change the phrasal verb or add a deliberate pause.',
8:'The two brief practical questions form one natural reply and need no inherited Japanese staging break.',
11:'The complete knowledge question is one readable row and remains directly associated with both Yes/No labels.',
27:'The sarcastic army description keeps chivalrous army and Holy Land intact. Fighting/to is an ordinary complete-word boundary before the purpose infinitive; the question remains one utterance.',
33:'The attributed European account remains a single thought. Apparently/call and that/fought are ordinary complete-word adverb/verb and relative-clause boundaries; preserving every word and full rows is preferable to adding a short row solely to avoid the function word that.',
39:'The emphatic lie accusation is followed by a local-knowledge sentence. Here/know and Crusaders/were are ordinary subject/predicate boundaries; the shared answer remains complete.',
42:'The short idiomatic explanation question is one complete spoken beat.',
46:'The complete report, wealth question and plunder/slaughter examples stay on page1; the full anything-went report and hearsay tag stay together on page2. Six generated rows reflect the word-preserving coherent page boundary, not a narrowed physical viewport. About/it, after/this and wealth/right are ordinary complete-word continuations in this complete conversational paragraph.',
49:'The angry objection and local hero declaration remain one paragraph. History/twisted, passed/down and hero/is are ordinary complete-word continuations, without a new dramatic pause or a shorter global width; the complete clause and contrast remain in the same native page.',
52:'The name echo and direct identity question fit one row and preserve Lil\'s lack of recognition.',
56:'The great-figure introduction precedes the complete Islamic-history and more-than-driving-back explanation. Figure/in and far/more are ordinary complement and comparative continuations; Islamic history stays intact without inventing a title.',
60:'The complete first statement keeps all three humane-conduct examples, including peace terms, on page1. The entire following praise stays on page2, keeping dirty tricks intact. The shorter treatment line preserves the complete prisoners-and-civilians phrase in the following row; four physical rows per page and the whole wording remain unchanged.',
63:'The strength-and-character question and two enthusiastic exclamations remain two coherent rows instead of copying the source\'s extra staging row.',
67:'The remembered hearsay and conditional suggestion remain four full rows. The exact reviewed had/gone boundary is an ordinary auxiliary/complement wrap that keeps gone missing together without an extra row. Heard/that and follow/his keep their complete complements on subsequent rows; no rumor becomes a guaranteed find.',
}
ROW_REASONS={
8:'Two short source-staged questions become one complete English row without a lost beat.',
27:'The favorable-account challenge is two English rows while preserving the collective army,chivalry,Holy Land and checking tag.',
33:'The alternative attributed report uses three English rows rather than copying four Japanese rows; Europe and apparently remain.',
39:'The emphatic accusation and complete local-knowledge claim naturally occupy three English rows rather than four source rows.',
46:'All140 English characters and the complete reported allegation remain across six generated rows/two original four-row pages. The source has four Japanese rows; no prose is cut to imitate that count.',
60:'All139 English characters,three humane-conduct examples and the separate praise remain across six generated rows/two original four-row pages. No prose or display geometry is changed merely to preserve the four Japanese rows.',
63:'The complete admiration and exclamations occupy two English rows rather than the source\'s three staging rows.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan,font,names,menu,qa,actual=map(read,[DOC,PLAN,FONT,NAMES,MENU,QA,ACTUAL])
    assert font['manuscript_sha256']==plan['manuscript_sha256']==qa['manuscript_sha256']==sha(DOC.read_bytes())
    assert font['layout_plan_sha256']==qa['layout_plan_sha256']==sha(PLAN.read_bytes())
    assert font['complete_native_pages']==16 and font['logical_compiled_input_alignment_cases']==112
    assert font['fresh_compiled_alignment_cases']==4 and font['exact_alignment_cases_reused']==108
    assert names['name_literal_alignment_count']==36 and names['complete_name_component_plane_count']==9
    assert menu['native_selection_cancel_cases']==9 and menu['complete_current_and_reviewed_style_label_planes']==12
    assert actual['actual_source_unique_speeches']==14 and actual['actual_speech_observations']==26
    assert actual['actual_complete_source_body_holds']==actual['actual_complete_name_holds']==102
    assert actual['incomplete_sampled_body_holds']==0 and actual['all_jobs_terminal_and_reaped']
    assert actual['all30_stored_commands_executed_in_union']
    issues=[i for r in qa['records'] for i in r['base_QA']['issues']]
    assert not [i for i in issues if i['severity'] in ['warning','error']]
    info=[r for r in qa['records'] if any(i['code']=='line-break-count' for i in r['base_QA']['issues'])]
    assert len(info)==7
    viewed=[]
    for index,row in enumerate(font['review_sheets']):
        p=Path(row['path']);assert sha(p.read_bytes())==row['sha256']
        if index<2:
            prior=Path(str(p).replace('native_pages_v6980c','native_pages_v6980b'))
            assert p.read_bytes()==prior.read_bytes()
            viewed.append(dict(path=str(prior),sha256=sha(prior.read_bytes()),note='Individually viewed; final sheet is byte-identical.'))
        viewed.append(dict(path=str(p),sha256=sha(p.read_bytes()),note='Final native body sheet; individually viewed or exact-byte reuse as specified.'))
    for spec in [names['review_sheet'],dict(path=menu['visual_review_sheet'],sha256=menu['visual_review_sheet_sha256'])]:
        assert sha(Path(spec['path']).read_bytes())==spec['sha256'];viewed.append(dict(**spec,note='Individually viewed complete native names or menu labels.'))
    panes=[]
    for version in actual['versions']:
        for spec in version['review_sheets']+[version['transition_sheet']]:
            assert sha(Path(spec['path']).read_bytes())==spec['sha256'];viewed.append(dict(path=spec['path'],sha256=spec['sha256'],note='Individually returned and viewed source capture sheet.'))
        for index,panel in enumerate(version['source_speech_observations']):
            spec=version['review_sheets'][index//6]
            overview=Image.open(spec['path']).convert('RGB');photo=panel['selected_capture']
            assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256']
            raw=Image.open(photo['path']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
            cell=index%6;x=cell%3*520+4;y=cell//3*416+24
            assert overview.crop((x,y,x+512,y+384)).tobytes()==raw.tobytes()
            panes.append(dict(choice=version['selected_original_option'],id=panel['id'],frame=photo['frame'],original_capture=photo['path'],source_sheet=spec['path'],whole_192px_lower_screen_crop_pixel_equal=True))
    rows=[]
    for row in plan['records']:
        index=int(row['id'].rsplit('R',1)[1]);source=next(r for r in doc['records'] if r['id']==row['id'])
        assert index in NOTES
        boundaries=[dict(after_line=i+1,last_word=a.split()[-1],next_first_word=b.split()[0],native_page_boundary=(i+1)%4==0,
            reason=(plan['page_boundary_reasons'][row['id']] if (i+1)%4==0 else NOTES[index]))
            for i,(a,b) in enumerate(zip(row['lines'],row['lines'][1:]))]
        rows.append(dict(id=row['id'],source_reference=source['source_reference'],current_reference=source['current_reference'],
            paragraph=source['english'],formatted_markup=row['formatted_markup'],line_lengths=row['line_lengths'],
            ordinary_boundary_reasons=boundaries,row_count_reason=ROW_REASONS.get(index),
            complete_paragraph_read_in_exchange=True,native_pages=row['expected_native_pages'],
            English_actual_button_progression_and_final_stored_reference_pending=True))
    assert {int(r['id'].rsplit('R',1)[1]) for r in info}==set(ROW_REASONS)
    assert len(panes)==26
    ROOT.mkdir(parents=True)
    save(ROOT/'all_native_pages_names_menu_both_source_choices_and_exact_wrap_reasons_viewed.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),paragraph_plan=str(PLAN),paragraph_plan_sha256=sha(PLAN.read_bytes()),
        actual_source_proof=str(ACTUAL),actual_source_proof_sha256=sha(ACTUAL.read_bytes()),
        records=rows,viewed_images=viewed,all26_source_overview_panes_complete_and_pixel_equal=panes,
        all16_final_native_body_pages_nine_name_planes_and_menu_sheet_viewed=True,
        all8_source_sheets_individually_returned_and_viewed=True,
        source_Yes_highlight0_to_R27_and_No_highlight1_to_R33_visually_confirmed=True,
        source_normal_ends0_0_and0_1_and_both_normal_Amsterdam_ports6310_viewed=True,
        actual_source_all14_speeches102_bodies102_current_headers30_commands_union=True,
        native_code_checks_and_actual_source_captures_are_separate=True,
        original_QA_all_diagnostics_preserved_zero_errors_zero_warnings_seven_info_reasons=True,
        exact_R67_had_gone_auxiliary_boundary_reason=str(WRAP),exact_R67_had_gone_auxiliary_boundary_reason_sha256=sha(WRAP.read_bytes()),
        original_failed_probes_and_all_earlier_plans_retained=True,
        all_English_dialogue_formatting_gates_remain_false=True,
        English_two_page_buttons_final_stored_relocation_policy_and_release_pending=True,
        Square_Shopkeeper_current_rendering_is_not_approval_of_its_localization=True,
        separate_ten_Shopkeeper_proposals_shared_native_target_actual_and_registered_layer_pending=True,
        full_catalogue_UI_unvisited_no_global207_name_approval=True,
        no_new_ROM_name_asset_registry_ledger_or_duplicate_review_credit=True,
        visual_review_pending=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,FONT,NAMES,MENU,QA,ACTUAL,WRAP,Path(__file__)]}))
    print(dict(native_pages=16,name_planes=9,source_sheets=8,source_crop_checks=26,
        ordinary_boundaries=sum(len(r['ordinary_boundary_reasons']) for r in rows),info_reasons=7,
        English_actual_and_registered_release_pending=True,credit=0))
