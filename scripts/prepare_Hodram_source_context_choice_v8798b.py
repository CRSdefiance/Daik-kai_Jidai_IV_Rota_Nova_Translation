"""Qualify the exact clean B37 choice reading: prepare to attack, not an invented endorsement."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_source_review_tools_v8798b');assert not root.exists()
    receipt=derive('scripts/review_Hodram_B54_B60_source_v8798.py','scripts/review_Hodram_B54_B60_source_v8798b.py',{
        'Hodram_B54_B60_source_review_v8798':'Hodram_B54_B60_source_review_v8798b',
        '攻撃上等だ':'攻撃準備だ',
        'offers attack versus concern about exceeding authority':'offers an imperative to prepare to attack versus concern about exceeding authority',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,
        exact_clean_choice_hex_8d558c828f8094f582be_decodes_to_attack_preparations=True,
        stopped_reader_wrong_Japanese_choice_expectation_preserved_no_review_orname_packet_had_been_written=True,
        all_actual_source_bytes_controls_names_anddirect_view_guards_preserved=True,new_credit=0,full_goal_complete=False))
