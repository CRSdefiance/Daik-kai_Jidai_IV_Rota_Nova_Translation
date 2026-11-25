"""Seal the verified proofs with the complete natural-dialogue-v2 name schema."""
from scripts.finalize_rafael_B181_B200_research_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Rafael_B181_B200_research_final_v2_20261106': 'Rafael_B181_B200_research_final_v3_20261106',
    "names.update(encoder='dialogue-relocatable-v1',": "names.update(encoder='dialogue-relocatable-v1',review_gates=list(PASSES),",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-evidence-guards-complete-name-schema', 'exec'),globals())
