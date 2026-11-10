"""Prepare typed B196 relocation,52 branch fixups,seven ends and final stored proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_relocation_tools_v5615')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B164_relocation_v3986.py','scripts/research_lil_B196_relocation_v5615.py',{
        'B164':'B196','relocation_v3986':'relocation_v5615','editorial_manuscript_v9':'editorial_manuscript_v3',
        'combined_v3954':'combined_v5580','number==164 and len(end_maps)==2':'number==196 and len(end_maps)==7',
        "        assert end_maps[0]['target_offset']+4<end_maps[1]['target_offset'] # separated advice outcomes,not adjacent suffix":
        "        assert all(a['target_offset']+4<b['target_offset'] for a,b in zip(end_maps,end_maps[1:])) # six purchases and final refusal have distinct ends",
        '        assert bytes(restored)==source[:old_end]':
        '        assert bytes(restored)==source[:old_end]\n        assert source[old_end:]==bytes(2) and bytes(restored)+source[old_end:]==source',
        "text_records']) for r in results)==47":"text_records']) for r in results)==24",
        "choice_commands']) for r in results)==1":"choice_commands']) for r in results)==6",
        "relative_skip_fixups']) for r in results)==4":"relative_skip_fixups']) for r in results)==52",
        "target_native_skip_cases']) for r in results)==20":"target_native_skip_cases']) for r in results)==260",
        "command_map']) for r in results)==61":"command_map']) for r in results)==119",'in [164]':'in [196]',
        'inverse_restoration_recovers_every_original_logical_byte=True,':'inverse_restoration_recovers_every_original_logical_byte=True,inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte=True,',
        'one_original2100_object_two_source_ordered_advice_labels':'six_original2100_objects_twelve_source_ordered_buy_refusal_labels',
        'all47speech_and4_relative_operands':'all24speech_six_menus_and52_relative_operands',
        'all20_relocated_native_skip_cases':'all260_relocated_native_skip_cases','source_FE_system_objects=0':'source_FE_system_objects=1',
        'two_separated_declared_advice_end_words_exact':'seven_separated_declared_purchase_refusal_end_words_exact',
        '61commands/47speech/one2100/4spans/20targetskipcases,two separated endwords,inversebytes and335otherblocks exact.':
        '119commands/24speech/six2100/52spans/260targetskipcases,seven separated ends,all1816 source bytes inverse and335otherblocks exact.'})]
    rows.append(derive('scripts/prove_lil_B195_stored_v5562.py','scripts/prove_lil_B196_stored_v5616.py',{
        'B195':'B196','all20':'all24','all20 final':'all24 final','stored_v5562':'stored_v5616','relocation_v5561':'relocation_v5615',
        'voices_v5542':'voices_v5591','[92,103,119,254]':'[2,6,19,20,25,173,254]',
        "                expanded=stored[1:]\n                assert not any(m in expanded for m in [b'FI',b'FA',b'FO'])":
        "                expanded=stored[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')",
        'len(cases)==20':'len(cases)==24','fresh+reused==80':'fresh+reused==96','targets80_macro':'targets96_macro',
        'current_final_stored_macro_alignment_cases=80':'current_final_stored_macro_alignment_cases=96',
        'actual_selected_B195_linear_A000_C200_and_end_reachability_unexecuted':'actual_selected_B196_price_branches_and_source_controls_unexecuted',
        'stored_targets=20,progressive=19,FE=1,macro_cases=80':'stored_targets=24,progressive=23,FE=1,macro_cases=96'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_typed_source_relocation_and_stored_checks.json',dict(tools=rows,
        source_block196_commands119_speeches24_six_menus_twelve_labels_relative_sites52_target_skip_cases260_seven_ends=True,
        full_logical_plus_two_tailzero_source_inverse_required=True,
        exact_R74_ordinary_wrap_compiled_bytes_and_current_default_FI_preserved=True,
        no_ROM_registry_ledger_or_completion_change=True,full_goal_complete=False))
