"""Prepare full B230 source/current binding behind the completed V7418 checkpoint."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_source_tools_v7428')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={'B229':'B230','source_v7381':'source_v7428','source_span_binding_v7381':'source_span_binding_v7428','verification_v7378':'verification_v7425','clean_context_v7380/all17_clean_giant_tortoise_shield_callback_glosses_before_old_English':'clean_context_v7427/all17_clean_phoenix_bascinet_callback_glosses_before_old_English','current_V7371_native_v7376':'current_V7418_native_v7423','len(known)==6722':'len(known)==6739','blocks[229]':'blocks[230]','block=229':'block=230','ends==[944,944] and len(source)==len(target)==944 and source[944:]==target[944:]==bytes(0)':'ends==[988,988] and len(source)==len(target)==988 and source[988:]==target[988:]==bytes(0)','source_bytes=944,current_bytes=944,source_logical_end=944,current_logical_end=944':'source_bytes=988,current_bytes=988,source_logical_end=988,current_logical_end=988','complete944_byte_inverse':'complete988_byte_inverse','seventeen_clean_current_giant_tortoise_callback_source_references':'seventeen_clean_current_phoenix_bascinet_callback_source_references','stored=944,logical=944,tail=0':'stored=988,logical=988,tail=0'}
    jobs=[('scripts/lil_B229_source_span_binding_v7381.py','scripts/lil_B230_source_span_binding_v7428.py',{'v7371':'v7418'}),('scripts/map_lil_B229_source_v7381.py','scripts/map_lil_B230_source_v7428.py',changes)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_source_tools.json',dict(tools=rows,all17_clean_glosses_required_before_predecessor_comparison=True,completed_V7418_andown_strict_native_input_required=True,all_three_existing_renderer_BL_replacements_andall_other_native_bytes_preserved=True,source988_logical988_no_tail_bound_independently=True,new_credit=0,full_goal_complete=False))
