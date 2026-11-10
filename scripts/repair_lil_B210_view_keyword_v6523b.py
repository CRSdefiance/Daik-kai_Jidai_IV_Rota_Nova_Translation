"""Repair one invalid metadata keyword in an unexecuted review producer; preserve its failed source."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B210_view_keyword_tools_v6523b')
if __name__=='__main__':
    source=Path('scripts/review_lil_B210_and_Al_Ferid_v6523.py');target=Path('scripts/review_lil_B210_and_Al_Ferid_v6523b.py');assert not ROOT.exists() and not target.exists();before=source.read_bytes();bad=b',621_name_table_pointers_and_cache_plan_unchanged=';good=b',all621_name_table_pointers_and_cache_plan_unchanged=';assert before.count(bad)==1;after=before.replace(bad,good);assert after.replace(good,bad)==before;compile(after,str(target),'exec');target.write_bytes(after);ROOT.mkdir(parents=True)
    save(ROOT/'exact_keyword_repair.json',dict(source=str(source),source_sha256=sha(before),target=str(target),target_sha256=sha(after),exact_replacement=dict(before=bad.decode(),after=good.decode()),original_syntax_error_occurred_before_any_producer_body_or_document_write=True,only_metadata_keyword_prefix_repaired_no_native_address_logic_OR_proof_condition_change=True,failed_source_preserved=True,full_goal_complete=False));print('Single invalid metadata keyword repaired in a compiled successor;failed original source and all evidence preserved.')
