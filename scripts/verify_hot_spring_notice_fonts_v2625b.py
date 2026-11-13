"""Use verified already-current V1676 payload;preserve2625 pre-output refusal."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_hot_spring_notice_fonts_v2625.py').read_text().replace('current_common_native_context_v2620 import','current_common_native_context_v2620b import').replace('hot_spring_notice_fonts_v2625','hot_spring_notice_fonts_v2625b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
