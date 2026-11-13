"""Seal20 native-format reviews while keeping references/release separate."""
from pathlib import Path
from copy import deepcopy
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_seville_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_font_approval_v2715')
OLD=Path('translations/lil_seville_encounter_editorial_manuscript_v2.json');DOC=Path('translations/lil_seville_encounter_editorial_manuscript_v3.json')
MENU=Path('translations/lil_seville_choices_editorial_draft_v1.json');MENU_OUT=Path('translations/lil_seville_choices_editorial_draft_v2.json')
FONT=Path('work/analysis/lil_Seville_fonts_v2712c/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Seville_FE_v2713/current_FE_macro_font_and_typed_paper_proof.json')
CHOICE=Path('work/analysis/lil_Seville_choice_v2714/original_choice_decoder_VM_geometry_and_native_pixels.json')
BODY=Path('work/analysis/lil_Seville_body_probe_v2708b/body_only_layout_and_native_fonts.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,MENU_OUT]);doc,menu,font,fe,choice,body=map(read,[OLD,MENU,FONT,FE,CHOICE,BODY])
    assert font['manuscript_sha256']==fe['manuscript_sha256']==sha(OLD.read_bytes()) and choice['manuscript_sha256']==sha(MENU.read_bytes())
    assert len(font['cases'])==17 and font['current_original_macro_alignment_calls']==136 and len(font['all18_full_QA_reports'])==18 and len(font['negative_controls'])==10
    assert fe['current_original_null_actor_macro_alignment_cases']==8 and fe['one_native_page_consumes_complete_target'] and fe['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']
    assert fe['historical_calibration']['complete_current_native_ink_and_blank_mask_equal'] and fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter'] and fe['native_plane_sha256']==fe['old_current_text_native_plane_sha256']
    assert choice['six_original_VM_selection_and_cancel_cases_pass'] and choice['eight_complete_native_style_label_planes_pass'] and choice['stored_option_indices_and_original_selection_return_values_preserved']
    oldbody={r['id']:r for r in body['records']}
    assert all(c['whole_native_plane_sha256']==oldbody[c['id']]['whole_native_font_plane_sha256'] and c['preview_sha256']==oldbody[c['id']]['preview_sha256'] for c in font['cases'])
    assert [s['sha256'] for s in font['review_sheets']]==[s['sha256'] for s in body['review_sheets']]
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    cases=[]
    for c in font['cases']:
        item=deepcopy(c);item.update(consumer='progressive',macro_cases=[v for p in c['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=c['whole_native_plane_sha256'],whole_native_independent_font_plane_exact=True);cases.append(item)
    cases.append(dict(id=fe['id'],consumer='FE-paper',encoded_hex=fe['encoded_hex'],formatted_markup=fe['formatted_markup'],macro_cases=[v for p in fe['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=fe['native_plane_sha256'],whole_native_independent_font_plane_exact=True,logical_geometry=[228,48],physical_row_advance=16,native_glyphs=fe['native_glyphs'],preview=fe['preview'],preview_sha256=fe['preview_sha256']))
    assert len(cases)==18 and sum(len(c['macro_cases']) for c in cases)==144;byid={c['id']:c for c in cases}
    ROOT.mkdir(parents=True);merged=ROOT/'all18_native_macro_font_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),cases=cases,
        current_original_macro_alignment_calls=144,all18_current_native_planes_and_complete_glyphs_pass=True,all3_progressive_sheets_identical_to_previously_viewed_body_sheets=True,one_new_FE_and_one_choice_sheet_viewed=True,FE_paper_calibrates_to_historical_actual_hold_without_whole_RAM_overlay=True,
        record115_phrase_flow_review='Read as a complete qualified strength comparison followed by temporary advice. Compiler continuations between we/are andour/strength preserve both clauses andthe full object. No authored breaks,isolated final predicate,lost word oradditional warning waiver;the ordinary full QA andall ordered native glyphs pass.',
        evidence={str(p):sha(p.read_bytes()) for p in [FONT,FE,CHOICE,BODY,Path('dk4tool/dialogue/lil_seville_profile.py')]},actual_Seville_IDs=[],new_emulator_runs=0,reference_map_representative_and_registered_release_pending=True,full_goal_complete=False))
    for row in doc['records']:
        case=byid[row['id']];consumer='FE-paper' if row['kind']=='system-FE' else 'progressive';compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,blocks[row['block']],consumer))
        assert compiled.encoded.hex()==case['encoded_hex'];row.update(compiled_hex=case['encoded_hex'],native_font_case=case,native_formatting_consumer=consumer,status='source-prose-and-current-native-formatting-approved;references-representative-release-pending',actual_Seville_gameplay_visited=False)
        row['review']['formatting']=True
    for row in menu['records']:
        row['review']['formatting']=True;row.update(status='source-prose-and-current-native-choice-format-approved;references-representative-release-pending',native_choice_proof=str(CHOICE),native_choice_proof_sha256=sha(CHOICE.read_bytes()),actual_Seville_selection_not_claimed=True)
    doc.update(formatting_review_pending=False,status='current-native-format-approved;reference-map-representative-and-registered-integration-pending',scoped_B28_B29_profile_still_required=False,scoped_profile_module='dk4tool/dialogue/lil_seville_profile.py',scoped_profile_module_sha256=sha(Path('dk4tool/dialogue/lil_seville_profile.py').read_bytes()),
        native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_choice_proof=str(CHOICE),all18_current_native_cases_and144_macro_calls_pass=True,all5_review_sheets_viewed_or_identical_to_previously_viewed=True,registered_integration_pending=True,reference_map_pending=True,
        previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()))
    menu.update(formatting_review_pending=False,status='current-native-choice-format-approved;references-representative-and-registered-release-pending',native_choice_proof=str(CHOICE),native_choice_proof_sha256=sha(CHOICE.read_bytes()),previous_manuscript=str(MENU),previous_manuscript_sha256=sha(MENU.read_bytes()))
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(OLD)['records']] and [r['english'] for r in menu['records']]==[r['english'] for r in read(MENU)['records']]
    validate_natural_dialogue_batch(doc);validate_natural_dialogue_batch({**menu,'encoder':'dialogue-relocatable-v1'})
    save(DOC,doc);save(MENU_OUT,menu)
    sheets=font['review_sheets']+[dict(path=fe['review_sheet'],sha256=fe['review_sheet_sha256']),dict(path=choice['visual_review_sheet'],sha256=choice['visual_review_sheet_sha256'])]
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(MENU_OUT),choices_sha256=sha(MENU_OUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),current_native_macro_calls=144,progressive_planes=17,FE_planes=1,choice_style_planes=8,VM_selection_cancel_cases=6,
        all20_formatting_gates_true=True,English_and_source_controls_unchanged=True,all5_review_sheets=sheets,actual_Seville_IDs=[],new_emulator_runs=0,no_reference_or_registered_release_completion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('20formatting gates sealed:18native panels/144current macro calls,8choice planes/6VMreturns,10scope controls. Prose unchanged;references/representative/release pending,zero completion credit.')
