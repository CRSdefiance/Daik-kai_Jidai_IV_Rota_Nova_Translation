"""Ordinary current recruitment from the unchanged genuine Istanbul save; no fixture."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

original=Path('scripts/run_town_yard_context_v2156b.py')
source=original.read_text()
prior=Path('E:/Rota Nova translations/Generated/work/emulation_v193/recruitment_v773_return_v773/capture_report.json')
report=read(prior)
assert report['frames']==8801 and report['cold_boot']and not report['savestate_loaded']
assert not any(v for k,v in report.items()if k.startswith('synthetic_'))
changes={
 'ROOT=observed.ROOT\nROM=observed.ROM':"ROOT=Path('work/analysis/recruitment_actual_v2202')\nROM=Path('out/all_routes_combined_v2171_candidate.nds')\nobserved.ROOT=ROOT;observed.ROM=ROM",
 'town_yard_live_v2156b_V2143':'recruitment_actual_v2202_V2171',
 'port_services_v762_sell_762':'recruitment_v773_return_v773',
 'frames=[3200,3400,3800,4200,4600,5000,5400,5800,6200,6400]':"frames=sorted({r['frame']for r in report['frames_captured']})",
 '6401':'8801',
}
for before,after in changes.items():
 assert source.count(before)>=1,before
 source=source.replace(before,after)
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
from scripts.verify_village_wrap_v608 import save
save(env['ROOT']/'launcher_provenance.json',dict(original=str(original),original_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),current_ROM='out/all_routes_combined_v2171_candidate.nds',no_fixture_or_savestate=True,original_observer_and_harness_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
