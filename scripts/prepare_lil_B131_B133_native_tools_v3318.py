"""Complete current native planes andsource00-specific negative controls."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B131_B133_native_tools_v3318')
if __name__=='__main__':
    assert not ROOT.exists();pairs=[]
    def generate(old,new,changes):
        old,new=Path(old),Path(new);assert not new.exists();t=old.read_text(encoding='utf-8')
        for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
        return old,new,t
    old,new,t=generate('scripts/verify_lil_B122_B127_fonts_v3277.py','scripts/verify_lil_B131_B133_fonts_v3319.py',{
      'lil_B122_B127_fonts_v3277':'lil_B131_B133_fonts_v3319',
      'lil_B122_B127_editorial_manuscript_v3.json':'lil_B131_B133_editorial_manuscript_v2.json',
      'lil_B122_B127_profile_v2':'lil_B131_B133_profile',
      'lil_B122_B127_layout_v1':'lil_B131_B133_layout_v1',
      'len(cases)==145 and len(qa_reports)==155 and macro_calls==1160':'len(cases)==60 and len(qa_reports)==61 and macro_calls==480',
      'blocks[122]':'blocks[131]','blocks[121]':'blocks[130]',
      'selectors=[2,6,9,20,26,92,95,151]':'selectors=[0,2,5,9,20]',
      'len(negatives)==23':'len(negatives)==22',
      'all155_complete_source_speech_prefixes_preserved':'all61_complete_source_speech_prefixes_preserved',
      'all155_full_QA_reports':'all61_full_QA_reports','current_original_macro_alignment_calls=1160':'current_original_macro_alignment_calls=480',
      'all145_':'all60_','ten_FE_and_four_two_option_labels_separately_required':'one_FE_and_two_two_option_labels_separately_required',
      'actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs'})
    anchor='    assert len(negatives)==22';assert t.count(anchor)==1
    t=t.replace(anchor,'''    zero=next(r for r in doc['records'] if r['source_presentation_prefix_hex']=='00')
    zero_raw=bytes.fromhex(zero['source_hex'])
    reject('source00-extra-body-NUL',lambda:encode_relocatable_dialogue(zero_raw,zero['english'].replace('}','}{HEX:00}',1),progressive))
    reject('source00-trailing-NUL',lambda:encode_relocatable_dialogue(zero_raw,zero['english']+'{HEX:00}',progressive))
    reject('source00-duplicate-selector',lambda:encode_relocatable_dialogue(zero_raw,'{SPEAKER:00}'+zero['english'],progressive))
    reject('nonzero-embedded-NUL',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+'{HEX:00}',progressive))
    from dk4tool.dialogue.encoder import encode_relocatable_dialogue as unscoped_encode
    reject('shared-encoder-still-rejects-source00',lambda:unscoped_encode(zero_raw,zero['english'],progressive))
'''+anchor)
    t=t[:t.rindex('    print(')]+"    print('60 complete progressive planes,480macro alignments,61QA plans and22 source-consumer/zero-prefix negatives pass;eight sheets require visual review. No gameplay orcredit.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=generate('scripts/verify_lil_B122_B127_FE_v3278.py','scripts/verify_lil_B131_B133_FE_v3320.py',{
      'lil_B122_B127_FE_v3278':'lil_B131_B133_FE_v3320',
      'lil_B122_B127_editorial_manuscript_v3.json':'lil_B131_B133_editorial_manuscript_v2.json',
      'lil_B122_B127_profile_v2':'lil_B131_B133_profile','lil_B122_B127_layout_v1':'lil_B131_B133_layout_v1',
      'len(cases) == 10 and calls == 80 and len(staging) == 7':'len(cases) == 1 and calls == 8 and len(staging) == 0',
      'all10_':'all1_','seven_source_staging_cases_start_English_firstline_with_complete_glyphs':'no_source_leading_vertical_staging_in_share_notice',
      'actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs'})
    t=t[:t.rindex('    print(')]+"    print('One complete FE share-exchange notice/eight null-actor macro cases pass;one sheet requires visual review. No gameplay orcredit.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old,new,t=generate('scripts/prove_lil_B122_B127_choices_v3279.py','scripts/prove_lil_B131_B133_choices_v3321.py',{
      'lil_B122_B127_choices_v3279':'lil_B131_B133_choices_v3321',
      'work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json':'work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json',
      'lil_B122_B127_choice_manuscript_v2.json':'lil_B131_B133_choice_manuscript_v2.json',
      '[(125,468),(126,176)]':'[(133,1530)]','len(cases)==2':'len(cases)==1',
      'all2_typed_menu_native_proof':'all1_typed_menu_native_proof',
      'native_selection_cancel_cases=12':'native_selection_cancel_cases=6',
      'complete_current_and_reviewed_style_label_planes=16':'complete_current_and_reviewed_style_label_planes=8',
      'clean_current_reviewed_native_decoder_cases=6':'clean_current_reviewed_native_decoder_cases=3',
      'all4_labels_source_order_pointers_counts_and_original_selection_results_preserved':'all2_labels_source_order_pointers_counts_and_original_selection_results_preserved'})
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    ROOT.mkdir(parents=True);save(ROOT/'native_consumer_successor_provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],source00_specific_NUL_rejections_include_unchanged_shared_encoder=True,complete_native_font_macro_menu_and_FE_consumers_preserved=True,no_global_helper_orROM_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
