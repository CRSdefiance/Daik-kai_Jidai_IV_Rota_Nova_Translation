"""Bind the completed clean prerequisite context without adding dialogue credit."""
from scripts.source_locked_derivation_v5118 import derive
PACKET='work/analysis/Rafael_B49_prerequisite_B39_v8076/complete_clean_SC0_B39_EV0_andcoverage_before_current_English.json'
GLOSS='work/analysis/Rafael_B49_prerequisite_gloss_v8077/complete22_clean_B39_glosses_explicit_B49_prerequisite_context_only.json'
if __name__=='__main__':
    print(derive('scripts/complete_Rafael_B48_v8071c.py','scripts/complete_Rafael_B48_v8071d.py',{
        'review full event39 context and prove native entry':'the full 22-speech clean event39 prerequisite has also been read and glossed at '+GLOSS+'; prove native entry',
        'native_controls_event39_context_paths_names_current_comparison_andrelease_pending=True':
            'event39_clean_context_complete=True,event39_context_packet='+repr(PACKET)+',event39_context_gloss='+repr(GLOSS)+',native_controls_paths_names_current_comparison_andrelease_pending=True',
        "Path(__file__)]}":'Path('+repr(PACKET)+'),Path('+repr(GLOSS)+'),Path(__file__)]}',
    }))
