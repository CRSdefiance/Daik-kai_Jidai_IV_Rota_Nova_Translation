"""Keep prior outputs;correct inherited sheet caption to the verified V1404 ROM."""
from pathlib import Path
if __name__=='__main__':
 outer=Path('scripts/rebind_battle_victory_history_v2591b.py').read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured=source'),__file__,'exec'),env);source=env['captured'];assert source.count('Historical V1364')==1
 source=source.replace('Historical V1364','Historical V1404').replace('battle_victory_history_v2591b','battle_victory_history_v2591c')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
