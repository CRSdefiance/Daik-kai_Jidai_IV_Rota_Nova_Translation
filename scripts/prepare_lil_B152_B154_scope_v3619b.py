"""Use the actual eight source relative sites;preserve the failed estimated-count producer."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B152_B154_scope_v3619.py');t=p.read_text(encoding='utf-8');a="doc['source_relative_sites']==9";assert t.count(a)==1;t=t.replace(a,"doc['source_relative_sites']==8");exec(compile(t,str(Path(__file__))+'::exact_eight_relative_sites','exec'),dict(__name__='__main__',__file__=__file__));save(Path('work/analysis/lil_B152_B154_source_v3619/source_count_correction.json'),dict(previous=str(p),previous_sha256=sha(p.read_bytes()),source_relative_sites=8,initial_estimate9_rejected_before_source_packet_written=True,no_source_prose_or_ROM_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
