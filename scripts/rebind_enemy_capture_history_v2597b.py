"""Keep2597;resident cache is the %s template,wrapped cache is expanded prose."""
from pathlib import Path
if __name__=='__main__':
 outer=Path('scripts/rebind_enemy_capture_history_v2597.py').read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured=source'),__file__,'exec'),env);source=env['captured']
 changes={"==entries[2082].text.replace(b'%s',name)":"==entries[2082].text","case['native_formatted_hex']":"case['native_pipeline']['formatted_hex']",'enemy_capture_history_v2597':'enemy_capture_history_v2597b'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
