"""Expose the older B158 English only after complete clean glosses and source contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    row=derive('scripts/compare_lil_B157_effective_v3750.py','scripts/compare_lil_B158_effective_v3791.py',{
        'lil_B157_comparison_v3750':'lil_B158_comparison_v3791','lil_B157_source_v3746/all75_clean_current_complete_context':'lil_B158_source_v3788b/all19_clean_current_complete_context',
        'lil_B157_source_v3746/subset150_dispatches_and27_source_exact_control_leaves':'lil_B158_source_v3788b/subset38_dispatches_and22_source_exact_control_leaves',
        'lil_B157_clean_context_v3745/all75_complete_B157_exchange_and_fresh_glosses':'lil_B158_clean_context_v3787b/all19_complete_B158_exchange_and_fresh_glosses',
        'lil_B157_source_v3746/seven_names_two_FE_and_original_entry_binding':'lil_B158_source_v3788b/four_names_four_FE_and_original_entry_binding',
        'lil_B157_controls_v3749/two_predicates_two_C200_three_resource_sites_and27_source_leaves':'lil_B158_controls_v3790/six_predicates_four_resource_sites_two_pauses_and22_source_leaves',
        'all75_clean_source_speeches_and_optional_Fernando_Emilio_branches_read':'all19_clean_source_speeches_and_optional_Camille_Emilio_branches_read','all75_glosses_before_older_English':'all19_glosses_before_older_English',
        'len(rows)==75':'len(rows)==19','block=157':'block=158','all75':'all19','fresh75':'fresh19','B157':'B158','All75':'All19','and75 fresh glosses':'and19 fresh glosses',
        'Seven static actors,73 progressive/two FE null-actor consumers,FI2,original entry,two predicates,two C200 requests,three resource sites/two values andeight relative sites are bound. One two-byte pause,C281/4885 andother exact control leaves require focused actual checks;FE geometry has its separate native proof.':'Four static actors,15 progressive/four FE null-actor consumers,FI1,original entry,six predicates,four resource sites/values and24 relative sites are bound. Two original two-byte pauses,picture/music/4650/4660/4670 andother exact control leaves require focused actual checks;FE geometry and embedded patron labels require separate native proof.'})
    root=Path('work/analysis/lil_B158_comparison_tools_v3791');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(tool=row,no_editorial_decisions_or_credit_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
