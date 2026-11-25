"""Select original Declare War mode immediately after the sole location fixture."""
from pathlib import Path

if __name__=='__main__':
    source=Path('scripts/run_stronger_fleet_location_v1472.py').read_text(encoding='utf-8')
    replacements=[
        ('stronger_fleet_location_v1472','stronger_fleet_early_modes_v1475'),
        ("r.get('until',100000)<=5000","r.get('until',100000)<=4900"),
        ("assert commands[-1]['until']==5000","assert commands[-1]['until']==4900"),
        ("commands.append({'until':5100,'duration':1})", "commands[-1].update(until=4810,buttons=['Y'],duration=4)\n    commands.extend([{'until':4820,'buttons':['Y'],'duration':4},{'until':4830,'buttons':['Y'],'duration':4}])")]
    for old,new in replacements:
        assert old in source,old
        source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
