"""Correct the relocation producer's gate-list schema check; preserve its stopped first run."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/research_lil_B194_relocation_v5506.py',
                 'scripts/research_lil_B194_relocation_v5506b.py', {
                     "work/analysis/lil_B194_relocation_v5506": "work/analysis/lil_B194_relocation_v5506b",
                     'from scripts.verify_village_wrap_v608 import read, save':
                     'from scripts.verify_village_wrap_v608 import read, save\nfrom dk4tool.dialogue.review import validate_natural_dialogue_batch',
                     "assert all(doc['review_gates'].values()) and len(doc['records']) == 11":
                     "validate_natural_dialogue_batch(doc)\n    assert len(doc['records']) == 11",
                 }))
