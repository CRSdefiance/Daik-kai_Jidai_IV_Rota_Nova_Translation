"""Preserve2644 pre-output schema refusal;read the referenced source-fragment file."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/prepare_support_context_v2644.py').read_text().replace("for row in old['original_source_fragments']:","for row in read(old['original_source_fragments']):").replace("row['address']-BASE","row['start']-BASE").replace('support_context_v2644','support_context_v2644b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
