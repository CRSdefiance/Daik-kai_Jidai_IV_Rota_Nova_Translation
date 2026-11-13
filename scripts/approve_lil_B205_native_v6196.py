"""Seal all17 individual editorial gates;relocation,English gameplay and integration remain pending."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dataclasses import replace
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B205_profile_v2 import profile_for
from dk4tool.dialogue import lil_B205_layout_v2 as codec
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_native_approval_v6196')
INPUT=Path('translations/lil_B205_editorial_manuscript_v4.json');OUTPUT=Path('translations/lil_B205_editorial_manuscript_v5.json')
FONT=Path('work/analysis/lil_B205_fonts_v6195/all17_progressive_FE_native_planes_and136_alignment_cases.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));font=read(FONT);im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[205]
    assert len(font['cases'])==17 and font['current_original_macro_alignment_calls']==136 and len(font['negative_controls'])==18 and all(r['rejected'] for r in font['negative_controls'])
    assert font['complete_progressive_planes']==10 and font['complete_FE_logical_and_physical_planes']==7 and font['new_emulator_runs']==0
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    initial={r['id']:r for r in read('translations/lil_B205_editorial_manuscript_v2.json')['records']};cases={r['id']:r for r in font['cases']};notes=[];invariants=[]
    for row in doc['records']:
        fe=row['kind']=='system-FE';raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block,'FE-paper' if fe else 'progressive');encoded=codec.encode_relocatable_dialogue(raw,row['english'],p);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p);case=cases[row['id']]
        assert encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup)
        assert row['english']==initial[row['id']]['english'] and row['source_hex']==initial[row['id']]['source_hex']
        assert all(raw[1:].count(m)==encoded.encoded[1:].count(m)==0 for m in [b'FI',b'FA',b'FO'])
        assert case['one_native_page_consumes_complete_target'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and sum(len(v['cases']) for v in case['current_native_macro_pipelines'])==8
        if fe:assert case['complete_native_independent228x48_plane_equal'] and case['original_null_actor_consumer_preserved'] and case['input_objects_canaries_and_all_glyphs_complete']
        else:assert case['complete_native_independent216x64_plane_equal'] and case['original_progressive54020_consumer_preserved']
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code']!='line-break-count']
        if any(i['code']=='line-break-count' for i in qa['issues']):
            assert row['source_record_index'] in [17,51,59] and row['qa_waivers']==['line-break-count'] and row['qa_waiver_reason'];notes.append(dict(id=row['id'],reason=row['qa_waiver_reason']))
        else:assert not row.get('qa_waivers')
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        row['review']['formatting']=True;row.update(native_font_case=case,native_formatting_consumer='FE-paper' if fe else 'progressive',current_text_hex=row['current_hex'],current_complete_native_display_pending=False,native_plane_verified_not_actual_English_gameplay=True,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending')
        invariants.append(dict(id=row['id'],selector=raw[0],source_and_all_English_words_exact_since_prose_v2=True,compiled_sha256=sha(encoded.encoded),visible_lines=qa['visible_lines']))
    assert len(notes)==3 and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':8,'retain-wording':9}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Unsafe formatter accepted:'+label)
    for consumer,selector in [('progressive',15),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('wrong228-host-capacity',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),formatting_review_pending=False,status='source-context-prose-current-native-format-approved;relocation-English-actual-registered-release-pending',native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),current_font_oracle='scripts/lil_current_font_oracles_v6122.py',current_font_oracle_sha256=sha(Path('scripts/lil_current_font_oracles_v6122.py').read_bytes()),all17_current_native_previews_viewed=True,all17_objects_still_uncredited=True,caught_weak_ending_first_plan_and_all_successors_preserved=True,source_bound_phrase_layout_changed_only_index=67,no_words_metrics_native_viewports_guards_phase_or_four_row_limits_changed_since_prose_v2=True,ordinary_boundary_exception_required=False)
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True);save(ROOT/'all17_source_prose_current_native_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),all17_five_gates_approved=True,revised=8,retained=9,paragraph_invariants=invariants,three_individual_rowcount_reasons=notes,formatter_negative_controls=negatives,source_consumer_negative_controls=font['negative_controls'],complete_native_planes=17,progressive_planes=10,FE_planes=7,covered_native_alignment_cases=136,new_final_native_alignment_cases=136,exact_input_reused_native_alignment_cases=0,viewed_sheets=[dict(**s,viewed_after_image_return=True) for s in font['review_sheets']],native_228px_bitmap_and_measured216px_text_capacity_distinguished=True,no_word_changes_since_prose_v2_or_unreviewed_waivers=True,all17_uncredited_pending_relocation_actual_English_and_registered_release=True,source_names_and_five_echo_pairs_bound_without_new_name_credit=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,FONT,Path('work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json'),Path(__file__)]}));print('B20517 five-gate approvals:8 revisions/9 retentions;136 fresh alignments,18 source and28 formatter negatives. Relocation/actual English/release and credit pending.')
