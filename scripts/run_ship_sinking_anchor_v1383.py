"""Replay the declared loadout pilot to10090,then accept normal commands."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read


if __name__=='__main__':
    path = Path('scripts/run_ship_sinking_loadout_v1379.py')
    plan = read('work/analysis/ship_sinking_loadout_v1379/run_plan.json')
    assert sha(path.read_bytes())==plan['runner_sha256']
    source = path.read_text(encoding='utf-8')
    for old,new in [
        ('work/analysis/ship_sinking_live_v1353/navigation.jsonl','work/analysis/ship_sinking_loadout_v1379/navigation.jsonl'),
        ('work/analysis/ship_sinking_live_v1353/terminal_preservation.json','work/analysis/ship_sinking_loadout_v1379/terminal_preservation.json'),
        ('<=9100','<=10090'),('==9100','==10090'),
        ('work/analysis/ship_sinking_loadout_v1379','work/analysis/ship_sinking_anchor_v1383'),
        ('ship_sinking_loadout_v1379_1364','ship_sinking_anchor_v1383_1364')]:
        if old=='work/analysis/ship_sinking_loadout_v1379':
            # Keep the two terminal source references above on their frozen run.
            needle="'ROOT':Path('"+old+"')"
            assert source.count(needle)==1
            source = source.replace(needle,"'ROOT':Path('"+new+"')")
        else:
            assert source.count(old)==1,(old,source.count(old))
            source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
