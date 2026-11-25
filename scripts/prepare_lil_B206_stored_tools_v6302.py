"""Source-locked final stored-speech verifier with exact current runtime and no source FE objects."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B206_stored_tools_v6302')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B205_stored_v6202.py','scripts/prove_lil_B206_stored_v6302.py',{
      'B205':'B206','current_build_native_context_v6097':'current_build_native_context_v6261b','lil_current_font_oracles_v6122':'shady_man_font_oracles_v6263','lil_B205_stored_v6202':'lil_B206_stored_v6302','editorial_manuscript_v6.json':'editorial_manuscript_v7.json','lil_B205_relocation_v6201':'lil_B206_relocation_v6301','current_V6160_native_v6168':'current_V6270_native_v6279','[2,15,254]':'[2,7,173]',
      'len(cases)==17':'len(cases)==24','fresh+reused==68':'fresh+reused==96',"sum(c['consumer']=='FE-paper' for c in cases)==7":"sum(c['consumer']=='FE-paper' for c in cases)==0",'all17':'all24','targets68_macro':'targets96_macro','current_final_stored_macro_alignment_cases=68':'current_final_stored_macro_alignment_cases=96','stored_targets=17,progressive=10,FE=7,macro_cases=68':'stored_targets=24,progressive=24,FE=0,macro_cases=96',
      'parrot_echoes_sounds_capture_joke_and_end_reachability':'ceramic_earring_pitch_purchase_both_refusals_and_end_reachability',
    });ROOT.mkdir(parents=True);save(ROOT/'exact24_no_FE_final_stored_speech_native_tool.json',dict(verifier=proof,source_speeches=24,source_FE=0,source_static_selectors=[2,7,173],new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Exact24-speech/no-FE final stored parity/native verifier prepared;96 covered alignment cases.')
