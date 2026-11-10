"""Allow one ordinary Chinese/empress boundary instead of a needlessly short first row."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_B220_wrap_tools_v6927b');old=Path('work/analysis/lil_B220_layout_v6927/seventeen_whole_paragraph_plans_no_macros_no_prose_changes.json');assert not root.exists();root.mkdir(parents=True)
    p=derive('scripts/plan_lil_B220_layout_v6927.py','scripts/plan_lil_B220_layout_v6927b.py',{'layout_v6927':'layout_v6927b',"            candidate=((cost[0]+tiny":"            if row['id']=='DK4_MES_B220_R0035' and pair==('chinese','empress'):weak=0\n            candidate=((cost[0]+tiny"})
    save(root/'source_locked_fuller_first_row_reason.json',dict(derivation=p,prior_plan=str(old),prior_plan_sha256=sha(old.read_bytes()),record='DK4_MES_B220_R0035',prior_line_lengths=next(r['line_lengths'] for r in read(old)['records'] if r['id']=='DK4_MES_B220_R0035'),reason='Permit a complete-word Chinese/empress soft boundary in this one paragraph. The original20-cell first row keeps a generic adjective/noun pair together at the expense of unnecessary empty space. The source Chinese identity remains explicit across adjacent rows;no word,glyph,metric,page capacity or source command changes. The generic pair preference remains for every other occurrence and all literal-I/native safety rules remain.',no_prose_or_global_width_warning_or_native_scope_change=True,new_review_credit=0,full_goal_complete=False))
    derive('scripts/probe_lil_B220_paragraph_QA_v6932.py','scripts/probe_lil_B220_paragraph_QA_v6932b.py',{'base_QA_v6932':'base_QA_v6932b','layout_v6927/':'layout_v6927b/','native_pages_v6928/':'native_pages_v6928b/'})
