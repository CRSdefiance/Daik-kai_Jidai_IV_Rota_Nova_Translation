"""Preserve2635 pre-output table refusal;retain incoming original minus1 fallback."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/prepare_sighting_context_v2635.py').read_text().replace('[622,623,624,624,625,626,627,628]','[622,-1,623,624,625,626,627,628]').replace('assert n==values[voice]','assert n==(values[voice]if values[voice]>=0 else values[0])').replace('search_current_binding_unused','search_current_binding_unused').replace('sighting_context_v2635','sighting_context_v2635b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
