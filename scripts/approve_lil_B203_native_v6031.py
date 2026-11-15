"""Approve source/prose/native formatting;keep relocation,English gameplay and release pending."""
from copy import deepcopy
from dataclasses import replace
from collections import Counter
from pathlib import Path
from dk4tool.dialogue import lil_B203_layout_v2 as codec
from dk4tool.dialogue.lil_B203_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_native_approval_v6031')
INPUT=Path('translations/lil_B203_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B203_editorial_manuscript_v4.json')
FONT=Path('work/analysis/lil_B203_fonts_v6030/all22_progressive_FE_native_planes_and176_alignment_cases.json')
ROW_REASONS={
28:'The complete common-name identification That is caterpillar fungus fits on one English row. Preserve the substance and measured explanation without importing the Japanese staging break.',
35:'The complete statement about prized medicinal use in China fits on one English row. Retain the cultural context and statement scope without a forced English break.',
54:'The complete concise answer about a book on medicinal ingredients fits on one English row. Preserve its reference-work subject and omit an unspoken title;the source line break is ordinary staging.',
70:'The startled/hesitant Huh? Well... stays together,and the complete I just wanted to read that book follows on a second row. This preserves all reading-admission words and avoids the isolated that book tail;Japanese uses three rows but supplies no third English dramatic boundary.',
77:'The laugh and complete100-gold acceptance fit naturally on one English row. Preserve the exact amount and generous counteroffer rather than copying the Japanese line break.',
80:'The established concise FI: Charm +1! system notation fits on one modal row. Preserve the FE null-actor consumer,FI substitution and exact stat/increment;Japanese explanatory grammar needs no corresponding forced row.'}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font=read(FONT);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[203]
    assert len(font['cases'])==22 and font['current_original_macro_alignment_calls']==176 and font['new_native_alignment_calls']==16 and font['exact_input_byte_identical_reused_native_alignment_cases']==160
    assert len(font['negative_controls'])==22 and all(r['rejected'] for r in font['negative_controls']) and font['complete_progressive_planes']==21 and font['complete_FE_logical_and_physical_planes']==1
    prior=read(font['prior_native_proof']);assert sha(Path(font['prior_native_proof']).read_bytes())==font['prior_native_proof_sha256']
    assert [a['sha256']==b['sha256'] for a,b in zip(font['review_sheets'],prior['review_sheets'],strict=True)]==[True,True,False]
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    cases={r['id']:r for r in font['cases']};initial={r['id']:r for r in read('translations/lil_B203_editorial_manuscript_v2.json')['records']};invariants=[];notes=[];changed=[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);isFE=row['kind']=='system-FE';p=profile_for(arm,block,'FE-paper' if isFE else 'progressive');case=cases[row['id']]
        enc=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        assert enc.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(enc.formatted_markup)
        assert all(raw[1:].count(m)==enc.encoded[1:].count(m) for m in [b'FI',b'FA',b'FO'])
        assert case['one_native_page_consumes_complete_target'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and sum(len(r['cases']) for r in case['current_native_macro_pipelines'])==8
        if isFE:assert case['complete_native_independent228x48_plane_equal'] and case['original_null_actor_consumer_preserved'] and case['input_objects_canaries_and_all_glyphs_complete']
        else:assert case['complete_native_independent216x64_plane_equal'] and case['original_progressive54020_consumer_preserved']
        assert not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries')
        if any(i['code']=='line-break-count' for i in qa['issues']):
            reason=ROW_REASONS[row['source_record_index']]+' Only source/English row count differs;no glyph,bounds,pagination,control,macro,weak-ending,orphan or blank-page exemption.'
            row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=row['id'],reason=reason))
        else:row.pop('qa_waivers',None);row.pop('qa_waiver_reason',None)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code']!='line-break-count']
        logical=row['english'].split('}',1)[1]
        for macro in ['FI','FA','FO']:logical=logical.replace('{MACRO:'+macro+'}',macro)
        if row['editorial_decision']=='retain-wording':assert logical==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        old=initial[row['id']];assert row['english']==old['english'] and row['source_hex']==old['source_hex']
        if row['compiled_hex']!=old['compiled_hex']:changed.append(row['source_record_index'])
        row['review']['formatting']=True
        row.update(native_font_case=case,current_text_hex=row['current_hex'],native_formatting_consumer='FE-paper' if isFE else 'progressive',current_complete_native_display_pending=False,native_plane_verified_not_actual_English_gameplay=True,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending')
        if row['source_record_index']==67:row['native_layout_review_reason']='The complete chuckle precedes the intact Your companion seems to want it clause. Avoid stranding seems before a short to want it tail. The automatic source-bound phrase planner changes no words,widths,guards or limits;this complete-utterance first row is deliberate rather than a narrowed viewport.'
        if row['source_record_index']==70:row['native_layout_review_reason']=ROW_REASONS[70]+' Automatic phrase grouping changes no words,widths,guards,limits or authored breaks.'
        invariants.append(dict(id=row['id'],source_selector=raw[0],semantic_tokens_and_source_macro_counts_exact=True,encoded_sha256=sha(enc.encoded),visible_lines=qa['visible_lines']))
    assert len(notes)==6 and changed==[67,70] and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':9,'retain-wording':13}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Invalid formatter accepted:'+label)
    for consumer,selector in [('progressive',76),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(consumer+'-'+label,lambda bad=bad,raw=raw,r=r:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-'+tag,lambda tag=tag,raw=raw,r=r,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda raw=raw,r=r,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    doc.update(formatting_review_pending=False,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending',native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),current_font_oracle='scripts/lil_current_font_oracles_v5918.py',current_font_oracle_sha256=sha(Path('scripts/lil_current_font_oracles_v5918.py').read_bytes()),all22_current_native_previews_viewed_or_hash_identical_to_viewed_sheets=True,no_record_specific_ordinary_boundary_exception_required=True,source_bound_phrase_layout_changed_only_indices=[67,70],all22_objects_still_uncredited=True)
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'all22_source_prose_current_native_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),all22_five_gates_approved=True,paragraph_invariants=invariants,six_individual_rowcount_reasons=notes,formatter_negatives=negatives,changed_phrase_layout_indices=changed,all22_words_controls_native_metrics_guards_phase_and_four_row_limits_unchanged=True,complete_native_planes=22,progressive_planes=21,FE_planes=1,covered_native_alignment_cases=176,new_native_alignment_cases_in_final_reconciliation=16,exact_byte_identical_reused_native_alignment_cases=160,source_consumer_negatives=22,
        viewed_sheets=[dict(**s,viewed_after_image_return=True,original_detail=True,reused_exact_viewed_previous_sheet=i<2) for i,s in enumerate(font['review_sheets'])],English_scene_relocation_and_registered_release_pending=True,all22_objects_uncredited=True,source_defined_names_and_unspoken_item_title_scope_bound_no_new_name_or_widget_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [INPUT,FONT,Path(font['prior_native_proof']),Path(__file__),Path('scripts/refine_lil_B203_phrases_v6029.py')]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B20322 five-gate native approvals:nine revisions/13 retentions,22 planes/176 covered alignments/22 consumer and28 formatter negatives. Six row reasons;R67/R70 phrases improved. Still uncredited pending English scene/reference/release.')
