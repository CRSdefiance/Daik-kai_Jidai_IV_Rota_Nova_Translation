"""Successor accepts the cancellation prompt and leaves refit normally."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/run_refit_spritsail_v2287.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'observe_refit_spritsail_v2286':'observe_refit_exit_v2291',
 'refit_spritsail_runs_v2287':'refit_spritsail_runs_v2292',
 'refit_spritsail_v2287_':'refit_spritsail_v2292_',
 "(17001,'B')":"(17001,'A'),(17301,'B')",
 'frames=17401;captures':'frames=17701;captures',
 'range(12800,17401,300)':'range(12800,17701,300)'
 }
 for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_spritsail_runs_v2292/successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),original_run_preserved=True,reason='Initial plan selected B at cancellation prompt,so it declined cancellation. The successor selects A then B to dismiss ship selection. No ROM or runtime change.',same_inputs_through17000=True,no_new_RAM_code_gameplay_fixture_or_savestate=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
