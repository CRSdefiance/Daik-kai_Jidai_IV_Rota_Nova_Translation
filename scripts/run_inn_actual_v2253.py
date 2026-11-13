"""Ordinary current one/three-night Inn interactions; no runtime fixture."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
original=Path('scripts/run_town_yard_context_v2156b.py');source=original.read_text()
for old,new in (
 ('ROOT=observed.ROOT\nROM=observed.ROM',"ROOT=Path('work/analysis/inn_actual_v2253')\nROM=Path('out/all_routes_combined_v2171_candidate.nds')\nobserved.ROOT=ROOT;observed.ROM=ROM"),
 ('town_yard_live_v2156b_V2143','inn_actual_v2253_V2171'),
 ('port_services_v762_sell_762','inn_v803_stays'),
 ("donor=Path('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv')","donor=Path(battery['source'])"),
 ('frames=[3200,3400,3800,4200,4600,5000,5400,5800,6200,6400]',"frames=sorted({r['frame']for r in report['frames_captured']})"),
 ('6401','8601'),
 ('original_genuine_save=str(donor)','original_genuine_save=str(donor), inherited_source_battery_provenance_not_reearned=True'),
):
    assert old in source,old;source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'launcher_provenance.json',dict(original=str(original),original_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),ordinary_current_Inn_run_no_fixture_or_savestate=True,inherited_source_battery_history_not_reearned=True,original_donor_and_harness_core_unchanged=True,full_goal_complete=False))
