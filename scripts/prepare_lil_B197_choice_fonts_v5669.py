"""Reuse original three-option geometry with the already validated current font descent."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_choice_tools_v5669')
if __name__=='__main__':
    assert not ROOT.exists()
    anchor='    cases,pictures = [],[]'
    ink='''    # Current ARM9's independently validated one-pixel ASCII ink descent.
    old_ink='expected[(y + yy) * stride + x + index * 6 + xx]'
    assert painter.count(old_ink)==1
    painter=painter.replace(old_ink,'expected[(y + yy + 1) * stride + x + index * 6 + xx]')
    painter=painter.replace('    width, height = LABEL_WIDTH, 20','    assert sha(arm)==CURRENT_ARM9\\n    width, height = LABEL_WIDTH, 20')
'''
    tool=derive('scripts/prove_lil_shrines_choices_v3188.py','scripts/prove_lil_B197_choices_v5669.py',{
        'from scripts.verify_village_wrap_v608 import read, save':'from scripts.verify_village_wrap_v608 import read, save\nfrom scripts.lil_current_font_oracles_v4792 import CURRENT_ARM9',
        'lil_Shrines_Temples_choices_v3188':'lil_B197_choices_v5669',
        'work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json':'work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json',
        'translations/lil_shrines_temples_choice_manuscript_v2.json':'translations/lil_B197_choice_manuscript_v1.json',
        anchor:ink+anchor,
        "env = {**prior.__dict__,'LABEL_WIDTH':width,'sha':sha}":"env = {**prior.__dict__,'LABEL_WIDTH':width,'sha':sha,'CURRENT_ARM9':CURRENT_ARM9}",
        '[(105,186),(105,424),(105,842),(109,384),(110,336)]':'[(197,230)]',
        'len(cases)==5':'len(cases)==1','all5_typed_menu':'all1_typed_menu','native_selection_cancel_cases=40':'native_selection_cancel_cases=8',
        'complete_current_and_reviewed_style_label_planes=60':'complete_current_and_reviewed_style_label_planes=12',
        'clean_current_reviewed_native_decoder_cases=15':'clean_current_reviewed_native_decoder_cases=3',
        'all15_labels_source_order':'all3_labels_source_order'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_three_option_geometry_and_current_ink_adapter.json',dict(tool=tool,
        unchanged_native_dispatch_VM_geometry_metrics_and_canvas=True,current_ARM9_one_pixel_ink_descent_already_validated=True,
        no_runtime_font_or_display_geometry_mutation=True,actual_English_selection_still_pending=True,new_credit=0))
