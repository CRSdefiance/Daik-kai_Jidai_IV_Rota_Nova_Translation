"""Record actual timing/RNG differences without masking them or asserting broad equivalence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/audit_shady_man_scene_v6265.py')
if __name__=='__main__':
    comparison="""    pair_differences=[dict(index=i,source=a,target=b,different_fields=[k for k in a if a[k]!=b[k]]) for i,(a,b) in enumerate(zip(old['command_pairs'],pairs,strict=True)) if a!=b]
    assert len(pair_differences)==16
    for a,b in zip(old['command_pairs'],pairs,strict=True):
        assert all(a[k]==b[k] for k in ['fixture_offset','source_offset','word','native_result','decoded_length','UI_after'])
    following_differences=[dict(source=a,target=b) for a,b in zip(old['following_native_commands'],following,strict=True) if a!=b]
    for a,b in zip(old['following_native_commands'],following,strict=True):
        assert all(a[k]==b[k] for k in ['block','offset','word','native_result'])
    assert pair_differences[0]['index']==21 and pair_differences[0]['different_fields']==['returned']
    save(ROOT/'unmasked_source_target_timing_and_RNG_differences.json',dict(command_differences=pair_differences,following_differences=following_differences,first_return_difference_source=5737,first_return_difference_target=5736,first_menu_source=[6217,6445],first_menu_target=[6216,6448],all_command_offsets_words_results_lengths_and_UI_words_equal=True,no_timing_RNG_whole_state_or_broad_simulation_equivalence_claim=True,all_capture_schedules_and_raw_traces_retained=True))"""
    text=checked_text(source.read_text('utf-8'),{
      "ROOT=Path('work/analysis/shady_man_scene_v6265')":"ROOT=Path('work/analysis/shady_man_scene_v6265c')",
      "    assert pairs==old['command_pairs'] and following==old['following_native_commands']":comparison,
      "and pairs[-1]['returned']==7893":"and pairs[-1]['returned']==7896",
      "source_and_target_all_command_start_return_RNG_and_UI_words_exact=True":"source_and_target_command_offsets_words_results_lengths_and_UI_words_exact=True,timing_and_RNG_differences_explicit=str(ROOT/'unmasked_source_target_timing_and_RNG_differences.json')",
      "exit_frame=7893,following_B120_end_frame=12694":"exit_frame=7896,following_B120_end_frame=12697",
      "Same command timings,RNG/UI and complete B120 return.":"Command order/results/UI agree;timing/RNG differences preserved. Complete B120 return observed.",
    })
    exec(compile(text,str(source)+'::honest-observed-differences','exec'),dict(__name__='__main__',__file__=__file__))
