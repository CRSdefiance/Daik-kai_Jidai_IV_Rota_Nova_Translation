"""Approve complete native B202 paragraphs;leave actual English and release pending."""
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B202_layout_v2 as codec
from dk4tool.dialogue.lil_B202_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_native_approval_v5979')
INPUT=Path('translations/lil_B202_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B202_editorial_manuscript_v4.json')
FONT=Path('work/analysis/lil_B202_fonts_v5978/all19_progressive_native_planes_and152_alignment_cases.json')
ROW_REASONS={
20:'The complete spotting exclamation and urgent stop command fit naturally on one English row. Keep both beats and their rough urgency without copying the Japanese staging break.',
55:'The examination cue and complete quoted Glassmaking Guide title fit together on one English row. This retains both pauses and all title words while avoiding a premature title break imported from Japanese.',
58:'The casual Hm and complete might-as-well advice fit on one English row. The source line break supplies no distinct English dramatic pause;keep the concise existing line.'}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font=read(FONT);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[202]
    assert len(font['cases'])==19 and font['current_original_macro_alignment_calls']==152 and font['new_native_alignment_calls']==8 and font['exact_input_byte_identical_reused_native_alignment_cases']==144 and len(font['negative_controls'])==21 and all(r['rejected'] for r in font['negative_controls'])
    prior=read(font['prior_native_proof']);assert sha(Path(font['prior_native_proof']).read_bytes())==font['prior_native_proof_sha256'];assert [a['sha256']==b['sha256'] for a,b in zip(font['review_sheets'],prior['review_sheets'],strict=True)]==[False,True,True]
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    cases={r['id']:r for r in font['cases']};initial={r['id']:r for r in read('translations/lil_B202_editorial_manuscript_v2.json')['records']};invariants=[];notes=[];changed=[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block);case=cases[row['id']];enc=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        assert enc.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(enc.formatted_markup)
        assert all(raw[1:].count(m)==enc.encoded[1:].count(m)==0 for m in [b'FI',b'FA',b'FO'])
        assert case['complete_native_independent216x64_plane_equal'] and case['one_native_page_consumes_complete_target'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and sum(len(r['cases']) for r in case['current_native_macro_pipelines'])==8
        assert not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries')
        if any(i['code']=='line-break-count' for i in qa['issues']):
            reason=ROW_REASONS[row['source_record_index']]+' Only source/English row count differs;no complete-glyph,bounds,pagination,control,macro,weak-ending,orphan or blank-page exemption.';row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=row['id'],reason=reason))
        else:row.pop('qa_waivers',None);row.pop('qa_waiver_reason',None)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code']!='line-break-count']
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        old=initial[row['id']];assert row['english']==old['english'] and row['source_hex']==old['source_hex']
        if row['compiled_hex']!=old['compiled_hex']:changed.append(row['source_record_index'])
        row['review']['formatting']=True;row.update(native_font_case=case,current_text_hex=row['current_hex'],native_formatting_consumer='progressive',current_complete_native_display_pending=False,native_plane_verified_not_actual_English_gameplay=True,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending')
        if row['source_record_index']==13:row['native_layout_review_reason']='The complete handoff sentence ends the first row;Use it however you like! stays intact on the second. This replaces the isolated you like! continuation without authored line breaks,prose cuts,changed metrics or a weak-boundary waiver. A shorter complete-sentence row is appropriate to these two distinct utterances.'
        invariants.append(dict(id=row['id'],source_selector=raw[0],semantic_tokens_and_source_macro_absence_exact=True,encoded_sha256=sha(enc.encoded),visible_lines=qa['visible_lines']))
    assert len(notes)==3 and changed==[13] and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':6,'retain-wording':13}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Invalid formatter accepted:'+label)
    p=profile_for(arm,block);r=next(r for r in doc['records'] if r['source_selector']==18);raw=bytes.fromhex(r['source_hex'])
    for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(label,lambda bad=bad:codec.encode_relocatable_dialogue(raw,r['english'],bad))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})));assert len(negatives)==14
    doc.update(formatting_review_pending=False,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending',native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),current_font_oracle='scripts/lil_current_font_oracles_v5918.py',current_font_oracle_sha256=sha(Path('scripts/lil_current_font_oracles_v5918.py').read_bytes()),all19_current_native_previews_viewed_or_hash_identical_to_viewed_sheets=True,no_record_specific_ordinary_boundary_exception_required=True,source_bound_phrase_layout_changed_only_indices=[13],all19_objects_still_uncredited=True)
    doc['review_gates']['formatting']=True;validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'all19_source_prose_current_native_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),all19_five_gates_approved=True,paragraph_invariants=invariants,three_individual_rowcount_reasons=notes,formatter_negatives=negatives,changed_phrase_layout_indices=changed,all19_words_controls_native_metrics_guards_phase_and_four_row_limits_unchanged=True,complete_native_planes=19,covered_native_alignment_cases=152,new_native_alignment_cases_in_final_reconciliation=8,exact_byte_identical_reused_native_alignment_cases=144,source_consumer_negatives=21,
        viewed_sheets=[dict(**s,viewed_after_image_return=True,original_detail=True,reused_exact_viewed_previous_sheet=i>0) for i,s in enumerate(font['review_sheets'])],
        English_scene_relocation_and_registered_release_pending=True,all19_objects_uncredited=True,source_defined_names_and_spoken_item_title_bound_no_new_name_or_widget_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [INPUT,FONT,Path(font['prior_native_proof']),Path(__file__),Path('scripts/refine_lil_B202_permission_wrap_v5977.py')]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B20219 five-gate native approvals:six revisions/13 retentions,19 planes/152 covered alignments/21 consumer and14 formatter negatives. Three row reasons;R13 phrase improved. Still uncredited pending English scene/reference/release.')
