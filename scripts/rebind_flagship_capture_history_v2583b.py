"""Preserve2583;correct11500 label and include actual cargo/discard prompt frames."""
from pathlib import Path
if __name__=='__main__':
 outer=Path('scripts/rebind_flagship_capture_history_v2583.py').read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured=source'),__file__,'exec'),env);source=env['captured']
 changes={
  'flagship_capture_history_v2583':'flagship_capture_history_v2583b',
  "(11500,'cargo handling;no retained untransferred spoils claim')":"(11500,'national-coins reward;context only'),(12400,'actual cargo-transfer screen before normal X Finish'),(12700,'original confirmation before normal touch Yes discards untransferred spoil cargo')",
  "(1024,820)":"(768,1230)",'x,y=i%4*256,i//4*410':'x,y=i%3*256,i//3*410',
  '15 original states and7 reward/cargo/sailing transitions':'15 original states and9 reward/cargo/sailing transitions',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
