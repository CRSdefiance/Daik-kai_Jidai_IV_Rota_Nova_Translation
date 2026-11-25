"""Keep failed source-key assumption;derive exact-key successor without native changes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    row=derive('scripts/review_shachihoko_source_context_v6075.py','scripts/review_shachihoko_source_context_v6075b.py',{"r['source_Japanese']":"r['Japanese']"})
    print(row)
