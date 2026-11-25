"""Seal viewed10-panel source/prose/native approval; actual and release stay open."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dataclasses import replace
from dk4tool.dialogue import lil_B181_layout_v1 as codec
from dk4tool.dialogue.lil_B181_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B181_native_approval_v4845')
INPUT=Path('translations/lil_B181_editorial_manuscript_v2.json')
OUTPUT=Path('translations/lil_B181_editorial_manuscript_v3.json')
FONT=Path('work/analysis/lil_B181_fonts_v4844/all10_progressive_FE_native_planes_and80_alignment_cases.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc,font=deepcopy(read(INPUT)),read(FONT)
    assert font['manuscript_sha256']==sha(INPUT.read_bytes()) and len(font['cases'])==10
    assert font['current_original_macro_alignment_calls']==80
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(9,1)
    assert len(font['negative_controls'])==20 and all(r['rejected'] for r in font['negative_controls'])
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[181]
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']
    for p in font['review_sheets']:assert sha(Path(p['path']).read_bytes())==p['sha256']
    assert len(font['review_sheets'])==2
    cases={r['id']:r for r in font['cases']};invariants=[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);isFE=row['kind']=='system-FE';case=cases[row['id']]
        p=profile_for(arm,block,'FE-paper' if isFE else 'progressive')
        encoded=codec.encode_relocatable_dialogue(raw,row['english'],p)
        assert encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex']
        assert semantic_tokens(row['english'])==semantic_tokens(encoded.formatted_markup)
        assert not any(s in raw[1:] for s in [b'FI',b'FA',b'FO']) and '{MACRO:' not in row['english']
        assert case['complete_native_independent228x48_plane_equal' if isFE else 'complete_native_independent216x64_plane_equal']
        assert case['one_native_page_consumes_complete_target'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        assert sum(len(x['cases']) for x in case['current_native_macro_pipelines'])==8
        if isFE:assert all(c['null_source_actor'] for v in case['current_native_macro_pipelines'] for c in v['cases'])
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],p)
        assert row.get('qa_waivers') in [None,['line-break-count']]
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not
            (i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waiver_reason'))]
        assert all(row['review'][g] for g in ['source','context','localization','naturalness'])
        row['review']['formatting']=True
        row.update(record_index=row['current_record_index'],current_text_hex=row['current_hex'],native_font_case=case,
            native_formatting_consumer='FE-paper' if isFE else 'progressive',native_plane_verified_not_actual_gameplay=True,
            current_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,
            status='source-prose-current-native-format-approved;relocation-actual-registered-release-pending')
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
        invariants.append(dict(id=row['id'],source_selector=raw[0],semantic_tokens_and_controls_exact=True,encoded_sha256=sha(encoded.encoded)))
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':5,'retain-wording':5}
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Invalid formatter accepted: '+label)
    for consumer,selector in [('progressive',166),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),
            ('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),
            ('disabled-guard',replace(p,guard_linebreaks=False)),('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),
            ('disabled-balancing',replace(p,balanced_wrapping=False)),
            ('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),
            ('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:
            reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    doc.update(formatting_review_pending=False,status='source-prose-current-native-format-approved;relocation-actual-registered-release-pending',
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        current_font_oracle='scripts/lil_current_font_oracles_v4792.py',current_font_oracle_sha256=sha(Path('scripts/lil_current_font_oracles_v4792.py').read_bytes()),
        all10_current_native_previews_viewed_on_two_sheets=True,viewed_phrases_use_full_verified_width_and_complete_clauses=True,
        no_new_phrase_exception_shared_metric_guard_or_manual_break=True,
        FE_historical_evidence_is_typed_geometry_not_current_font_gameplay=True,
        actual_B181_story_selection_and_all_release_gates_pending=True,
        clean_first_notes_are_historical_and_precede_current_native_bindings=True,
        source_prose_or_completion_credit_added=0,full_goal_complete=False)
    validate_natural_dialogue_batch(doc)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all10_source_prose_current_native_approval.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        source_context=doc['source_context'],source_context_sha256=doc['source_context_sha256'],invariants=invariants,
        reviewed_sheets=[{**p,'viewed_in_full_current_turn':True} for p in font['review_sheets']],
        all10_complete_native_panels_read_as_one_exchange=True,source_consumer_negatives=20,formatter_negatives=negatives,
        source_English_rowcount_notes_not_other_safety_waivers=True,
        five_revisions_and_five_individually_justified_retentions=True,
        explicit_wistful_wish_and_three_audible_sighs_refined=True,
        all80_current_native_alignment_cases_and_complete_planes_pass=True,
        actual_story_gameplay_relocation_and_registered_release_pending=True,
        no_new_ROM_or_emulator_run_or_review_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All10 source/prose/current-native reviews approved:5 revisions/5 justified retentions,80 alignments,20 consumer/28 formatter negatives. Relocation,actual and release remain pending;no credit.')
