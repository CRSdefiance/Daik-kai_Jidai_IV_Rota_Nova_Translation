"""Record viewed32 native matrices and guard tests;page72 actual advance remains an explicit gate."""
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.maria_B97_profile import profile_for
from dk4tool.dialogue import maria_B97_layout_v2 as codec
from dk4tool.dialogue.profiles import get_dialogue_profile
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_native_review_v5016')
INPUT=Path('translations/maria_B97_editorial_manuscript_v3.json')
OUTPUT=Path('translations/maria_B97_editorial_manuscript_v4.json')
FONT=Path('work/analysis/maria_B97_fonts_v5013b/all32_font_matrices_256_alignments_and_source72_page_projection.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc,font=deepcopy(read(INPUT)),read(FONT)
    assert font['manuscript_sha256']==sha(INPUT.read_bytes()) and len(font['cases'])==32 and font['current_original_macro_alignment_calls']==256
    assert len(font['negative_controls'])==24 and all(r['rejected'] for r in font['negative_controls']) and len(font['review_sheets'])==5
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks[97]
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256'] and sha(Path(doc['current_ROM']).read_bytes())==font['candidate_sha256']==doc['current_ROM_sha256']
    for p in font['review_sheets']:assert sha(Path(p['path']).read_bytes())==p['sha256']
    cases={r['id']:r for r in font['cases']};invariants=[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);paged=row['source_record_index']==72;consumer='FE-paper' if row['kind']=='system-FE' else ('progressive-two-page' if paged else 'progressive');p=profile_for(arm,block,consumer,raw)
        encoded=codec.encode_relocatable_dialogue(raw,row['english'],p);case=cases[row['id']]
        assert encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'] and semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup)
        assert all(raw.count(m)==encoded.encoded.count(m) for m in [b'FI',b'FA',b'FO'])
        assert case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['all_visible_origins_zero_and_current_width_bounds_exact']
        for preview in case['previews']:assert sha(Path(preview['path']).read_bytes())==preview['sha256']
        assert sha(Path(case['whole_font_plane']).read_bytes())==case['whole_font_plane_sha256'] and sum(len(v['cases']) for v in case['current_native_macro_pipelines'])==8
        assert all(row['review'][g] for g in ['source','context','localization','naturalness'])
        row['review']['formatting']=not paged
        row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_font_case=case,native_formatting_consumer=consumer,native_font_matrix_verified_not_actual_gameplay=True,current_complete_native_display_pending=paged,status='source-prose-and-font-matrix-reviewed;actual-page-advance-relocation-release-open' if paged else 'source-prose-native-format-approved;actual-reference-release-open')
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        invariants.append(dict(id=row['id'],source_selector=raw[0],semantic_tokens_and_source_macros_exact=True,font_matrix_verified=True,actual_A_continuation_pending=paged))
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':23,'retain-wording':9}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(dict(case=label,rejected=True))
        else:raise AssertionError('Unsafe formatter accepted:'+label)
    for consumer,index in [('progressive',13),('FE-paper',5),('progressive-two-page',72)]:
        r=next(r for r in doc['records'] if r['source_record_index']==index);raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,consumer,raw)
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':8})),('unscoped-base',get_dialogue_profile('maria-story-shared-events-live'))]:
            reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{85})))
    assert len(negatives)==42
    soft=[]
    for index in [46,78,114]:
        row=next(r for r in doc['records'] if r['source_record_index']==index);raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block)
        exact=codec.audit_relocatable_dialogue_record(raw,row['english'],p);assert exact.get('reviewed_ordinary_soft_wrap')
        changed=codec.audit_relocatable_dialogue_record(raw,row['english']+' Truly.',p)
        assert 'reviewed_ordinary_soft_wrap' not in changed and not any(i['code']=='reviewed-ordinary-soft-wrap' for i in changed['issues'])
        changedsource=codec.audit_relocatable_dialogue_record(raw+b' ',row['english'],p)
        assert 'reviewed_ordinary_soft_wrap' not in changedsource and not any(i['code']=='reviewed-ordinary-soft-wrap' for i in changedsource['issues'])
        soft.append(dict(id=row['id'],exact_full_source_and_paragraph_and_boundary_only=True,changed_source_and_paragraph_do_not_inherit_acceptance=True))
    doc.update(formatting_review_pending=True,status='32-source-prose-current-font-matrices-reviewed;source72-actual-page-and-all-release-gates-open',native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),all32_current_font_matrices_and33_native_or_projected_panels_viewed=True,reviewed_sheets_count=5,source72_two_pages_are_offline_projection_until_fresh_A_advance=True,no_global_font_width_guard_or_historical_compiler_change=True,source_prose_or_completion_credit_added=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all32_viewed_matrices_42_formatter_negatives_and_one_actual_page_gate.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),invariants=invariants,viewed_sheets=[dict(p,viewed_in_full_current_turn=True) for p in font['review_sheets']],formatter_negatives=negatives,exact_soft_wrap_scope_negative_cases=soft,source_consumer_negatives=24,initial_native_macro_alignments=256,one_page_progressive=30,one_FE=1,two_page_projected_record='DK4_MES_B97_R0072',native_pagination_not_yet_approved=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,not_full_batch_actual_or_release_approval=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('32 matrices/33 panels on five sheets viewed;42 formatter negatives and three exact soft-wrap scope checks pass. R72 actual A continuation still blocks full formatting approval;zero credit.')
