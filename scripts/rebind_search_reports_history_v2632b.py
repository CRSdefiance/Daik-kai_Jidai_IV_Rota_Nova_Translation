"""Preserve2632 refusal;bind failure voice1's original minus1 fallback correctly."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/rebind_search_reports_history_v2632.py').read_text();old="assert identity==18 and get(0x7E988,get(0xCB184)+4+32*identity)==0";new="assert identity==(16 if n==2217 else 18)and get(0x7E988,get(0xCB184)+4+32*identity)==(1 if n==2217 else 0)";assert source.count(old)==1;source=source.replace(old,new).replace('search_reports_history_v2632','search_reports_history_v2632b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
