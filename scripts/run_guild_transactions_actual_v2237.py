"""Ordinary current Seoul item transactions; inherited battery, no runtime fixture."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original=Path('scripts/run_town_yard_context_v2156b.py')
source=original.read_text()
for old,new in (
 ('ROOT=observed.ROOT\nROM=observed.ROM',"ROOT=Path('work/analysis/guild_transactions_actual_v2237')\nROM=Path('out/all_routes_combined_v2171_candidate.nds')\nobserved.ROOT=ROOT;observed.ROM=ROM"),
 ('town_yard_live_v2156b_V2143','guild_transactions_actual_v2237_V2171'),
 ('port_services_v762_sell_762','item_transactions_v789_live'),
 ("donor=Path('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv')","donor=Path(battery['source'])"),
 ('d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132','942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'),
 ('frames=[3200,3400,3800,4200,4600,5000,5400,5800,6200,6400]',"frames=sorted({r['frame']for r in report['frames_captured']})"),
 ('6401','15601'),
 ('original_genuine_save=str(donor)','original_genuine_save=str(donor), inherited_source_battery_provenance_not_reearned=True'),
):
 assert old in source,old
 source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'launcher_provenance.json',dict(original=str(original),original_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),ordinary_current_Seoul_run_no_fixture_or_savestate=True,inherited_source_battery_history_not_reearned=True,original_donor_and_harness_core_unchanged=True,full_goal_complete=False))
