"""Preserve3306; correct the independently summed eight-block command total."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    old=Path('scripts/map_lil_remaining_B131_B140_source_v3306.py');new=Path('scripts/map_lil_remaining_B131_B140_source_v3306b.py');assert not new.exists()
    packet=read('work/analysis/lil_after_B119_clean_scope_v3257c/complete_clean_next_exchange_inventory.json');counts={b['block']:len(b['commands']) for b in packet['blocks'] if b['block'] in [131,133,135,136,137,138,139,140]};assert sum(counts.values())==547
    text=old.read_text(encoding='utf-8').replace('lil_remaining_B131_B140_source_v3306','lil_remaining_B131_B140_source_v3306b').replace('==647','==547').replace('/647commands','/547commands')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf-8')
    root=Path('work/analysis/lil_remaining_command_total_v3306b');root.mkdir(parents=True);save(root/'preserved_assertion_and_correct_total.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),command_counts_by_source_block=counts,total_commands=547,failure='3306 counted all source/current objects then rejected an arithmetic expectation647. Independent per-block prior native counts sum547. No packet,ROM,ledger orreview credit was written.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
