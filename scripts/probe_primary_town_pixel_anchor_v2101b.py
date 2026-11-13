"""Measure per-row native-ink origins; preserve the failed whole-plane guess."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/probe_primary_town_pixel_anchor_v2101.py').read_text(encoding='utf-8-sig').replace('v2101','v2101b')
 a=source.index(' for dy in range(290,311):');b=source.index(' print(dict(',a)
 source=source[:a]+''' row_matches=[]
 for row_index in sorted({y//12 for x,y in ink}):
  segment={(x,y-row_index*12)for x,y in ink if y//12==row_index};found=[]
  for dy in range(290,341):
   for dx in range(29):
    expected={(x+dx,y+dy)for x,y in segment}
    if expected<=pixels:found.append([dx,dy])
  row_matches.append(dict(native_row=row_index,matches=found,pixels=len(segment)))
 matches=row_matches
'''+source[b:]
 source=source.replace('assert len(matches)==1','assert all(len(r["matches"])==1 for r in matches)')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
