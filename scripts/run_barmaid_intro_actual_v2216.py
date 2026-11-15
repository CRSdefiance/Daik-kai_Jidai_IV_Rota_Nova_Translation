"""Ordinary London barmaid dialogue; copied historical battery, no fixture/savestate."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original=Path('scripts/run_town_yard_context_v2156b.py')
source=original.read_text()
for old,new in (
    ('ROOT=observed.ROOT\nROM=observed.ROM',"ROOT=Path('work/analysis/barmaid_intro_actual_v2216')\nROM=Path('out/all_routes_combined_v2171_candidate.nds')\nobserved.ROOT=ROOT;observed.ROM=ROM"),
    ('town_yard_live_v2156b_V2143','barmaid_intro_actual_v2216_V2171'),
    ('port_services_v762_sell_762','tavern_direct_actual_v2190_V2171'),
    ('hodram-istanbul-golden-cutlass-blue-oak-v474.dsv','hodram-london-rested-minimum-crew-v464.dsv'),
    ("==battery['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'","=='05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'"),
    ('frames=[3200,3400,3800,4200,4600,5000,5400,5800,6200,6400]','frames=[3200,5000,5200,5400,5800,6200,6600,7000,7200,7400,7600,8000,8400,8800,9000,9200]'),
    ('6401','9201'),
    ("assert sha(donor.read_bytes())==battery['source_sha256']","assert sha(donor.read_bytes())=='05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'"),
):
    assert old in source,old
    source=source.replace(old,new)
# The input reference supplies only a known ordinary navigation schedule. Its Istanbul donor is not used here.
source=source.replace('original_genuine_save=str(donor)','original_genuine_save=str(donor), inherited_battery_provenance_not_reearned=True, schedule_reference_donor_differs_from_current_London_donor=True')
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'launcher_provenance.json',dict(original=str(original),original_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),ordinary_fixture_free_current_London_battery=True,no_new_earned_source_save_claim=True,full_goal_complete=False))
