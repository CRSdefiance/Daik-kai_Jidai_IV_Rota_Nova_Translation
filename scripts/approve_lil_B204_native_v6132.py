"""Seal source,context,prose and complete native formatting;actual/release remain pending."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B204_profile_v2 import profile_for
from dk4tool.dialogue import lil_B204_layout_v4 as codec
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_native_approval_v6132')
INPUT=Path('translations/lil_B204_editorial_manuscript_v5.json');OUTPUT=Path('translations/lil_B204_editorial_manuscript_v6.json')
FONT=Path('work/analysis/lil_B204_fonts_v6131/all20_progressive_FE_native_planes_and160_alignment_cases.json')
ROW_REASONS={
9:'The nearby-attraction question and complete boredom/walk explanation occupy two natural English rows. Retain Ma\'am without kinship and Jam\'s casual spoken fragment;do not copy the three Japanese staging rows.',
13:'The complete eastward lord\'s-castle answer fits one English row. The source filler and staging break are not a second English thought.',
16:'The recognition beat is complete on the first row;Sounds good stays intact and the full local-castles intention follows. Three English rows preserve the cross-language joke without adding a manual break or shortening words.',
19:'Lil\'s complete Jam! call and exasperated whereabouts question fit one English row. No separate dramatic paragraph is required by the Japanese staging.',
22:'The full casual apology and heavy-object excuse fit one English row. Preserve every retained word without carrying over the Japanese break.',
29:'Jam\'s cocky identification is one complete row;the explicit Japan boast and genuine-article flourish occupy the second. Every source intention survives without the Japanese three-row staging.',
36:'The theft qualification forms one English row and the full departure instruction another. Retain the suspicion and urgency without a forced third row.',
40:'The complete compliance and brief-wait request fit one English row. The idiomatic minute is a casual wait expression,not a newly asserted measured event duration.',
48:'The complete irritated demand and racket complaint fill two English rows. The morning detail is retained and dawn/sleep are not invented;English grammar need not follow the source row count.',
52:'The missing shachihoko,the frightened letter introduction and explicit foreign-writing fact occupy three complete English rows. Preserve the two stammers without forcing the Japanese two-row staging or clipping the script detail.',
55:'The startled missing-ornament statement,the complete disaster reaction and Find that thief order occupy three natural English rows. The source four-row staging is not an extra English page or pause.',
72:'The casual sign-off,explicit Signed marker and full Jam Jack Ludwyan signature fit one native row. The source indentation is evidence of a signature,not permission for authored spaces or premature wrapping.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font=read(FONT);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[204]
    assert len(font['cases'])==20 and font['current_original_macro_alignment_calls']==160 and font['new_native_alignment_calls']==40 and font['exact_input_byte_identical_reused_native_alignment_cases']==120
    assert font['changed_source_indices']==[16,33,45,55,69] and len(font['negative_controls'])==24 and all(r['rejected'] for r in font['negative_controls'])
    assert font['complete_progressive_planes']==16 and font['complete_FE_logical_and_physical_planes']==4
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert sha(Path(font['prior_native_proof']).read_bytes())==font['prior_native_proof_sha256']
    initial={r['id']:r for r in read('translations/lil_B204_editorial_manuscript_v1.json')['records']};cases={r['id']:r for r in font['cases']};notes=[];invariants=[]
    for row in doc['records']:
        isFE=row['kind']=='system-FE';raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block,'FE-paper' if isFE else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p);case=cases[row['id']]
        assert encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup)
        assert row['english']==initial[row['id']]['english'] and row['source_hex']==initial[row['id']]['source_hex']
        assert all(raw[1:].count(m)==encoded.encoded[1:].count(m)==0 for m in [b'FI',b'FA',b'FO'])
        assert case['one_native_page_consumes_complete_target'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and sum(len(v['cases']) for v in case['current_native_macro_pipelines'])==8
        if isFE:assert case['complete_native_independent228x48_plane_equal'] and case['original_null_actor_consumer_preserved'] and case['input_objects_canaries_and_all_glyphs_complete']
        else:assert case['complete_native_independent216x64_plane_equal'] and case['original_progressive54020_consumer_preserved']
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code']!='line-break-count']
        index=row['source_record_index']
        if any(i['code']=='line-break-count' for i in qa['issues']):
            reason=ROW_REASONS[index]+' Only source/English row-count differences are accepted. No weak-ending,phrase,glyph,bounds,control,macro,orphan,blank-page or pagination waiver.'
            row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=row['id'],reason=reason))
        else:row.pop('qa_waivers',None);row.pop('qa_waiver_reason',None)
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        row['review']['formatting']=True;row.update(native_font_case=case,native_formatting_consumer='FE-paper' if isFE else 'progressive',current_text_hex=row['current_hex'],current_complete_native_display_pending=False,native_plane_verified_not_actual_English_gameplay=True,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending')
        invariants.append(dict(id=row['id'],selector=raw[0],source_and_all_English_words_exact_since_prose_v1=True,compiled_sha256=sha(encoded.encoded),visible_lines=qa['visible_lines']))
    assert len(notes)==12 and set(ROW_REASONS)=={int(x['id'].rsplit('R',1)[1]) for x in notes}
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':12,'retain-wording':8}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Unsafe formatter accepted:'+label)
    for consumer,selector in [('progressive',11),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('wrong228-host-capacity',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),formatting_review_pending=False,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending',native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),current_font_oracle='scripts/lil_current_font_oracles_v6122.py',current_font_oracle_sha256=sha(Path('scripts/lil_current_font_oracles_v6122.py').read_bytes()),all20_current_native_previews_viewed=True,all20_objects_still_uncredited=True,failed_wider_FE_host_plan_and_all_successors_preserved=True,source_bound_phrase_layout_changed_only_indices=[16,33,45,55,69],no_words_metrics_native_viewports_guards_phase_or_four_row_limits_changed=True,ordinary_boundary_exception_required=False)
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'all20_source_prose_current_native_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),all20_five_gates_approved=True,revised=12,retained=8,paragraph_invariants=invariants,twelve_individual_rowcount_reasons=notes,formatter_negative_controls=negatives,source_consumer_negative_controls=font['negative_controls'],complete_native_planes=20,progressive_planes=16,FE_planes=4,covered_native_alignment_cases=160,new_final_native_alignment_cases=40,exact_input_reused_native_alignment_cases=120,changed_phrase_indices=[16,33,45,55,69],viewed_sheets=[dict(**s,viewed_after_original_detail_image_return=True) for s in font['review_sheets']],native_228px_bitmap_and_measured216px_text_capacity_distinguished=True,no_word_changes_or_unreviewed_waivers=True,all20_uncredited_pending_relocation_actual_English_and_registered_release=True,source_names_roles_and_full_signature_bound_without_new_name_credit=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,FONT,Path(font['prior_native_proof']),Path('work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json'),Path(__file__)]}))
    print('B20420 five-gate approvals:12 revisions/8 retentions,20 complete planes,160 covered alignments,24 source and28 formatter negatives. Actual English/reference/release and completion credit pending.')
