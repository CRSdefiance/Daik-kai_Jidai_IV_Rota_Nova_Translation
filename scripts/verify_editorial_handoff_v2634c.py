"""Audit canonical V2633 headline;2633b is its successful producer variant."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2634.py').read_text()
 for old,new in [('else2','else 2'),('else0','else 0'),('else6','else 6'),('else4','else 4'),('editorial_handoff_verification_v2634','editorial_handoff_verification_v2634c'),("handoff.startswith('# Current editorial handoff - V2633b')","handoff.startswith('# Current editorial handoff - V2633')"),("checkpoint='V2633b'","checkpoint='V2633',successful_producer_variant='2633b'"),('Independent V2633b audit passes','Independent V2633 audit passes')]:source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
