"""Seal 152 contextual/native-format reviews without release or gameplay credit."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_mediterranean_africa_profile import profile_for
from dk4tool.dialogue import lil_mediterranean_africa_layout_v3 as codec
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Mediterranean_Africa_font_approval_v2773')
OLD=Path('translations/lil_mediterranean_africa_editorial_manuscript_v3.json')
DOC=Path('translations/lil_mediterranean_africa_editorial_manuscript_v4.json')
MENU=Path('translations/lil_mediterranean_africa_choices_editorial_draft_v2.json')
MENU_OUT=Path('translations/lil_mediterranean_africa_choices_editorial_draft_v3.json')
FONT=Path('work/analysis/lil_Mediterranean_Africa_fonts_v2770/current_macro_QA_and_progressive_font_proof.json')
FE=Path('work/analysis/lil_Mediterranean_Africa_FE_v2771/current_FE_macro_font_and_typed_paper_proof.json')
CHOICE=Path('work/analysis/lil_Mediterranean_Africa_choices_v2772e/all3_typed_menus_native_proof.json')

def semantic_tokens(markup):
    tokens=parse_markup(markup)
    controls=[(t.kind,t.value) for t in tokens if t.kind not in ['text','line_break','align']]
    words=' '.join(''.join(t.value if t.kind=='text' else (' ' if t.kind=='line_break' else '{'+t.kind+':'+t.value+'}') for t in tokens).split())
    return controls,words

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,MENU_OUT])
    doc,menu,font,fe,choice=map(read,[OLD,MENU,FONT,FE,CHOICE])
    assert font['manuscript_sha256']==fe['manuscript_sha256']==sha(OLD.read_bytes())
    assert len(font['cases'])==145 and len(font['all146_full_QA_reports'])==146
    assert font['current_original_macro_alignment_calls']==1160 and font['newly_executed_current_macro_alignment_calls']==72 and font['reused_current_macro_alignment_calls']==1088
    assert font['all145_progressive_full_QA_and_complete_native_fonts_pass'] and len(font['negative_controls'])==7
    assert fe['current_original_null_actor_macro_alignment_cases']==8 and fe['one_native_page_consumes_complete_target'] and fe['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']
    assert fe['historical_calibration']['complete_current_native_ink_and_blank_mask_equal'] and fe['no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter']
    assert len(choice['menus'])==3 and choice['native_selection_cancel_cases']==18 and choice['complete_current_and_reviewed_style_label_planes']==24
    assert choice['all6_labels_source_order_pointers_counts_and_original_selection_results_preserved']
    for m in choice['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256']
        proof=read(m['proof']);assert proof['manuscript_sha256']==sha(MENU.read_bytes())
        assert proof['stored_option_indices_and_original_selection_return_values_preserved']
        for case in proof['current_and_reviewed_VM_and_font_cases']:
            for plane in case['all_four_style_label_planes']:
                assert plane['storage_padding_all_blank'] and plane['independent_complete_native_pixels_match']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(arm)==doc['required_runtime_ARM9_sha256']==font['ARM9_sha256']==fe['ARM9_sha256']
    original=read(font['reused_proof']);assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    sheets=[]
    changed_sheets={i//8 for i,c in enumerate(font['cases']) if not c.get('reused_current_native_case')}
    assert changed_sheets=={3,5,9,10,13,14,15,16}
    # All 19 original sheets, all eight changed successor sheets, FE and three menus were viewed.
    for i,s in enumerate(font['review_sheets']):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        if i not in changed_sheets:assert s['sha256']==original['review_sheets'][i]['sha256']
        sheets.append(dict(**s,review='viewed current sheet' if i in changed_sheets else 'hash-identical to viewed 2768 sheet'))
    sheets.append(dict(path=fe['review_sheet'],sha256=fe['review_sheet_sha256'],review='viewed FE target and historical tutorial calibration'))
    sheets.extend(dict(path=m['review_sheet'],sha256=m['review_sheet_sha256'],review='viewed current and reviewed labels') for m in choice['menus'])
    assert len(sheets)==23 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    cases=[]
    for c in font['cases']:
        cases.append(dict(**c,consumer='progressive',macro_cases=[v for p in c['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=c['whole_native_plane_sha256'],whole_native_independent_font_plane_exact=True))
    cases.append(dict(id=fe['id'],consumer='FE-paper',encoded_hex=fe['encoded_hex'],formatted_markup=fe['formatted_markup'],macro_cases=[v for p in fe['current_native_macro_pipelines'] for v in p['cases']],native_font_plane_sha256=fe['native_plane_sha256'],whole_native_independent_font_plane_exact=True,logical_geometry=[228,48],physical_row_advance=16,native_glyphs=fe['native_glyphs'],preview=fe['preview'],preview_sha256=fe['preview_sha256']))
    assert len(cases)==146 and sum(len(c['macro_cases']) for c in cases)==1168
    byid={c['id']:c for c in cases};invariants=[]
    for row in doc['records']:
        c=byid[row['id']];consumer='FE-paper' if row['kind']=='system-FE' else 'progressive'
        result=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,blocks[row['block']],consumer))
        assert result.encoded.hex()==c['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(result.formatted_markup)
        assert result.encoded[:1]==bytes.fromhex(row['source_presentation_prefix_hex']) and b'\0' not in result.encoded
        assert c['whole_native_independent_font_plane_exact']
        invariants.append(dict(id=row['id'],source_speaker_macro_order_and_complete_English_tokens_exact=True,encoded_sha256=sha(result.encoded)))
        row['review']['formatting']=True
        row.update(compiled_hex=c['encoded_hex'],native_font_case=c,native_formatting_consumer=consumer,record_index=row['current_record_index'],current_text_hex=row['current_hex'],status='source-prose-current-native-format-approved;reference-representative-release-pending')
    negatives=[]
    row=doc['records'][0];raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']])
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
        reject(label,lambda p=p:codec.encode_relocatable_dialogue(raw,row['english'],p))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:
        reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,row['english']+tag,profile))
    assert len(negatives)==13
    for path,digest in codec.DEPENDENCIES.items():assert sha(Path(path).read_bytes())==digest
    for row in menu['records']:
        row['review']['formatting']=True;row.update(status='source-prose-current-native-choice-format-approved;reference-representative-release-pending',native_choice_proof=str(CHOICE),native_choice_proof_sha256=sha(CHOICE.read_bytes()),actual_selection_gameplay_claimed=False)
    assert Counter(r['editorial_decision'] for r in doc['records']+menu['records'])=={'revise':110,'retain-wording':42}
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==54 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    ROOT.mkdir(parents=True);merged=ROOT/'all146_native_macro_font_reconciliation.json'
    save(merged,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),cases=cases,current_original_macro_alignment_calls=1168,all146_current_native_planes_and_complete_glyphs_pass=True,all23_review_sheets=sheets,source_English_macro_control_invariants=invariants,source_bound_formatter_negatives=negatives,effective_planner_sha256=codec.EFFECTIVE_PLANNER_SHA256,global_helpers_unchanged=codec.DEPENDENCIES,evidence={str(p):sha(p.read_bytes()) for p in [FONT,FE,CHOICE,Path(doc['native_formatter_module']),Path(doc['scoped_profile_module'])]},actual_selected_Mediterranean_Africa_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,full_goal_complete=False))
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_font_proof=str(merged),native_font_proof_sha256=sha(merged.read_bytes()),native_progressive_proof=str(FONT),native_FE_proof=str(FE),native_choice_proof=str(CHOICE),formatting_review_pending=False,all146_native_planes_and1168_current_macro_calls_pass=True,all23_review_sheets_viewed_or_identical=True,formatter_phrase_flow_findings_resolved_without_waiver=True,status='source-prose-current-native-format-approved;reference-representative-release-pending')
    menu.update(previous_manuscript=str(MENU),previous_manuscript_sha256=sha(MENU.read_bytes()),formatting_review_pending=False,native_choice_proof=str(CHOICE),native_choice_proof_sha256=sha(CHOICE.read_bytes()),status='source-prose-current-native-choice-format-approved;reference-representative-release-pending')
    validate_natural_dialogue_batch(doc);validate_natural_dialogue_batch({**menu,'encoder':'dialogue-relocatable-v1'})
    save(DOC,doc);save(MENU_OUT,menu)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(MENU_OUT),choices_sha256=sha(MENU_OUT.read_bytes()),merged_native_proof=str(merged),merged_native_proof_sha256=sha(merged.read_bytes()),all152_five_review_gates_true=True,progressive_planes=145,FE_planes=1,current_macro_alignment_cases=1168,choice_style_planes=24,VM_selection_cancel_cases=18,formatter_negatives=13,narrow_line_count_notes=54,all23_review_sheets=sheets,actual_selected_Mediterranean_Africa_IDs=[],new_emulator_runs=0,reference_representative_registered_release_pending=True,source_prose_orcompletion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('152 formatting gates sealed:146 panels/1168 macro cases,24 choice planes/18 VM returns,13 formatter rejections. Reference,representative and registered release gates pending;zero completion credit.')
