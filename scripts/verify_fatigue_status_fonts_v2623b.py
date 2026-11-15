"""Preserve2623 pre-output import failure;use the established native Loader."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_fatigue_status_fonts_v2623.py').read_text().replace('scripts.verify_main_head_cache_v480','scripts.probe_common_single_cache_v862').replace('fatigue_status_fonts_v2623','fatigue_status_fonts_v2623b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
