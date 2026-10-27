"""Preserve2591 partial sheets;use the victory receipt's prebattle fixture key."""
from pathlib import Path
if __name__=='__main__':
 outer=Path('scripts/rebind_battle_victory_history_v2591.py').read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured=source'),__file__,'exec'),env);source=env['captured']
 assert source.count('historical["sole_fixture"]')==1;source=source.replace('historical["sole_fixture"]','historical["sole_prebattle_fixture"]').replace('battle_victory_history_v2591','battle_victory_history_v2591b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
