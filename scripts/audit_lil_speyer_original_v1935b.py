"""Successor: B74 has one join panel and one tutorial choice, not two art pauses."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/audit_lil_speyer_original_v1935.py')
SOURCE_SHA = '899bd4df0fae9bba28915b6bbbd468c1561cd030af5800db3b85e16bff28f98f'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes())==SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    old = "assert not missing and len(nav['original_art_pauses'])==2 and not nav['choices']"
    new = """assert not missing and len(nav['original_art_pauses'])==len(nav['choices'])==1
            tutorial=next(r for r in pairs if r['word']==0x2100)
            assert tutorial['offset']==3504 and tutorial['native_result_words'][:2]==[2,0]"""
    assert text.count(old)==1
    text = text.replace(old,new)
    assert text.count("lil_Speyer_original_audit_v1935'")==1
    text = text.replace("lil_Speyer_original_audit_v1935'","lil_Speyer_original_audit_v1935b'")
    marker='        actual79_B74_speeches_and_Gerhard_join_panel_captured_but_not_editorially_reviewed=True,'
    assert text.count(marker)==1
    text=text.replace(marker,marker+"\n        B74_tutorial_choice0_Yes_please_observed_choice1_not_played=True,\n        frozen1935_predecessor_rejected_wrong_interstitial_count_before_output_or_state_changes=True,")
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
