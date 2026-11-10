"""Seal24 source/native reviews after all four returned English sheets were viewed."""
import re
from collections import Counter
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import lil_B197_layout_v1 as codec
from dk4tool.dialogue.lil_B197_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_kuhn_china_fonts_v2905 import semantic_tokens
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_native_approval_v5670')
INPUTS=[Path('translations/lil_B197_editorial_manuscript_v2.json'),Path('translations/lil_B197_choice_manuscript_v1.json')]
OUTPUTS=[Path('translations/lil_B197_editorial_manuscript_v3.json'),Path('translations/lil_B197_choice_manuscript_v2.json')]
FONT=Path('work/analysis/lil_B197_fonts_v5668/all21_progressive_FE_native_planes_and168_alignment_cases.json')
MENU=Path('work/analysis/lil_B197_choices_v5669/all1_typed_menu_native_proof.json')
WRAP=Path('work/analysis/lil_B197_layout_review_v5667c/one_exact_R74_boundary_review_and_unchanged_planner.json')

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    doc,menu=[deepcopy(read(p)) for p in INPUTS];font,menus,wrap=map(read,[FONT,MENU,WRAP])
    assert font['manuscript_sha256']==sha(INPUTS[0].read_bytes())
    assert len(font['cases'])==21 and font['current_original_macro_alignment_calls']==168
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(20,1)
    assert len(font['negative_controls'])==18 and all(r['rejected'] for r in font['negative_controls'])
    assert len(menus['menus'])==1 and menus['native_selection_cancel_cases']==8 and menus['complete_current_and_reviewed_style_label_planes']==12
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[197]
    assert sha(arm)==font['ARM9_sha256']==doc['required_runtime_ARM9_sha256']
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']
    sheets=[]
    for s in font['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append({**s,'viewed_in_full_current_turn':True,'viewed_after_image_return':True,'original_detail':True,
            'review':'Viewed complete exchange panels:Indian classic/celestial maiden/sage,8500 gold,Admiral decision,purchase before romantic rebuff,personal inability and gift,future romantic wish,stammer,tentative identity and common Ian Charm notice. All full words,punctuation,first/internal/final glyphs remain on one page. Ordinary adjacent-row boundaries are readable in context,including exact R74 negative-verb wrap. No authored break,maximum-fill rule,prose shortening or actual English gameplay claim.'})
    assert len(sheets)==3
    byid={c['id']:c for c in font['cases']};invariants=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);fe=r['kind']=='system-FE';p=profile_for(arm,block,'FE-paper' if fe else 'progressive');c=byid[r['id']]
        enc=codec.encode_relocatable_dialogue(raw,r['english'],p)
        assert enc.encoded.hex()==r['compiled_hex']==c['encoded_hex']
        assert semantic_tokens(r['english'])==semantic_tokens(enc.formatted_markup)
        assert not re.findall(rb'FI|FA|FO',raw) and not re.findall(r'\{MACRO:(FI|FA|FO)\}',r['english'])
        assert c['complete_native_independent228x48_plane_equal' if fe else 'complete_native_independent216x64_plane_equal']
        assert c['one_native_page_consumes_complete_target'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells']
        assert c['all_visible_origins_zero_and_within_four_rows'] and sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        assert sum(len(v['cases']) for v in c['current_native_macro_pipelines'])==8
        if fe:assert all(v['null_source_actor'] for pipeline in c['current_native_macro_pipelines'] for v in pipeline['cases'])
        qa=codec.audit_relocatable_dialogue_record(raw,r['english'],p)
        if r['source_record_index']==74:
            assert r['id']==wrap['exact_record'] and r['source_hex']==wrap['source_hex'] and r['english']==wrap['english']
            assert qa['visible_lines']==r['exact_reviewed_soft_wrap_rows']==wrap['visible_rows']
            assert r['qa_waivers']==['weak-line-ending'] and r['qa_waiver_reason']==wrap['reason']
            assert [i['code'] for i in qa['issues']]==['weak-line-ending']
        else:assert r.get('qa_waivers') in [None,['line-break-count']]
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]) and r.get('qa_waiver_reason'))]
        assert all(r['review'][k] for k in ['source','context','localization','naturalness']);r['review']['formatting']=True
        r.update(record_index=r['current_record_index'],current_text_hex=r['current_hex'],native_font_case=c,
            native_formatting_consumer='FE-paper' if fe else 'progressive',native_plane_verified_not_actual_gameplay=True,
            current_complete_native_display_pending=False,current_native_voice_macro_entry_and_context_pending=False,
            status='source-prose-current-native-format-approved;relocation-English-actual-registered-release-pending')
        if r['editorial_decision']=='retain-wording':assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
        invariants.append(dict(id=r['id'],source_selector=raw[0],semantic_tokens_macros_and_controls_exact=True,encoded_sha256=sha(enc.encoded)))
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):negatives.append(label)
        else:raise AssertionError('Invalid formatter accepted:'+label)
    for consumer,selector in [('progressive',169),('FE-paper',254)]:
        p=profile_for(arm,block,consumer);r=next(r for r in doc['records'] if r['source_selector']==selector);raw=bytes.fromhex(r['source_hex'])
        for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),
            ('row-spacing',replace(p,line_height_px=12)),('disabled-guard',replace(p,guard_linebreaks=False)),
            ('disabled-pair-phase',replace(p,pair_phase_safe_breaks=False)),('disabled-balancing',replace(p,balanced_wrapping=False)),
            ('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:
            reject(consumer+'-'+label,lambda bad=bad,r=r,raw=raw:codec.encode_relocatable_dialogue(raw,r['english'],bad))
        for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject(consumer+'-manual-'+tag,lambda tag=tag,r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english']+tag,p))
        reject(consumer+'-widened-selectors',lambda r=r,raw=raw,p=p:codec.encode_relocatable_dialogue(raw,r['english'],replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{3})))
    assert len(negatives)==28
    item=menus['menus'][0];path=Path(item['proof']);proof=read(path)
    assert sha(path.read_bytes())==item['sha256'] and proof['manuscript_sha256']==sha(INPUTS[1].read_bytes())
    assert proof['candidate_sha256']==doc['current_ROM_sha256']
    assert proof['eight_original_VM_selection_and_cancel_cases_pass'] and proof['twelve_complete_native_style_label_planes_pass']
    assert sha(Path(proof['visual_review_sheet']).read_bytes())==proof['visual_review_sheet_sha256']
    assert len(bytes.fromhex(proof['typed_target_object_hex']))==40
    assert [r['english'] for r in sorted(menu['records'],key=lambda r:r['option_index'])]==["Let's buy it",'Pass','You decide']
    for r in menu['records']:
        r['review']['formatting']=True
        r.update(typed_target_object_hex=proof['typed_target_object_hex'],compiled_hex=proof['typed_target_object_hex'],
            native_choice_proof=str(path),native_choice_proof_sha256=sha(path.read_bytes()),
            choice_consumer_selection_geometry_native_display_pending=False,actual_choice_selection_still_pending=True,
            current_native_typed_choice_font_reference_and_outcome_binding_pending=False,
            status='source-prose-current-native-format-approved;relocation-English-actual-registered-release-pending')
    menu_sheets=[dict(path=proof['visual_review_sheet'],sha256=proof['visual_review_sheet_sha256'],viewed_in_full_current_turn=True,viewed_after_image_return=True,original_detail=True,
        review="Viewed all six current/reviewed labels:Let's buy it/Pass/You decide preserve proposal/refusal/delegation and indices0/1/2. Reviewed labels are centered with complete first/internal/final glyphs;both native styles and storage padding pass. Original modal input loop remains bridged;actual English selections still pending.")]
    assert Counter(r['editorial_decision'] for r in doc['records']+menu['records'])=={'revise':16,'retain-wording':8}
    for data,previous,output in zip([doc,menu],INPUTS,OUTPUTS,strict=True):
        data.update(formatting_review_pending=False,status='source-prose-current-native-format-approved;relocation-English-actual-registered-release-pending',
            previous_manuscript=str(previous),previous_manuscript_sha256=sha(previous.read_bytes()),
            native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),typed_choice_proof=str(MENU),typed_choice_proof_sha256=sha(MENU.read_bytes()),
            source_bound_wrap_retention_proof=str(WRAP),source_bound_wrap_retention_proof_sha256=sha(WRAP.read_bytes()),
            current_font_oracle='scripts/lil_current_font_oracles_v4792.py',
            no_shared_metric_guard_manual_break_prose_shortening_or_pagination_change=True,
            actual_English_B197_three_choices_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,
            prose_companions=[str(p) for p in OUTPUTS if p!=output],full_goal_complete=False)
        for key in ['native_formatter_module','scoped_profile_module']:
            data[key]=doc[key];data[key+'_sha256']=sha(Path(data[key]).read_bytes())
        data['current_font_oracle_sha256']=sha(Path(data['current_font_oracle']).read_bytes())
        validate_natural_dialogue_batch(data)
    ROOT.mkdir(parents=True)
    for path,data in zip(OUTPUTS,[doc,menu],strict=True):save(path,data)
    save(ROOT/'all24_source_prose_current_native_speech_choice_approval.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},
        speech_objects=21,choice_labels=3,source_menus=1,total_objects=24,revised=16,retained=8,
        native_speech_proof=str(FONT),native_speech_proof_sha256=sha(FONT.read_bytes()),typed_choice_proof=str(MENU),typed_choice_proof_sha256=sha(MENU.read_bytes()),
        reviewed_sheets=sheets,reviewed_menu_sheets=menu_sheets,menu_native_proofs=[dict(path=str(path),sha256=sha(path.read_bytes()))],
        source_English_macro_control_invariants=invariants,formatter_negatives=negatives,source_consumer_negative_controls=font['negative_controls'],
        speech_processor_alignment_cases=168,choice_selection_cancel_cases=8,choice_current_and_reviewed_style_label_planes=12,
        all24_five_source_context_localization_naturalness_formatting_gates_true=True,
        exact_R74_source_bound_wrap_proof=str(WRAP),exact_R74_source_bound_wrap_proof_sha256=sha(WRAP.read_bytes()),
        all_relocation_final_stored_English_actual_scene_and_registered_release_gates_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [*INPUTS,FONT,MENU,WRAP,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B197 native approval:24 objects,16 revisions/8 retentions;168 speech alignments,8 menu outcomes,12 label planes,18 consumer/28 formatter negatives. All4 sheets viewed. No completion credit.')
