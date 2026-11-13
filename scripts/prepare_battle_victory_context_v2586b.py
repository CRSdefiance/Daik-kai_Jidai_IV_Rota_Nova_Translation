"""Preserve2586;correct2129 storage neighbor and remove an unsupported context hint."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/prepare_battle_victory_context_v2586.py').read_text()
 changes={'battle_victory_context_v2586':'battle_victory_context_v2586b','formal/familiar voices and any anticipation of the end of battle':'formal/familiar voices','Adjacent2129 withdrawal':'Adjacent2129 attack confirmation'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
