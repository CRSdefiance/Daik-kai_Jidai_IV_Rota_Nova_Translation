"""Use verified already-current V1676 payload;preserve2624 pre-output refusal."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_hot_spring_fonts_v2624.py').read_text().replace('current_common_native_context_v2620 import','current_common_native_context_v2620b import').replace('hot_spring_fonts_v2624','hot_spring_fonts_v2624b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
