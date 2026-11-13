"""Approve viewed complete B201 native paragraphs and two retained menu labels;no release credit."""
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B201_layout_v4 as codec
from dk4tool.dialogue.lil_B201_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_native_approval_v5925')
INPUT=Path('translations/lil_B201_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B201_editorial_manuscript_v5.json')
MENU=Path('translations/lil_B201_choice_manuscript_v1.json')
MENU_OUT=Path('translations/lil_B201_choice_manuscript_v2.json')
FONT=Path('work/analysis/lil_B201_fonts_v5923c/all24_progressive_FE_native_planes_and192_alignment_cases.json')
MENU_PROOF=Path('work/analysis/lil_B201_choices_v5924/B201_C880/original_choice_decoder_VM_geometry_and_native_pixels.json')
ROW_REASONS={
5:'The direct wear observation is one natural complete English row;the source two-row wrap carries no extra pause or meaning.',
8:'The skeptical Really? and subjective answer fit together in one complete row. Keep the breezy existing response without importing the Japanese wrap.',
14:'Two complete-word rows preserve the free-replacement joke. The comma before the intact of course? tag is a natural comic/discourse boundary;forcing free/of together creates a stranded group elsewhere. No authored break or weak-boundary exception is used.',
18:'Three complete beats preserve the flustered denial,the discount concession,and exact initial300000 offer. Source four-row staging is unnecessary in English.',
21:'Three rows preserve the repeated interruption and the full incredulous question with explicit Admiral. Keep thinking of paying that as one complement rather than splitting thinking/of;all words remain.',
24:'Two complete natural groups retain the already quoted300000 challenge and complete Rope\'s worth30,000 tops valuation. The original four Japanese rows are not English timing controls.',
27:'The stammered protest/one-of-a-kind claim and exact200000 offer fit in two fluent English rows rather than four Japanese rows.',
41:'Two rows preserve the concession/final100000 offer and separate complete minimum-price claim. No floor or amount is changed to match the source three rows.',
59:'The existing complete assurance fits on one English row. No literal source wrap or added delivery detail is needed.',
77:'The complete source player macro,Charm and exact+1 fit on one FE row in the established status style. Preserve all source information without Japanese row staging.',
80:'Carlo,the approved Wits stat and exact+1 fit on one complete FE row. The old singular wit is corrected without adding or losing an attribute.',
94:'The existing shocked question and pointed browsing complaint fit naturally on one row. Preserve tone without the source-only wrap.',
100:'The refusal-only player macro,Spirit and exact+1 fit on one complete FE row. Preserve the permanent attribute distinction from Mood.'}

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not MENU_OUT.exists()
    doc=deepcopy(read(INPUT));font=read(FONT);menu=deepcopy(read(MENU));mp=read(MENU_PROOF)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[201]
    assert font['new_native_alignment_calls']==0 and font['exact_input_byte_identical_reused_native_alignment_cases']==192
    assert len(font['negative_controls'])==24 and all(r['rejected'] for r in font['negative_controls'])
    for sheet in font['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert sha(Path(mp['visual_review_sheet']).read_bytes())==mp['visual_review_sheet_sha256']
    assert mp['six_original_VM_selection_and_cancel_cases_pass'] and mp['eight_complete_native_style_label_planes_pass']
    cases={r['id']:r for r in font['cases']};invariants=[];notes=[]
    initial=read('translations/lil_B201_editorial_manuscript_v2.json');initial_byid={r['id']:r for r in initial['records']}
    changed=[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);isFE=row['kind']=='system-FE';p=profile_for(arm,block,'FE-paper' if isFE else 'progressive');case=cases[row['id']]
        enc=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        assert enc.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(enc.formatted_markup)
        for token in [b'FI',b'FA',b'FO']:assert raw[1:].count(token)==enc.encoded[1:].count(token)
        assert case['complete_native_independent228x48_plane_equal' if isFE else 'complete_native_independent216x64_plane_equal']
        assert case['one_native_page_consumes_complete_target'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert sum(len(r['cases']) for r in case['current_native_macro_pipelines'])==8
        if isFE:assert all(c['null_source_actor'] for v in case['current_native_macro_pipelines'] for c in v['cases'])
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        assert not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries')
        different=any(i['code']=='line-break-count' for i in qa['issues']);idx=row['source_record_index']
        if different:
            assert idx in ROW_REASONS
            reason=ROW_REASONS[idx]+' Only source/English row count differs;no complete-glyph,bounds,pagination,control,macro,weak-ending,orphan or blank-page exemption.'
            row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=row['id'],reason=reason))
        else:row.pop('qa_waivers',None);row.pop('qa_waiver_reason',None)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code']!='line-break-count']
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1].replace('{MACRO:FI}','FI')==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        previous=initial_byid[row['id']];assert row['english']==previous['english'] and row['source_hex']==previous['source_hex']
        if row['compiled_hex']!=previous['compiled_hex']:changed.append(idx)
        row['review']['formatting']=True
        row.update(native_font_case=case,current_text_hex=row['current_hex'],native_formatting_consumer='FE-paper' if isFE else 'progressive',
            current_complete_native_display_pending=False,native_plane_verified_not_actual_English_gameplay=True,
            status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending')
        if idx==11:row['native_layout_retention_reason']='Four complete word rows retain the contradiction,replacement question and full reported-power claim. The balanced some / mysterious power continuation is preferable to a premature row containing only They say;the original noun group remains protected and every glyph is present.'
        invariants.append(dict(id=row['id'],source_selector=raw[0],semantic_tokens_and_runtime_macros_exact=True,encoded_sha256=sha(enc.encoded),visible_lines=qa['visible_lines']))
    assert len(notes)==13 and changed==[21,24,34,86,97]
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':12,'retain-wording':12}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Invalid formatter accepted:'+label)
    for consumer,selector in [('progressive',19),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),
            ('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),
            ('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    for row in menu['records']:
        assert row['english']==row['previous_logical_label'] and row['fresh_retained_wording_justification']
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']);row['review']['formatting']=True
        row.update(native_menu_proof=str(MENU_PROOF),native_menu_proof_sha256=sha(MENU_PROOF.read_bytes()),
            current_complete_native_display_pending=False,native_plane_verified_not_actual_English_gameplay=True)
    doc.update(formatting_review_pending=False,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending',
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),current_font_oracle='scripts/lil_current_font_oracles_v5918.py',
        current_font_oracle_sha256=sha(Path('scripts/lil_current_font_oracles_v5918.py').read_bytes()),all24_current_native_previews_viewed_on_three_sheets=True,
        no_record_specific_ordinary_boundary_exception_required=True,previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),
        source_bound_phrase_layout_changed_only_indices=changed,typed_choice_manuscript=str(MENU_OUT),full_goal_complete=False)
    menu.update(formatting_review_pending=False,status=doc['status'],native_choice_proof=str(MENU_PROOF),native_choice_proof_sha256=sha(MENU_PROOF.read_bytes()),
        source_two_options_and_indices_geometry_complete_first_final_glyphs_VM_cancel_and_eight_style_planes_approved=True,
        actual_English_choice_association_and_relocated_reference_still_pending=True,previous_manuscript=str(MENU),previous_manuscript_sha256=sha(MENU.read_bytes()))
    validate_natural_dialogue_batch(doc)
    save(MENU_OUT,menu);doc['typed_choice_manuscript_sha256']=sha(MENU_OUT.read_bytes());save(OUTPUT,doc)
    ROOT.mkdir(parents=True);save(ROOT/'all26_source_prose_current_native_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        choice_manuscript=str(MENU_OUT),choice_manuscript_sha256=sha(MENU_OUT.read_bytes()),all26_five_gates_approved=True,
        paragraph_invariants=invariants,thirteen_individual_rowcount_reasons=notes,formatter_negatives=negatives,
        changed_phrase_layout_indices=changed,all24_words_controls_native_metrics_guards_phase_and_four_row_limits_unchanged=True,
        complete_native_planes=24,covered_native_alignment_cases=192,new_native_alignment_cases_in_final_reconciliation=0,
        exact_byte_identical_reused_native_alignment_cases=192,source_consumer_negatives=24,
        source_two_menu_labels_six_VM_cases_eight_native_style_planes_viewed=True,viewed_sheets=font['review_sheets']+[dict(path=mp['visual_review_sheet'],sha256=mp['visual_review_sheet_sha256'])],
        English_scene_relocation_and_registered_release_pending=True,all26_objects_uncredited=True,
        existing_Trader_role_retention_context_bound_no_name_bytes_or_duplicate_name_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [INPUT,OUTPUT,MENU,MENU_OUT,FONT,MENU_PROOF,Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B20126 five-gate native approvals:24complete planes/192 exact-reused alignments,24consumer/28formatter negatives,one two-label menu/eightstyleplanes.13 individual rowcount reasons;five phrase layouts improved. Relocation/English actual/release pending;zero credit.')
