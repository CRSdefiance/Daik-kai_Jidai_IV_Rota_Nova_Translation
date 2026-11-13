"""Seal36 contextual/native reviews after all nine returned sheets were viewed."""
import re
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B196_layout_v3 as codec
from dk4tool.dialogue.lil_B196_profile_v2 import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_native_approval_v5612')
INPUTS=[Path('translations/lil_B196_editorial_manuscript_v2.json'),Path('translations/lil_B196_choice_manuscript_v1.json')]
OUTPUTS=[Path('translations/lil_B196_editorial_manuscript_v3.json'),Path('translations/lil_B196_choice_manuscript_v2.json')]
FONT=Path('work/analysis/lil_B196_fonts_v5609b/all24_progressive_FE_native_planes_and192_alignment_cases.json')
MENU=Path('work/analysis/lil_B196_choices_v5610b/all6_typed_menu_native_proof.json')
WRAP=Path('work/analysis/lil_B196_R74_wrap_v5611/exact_R74_three_ordinary_boundaries_four_native_partitions_and_six_nontransfer_cases.json')
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    doc,menu=[deepcopy(read(p)) for p in INPUTS];font,menus,wrap=map(read,[FONT,MENU,WRAP])
    assert font['manuscript_sha256']==sha(INPUTS[0].read_bytes()) and len(font['cases'])==24 and font['current_original_macro_alignment_calls']==192
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(23,1)
    assert len(font['negative_controls'])==30 and all(r['rejected'] for r in font['negative_controls'])
    assert len(menus['menus'])==6 and menus['native_selection_cancel_cases']==36 and menus['complete_current_and_reviewed_style_label_planes']==48
    assert wrap['all24_words_source_controls_compiled_bytes_and_native_planes_unchanged']
    assert len(wrap['six_source_or_prose_changes_do_not_inherit_review'])==6
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[196]
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']
    sheets=[]
    for s in font['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append({**s,'viewed_in_full_current_turn':True,'viewed_after_image_return':True,
            'review':'Viewed every full speech panel as the whole negotiation. Six exact offers,three distinct personal advice voices,Lil silent beat,gender-neutral seller,Charm FI notice,pleading/regret and future sell-elsewhere intent stay complete. Carlo R74 has all129 characters/23 words on four guarded rows;its three exact ordinary soft boundaries are readable in context and the next word cannot fit. Other shorter rows preserve complete sentences or final phrases instead of forcing maximum fill. Every first/internal/final glyph,punctuation,origin,bounds and page is intact. No actual gameplay claim.'})
    assert len(sheets)==3
    byid={c['id']:c for c in font['cases']};invariants=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);fe=r['kind']=='system-FE';p=profile_for(arm,block,'FE-paper' if fe else 'progressive');c=byid[r['id']]
        enc=codec.encode_relocatable_dialogue(raw,r['english'],p)
        assert enc.encoded.hex()==r['compiled_hex']==c['encoded_hex'] and semantic_tokens(r['english'])==semantic_tokens(enc.formatted_markup)
        assert re.findall(rb'FI|FA|FO',raw)==[v.encode() for v in re.findall(r'\{MACRO:(FI|FA|FO)\}',r['english'])]
        assert c['complete_native_independent228x48_plane_equal' if fe else 'complete_native_independent216x64_plane_equal']
        assert c['one_native_page_consumes_complete_target'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert c['all_visible_origins_zero_and_within_four_rows'] and sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        assert sum(len(v['cases']) for v in c['current_native_macro_pipelines'])==8
        if fe:assert all(v['null_source_actor'] for pipeline in c['current_native_macro_pipelines'] for v in pipeline['cases'])
        qa=codec.audit_relocatable_dialogue_record(raw,r['english'],p)
        if r['source_record_index']==74:
            assert r['english']==wrap['exact_target'] and r['source_hex']==wrap['exact_source_hex'] and r['compiled_hex']==wrap['retained_compiled_hex']
            assert qa['reviewed_ordinary_boundaries']==r['reviewed_ordinary_boundaries']==wrap['exact_source_prose_boundaries']
            r['native_layout_retention_reason']=wrap['individual_layout_retention_reason']
        else:assert not qa.get('reviewed_ordinary_boundaries') and not r.get('reviewed_ordinary_boundaries')
        assert r.get('qa_waivers') in [None,['line-break-count']]
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and r.get('qa_waiver_reason'))]
        assert all(r['review'][k] for k in ['source','context','localization','naturalness']);r['review']['formatting']=True
        r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=c,
            native_formatting_consumer='FE-paper' if fe else 'progressive',native_plane_verified_not_actual_gameplay=True,
            current_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,
            status='source-prose-current-native-format-approved;relocation-actual-registered-release-pending')
        if r['editorial_decision']=='retain-wording':assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
        invariants.append(dict(id=r['id'],source_selector=raw[0],semantic_tokens_macros_and_controls_exact=True,encoded_sha256=sha(enc.encoded)))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Invalid formatter accepted:'+label)
    for consumer,selector in [('progressive',173),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),
            ('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),
            ('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),
            ('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    menu_sheets=[];menu_proofs=[]
    for item in menus['menus']:
        path=Path(item['proof']);proof=read(path);assert sha(path.read_bytes())==item['sha256']
        assert proof['manuscript_sha256']==sha(INPUTS[1].read_bytes()) and proof['candidate_sha256']==doc['current_ROM_sha256']
        assert proof['six_original_VM_selection_and_cancel_cases_pass'] and proof['eight_complete_native_style_label_planes_pass']
        assert proof['complete_current_ASCII_ink_offset_y']==1 and sha(Path(proof['visual_review_sheet']).read_bytes())==proof['visual_review_sheet_sha256']
        assert len(bytes.fromhex(proof['typed_target_object_hex']))==16
        records=sorted([r for r in menu['records'] if r['command_offset']==proof['original_command_offset']],key=lambda r:r['option_index'])
        assert [r['english'] for r in records]==['Buy','Pass']
        for r in records:
            assert r['english']==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
            r['review']['formatting']=True
            r.update(typed_target_object_hex=proof['typed_target_object_hex'],compiled_hex=proof['typed_target_object_hex'],
                native_choice_proof=str(path),native_choice_proof_sha256=sha(path.read_bytes()),
                choice_consumer_selection_geometry_native_display_pending=False,actual_choice_selection_still_pending=True,
                current_native_typed_choice_font_reference_and_outcome_binding_pending=False,
                status='source-prose-current-native-format-approved;relocation-actual-registered-release-pending')
        menu_proofs.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        menu_sheets.append(dict(path=proof['visual_review_sheet'],sha256=proof['visual_review_sheet_sha256'],viewed_in_full_current_turn=True,viewed_after_image_return=True,
            review='Viewed this complete source-bound menu sheet:retained Buy/Pass meanings and stored indices0/1. Both current and reviewed first/final/internal glyphs are complete in both styles. The reviewed sixteen-byte object centers both unpadded labels;old storage padding is not authored prose. Current one-pixel ink descent is accounted for by the independent oracle;runtime/font/canvas/geometry stay unchanged. Native input loops are bridged;actual branch selection remains pending.'))
    assert len(menu_sheets)==6
    allrows=doc['records']+menu['records'];assert Counter(r['editorial_decision'] for r in allrows)=={'revise':15,'retain-wording':21}
    for data,kind,previous in [(doc,'speech',INPUTS[0]),(menu,'player-choices',INPUTS[1])]:
        data.update(formatting_review_pending=False,status='source-prose-current-native-format-approved;relocation-actual-registered-release-pending',
            previous_manuscript=str(previous),previous_manuscript_sha256=sha(previous.read_bytes()),
            native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
            typed_choice_proof=str(MENU),typed_choice_proof_sha256=sha(MENU.read_bytes()),
            source_bound_wrap_retention_proof=str(WRAP),source_bound_wrap_retention_proof_sha256=sha(WRAP.read_bytes()),
            native_formatter_module='dk4tool/dialogue/lil_B196_layout_v3.py',scoped_profile_module='dk4tool/dialogue/lil_B196_profile_v2.py',
            current_font_oracle='scripts/lil_current_font_oracles_v4792.py',
            no_record_specific_ordinary_boundary_exception_required=False,only_R74_has_three_exact_source_prose_bound_ordinary_wraps=True,
            no_shared_metric_guard_manual_break_prose_shortening_or_pagination_change=True,
            actual_B196_source_event_selection_all_choice_paths_and_registered_release_pending=True,
            source_prose_or_completion_credit_added=0,prose_companions=[str(p) for p in OUTPUTS if p.name!=('lil_B196_editorial_manuscript_v3.json' if kind=='speech' else 'lil_B196_choice_manuscript_v2.json')],full_goal_complete=False)
        for key in ['native_formatter_module','scoped_profile_module','current_font_oracle']:data[key+'_sha256']=sha(Path(data[key]).read_bytes())
        validate_natural_dialogue_batch(data)
    ROOT.mkdir(parents=True)
    for path,data in zip(OUTPUTS,[doc,menu],strict=True):save(path,data)
    save(ROOT/'all36_source_prose_current_native_speech_choice_approval.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},
        speech_objects=24,choice_labels=12,source_menus=6,total_objects=36,revised=15,retained=21,
        native_speech_proof=str(FONT),native_speech_proof_sha256=sha(FONT.read_bytes()),typed_choice_proof=str(MENU),typed_choice_proof_sha256=sha(MENU.read_bytes()),
        reviewed_sheets=sheets,reviewed_menu_sheets=menu_sheets,menu_native_proofs=menu_proofs,
        source_English_macro_control_invariants=invariants,formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],
        speech_processor_alignment_cases=192,choice_selection_cancel_cases=36,choice_current_and_reviewed_style_label_planes=48,
        all36_five_source_context_localization_naturalness_formatting_gates_true=True,
        exact_R74_source_bound_wrap_proof=str(WRAP),exact_R74_source_bound_wrap_proof_sha256=sha(WRAP.read_bytes()),
        all_actual_scene_control_transition_relocation_final_stored_and_registered_release_gates_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [*INPUTS,FONT,MENU,WRAP,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B196 native approval:36 objects,15 revisions/21 retentions;192 speech alignments,36 choice outcomes/48 style planes,30 consumer/28 formatter negatives. All9 sheets viewed. Actual/relocation/release pending;zero credit.')
