"""Seal19 complete viewed native panels with individually justified layout retentions."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dataclasses import replace
from dk4tool.dialogue import lil_B200_layout_v2 as codec
from dk4tool.dialogue.lil_B200_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_native_approval_v5849')
INPUT=Path('translations/lil_B200_editorial_manuscript_v3.json')
OUTPUT=Path('translations/lil_B200_editorial_manuscript_v4.json')
FONT=Path('work/analysis/lil_B200_fonts_v5848/all19_progressive_FE_native_planes_and152_alignment_cases.json')
REFINEMENT=Path('work/analysis/lil_B200_phrase_layout_v5846/complete_courtesy_requests_and_source_bound_formatter_successors.json')
ROW_REASONS={
    17:'The two urgent source questions fit together on one complete native row. Preserve both questions and their urgency without treating a Japanese wrap as an English dramatic pause.',
    37:'The acknowledgment and polite apology form one natural short English row. Retain the recovering speaker\'s concise existing wording rather than a source-only line boundary.',
    47:'The call-back and doctor question fit as one natural English question. Preserve the profession question and ensuing denial without a pause imported from Japanese row staging.',
    54:'Two complete-word rows preserve the acknowledgment,modest token of thanks and full invitation to accept. The noun-complement continuation after token is readable and every word remains;no manual break,shortening or width exception is used.',
    62:'Three coherent English groups retain the full reason for insisting and keep Please accept it as an intact request. Preserve every word and the same native guard rather than forcing the Japanese two-row count.',
    69:'The intention to take care and warm thanks fit together on one complete English row. Preserve both beats with natural punctuation without importing Japanese staging.',
}
LAYOUT_REASONS={
    33:'Three complete groups preserve the inn location,collapse at the port and polite causative rescue explanation.',
    40:'Keep Still with the following concern. The reassurance,appearance concern and advice each form a complete natural group in three rows.',
    44:'Both complete departure and take-care sentences fit naturally in two rows;do not split the stock Take care phrase.',
    62:'Keep the full motivation and Please accept it intact in three natural rows;no words are shortened.',
    65:'Keep the qualified concession,explicit acceptance and complete take-care closing in three rows. This equals the source row count and needs no row-count waiver.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc,font=deepcopy(read(INPUT)),read(FONT)
    assert font['manuscript_sha256']==sha(INPUT.read_bytes()) and len(font['cases'])==19
    assert font['current_original_macro_alignment_calls']==152
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(17,2)
    assert len(font['negative_controls'])==18 and all(r['rejected'] for r in font['negative_controls'])
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[200]
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']
    assert len(font['review_sheets'])==3
    for sheet in font['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    cases={r['id']:r for r in font['cases']};invariants=[];row_notes=[];removed_stale=[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);isFE=row['kind']=='system-FE';case=cases[row['id']];p=profile_for(arm,block,'FE-paper' if isFE else 'progressive')
        encoded=codec.encode_relocatable_dialogue(raw,row['english'],p);assert encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex']
        assert semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup)
        assert all(raw[1:].count(m)==encoded.encoded[1:].count(m)==0 for m in [b'FI',b'FA',b'FO'])
        assert case['complete_native_independent228x48_plane_equal' if isFE else 'complete_native_independent216x64_plane_equal']
        assert case['one_native_page_consumes_complete_target'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        assert sum(len(x['cases']) for x in case['current_native_macro_pipelines'])==8
        if isFE:assert all(c['null_source_actor'] for v in case['current_native_macro_pipelines'] for c in v['cases'])
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p);idx=row['source_record_index']
        assert not qa.get('reviewed_ordinary_boundaries') and not row.get('reviewed_ordinary_boundaries')
        assert row.get('qa_waivers') in [None,['line-break-count']]
        notes=[i for i in qa['issues'] if i['severity']=='warning' and i['code']=='line-break-count']
        if notes:
            assert idx in ROW_REASONS
            reason=ROW_REASONS[idx]+' Only the source/English row count differs;no glyph,bounds,pagination,control,macro,weak-ending,orphan or blank-page exemption is granted.'
            row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);row_notes.append(dict(id=row['id'],reason=reason))
        else:
            if row.pop('qa_waivers',None):removed_stale.append(row['id'])
            row.pop('qa_waiver_reason',None)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and notes)]
        assert all(row['review'][g] for g in ['source','context','localization','naturalness']);row['review']['formatting']=True
        row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_font_case=case,
            native_formatting_consumer='FE-paper' if isFE else 'progressive',native_plane_verified_not_actual_English_gameplay=True,
            current_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,
            status='source-prose-current-native-format-approved;name-target-relocation-actual-registered-release-pending')
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        if idx in LAYOUT_REASONS:row['native_layout_retention_reason']=LAYOUT_REASONS[idx]
        invariants.append(dict(id=row['id'],source_selector=raw[0],semantic_tokens_and_controls_exact=True,encoded_sha256=sha(encoded.encoded),visible_lines=qa['visible_lines']))
    assert len(row_notes)==6 and removed_stale==['DK4_MES_B200_R0065']
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':13,'retain-wording':6}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Invalid formatter accepted: '+label)
    for consumer,selector in [('progressive',19),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),
            ('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),
            ('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),
            ('disabled-balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),
            ('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:
            reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    previous=read('translations/lil_B200_editorial_manuscript_v2.json');before={r['id']:r for r in previous['records']}
    changed=[r['id'] for r in font['cases'] if r['encoded_hex']!=before[r['id']]['compiled_hex']]
    assert changed==['DK4_MES_B200_R0040','DK4_MES_B200_R0044','DK4_MES_B200_R0062','DK4_MES_B200_R0065']
    assert all(r['english']==before[r['id']]['english'] and r['source_hex']==before[r['id']]['source_hex'] for r in doc['records'])
    assert read(REFINEMENT)['all19_prose_wordings_controls_metrics_guards_phase_and_four_row_limits_unchanged']
    doc.update(formatting_review_pending=False,status='source-prose-current-native-format-approved;name-target-relocation-actual-registered-release-pending',
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        current_font_oracle='scripts/lil_current_font_oracles_v4792.py',current_font_oracle_sha256=sha(Path('scripts/lil_current_font_oracles_v4792.py').read_bytes()),
        all19_current_native_previews_viewed_on_three_sheets=True,no_record_specific_ordinary_boundary_exception_required=True,
        no_shared_metric_guard_or_manual_break_change=True,source_bound_wrap_retention_proof=str(REFINEMENT),source_bound_wrap_retention_proof_sha256=sha(REFINEMENT.read_bytes()),
        actual_English_B200_content_name_target_relocation_and_registered_release_gates_pending=True,
        source_prose_or_completion_credit_added=0,full_goal_complete=False)
    validate_natural_dialogue_batch(doc);ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all19_source_prose_current_native_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        source_context=doc['source_context'],source_context_sha256=doc['source_context_sha256'],invariants=invariants,
        reviewed_sheets=[{**p,'viewed_in_full_current_turn':True} for p in font['review_sheets']],
        all19_complete_native_panels_read_as_one_exchange=True,source_consumer_negatives=18,formatter_negatives=negatives,
        six_individual_rowcount_reasons=row_notes,stale_rowcount_waiver_removed=removed_stale,
        thirteen_revisions_and6_individually_justified_retentions=True,
        complete_rescue_causative_doctor_denial_gift_progression_and_exact_Charm_increment_preserved=True,
        no_runtime_names_or_private_thoughts_inherited=True,all152_current_native_alignment_cases_and_complete_planes_pass=True,
        Stranger_label_target_not_applied_or_display_approved=True,actual_English_content_relocation_and_registered_release_pending=True,
        no_new_ROM_or_emulator_run_or_review_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B20019 source/prose/native panels approved:13 revisions/six retentions,152 alignments,18 consumer/28 formatter negatives. Name target,English actual and release pending;no credit.')
