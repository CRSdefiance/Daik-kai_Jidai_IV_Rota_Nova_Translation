"""Fresh current-ROM approach with ordinary sails closure before mode selection."""
from pathlib import Path

if __name__=='__main__':
    source=Path('scripts/run_stronger_fleet_location_v1472.py').read_text(encoding='utf-8')
    for old,new,count in [
        ('scripts.native_stronger_fleet_location_v1471 import apply_fixture,ROM','scripts.native_stronger_fleet_current_v1501 import apply_fixture,ROM',1),
        ('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json','work/analysis/battle_reaction_release_v1491/registered_release_verification.json',2),
        ('stronger_fleet_location_v1472','stronger_fleet_anchor_v1502',2),
        ('stronger_fleet_anchor_v1502_1456','stronger_fleet_anchor_v1502_1492',1),
        ("r.get('until',100000)<=5000","r.get('until',100000)<=4900",1),
        ("assert commands[-1]['until']==5000","assert commands[-1]['until']==4900",1),
        ("commands.append({'until':5100,'duration':1})","commands[-1].update(buttons=['B'],duration=8)\n    commands.append({'until':5200,'duration':1})",1)]:
        assert source.count(old)==count,(old,source.count(old))
        source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
