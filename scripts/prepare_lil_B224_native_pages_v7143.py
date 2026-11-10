"""Verify all fifteen paragraphs and retain R11's original CP932 ellipsis glyph."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_native_page_tools_v7143')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/verify_lil_B222_native_pages_v7047.py';b='scripts/verify_lil_B224_native_pages_v7143.py';s=Path(a).read_text('utf8')
    old="page_adapter=checked_text(inspect.getsource(old_pages),{'4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'})"
    new="page_adapter=read(SOURCE_FONT)['source_owned_CP932_page_adapter']"
    c={'B222':'B224','editorial_manuscript_v2.json':'editorial_manuscript_v1.json','layout_v7046b/sixteen_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7142b/fifteen_whole_paragraph_plans_no_macros_no_prose_changes','current_V7029_native_v7033':'current_V7118_native_v7123','native_pages_v7047':'native_pages_v7143',
      'from scripts.verify_village_wrap_v608 import read,save':'from scripts.prove_lil_B208_name_planes_v6405 import codes\nfrom scripts.verify_village_wrap_v608 import read,save',
      "if __name__=='__main__':":"SOURCE_FONT=Path('work/analysis/lil_B224_source_pages_v7137/all15_clean_objects_complete_native_CP932_pages_and_exact_consumption.json')\nif __name__=='__main__':",
      "len(plan['records'])==16":"len(plan['records'])==15",old:new,"page_env={**old_pages.__globals__,'expected_pixels':expected_pixels}":"page_env={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}",
      ".encode('ascii')":".encode('cp932')",'[2,16]':'[26,197]',
      'len(cases)==len(pictures)==16':'len(cases)==len(pictures)==15','alignments==128':'alignments==120',
      'all16_complete_pages_sheet':'all15_complete_pages_sheet','all16_paragraphs16_complete_native_pages128_alignments':'all15_paragraphs15_complete_native_pages120_alignments',
      'complete_native_pages=16':'complete_native_pages=15','logical_compiled_input_alignment_cases=128':'logical_compiled_input_alignment_cases=120','all16_single_pages':'all15_single_pages','only_original_static_selectors2_16':'only_original_static_selectors26_197','all16_formatting_gates_remain_false':'all15_formatting_gates_remain_false',
      '16 complete single native pages/128 alignments':'15 complete single native pages/120 alignments',
      'source_owned_expand_adapter=adapter':'original_source_current_R11_ellipsis_CP932_glyph_retained_without_punctuation_revision=True,source_owned_expand_adapter=adapter',
      '[DOC,PLAN,INPUT,Path(old_pages.__code__.co_filename),Path(__file__)]':'[DOC,PLAN,INPUT,SOURCE_FONT,Path(old_pages.__code__.co_filename),Path(__file__)]',
    }
    assert not Path(b).exists();checked_text(s,c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_native_checker.json',dict(tool=row,exact_source_CP932_page_adapter_reused_for_original_ellipsis=True,logical_and_compiled_four_alignments_each_required_for_all15=True,no_font_geometry_guard_pair_phase_actor_or_native_instruction_change=True,new_credit=0,full_goal_complete=False))
